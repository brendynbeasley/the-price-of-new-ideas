"""Do manufacturing markups pay for research? Romer's zero-profit condition across US industries, 2022.

In Romer (1990) a firm buys a design at price P_A, then sells the good it makes possible above marginal cost.
Free entry into research means the flow of operating rent just covers the interest on the design:
pi = r * P_A (equation 6' of the NBER version). Summed over an industry's designs, rents are r * P_A * A and
research spending is P_A * dA/dt, so rents / sales = (r / g_A) * (R&D / sales). With r at or above g_A, as on
Romer's balanced path (r = rho + sigma * g), an industry's margin over variable cost should rise at least one
for one with what it spends on research:

    PCM_i = a + b * RD_i + e_i,    Romer with free entry:  b = r / g_A >= 1 (tested as b = 1);
                                   price-taking with no rents:  b = 0.

PCM (price-cost margin) is the Collins-Preston measure from the 2022 Economic Census of manufacturing:
(value added - payroll - fringe benefits) / value of shipments. RD is the R&D intensity from the 2022
Business Enterprise R&D Survey (NCSES/Census): domestic R&D performed / domestic net sales of the companies
that performed or funded R&D. Industries are the most detailed BERD manufacturing rows that do not overlap,
36 in all; "other" rows are rebuilt in the Census data as parent minus the listed children.

Run from the repository root:
    python src/markups_and_research.py
Writes results/industries_2022.csv, results/markup_regressions.csv and results/markup_vs_rd.png.
"""
from pathlib import Path
import warnings
import zipfile

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

warnings.filterwarnings("ignore", message="Workbook contains no default style")

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"
EC_ZIP = RAW / "census" / "EC2231BASIC.zip"           # 2022 Economic Census, manufacturing, basic statistics
BERD_RD = RAW / "ncses" / "nsf24335-tab002.xlsx"      # BERD 2022 Table 2, R&D performance by industry
BERD_SALES = RAW / "ncses" / "nsf24335-tab008.xlsx"   # BERD 2022 Table 8, sales by industry

# BERD row (its NAICS code text) -> Census NAICS codes added (+) and subtracted (-) to match it.
# Leaves only: no BERD row in this list contains another one. Built from the BERD table's own code column.
INDUSTRIES = {
    "311": (["311"], []), "312": (["312"], []), "313–16": (["313", "314", "315", "316"], []),
    "321": (["321"], []), "322": (["322"], []), "323": (["323"], []), "324": (["324"], []),
    "3251": (["3251"], []), "3252": (["3252"], []), "3253": (["3253"], []), "3254": (["3254"], []),
    "3256": (["3256"], []), "3255, 3259": (["3255", "3259"], []),
    "326": (["326"], []), "327": (["327"], []), "331": (["331"], []), "332": (["332"], []),
    "33311": (["33311"], []), "333242": (["333242"], []), "3336": (["3336"], []),
    "other 333": (["333"], ["33311", "333242", "3336"]),
    "3342": (["3342"], []), "3344": (["3344"], []),
    "334510, 334517": (["334510", "334517"], []), "334511": (["334511"], []),
    "other 3345": (["3345"], ["334510", "334517", "334511"]),
    "other 334": (["334"], ["3342", "3344", "3345"]),
    "335": (["335"], []), "3361–63": (["3361", "3362", "3363"], []),
    "336411–13": (["336411", "336412", "336413"], []),
    "336414–15, 336419": (["336414", "336415", "336419"], []), "336992": (["336992"], []),
    "other 336": (["336"], ["3361", "3362", "3363", "3364", "336992"]),
    "337": (["337"], []), "3391": (["3391"], []), "3399": (["3399"], []),
}
EC_FIELDS = ["RCPTOT", "VALADD", "PAYANN", "BENEFIT", "ASTEND", "PCHADVT"]   # $1,000


def load_ec():
    with zipfile.ZipFile(EC_ZIP) as z:
        with z.open("EC2231BASIC.dat") as f:
            d = pd.read_csv(f, sep="|", dtype=str)
    d.columns = [c.lstrip("#") for c in d.columns]
    us = d[d["GEOTYPE"] == "01"].copy()
    print(f"Economic Census 2022 manufacturing: {len(d):,} rows, {len(us)} national industry rows kept")
    for c in EC_FIELDS:
        flagged = us[c + "_F"].notna().sum()
        us[c] = pd.to_numeric(us[c], errors="coerce")
        # Advertising is withheld (flag D) for a few small industries; it enters only as a control.
        # Of the flagged codes only 336415 and 336419 enter the sums below (guided missile row).
        if flagged:
            print(f"  {c}: {flagged} national rows flagged (D/other); treated as 0 in sums")
            us.loc[us[c + "_F"].notna(), c] = 0.0
    return us.set_index("NAICS2022")


def load_berd():
    rd = pd.read_excel(BERD_RD, header=None, engine="openpyxl")
    sa = pd.read_excel(BERD_SALES, header=None, engine="openpyxl")
    # Table 2: col 0 industry, col 1 NAICS text, col 8 domestic R&D performance total ($ millions).
    # Table 8: col 4 domestic sales of R&D performers or funders ($ millions).
    rd = rd.iloc[5:, [0, 1, 8]].set_axis(["industry", "naics", "rd_dom"], axis=1)
    sa = sa.iloc[6:, [1, 4]].set_axis(["naics", "sales_dom"], axis=1)
    for t in (rd, sa):
        t["naics"] = t["naics"].astype(str).str.strip()
    rd = rd.drop_duplicates("naics")
    sa = sa.drop_duplicates("naics")
    b = rd.merge(sa, on="naics", how="inner")
    b["rd_dom"] = pd.to_numeric(b["rd_dom"], errors="coerce")
    b["sales_dom"] = pd.to_numeric(b["sales_dom"], errors="coerce")
    print(f"BERD 2022: {len(rd)} rows in Table 2, {len(sa)} in Table 8, {len(b)} matched by NAICS text")
    return b.set_index("naics")


def wls(y, X, w=None):
    X = sm.add_constant(X)
    m = sm.WLS(y, X, weights=w) if w is not None else sm.OLS(y, X)
    return m.fit(cov_type="HC1")


def main():
    OUT.mkdir(exist_ok=True)
    ec = load_ec()
    berd = load_berd()

    rows = []
    for code, (plus, minus) in INDUSTRIES.items():
        missing = [c for c in plus + minus if c not in ec.index]
        if missing or code not in berd.index:
            print(f"  dropped {code}: missing Census codes {missing} or BERD row")
            continue
        v = ec.loc[plus, EC_FIELDS].sum() - (ec.loc[minus, EC_FIELDS].sum() if minus else 0)
        r = berd.loc[code]
        rows.append({"berd_naics": code, "industry": r["industry"], "shipments_bn": v["RCPTOT"] / 1e6,
                     "value_added_bn": v["VALADD"] / 1e6, "payroll_benefits_bn": (v["PAYANN"] + v["BENEFIT"]) / 1e6,
                     "pcm": (v["VALADD"] - v["PAYANN"] - v["BENEFIT"]) / v["RCPTOT"],
                     "capital_sales": v["ASTEND"] / v["RCPTOT"], "advertising_sales": v["PCHADVT"] / v["RCPTOT"],
                     "berd_rd_dom_bn": r["rd_dom"] / 1e3, "berd_sales_dom_bn": r["sales_dom"] / 1e3,
                     "rd_intensity": r["rd_dom"] / r["sales_dom"]})
    ind = pd.DataFrame(rows)
    ind["markup"] = 1 / (1 - ind["pcm"])                 # price / marginal cost implied by the Lerner index
    ind["pcm_net_of_rd"] = ind["pcm"] - ind["rd_intensity"]
    ind["rd_share_of_margin"] = ind["rd_intensity"] / ind["pcm"]
    ind = ind.sort_values("rd_intensity", ascending=False)
    print(f"Industries kept: {len(ind)} of {len(INDUSTRIES)}; shipments ${ind['shipments_bn'].sum():,.0f}bn, "
          f"BERD domestic R&D ${ind['berd_rd_dom_bn'].sum():,.1f}bn")
    ind.round(5).to_csv(OUT / "industries_2022.csv", index=False)
    print(ind[["berd_naics", "industry", "rd_intensity", "pcm", "pcm_net_of_rd", "shipments_bn"]]
          .round(3).to_string(index=False))

    # Totals for all manufacturing: Census sector 31-33 and BERD row 31-33.
    tot = ec.loc["31-33"]
    allm = berd.loc["31–33"]
    summary = pd.DataFrame([{
        "pcm_all_manufacturing": (tot["VALADD"] - tot["PAYANN"] - tot["BENEFIT"]) / tot["RCPTOT"],
        "rd_intensity_all_manufacturing": allm["rd_dom"] / allm["sales_dom"],
        "shipments_all_manufacturing_bn": tot["RCPTOT"] / 1e6,
        "industries": len(ind),
        "corr_pcm_rd": ind["pcm"].corr(ind["rd_intensity"]),
        "spearman_pcm_rd": ind["pcm"].corr(ind["rd_intensity"], method="spearman"),
        "mean_pcm_top_rd_tercile": ind["pcm"].iloc[: len(ind) // 3].mean(),
        "mean_pcm_bottom_rd_tercile": ind["pcm"].iloc[-(len(ind) // 3):].mean(),
        "mean_rd_top_tercile": ind["rd_intensity"].iloc[: len(ind) // 3].mean(),
        "mean_rd_bottom_tercile": ind["rd_intensity"].iloc[-(len(ind) // 3):].mean()}])
    summary.round(5).to_csv(OUT / "markup_summary.csv", index=False)
    print(summary.round(4).T.to_string())

    # Regressions. H0 (Romer, free entry): b = 1. H0 (no rents): b = 0. HC1 standard errors.
    out = []
    specs = [
        ("PCM on R&D intensity", ["rd_intensity"], None),
        ("PCM on R&D intensity, shipment-weighted", ["rd_intensity"], "shipments_bn"),
        ("PCM on R&D, capital and advertising intensity", ["rd_intensity", "capital_sales", "advertising_sales"], None),
        ("PCM on R&D intensity, excluding pharmaceuticals", ["rd_intensity"], None),
        ("PCM on R&D intensity, excluding petroleum and tobacco/beverages", ["rd_intensity"], None),
    ]
    for name, xs, w in specs:
        data = ind
        if "excluding pharmaceuticals" in name:
            data = ind[ind["berd_naics"] != "3254"]
        if "excluding petroleum" in name:
            data = ind[~ind["berd_naics"].isin(["324", "312"])]
        res = wls(data["pcm"], data[xs], data[w] if w else None)
        b, se = res.params["rd_intensity"], res.bse["rd_intensity"]
        t_one = (b - 1) / se
        p_one = 2 * stats.norm.sf(abs(t_one))
        ci = res.conf_int().loc["rd_intensity"]
        out.append({"model": name, "n": int(res.nobs), "const": res.params["const"], "const_se": res.bse["const"],
                    "b_rd": b, "se_rd": se, "ci_low": ci[0], "ci_high": ci[1], "p_b_eq_0": res.pvalues["rd_intensity"],
                    "p_b_eq_1": p_one, "r2": res.rsquared,
                    "b_capital": res.params.get("capital_sales", np.nan), "se_capital": res.bse.get("capital_sales", np.nan),
                    "b_advertising": res.params.get("advertising_sales", np.nan),
                    "se_advertising": res.bse.get("advertising_sales", np.nan)})
    reg = pd.DataFrame(out)
    reg.round(5).to_csv(OUT / "markup_regressions.csv", index=False)
    print(reg[["model", "n", "const", "b_rd", "se_rd", "p_b_eq_0", "p_b_eq_1", "r2"]].round(4).to_string(index=False))

    # Figure.
    fig, ax = plt.subplots(figsize=(7.5, 5))
    size = 20 + 300 * ind["shipments_bn"] / ind["shipments_bn"].max()
    ax.scatter(100 * ind["rd_intensity"], 100 * ind["pcm"], s=size, color="#4C78A8", alpha=0.6, edgecolor="white")
    res = wls(ind["pcm"], ind[["rd_intensity"]])
    xs = np.linspace(0, ind["rd_intensity"].max() * 1.05, 50)
    ax.plot(100 * xs, 100 * (res.params["const"] + res.params["rd_intensity"] * xs), color="#4C78A8",
            label=f"Fitted, slope {res.params['rd_intensity']:.2f}")
    ax.plot(100 * xs, 100 * (res.params["const"] + xs), color="#E45756", ls="--",
            label="Slope 1 (free entry; Romer implies at least this)")
    labels = {"3254": "Pharmaceuticals", "3344": "Semiconductors", "333242": "Chip-making machinery",
              "3342": "Communications equipment", "324": "Petroleum refining", "312": "Beverages and tobacco",
              "3361–63": "Motor vehicles and parts", "336411–13": "Aircraft", "3391": "Medical equipment",
              "311": "Food"}
    for _, r in ind.iterrows():
        if r["berd_naics"] in labels:
            ax.annotate(labels[r["berd_naics"]], (100 * r["rd_intensity"], 100 * r["pcm"]), fontsize=8,
                        xytext=(4, 3), textcoords="offset points")
    ax.set_xlabel("R&D as % of domestic sales (BERD 2022)")
    ax.set_ylabel("Price-cost margin, % of shipments (Economic Census 2022)")
    ax.set_title("Manufacturing industries: research spending and margins over variable cost")
    ax.legend(frameon=False, fontsize=9, loc="center right")
    ax.set_xlim(-1, 29)
    fig.tight_layout()
    fig.savefig(OUT / "markup_vs_rd.png", dpi=150)
    print("Wrote results/industries_2022.csv, results/markup_*.csv and results/markup_vs_rd.png")


if __name__ == "__main__":
    main()
