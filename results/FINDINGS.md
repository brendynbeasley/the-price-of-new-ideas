# Romer (1990) on US data: findings

## In plain English

Paul Romer's 1990 model says productivity growth is proportional to the number of people doing research, and that
the monopoly markup on each new design is what pays for the research behind it. This study checks both claims
against US data from 1949 to 2025 and against 36 manufacturing industries in 2022.

- **More research has not meant faster growth.** The resources the United States puts into R&D, measured in the
  number of workers the budget could hire, rose about 7 times from the 1950s to 2020–25, while productivity growth
  fell from 2.3% to about 1% a year. Each unit of research effort now buys roughly a sixteenth of the growth it did
  in the 1950s.
- **The decline is steady.** Research productivity has fallen about 4% a year, close to the 5% a year that Bloom,
  Jones, Van Reenen and Webb (2020) found. Growth tracks how fast research effort grows better than how large it is,
  as Charles Jones's 1995 critique predicts, but only because of the late 1950s and early 1960s; without those ten
  years the relation disappears.
- **Markups pay for research in drugs, not across manufacturing.** Pharmaceutical makers (Eli Lilly, Merck, Pfizer)
  spend 17% of sales on R&D and earn a 57% margin over production cost. Semiconductor makers (Intel, Micron) and
  chip-equipment makers (Applied Materials, Lam Research) spend as much on R&D but earn ordinary factory margins,
  while beverage and tobacco makers (Altria, Molson Coors) spend almost nothing on R&D and earn 52%. Across
  industries, margins do not rise with R&D spending.

The essay is in the [README](../README.md); the method is in [TECHNICAL.md](../TECHNICAL.md).

**Key to the labels below.** *g_tfp* = growth of BLS total factor productivity, private business, % a year.
*S_college_m* = total US R&D spending divided by the mean income of men 25+ with four or more years of college,
millions. *S_wage_m* = R&D divided by compensation per payroll job, millions. *S_ipp_college_m* = all intellectual
property investment divided by the college income, millions. *_index* = relative to the base decade (1970s for
college measures, 1950s otherwise). *rp_* = research productivity, g_tfp / S, indexed the same way. *pcm* =
price-cost margin, (value added − payroll − benefits) / shipments. *markup* = 1 / (1 − pcm). *rd_intensity* =
domestic R&D / domestic sales of R&D performers or funders (BERD). *capital_sales* = gross depreciable assets /
shipments. *advertising_sales* = advertising / shipments. Dollar figures are billions unless noted.

## Research effort and growth by decade (`growth_by_decade.csv`)

| decade | years | g_tfp | g_tfp_nonfarm | rd_bn | S_college_m | S_wage_m | S_ipp_college_m | oecd_researchers_m | S_college_index | rp_S_college_index | S_wage_index | rp_S_wage_index | S_ipp_college_index | rp_S_ipp_college_index | rd_real_index | rp_rd_real_index |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1950s | 10 | 2.315 | 1.873 | 6.758 |  | 1.452 |  |  |  |  | 1.000 | 1.000 |  |  | 1.000 | 1.000 |
| 1960s | 10 | 2.133 | 1.869 | 20.250 |  | 2.978 |  |  |  |  | 2.050 | 0.449 |  |  | 2.504 | 0.368 |
| 1970s | 10 | 1.167 | 1.050 | 40.291 | 2.072 | 3.296 | 2.707 |  | 1.000 | 1.000 | 2.270 | 0.222 | 1.000 | 1.000 | 3.100 | 0.163 |
| 1980s | 10 | 0.292 | 0.148 | 115.212 | 3.131 | 4.763 | 4.441 |  | 1.511 | 0.166 | 3.280 | 0.038 | 1.640 | 0.153 | 4.834 | 0.026 |
| 1990s | 10 | 0.907 | 0.817 | 201.392 | 3.540 | 5.595 | 5.830 | 0.903 | 1.709 | 0.455 | 3.853 | 0.102 | 2.153 | 0.361 | 6.394 | 0.061 |
| 2000s | 10 | 0.980 | 0.930 | 347.124 | 4.412 | 6.658 | 7.915 | 1.127 | 2.130 | 0.395 | 4.585 | 0.092 | 2.924 | 0.287 | 8.988 | 0.047 |
| 2010s | 10 | 0.739 | 0.745 | 534.698 | 5.734 | 7.859 | 10.628 | 1.325 | 2.768 | 0.229 | 5.412 | 0.059 | 3.926 | 0.161 | 11.556 | 0.028 |
| 2020–25 | 6 | 1.050 | 1.030 | 941.902 | 7.797 | 10.402 | 14.624 | 1.699 | 3.763 | 0.239 | 7.163 | 0.063 | 5.402 | 0.167 | 16.647 | 0.027 |

## Headline factors (`growth_headline_factors.csv`)

Change in research effort and research productivity between decade averages; per-year rates use the years between
decade midpoints.

| input | from | to | years_between_midpoints | g_tfp_from | g_tfp_to | effort_factor | effort_growth_pct_per_year | research_productivity_factor | rp_growth_pct_per_year |
|---|---|---|---|---|---|---|---|---|---|
| S_college | 1970s | 2010s | 40.000 | 1.167 | 0.739 | 2.768 | 2.545 | 0.229 | -3.685 |
| S_college | 1970s | 2020–25 | 47.500 | 1.167 | 1.050 | 3.763 | 2.790 | 0.239 | -3.011 |
| S_ipp_college | 1970s | 2010s | 40.000 | 1.167 | 0.739 | 3.926 | 3.419 | 0.161 | -4.559 |
| S_ipp_college | 1970s | 2020–25 | 47.500 | 1.167 | 1.050 | 5.402 | 3.551 | 0.167 | -3.772 |
| S_wage | 1950s | 2010s | 60.000 | 2.315 | 0.739 | 5.412 | 2.814 | 0.059 | -4.717 |
| S_wage | 1950s | 2020–25 | 67.500 | 2.315 | 1.050 | 7.163 | 2.917 | 0.063 | -4.087 |
| rd_real | 1950s | 2010s | 60.000 | 2.315 | 0.739 | 11.556 | 4.079 | 0.028 | -5.981 |
| rd_real | 1950s | 2020–25 | 67.500 | 2.315 | 1.050 | 16.647 | 4.166 | 0.027 | -5.337 |

## OECD researcher head count (`growth_oecd_researchers.csv`)

| researchers_1991 | researchers_2023 | factor | g_tfp_1991_2000 | g_tfp_2014_2023 |
|---|---|---|---|---|
| 822,350.250 | 1,733,124.311 | 2.107 | 1.007 | 0.796 |

## Regressions for the research equation (`growth_regressions.csv`)

Romer predicts a zero constant and a positive slope on effective researchers, and no trend in research
productivity. Annual models use Newey-West errors (4 lags); five-year block models use HC1 errors.

| model | term | coef | se | p | ci_low | ci_high | n | r2 | sample |
|---|---|---|---|---|---|---|---|---|---|
| annual: g on S (college deflator) | const | 0.798 | 0.388 | 0.040 | 0.037 | 1.559 | 59 | 0.000 | 1967-2025, Newey-West 4 lags |
| annual: g on S (college deflator) | S_college_m | 0.009 | 0.071 | 0.896 | -0.129 | 0.148 | 59 | 0.000 | 1967-2025, Newey-West 4 lags |
| annual: g on S (average-wage deflator) | const | 1.959 | 0.438 | 0.000 | 1.101 | 2.818 | 77 | 0.052 | 1949-2025, Newey-West 4 lags |
| annual: g on S (average-wage deflator) | S_wage_m | -0.151 | 0.067 | 0.023 | -0.282 | -0.021 | 77 | 0.052 | 1949-2025, Newey-West 4 lags |
| annual: g on OECD researchers (millions FTE) | const | 0.910 | 0.669 | 0.174 | -0.400 | 2.220 | 33 | 0.000 | 1991-2023, Newey-West 4 lags |
| annual: g on OECD researchers (millions FTE) | oecd_researchers_m | -0.004 | 0.511 | 0.994 | -1.005 | 0.997 | 33 | 0.000 | 1991-2023, Newey-West 4 lags |
| 5-year blocks: g on S (average-wage deflator) | const | 2.093 | 0.417 | 0.000 | 1.275 | 2.910 | 15 | 0.326 | 1950-2024, HC1 |
| 5-year blocks: g on S (average-wage deflator) | S_wage_m | -0.175 | 0.072 | 0.015 | -0.316 | -0.035 | 15 | 0.326 | 1950-2024, HC1 |
| 5-year blocks: g on S (college deflator) | const | 0.837 | 0.358 | 0.019 | 0.136 | 1.538 | 11 | 0.000 | 1970-2024, HC1 |
| 5-year blocks: g on S (college deflator) | S_college_m | 0.001 | 0.065 | 0.984 | -0.126 | 0.129 | 11 | 0.000 | 1970-2024, HC1 |
| 5-year blocks: ln research productivity on year (average-wage deflator) | const | 82.039 | 16.602 | 0.000 | 49.499 | 114.578 | 15 | 0.555 | 1950-2024, HC1 |
| 5-year blocks: ln research productivity on year (average-wage deflator) | year_mid | -0.042 | 0.008 | 0.000 | -0.058 | -0.026 | 15 | 0.555 | 1950-2024, HC1 |
| 5-year blocks: ln research productivity on year (college deflator) | const | 34.376 | 29.812 | 0.249 | -24.054 | 92.807 | 11 | 0.121 | 1970-2024, HC1 |
| 5-year blocks: ln research productivity on year (college deflator) | year_mid | -0.018 | 0.015 | 0.223 | -0.047 | 0.011 | 11 | 0.121 | 1970-2024, HC1 |
| 5-year blocks: g on growth of S (Jones 1995 alternative) | const | 0.735 | 0.175 | 0.000 | 0.393 | 1.077 | 14 | 0.255 | 1955-2024, HC1 |
| 5-year blocks: g on growth of S (Jones 1995 alternative) | dln_S_wage | 0.114 | 0.043 | 0.009 | 0.029 | 0.199 | 14 | 0.255 | 1955-2024, HC1 |
| 5-year blocks: g on growth of S, excluding 1955-64 | const | 0.939 | 0.197 | 0.000 | 0.553 | 1.326 | 12 | 0.002 | 1965-2024, HC1 |
| 5-year blocks: g on growth of S, excluding 1955-64 | dln_S_wage | -0.012 | 0.091 | 0.893 | -0.192 | 0.167 | 12 | 0.002 | 1965-2024, HC1 |

## Five-year blocks (`growth_five_year_blocks.csv`)

*block* is the first year of each five-year span. *dln_S_wage* is the growth of S_wage_m from the previous block,
% a year. *ln_rp_* is the log of g_tfp / S.

| block | g_tfp | S_college_m | S_wage_m | n | ln_S_wage | dln_S_wage | ln_rp_wage | ln_rp_college |
|---|---|---|---|---|---|---|---|---|
| 1950 | 2.689 |  | 1.057 | 5 | 0.055 |  | 0.934 |  |
| 1955 | 1.941 |  | 1.848 | 5 | 0.614 | 11.181 | 0.049 |  |
| 1960 | 2.596 |  | 2.625 | 5 | 0.965 | 7.023 | -0.011 |  |
| 1965 | 1.671 | 2.047 | 3.330 | 5 | 1.203 | 4.754 | -0.690 | -0.203 |
| 1970 | 0.961 | 1.958 | 3.183 | 5 | 1.158 | -0.900 | -1.198 | -0.712 |
| 1975 | 1.373 | 2.186 | 3.409 | 5 | 1.226 | 1.369 | -0.910 | -0.465 |
| 1980 | 0.117 | 2.880 | 4.271 | 5 | 1.452 | 4.511 | -3.598 | -3.204 |
| 1985 | 0.468 | 3.381 | 5.254 | 5 | 1.659 | 4.143 | -2.418 | -1.978 |
| 1990 | 0.566 | 3.480 | 5.337 | 5 | 1.675 | 0.312 | -2.244 | -1.817 |
| 1995 | 1.248 | 3.600 | 5.853 | 5 | 1.767 | 1.848 | -1.546 | -1.060 |
| 2000 | 1.672 | 4.082 | 6.384 | 5 | 1.854 | 1.737 | -1.340 | -0.893 |
| 2005 | 0.289 | 4.742 | 6.932 | 5 | 1.936 | 1.646 | -3.178 | -2.799 |
| 2010 | 0.788 | 5.385 | 7.302 | 5 | 1.988 | 1.040 | -2.227 | -1.922 |
| 2015 | 0.691 | 6.083 | 8.417 | 5 | 2.130 | 2.842 | -2.500 | -2.175 |
| 2020 | 1.095 | 7.761 | 10.285 | 5 | 2.331 | 4.010 | -2.240 | -1.958 |

The annual series behind these tables is in `growth_annual.csv` (1949–2025, 77 rows).

## Industries, 2022 (`industries_2022.csv`)

Sorted by R&D intensity. Shipments, value added and margins are from the 2022 Economic Census of manufacturing;
R&D and sales are from the 2022 Business Enterprise R&D Survey.

| berd_naics | industry | shipments_bn | pcm | markup | berd_rd_dom_bn | berd_sales_dom_bn | rd_intensity | pcm_net_of_rd | capital_sales | advertising_sales |
|---|---|---|---|---|---|---|---|---|---|---|
| 3344 | Semiconductor and other electronic components | 115.901 | 0.250 | 1.334 | 49.330 | 209.620 | 0.235 | 0.015 | 0.866 | 0.002 |
| 3254 | Pharmaceuticals and medicines | 234.230 | 0.568 | 2.314 | 116.073 | 685.744 | 0.169 | 0.399 | 0.487 | 0.008 |
| 333242 | Semiconductor machinery | 13.752 | 0.153 | 1.181 | 5.438 | 32.885 | 0.165 | -0.012 | 0.403 | 0.001 |
| 334511 | Search, detection, navigation, guidance, aeronautical, and nautical system and instruments | 53.454 | 0.297 | 1.422 | 4.146 | 25.280 | 0.164 | 0.133 | 0.217 | 0.001 |
| 334510, 334517 | Electromedical, electrotherapeutic, and irradiation apparatus | 48.743 | 0.302 | 1.432 | 4.578 | 34.617 | 0.132 | 0.169 | 0.201 | 0.004 |
| 3342 | Communications equipment | 41.261 | 0.248 | 1.329 | 11.665 | 94.162 | 0.124 | 0.124 | 0.289 | 0.003 |
| 336414–15, 336419 | Guided missile, space vehicle, and related parts | 36.732 | 0.139 | 1.161 | 10.785 | 102.365 | 0.105 | 0.034 | 0.410 | 0.000 |
| other 334 | Other computer and electronic products | 26.544 | 0.224 | 1.289 | 30.946 | 309.204 | 0.100 | 0.124 | 0.277 | 0.004 |
| 336411–13 | Aircraft, aircraft engine, and aircraft parts | 166.790 | 0.233 | 1.304 | 24.571 | 254.318 | 0.097 | 0.136 | 0.404 | 0.001 |
| other 3345 | Other measuring and controlling devices | 66.421 | 0.323 | 1.476 | 4.053 | 61.566 | 0.066 | 0.257 | 0.267 | 0.005 |
| 3391 | Medical equipment and supplies | 96.834 | 0.375 | 1.599 | 20.394 | 439.882 | 0.046 | 0.328 | 0.380 | 0.007 |
| 3336 | Engine, turbine, and power transmission equipment | 49.668 | 0.242 | 1.319 | 3.026 | 71.407 | 0.042 | 0.200 | 0.499 | 0.001 |
| 335 | Electrical equipment, appliances, and components | 172.684 | 0.319 | 1.469 | 7.086 | 190.989 | 0.037 | 0.282 | 0.302 | 0.002 |
| 3361–63 | Motor vehicles, bodies, trailers, and parts | 740.784 | 0.175 | 1.212 | 32.881 | 934.230 | 0.035 | 0.140 | 0.327 | 0.001 |
| other 336 | Other transportation | 72.538 | 0.225 | 1.290 | 2.992 | 85.180 | 0.035 | 0.190 | 0.293 | 0.002 |
| 3399 | Other miscellaneous manufacturing | 65.118 | 0.323 | 1.476 | 2.989 | 98.835 | 0.030 | 0.292 | 0.308 | 0.012 |
| other 333 | Other machinery | 329.631 | 0.270 | 1.370 | 8.713 | 313.360 | 0.028 | 0.242 | 0.310 | 0.003 |
| 336992 | Military armored vehicle, tank, and tank components | 6.884 | 0.371 | 1.589 | 0.030 | 1.288 | 0.023 | 0.347 | 0.176 | 0.000 |
| 33311 | Agricultural implement | 52.465 | 0.307 | 1.443 | 2.287 | 103.071 | 0.022 | 0.285 | 0.258 | 0.002 |
| 327 | Nonmetallic mineral products | 164.790 | 0.352 | 1.543 | 1.464 | 66.532 | 0.022 | 0.330 | 0.637 | 0.002 |
| 3256 | Soap, cleaning compound, and toilet preparations | 82.380 | 0.456 | 1.839 | 2.886 | 131.795 | 0.022 | 0.434 | 0.531 | 0.005 |
| 332 | Fabricated metal products | 465.673 | 0.296 | 1.421 | 3.526 | 188.388 | 0.019 | 0.278 | 0.407 | 0.002 |
| 3255, 3259 | Paint, coating, adhesive, and other chemicals | 107.978 | 0.332 | 1.497 | 1.223 | 67.008 | 0.018 | 0.314 | 0.390 | 0.002 |
| 3252 | Resin, synthetic rubber, and artificial synthetic fibers and filaments | 129.680 | 0.297 | 1.422 | 1.493 | 91.925 | 0.016 | 0.281 | 0.654 | 0.000 |
| 326 | Plastics and rubber products | 303.213 | 0.305 | 1.438 | 3.470 | 253.088 | 0.014 | 0.291 | 0.558 | 0.002 |
| 3253 | Pesticide, fertilizer, and other agricultural chemicals | 48.811 | 0.487 | 1.949 | 1.193 | 103.364 | 0.012 | 0.475 | 0.904 | 0.001 |
| 337 | Furniture and related products | 88.687 | 0.287 | 1.403 | 0.410 | 38.358 | 0.011 | 0.276 | 0.244 | 0.005 |
| 322 | Paper | 220.328 | 0.303 | 1.435 | 1.005 | 98.823 | 0.010 | 0.293 | 0.797 | 0.001 |
| 313–16 | Textile, apparel, and leather products | 64.844 | 0.244 | 1.324 | 0.635 | 71.745 | 0.009 | 0.236 | 0.386 | 0.004 |
| 311 | Food | 1,039.161 | 0.257 | 1.346 | 7.143 | 965.560 | 0.007 | 0.249 | 0.332 | 0.003 |
| 331 | Primary metals | 323.087 | 0.273 | 1.375 | 1.120 | 160.761 | 0.007 | 0.266 | 0.516 | 0.000 |
| 3251 | Basic chemicals | 297.894 | 0.369 | 1.586 | 2.860 | 413.607 | 0.007 | 0.362 | 0.724 | 0.000 |
| 312 | Beverage and tobacco products | 174.997 | 0.522 | 2.091 | 0.767 | 133.830 | 0.006 | 0.516 | 0.484 | 0.008 |
| 323 | Printing and related support activities | 90.914 | 0.309 | 1.448 | 0.165 | 29.296 | 0.006 | 0.304 | 0.481 | 0.004 |
| 321 | Wood products | 172.446 | 0.314 | 1.458 | 0.259 | 61.018 | 0.004 | 0.310 | 0.414 | 0.001 |
| 324 | Petroleum and coal products | 883.348 | 0.185 | 1.226 | 0.860 | 399.161 | 0.002 | 0.182 | 0.321 | 0.000 |

## Margin regressions (`markup_regressions.csv`)

PCM on R&D intensity across 36 industries, HC1 errors. Romer's free-entry condition implies b_rd = r / g_A, at
least 1 on his balanced growth path; *p_b_eq_1* tests the lower end, b_rd = 1.

| model | n | const | const_se | b_rd | se_rd | ci_low | ci_high | p_b_eq_0 | p_b_eq_1 | r2 | b_capital | se_capital | b_advertising | se_advertising |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PCM on R&D intensity | 36 | 0.316 | 0.019 | -0.239 | 0.344 | -0.913 | 0.436 | 0.488 | 0.000 | 0.023 |  |  |  |  |
| PCM on R&D intensity, shipment-weighted | 36 | 0.266 | 0.024 | 0.515 | 0.565 | -0.592 | 1.623 | 0.362 | 0.391 | 0.067 |  |  |  |  |
| PCM on R&D, capital and advertising intensity | 36 | 0.161 | 0.056 | -0.246 | 0.266 | -0.767 | 0.274 | 0.353 | 0.000 | 0.433 | 0.223 | 0.085 | 20.872 | 8.158 |
| PCM on R&D intensity, excluding pharmaceuticals | 35 | 0.323 | 0.018 | -0.561 | 0.218 | -0.988 | -0.134 | 0.010 | 0.000 | 0.146 |  |  |  |  |
| PCM on R&D intensity, excluding petroleum and tobacco/beverages | 34 | 0.312 | 0.017 | -0.211 | 0.338 | -0.874 | 0.451 | 0.531 | 0.000 | 0.022 |  |  |  |  |

## Summary statistics (`markup_summary.csv`)

| statistic | value |
|---|---|
| pcm_all_manufacturing | 0.282 |
| rd_intensity_all_manufacturing | 0.051 |
| shipments_all_manufacturing_bn | 7,048.664 |
| industries | 36 |
| corr_pcm_rd | -0.151 |
| spearman_pcm_rd | -0.232 |
| mean_pcm_top_rd_tercile | 0.279 |
| mean_pcm_bottom_rd_tercile | 0.321 |
| mean_rd_top_tercile | 0.121 |
| mean_rd_bottom_tercile | 0.008 |
