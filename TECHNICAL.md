# Technical notes

This is the technical companion to the [README](README.md). It covers the data, the method, every test statistic
and how to reproduce the results. All tables are in [results/FINDINGS.md](results/FINDINGS.md), and the review of
the original paper's methods is in [METHODS_REVIEW.md](METHODS_REVIEW.md).

## The original study

Paul M. Romer, "Endogenous Technological Change," *Journal of Political Economy* 98(5, Part 2), October 1990,
pp. S71–S102. I worked from the free NBER version (Working Paper 3210, December 1989); equation numbers below are
from that version. The paper is theoretical and has no data. Its formal core is the research equation
$`\dot{A} = \delta H_A A`$ (equation 3), the monopoly pricing of each design-based good against the demand curve in
equation 4, and the free-entry condition $`\pi = r P_A`$ (equation 6'). The balanced growth rate is
$`g = (\delta H - \Lambda\rho)/(\sigma\Lambda + 1)`$ with $`\Lambda = \alpha/[(\alpha+\beta)(1-\alpha-\beta)]`$
(equations 14 and 15), so growth rises with human capital and does not depend on labor. The abstract states that
"the stock of human capital determines the rate of growth" and that too little human capital goes to research.

The benchmark test is Bloom, Jones, Van Reenen and Webb (2020, Section I.B), restating Jones (1995): since the
1930s US research effort rose by a factor of 23 and research productivity fell by a factor of 41, or 5.1% a year
(p. 1110).

## Headline results

| Test | Estimate (s.e.) | p | N |
|---|---|---|---|
| TFP growth on effective researchers, college deflator, annual 1967–2025 | 0.009 (0.071) | 0.90 | 59 |
| TFP growth on effective researchers, average-wage deflator, annual 1949–2025 | −0.151 (0.067) | 0.023 | 77 |
| Same, five-year blocks 1950–2024 | −0.175 (0.072) | 0.015 | 15 |
| TFP growth on OECD FTE researchers (millions), annual 1991–2023 | −0.004 (0.511) | 0.99 | 33 |
| Trend in ln research productivity, average wage, per year | −0.042 (0.008) | < 0.001 | 15 |
| Trend in ln research productivity, college wage, per year, 1970–2024 | −0.018 (0.015) | 0.22 | 11 |
| TFP growth on growth of effective researchers (Jones) | 0.114 (0.043) | 0.009 | 14 |
| Same, excluding the 1955–59 and 1960–64 blocks | −0.012 (0.091) | 0.89 | 12 |
| Industry PCM on R&D intensity, 2022 (H0 b = 1) | −0.239 (0.344) | 0.0003 | 36 |
| Same, shipment-weighted (H0 b = 1) | 0.515 (0.565) | 0.39 | 36 |

Research effort rose 5.4 times from the 1950s to the 2010s (R&D over compensation per payroll job) while decade TFP
growth fell from 2.31% to 0.74%, so research productivity fell to 0.059 of its 1950s level. With all intellectual
property investment over the college wage, as in Bloom et al., the decline from the 1970s to the 2010s is 4.6% a year.

## Data

| File | Source | Used for |
|---|---|---|
| `data/raw/fred/MFPPBS.csv`, `MFPNFBS.csv` | BLS total factor productivity, private business and private nonfarm business, via FRED | Idea output |
| `data/raw/fred/Y694RC1A027NBEA.csv` | BEA gross domestic investment in R&D, business plus government | Research input |
| `data/raw/fred/Y006RC1A027NBEA.csv` | BEA private R&D investment | Reported only |
| `data/raw/fred/Y001RC1A027NBEA.csv`, `Y055RC1A027NBEA.csv` | BEA private and government intellectual property investment | Bloom et al. input |
| `data/raw/fred/A033RC1A027NBEA.csv`, `PAYEMS.csv` | BEA compensation of employees; BLS nonfarm payroll employment | Average-wage deflator |
| `data/raw/fred/A191RD3A086NBEA.csv` | BEA GDP price index | Real R&D |
| `data/raw/census/p19.xlsx`, `p18.xlsx` | Census CPS Tables P-19 (1967–1990) and P-18 (1991–2025), mean income of men 25+ | College deflator |
| `data/raw/oecd/oecd_msti_usa_researchers.csv` | OECD MSTI, US researchers, full-time equivalent | Head count |
| `data/raw/ncses/nsf24335-tab002.xlsx`, `tab008.xlsx` | 2022 Business Enterprise R&D Survey, Tables 2 and 8 | Industry R&D and sales |
| `data/raw/census/EC2231BASIC.zip` | 2022 Economic Census, manufacturing basic statistics | Industry margins |

All files were downloaded on November 1, 2026. The scripts download any FRED, Census CPS or OECD file that is
missing.

## Method

Rules fixed before looking at results:

1. Idea output is $`g_t = 100\,\Delta\ln \text{TFP}_t`$, BLS private business sector, 1949–2025.
2. Effective researchers are $`S_t = \text{R\&D}_t / w_t`$, with $`w_t`$ either mean income of college men (P-19
   "College, 4 years or more" spliced to P-18 "Bachelor's degree or more" at 1990/1991; the duplicate 2013 and 2017
   estimates are averaged) or BEA compensation divided by average payroll employment.
3. Decades are calendar decades; 2020–25 has six years. The college measure starts with the 1970s because the
   1960s have only three years.
4. Romer's prediction and the tests:

```math
\begin{aligned}
g_t &= a + b\,S_t + \varepsilon_t, \qquad H_0\colon a = 0,\ b > 0 \\
\ln(g_k/S_k) &= c + d\,\text{year}_k + u_k, \qquad H_0\colon d = 0 \\
g_k &= c_0 + c_1\,\Delta\ln S_k + v_k
\end{aligned}
```

   Annual regressions use Newey-West errors with four lags; five-year block regressions ($`k`$ = 1950–54, ...,
   2020–24) use HC1 errors.
5. For the industry test, the 36 most detailed non-overlapping manufacturing rows of BERD Table 2 are matched to
   Census NAICS codes, with "other" rows rebuilt as parent minus listed children. R&D intensity is domestic R&D
   performed over domestic sales of R&D performers or funders (BERD's own definition). Summed over an industry's
   designs, free entry gives rents over sales equal to $`r/g_A`$ times R&D over sales, and $`r = \rho + \sigma g`$
   is at least $`g`$ when $`\sigma \ge 1`$, so Romer implies a slope of at least one; the test is at its lower end.
   The margin and the test are:

```math
\begin{aligned}
\text{PCM}_i &= \frac{\text{VALADD}_i - \text{PAYANN}_i - \text{BENEFIT}_i}{\text{RCPTOT}_i} \\
\text{PCM}_i &= a + b\,\text{RD}_i + \gamma' X_i + e_i, \qquad H_0\colon b = 1
\end{aligned}
```

   with $`X_i`$ empty or containing gross depreciable assets over shipments and advertising over shipments, and
   HC1 errors. Advertising withheld by the Census (14 national rows flagged D) is set to zero. Only two of those
   codes, 336415 and 336419, enter the industry sums, so the guided missile and space vehicle row understates its
   advertising; the other flagged codes are detailed industries whose published parents are used instead.

Three robustness variants were also fixed in advance: shipment weights, dropping pharmaceuticals, and dropping
petroleum and beverages and tobacco. The Jones regression without the 1955–59 and 1960–64 blocks was added after
seeing that those two blocks have by far the fastest growth of research effort.

## Full industry results

| Specification | a (s.e.) | b (s.e.) | 95% CI for b | p (b = 0) | p (b = 1) | R² |
|---|---|---|---|---|---|---|
| Baseline | 0.316 (0.019) | −0.239 (0.344) | [−0.913, 0.436] | 0.49 | 0.0003 | 0.02 |
| Shipment-weighted | 0.266 (0.024) | 0.515 (0.565) | [−0.592, 1.623] | 0.36 | 0.39 | 0.07 |
| With capital and advertising | 0.161 (0.056) | −0.246 (0.266) | [−0.767, 0.274] | 0.35 | < 0.001 | 0.43 |
| Excluding pharmaceuticals | 0.323 (0.018) | −0.561 (0.218) | [−0.988, −0.134] | 0.010 | < 0.001 | 0.15 |
| Excluding petroleum, beverages and tobacco | 0.312 (0.017) | −0.212 (0.338) | [−0.874, 0.451] | 0.53 | 0.0003 | 0.02 |

In the controlled model, capital intensity enters at 0.223 (0.085) and advertising intensity at 20.9 (8.2). The
Spearman correlation between margin and R&D intensity is −0.23. All of manufacturing has a margin of 28.2% and an
R&D intensity of 5.1%.

## Judgment calls

The SEC's EDGAR servers returned HTTP 403 to every request during this work, so the planned firm-level version of
the markup test (gross margins and R&D expense from XBRL filings) was replaced by the industry version. Bloom et al.
deflate intellectual property investment rather than R&D; I use R&D as the main input because Romer's research
sector produces designs, and report the intellectual property version alongside. The BLS TFP series starts in 1948,
so the decade comparisons cannot start in the 1930s as Bloom et al.'s do.

## Reproducing the results

```bash
pip install -r requirements.txt
python src/ideas_and_growth.py
python src/markups_and_research.py
```

The first script writes `results/growth_*.csv` and `results/research_productivity.png`; the second writes
`results/industries_2022.csv`, `results/markup_*.csv` and `results/markup_vs_rd.png`. Both run in under a minute.

## References

- Bloom, N., Jones, C. I., Van Reenen, J. & Webb, M. (2020). Are ideas getting harder to find? *American Economic
  Review* 110(4), 1104–1144.
- Ha, J. & Howitt, P. (2007). Accounting for trends in productivity and R&D. *Journal of Money, Credit and Banking*
  39(4), 733–774.
- Jones, C. I. (1995). R&D-based models of economic growth. *Journal of Political Economy* 103(4), 759–784.
- National Center for Science and Engineering Statistics (2024). Business Enterprise Research and Development:
  2022. NSF 24-335.
- Romer, P. M. (1989). Endogenous technological change. NBER Working Paper 3210.
- Romer, P. M. (1990). Endogenous technological change. *Journal of Political Economy* 98(5, Part 2), S71–S102.
