"""Romer (1990) research equation on US data, 1949-2025.

Romer's research sector produces new designs at the rate  dA/dt = delta * H_A * A,  so the growth rate of
technology is proportional to the human capital working in research:  g_A = delta * H_A.  This script asks
whether US productivity growth has kept pace with the resources put into research, following the aggregate
exercise in Bloom, Jones, Van Reenen & Webb (2020, AER, Section I.B), which itself restates Jones (1995).

Output of the idea production function: growth of BLS total factor productivity, private business sector.
Input: "effective researchers", meaning nominal US R&D spending (business + government, BEA) divided by a
wage, so it counts how many people the R&D budget could hire. Two wages are used:
  * mean income of men 25+ with four or more years of college (Census CPS tables P-19 and P-18), the deflator
    Bloom et al. describe, available from 1967;
  * average compensation per payroll job (BEA compensation of employees / BLS payroll employment), from 1948.
A third input, OECD counts of full-time-equivalent researchers, covers 1991-2023.

Run from the repository root:
    python src/ideas_and_growth.py
Missing raw files are downloaded into data/raw/ (FRED, Census, OECD; no keys needed).
Writes results/growth_*.csv and results/research_productivity.png.
"""
from pathlib import Path
import urllib.request

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

# FRED series (fredgraph.csv endpoint, no key). Titles from the BEA series register and BLS.
FRED = {
    "MFPPBS": "TFP index, private business sector (BLS)",
    "MFPNFBS": "TFP index, private nonfarm business sector (BLS)",
    "Y694RC1A027NBEA": "Gross domestic investment in R&D, total, $bn (BEA)",
    "Y006RC1A027NBEA": "Private fixed investment in R&D, $bn (BEA Table 5.6.5 line 6)",
    "Y001RC1A027NBEA": "Private fixed investment in intellectual property products, $bn (BEA)",
    "Y055RC1A027NBEA": "Government investment in intellectual property products, $bn (BEA)",
    "A191RD3A086NBEA": "GDP implicit price deflator, 2017 = 100 (BEA)",
    "A033RC1A027NBEA": "Compensation of employees, $bn (BEA)",
    "PAYEMS": "All employees, total nonfarm, thousands, monthly (BLS)",
}
CENSUS_URL = "https://www2.census.gov/programs-surveys/cps/tables/time-series/historical-income-people/{}.xlsx"
OECD_URL = ("https://sdmx.oecd.org/public/rest/data/OECD.STI.STP,DSD_MSTI@DF_MSTI,/USA.A.T_RS+B_RS.FTE.."
            "?startPeriod=1960&format=csvfilewithlabels")

FIRST_YEAR = 1949        # first year with a TFP growth rate (BLS index starts 1948)
LAST_YEAR = 2025         # last year with BEA R&D and BLS TFP at download (November 2026)
HAC_LAGS = 4             # Newey-West lags for annual regressions, a common choice for ~75 annual observations
BASE_DECADE_COLLEGE = "1970s"   # first full decade with the CPS college-income deflator (starts 1967)
BASE_DECADE_WAGE = "1950s"


def fetch(url, path):
    """Download url to path unless it is already there."""
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    print(f"  downloading {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    tmp = path.with_suffix(path.suffix + ".part")
    with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as f:
        f.write(r.read())
    tmp.rename(path)


def load_fred(series):
    path = RAW / "fred" / f"{series}.csv"
    fetch(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}", path)
    d = pd.read_csv(path)
    d.columns = ["date", "value"]
    d["value"] = pd.to_numeric(d["value"], errors="coerce")
    d["year"] = pd.to_datetime(d["date"]).dt.year
    return d.groupby("year")["value"].mean()   # monthly PAYEMS becomes an annual average


def cps_section(table, section, first_col=2):
    """Male mean income (current dollars) for one education section of a CPS historical table."""
    path = RAW / "census" / f"{table}.xlsx"
    fetch(CENSUS_URL.format(table), path)
    x = pd.read_excel(path, header=None, engine="openpyxl")
    labels = [str(v) for v in x[0].tolist()]
    start = labels.index(section)
    rows = {}
    for i in range(start + 1, len(labels)):
        lab = labels[i]
        if lab[:4].isdigit():
            year = int(lab[:4])
            val = pd.to_numeric(x.iloc[i, first_col], errors="coerce")
            rows.setdefault(year, []).append(val)
        elif i > start + 4 and not lab.startswith("nan") and not lab.startswith("Educational") \
                and not lab.startswith("Years of school"):
            break
    # 2013 and 2017 appear twice (CPS redesign years); average the two estimates.
    return pd.Series({y: float(np.nanmean(v)) for y, v in rows.items()}).sort_index()


def load_oecd():
    path = RAW / "oecd" / "oecd_msti_usa_researchers.csv"
    fetch(OECD_URL, path)
    d = pd.read_csv(path)
    d = d[(d["TRANSFORMATION"] == "_Z") & (d["MEASURE"] == "T_RS")]
    return d.set_index("TIME_PERIOD")["OBS_VALUE"].sort_index()


def decade_label(y):
    return "2020–25" if y >= 2020 else f"{(y // 10) * 10}s"


def ols(y, X, hac=None):
    X = sm.add_constant(X)
    m = sm.OLS(y, X, missing="drop")
    return m.fit(cov_type="HAC", cov_kwds={"maxlags": hac}) if hac else m.fit(cov_type="HC1")


def reg_rows(name, res, sample):
    out = []
    for term in res.params.index:
        ci = res.conf_int().loc[term]
        out.append({"model": name, "term": term, "coef": res.params[term], "se": res.bse[term],
                    "t": res.tvalues[term], "p": res.pvalues[term], "ci_low": ci[0], "ci_high": ci[1],
                    "n": int(res.nobs), "r2": res.rsquared, "sample": sample})
    return out


def main():
    OUT.mkdir(exist_ok=True)
    print("Loading FRED series")
    s = {k: load_fred(k) for k in FRED}
    for k, v in s.items():
        print(f"  {k}: {v.index.min()}-{v.index.max()}, {len(v)} years  ({FRED[k]})")

    print("Loading Census CPS mean income, men 25+ with four or more years of college")
    old = cps_section("p19", "College, 4 Years or More")       # 1967-1990, years of school completed
    new = cps_section("p18", "Bachelor's Degree or More")      # 1991-2025, educational attainment
    college = pd.concat([old[old.index <= 1990], new[new.index >= 1991]]).sort_index()
    print(f"  P-19 rows {len(old)} ({old.index.min()}-{old.index.max()}), "
          f"P-18 rows {len(new)} ({new.index.min()}-{new.index.max()})")
    print(f"  spliced at 1990/1991: 1990 = ${college[1990]:,.0f}, 1991 = ${college[1991]:,.0f}")

    print("Loading OECD full-time-equivalent researchers")
    oecd = load_oecd()
    print(f"  {oecd.index.min()}-{oecd.index.max()}, {len(oecd)} years")

    years = range(1948, LAST_YEAR + 1)
    d = pd.DataFrame(index=pd.Index(years, name="year"))
    d["tfp"] = s["MFPPBS"]
    d["tfp_nonfarm"] = s["MFPNFBS"]
    d["rd_bn"] = s["Y694RC1A027NBEA"]
    d["rd_private_bn"] = s["Y006RC1A027NBEA"]
    d["ipp_bn"] = s["Y001RC1A027NBEA"] + s["Y055RC1A027NBEA"]
    d["gdp_deflator"] = s["A191RD3A086NBEA"]
    d["comp_per_job"] = s["A033RC1A027NBEA"] * 1e9 / (s["PAYEMS"] * 1e3)
    d["college_income"] = college
    d["oecd_researchers"] = oecd
    d["g_tfp"] = 100 * np.log(d["tfp"]).diff()
    d["g_tfp_nonfarm"] = 100 * np.log(d["tfp_nonfarm"]).diff()
    # Effective researchers, in millions of people the R&D budget could pay.
    d["S_college_m"] = d["rd_bn"] * 1e9 / d["college_income"] / 1e6
    d["S_wage_m"] = d["rd_bn"] * 1e9 / d["comp_per_job"] / 1e6
    d["S_ipp_college_m"] = d["ipp_bn"] * 1e9 / d["college_income"] / 1e6
    d["rd_real_bn2017"] = d["rd_bn"] / d["gdp_deflator"] * 100
    d["oecd_researchers_m"] = d["oecd_researchers"] / 1e6
    d = d.loc[FIRST_YEAR:LAST_YEAR]
    kept = d["g_tfp"].notna().sum()
    print(f"Annual panel {FIRST_YEAR}-{LAST_YEAR}: {len(d)} years, {kept} with TFP growth; "
          f"{d['S_college_m'].notna().sum()} with the college deflator; dropped none")
    d.round(6).to_csv(OUT / "growth_annual.csv")

    # Decade averages, Bloom et al. style.
    d["decade"] = [decade_label(y) for y in d.index]
    dec = d.groupby("decade", sort=False).agg(
        years=("g_tfp", "size"), g_tfp=("g_tfp", "mean"), g_tfp_nonfarm=("g_tfp_nonfarm", "mean"),
        rd_bn=("rd_bn", "mean"), rd_real_bn2017=("rd_real_bn2017", "mean"),
        S_college_m=("S_college_m", "mean"), S_wage_m=("S_wage_m", "mean"),
        S_ipp_college_m=("S_ipp_college_m", "mean"), oecd_researchers_m=("oecd_researchers_m", "mean"))
    dec.loc[dec.index.isin(["1940s", "1960s"]), ["S_college_m", "S_ipp_college_m"]] = np.nan  # partial
    for col, base in [("S_college_m", BASE_DECADE_COLLEGE), ("S_wage_m", BASE_DECADE_WAGE),
                      ("S_ipp_college_m", BASE_DECADE_COLLEGE), ("rd_real_bn2017", BASE_DECADE_WAGE)]:
        tag = col.replace("_m", "").replace("_bn2017", "")
        dec[f"{tag}_index"] = dec[col] / dec.loc[base, col]
        dec[f"rp_{tag}_index"] = (dec["g_tfp"] / dec[col]) / (dec.loc[base, "g_tfp"] / dec.loc[base, col])
    dec = dec.drop(index=[i for i in dec.index if i == "1940s"])
    dec.round(4).to_csv(OUT / "growth_by_decade.csv")
    print("\nDecade averages")
    print(dec[["years", "g_tfp", "S_college_m", "S_college_index", "rp_S_college_index",
               "S_wage_index", "rp_S_wage_index"]].round(3).to_string())

    # Headline factors, 1970s to the 2010s and to 2020-25, and the 1950s-based wage version.
    head = []
    for col, base in [("S_college", BASE_DECADE_COLLEGE), ("S_ipp_college", BASE_DECADE_COLLEGE),
                      ("S_wage", BASE_DECADE_WAGE), ("rd_real", BASE_DECADE_WAGE)]:
        for end in ["2010s", "2020–25"]:
            span = (int(end[:4]) + (5 if end == "2010s" else 2.5)) - (int(base[:4]) + 5)
            f_s = dec.loc[end, f"{col}_index"]
            f_rp = dec.loc[end, f"rp_{col}_index"]
            head.append({"input": col, "from": base, "to": end, "years_between_midpoints": span,
                         "g_tfp_from": dec.loc[base, "g_tfp"], "g_tfp_to": dec.loc[end, "g_tfp"],
                         "effort_factor": f_s, "effort_growth_pct_per_year": 100 * np.log(f_s) / span,
                         "research_productivity_factor": f_rp,
                         "rp_growth_pct_per_year": 100 * np.log(f_rp) / span})
    head = pd.DataFrame(head)
    head.round(4).to_csv(OUT / "growth_headline_factors.csv", index=False)
    print("\nHeadline factors")
    print(head.round(3).to_string(index=False))

    # OECD headcount: researchers vs TFP growth, 1991-2023.
    o = d.loc[1991:2023]
    oecd_summary = pd.DataFrame([{
        "researchers_1991": o["oecd_researchers"].iloc[0], "researchers_2023": o["oecd_researchers"].iloc[-1],
        "factor": o["oecd_researchers"].iloc[-1] / o["oecd_researchers"].iloc[0],
        "g_tfp_1991_2000": d.loc[1991:2000, "g_tfp"].mean(), "g_tfp_2014_2023": d.loc[2014:2023, "g_tfp"].mean()}])
    oecd_summary.round(4).to_csv(OUT / "growth_oecd_researchers.csv", index=False)
    print("\nOECD researchers (FTE)")
    print(oecd_summary.round(3).to_string(index=False))

    # Regressions. Romer: g_t = delta' * S_t, so a = 0 and b > 0.
    rows = []
    a = d.dropna(subset=["g_tfp", "S_college_m"])
    rows += reg_rows("annual: g on S (college deflator)", ols(a["g_tfp"], a[["S_college_m"]], HAC_LAGS),
                     f"{a.index.min()}-{a.index.max()}, Newey-West {HAC_LAGS} lags")
    a = d.dropna(subset=["g_tfp", "S_wage_m"])
    rows += reg_rows("annual: g on S (average-wage deflator)", ols(a["g_tfp"], a[["S_wage_m"]], HAC_LAGS),
                     f"{a.index.min()}-{a.index.max()}, Newey-West {HAC_LAGS} lags")
    a = d.dropna(subset=["g_tfp", "oecd_researchers_m"])
    rows += reg_rows("annual: g on OECD researchers (millions FTE)",
                     ols(a["g_tfp"], a[["oecd_researchers_m"]], HAC_LAGS),
                     f"{a.index.min()}-{a.index.max()}, Newey-West {HAC_LAGS} lags")
    # Five-year blocks reduce cyclical noise in annual TFP growth.
    d["block"] = (d.index // 5) * 5
    b = d.loc[1950:2024].groupby("block").agg(g_tfp=("g_tfp", "mean"), S_college_m=("S_college_m", "mean"),
                                               S_wage_m=("S_wage_m", "mean"), n=("g_tfp", "size"))
    b["ln_S_wage"] = np.log(b["S_wage_m"])
    b["dln_S_wage"] = 100 * b["ln_S_wage"].diff() / 5          # growth of research effort, % per year
    b["ln_rp_wage"] = np.log(b["g_tfp"] / b["S_wage_m"])
    b["ln_rp_college"] = np.log(b["g_tfp"] / b["S_college_m"])
    b.round(5).to_csv(OUT / "growth_five_year_blocks.csv")
    bb = b.dropna(subset=["S_wage_m"])
    rows += reg_rows("5-year blocks: g on S (average-wage deflator)", ols(bb["g_tfp"], bb[["S_wage_m"]]),
                     f"{bb.index.min()}-{bb.index.max() + 4}, HC1")
    bc = b.dropna(subset=["S_college_m"])
    bc = bc[bc.index >= 1970]
    rows += reg_rows("5-year blocks: g on S (college deflator)", ols(bc["g_tfp"], bc[["S_college_m"]]),
                     f"{bc.index.min()}-{bc.index.max() + 4}, HC1")
    bt = b.copy()
    bt["year_mid"] = bt.index + 2
    rows += reg_rows("5-year blocks: ln research productivity on year (average-wage deflator)",
                     ols(bt["ln_rp_wage"], bt[["year_mid"]]), "1950-2024, HC1")
    btc = bt[bt.index >= 1970]
    rows += reg_rows("5-year blocks: ln research productivity on year (college deflator)",
                     ols(btc["ln_rp_college"], btc[["year_mid"]]), "1970-2024, HC1")
    bj = b.dropna(subset=["dln_S_wage"])
    rows += reg_rows("5-year blocks: g on growth of S (Jones 1995 alternative)",
                     ols(bj["g_tfp"], bj[["dln_S_wage"]]), f"{bj.index.min()}-{bj.index.max() + 4}, HC1")
    # Sensitivity: the two blocks of fastest effort growth (1955-59 and 1960-64) left out.
    bj2 = bj[~bj.index.isin([1955, 1960])]
    rows += reg_rows("5-year blocks: g on growth of S, excluding 1955-64",
                     ols(bj2["g_tfp"], bj2[["dln_S_wage"]]), "1965-2024, HC1")
    reg = pd.DataFrame(rows)
    reg.round(5).to_csv(OUT / "growth_regressions.csv", index=False)
    print("\nRegressions")
    print(reg[["model", "term", "coef", "se", "p", "n", "r2"]].round(4).to_string(index=False))

    # Figure: Bloom et al. Figure 1 on current data.
    fig, ax1 = plt.subplots(figsize=(8, 4.6))
    dd = dec
    x = np.arange(len(dd))
    ax1.bar(x, dd["g_tfp"], color="#4C78A8", width=0.6, label="TFP growth, % a year (left)")
    ax1.set_ylabel("TFP growth, % per year")
    ax1.set_xticks(x)
    ax1.set_xticklabels(dd.index)
    ax2 = ax1.twinx()
    ax2.plot(x, dd["S_wage_index"], color="#E45756", marker="o",
             label="Effective researchers, 1950s = 1 (right)")
    ax2.set_ylabel("Effective researchers, multiple of 1950s")
    ax2.set_ylim(0, None)
    ax1.set_ylim(0, max(dd["g_tfp"].max() * 1.3, 2.5))
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left", frameon=False, fontsize=9)
    ax1.set_title("US research effort and productivity growth by decade")
    fig.text(0.01, 0.01, "TFP: BLS private business. Effective researchers: BEA R&D spending / compensation "
             "per payroll job.", fontsize=7, color="#555")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / "research_productivity.png", dpi=150)
    print("\nWrote results/growth_*.csv and results/research_productivity.png")


if __name__ == "__main__":
    main()
