# Methods review: Romer (1990)

- **Paper.** Paul M. Romer, "Endogenous Technological Change," *Journal of Political Economy* 98(5, Part 2),
  October 1990, pp. S71–S102.
- **Statistical focus.** The research equation $`\dot{A} = \delta H_A A`$, which makes the growth rate proportional
  to human capital in research, and the free-entry condition $`\pi = rP_A`$, which makes monopoly rents on designs
  exactly cover their cost.
- **Review standard.** Internal consistency of the formal results, explicitness of assumptions, and the testability
  of the predictions.
- **What was read.** The full text of NBER Working Paper 3210 (December 1989), the free version of the paper,
  including the appendix. I did not read the published *JPE* text, so equation numbers and page references below
  are to the working paper; the published version may differ in numbering and wording. Bibliographic details of the
  published version were checked against Crossref. Secondary accounts read: Bloom, Jones, Van Reenen and Webb
  (2020, *AER*), Section I.B and Section VII.

## Methods summary

The paper is a theoretical general-equilibrium growth model with no data. Section 2 argues from a replication
argument that a production function with productive nonrival inputs cannot be concave, so price-taking equilibrium
cannot pay for the nonrival input. Section 3 specifies three sectors: research (designs produced by human capital
and the existing stock of designs, equation 3), intermediate goods (each design licenses a monopoly producer of a
durable, facing the inverse demand of equation 4), and final goods (an extended Cobb-Douglas in human capital, labor
and the continuum of durables, equation 1). Preferences are constant-elasticity with discount rate $`\rho`$ and
parameter $`\sigma`$. Section 5 solves for a balanced growth path in closed form (equations 10 to 17) and compares it
with the planner's solution (equation 19, appendix A2). Section 6 discusses trade and cites Sokoloff (1988) as
supportive historical evidence on canals and patenting.

Research design, sampling strategy, sample size, inclusion and exclusion criteria, missing data treatment,
confidence intervals and p-values do not apply, because the paper estimates nothing. The independent variables of
the theory are the parameters $`\delta, H, L, \eta, \alpha, \beta, \rho, \sigma`$ and the dependent variables are the
growth rate $`g`$, the research share $`H_A/H`$, the interest rate and the price of designs. The "statistics" are the
formal results below.

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Research technology | $`\dot{A} = \delta H_A A`$, designs per unit time | Section 3, equation 3 | Output of new designs is linear in research human capital and in the existing stock | That the linearity in $`A`$ (no diminishing returns to ideas) holds empirically; the paper calls both linearities functional-form assumptions made "for analytical convenience" |
| Growth rate of designs | $`g = \delta H_A`$, per unit time | Section 5, text after equation 10 | Balanced growth rate as a function of research input | Any magnitude; $`\delta`$ is not calibrated |
| Monopoly price | $`p = r\eta/(1-\alpha-\beta)`$, markup $`1/(1-\alpha-\beta)`$ | Equations 5 and 13 (first-order condition) | Price set by each durable producer against the demand in equation 4 | That observed markups equal this value; no calibration of $`\alpha, \beta`$ is given |
| Free-entry condition | $`\pi(t) = r(t) P_A`$ | Equation 6' (from equation 6) | Flow rent on a design equals interest on its price | That rents and design costs are equal in any industry; it is an equilibrium assumption |
| Interest rate | $`r = \rho + \sigma g`$ | Equation 11 | Euler equation on the balanced path | Nothing beyond the preference specification |
| Equilibrium growth | $`g = (\delta H - \Lambda\rho)/(\sigma\Lambda + 1)`$, $`\Lambda = \alpha/[(\alpha+\beta)(1-\alpha-\beta)]`$ | Equations 14 and 15; appendix A1 | Growth rises with total human capital $`H`$ and is independent of $`L`$ and $`\eta`$ | Scale of the effect; the formula holds only on the balanced path with fixed $`H`$ and $`L`$ |
| Research threshold | $`H_A = 0`$ when $`H`$ is low enough | Equation 16, Figure 2 | Possibility of stagnation; research behaves like a luxury good | That any country is actually below the threshold |
| Social optimum | Planner's growth exceeds the equilibrium rate, coefficient $`\Theta = \alpha/(\alpha+\beta) < \Lambda`$ | Equation 19, appendix A2 | Too little research in equilibrium because of the knowledge spillover and the markup | Size of the gap or the optimal subsidy; transition dynamics are explicitly not analyzed |
| Trade result | Integration replaces $`H`$ with world human capital, raising $`g`$ | Section 6 | Growth effect of market integration | Empirical effect; supported only by citation of Sokoloff (1988) |

## Interpretation notes

- The headline claims in the abstract (human capital determines growth, too little research in equilibrium, trade
  raises growth, population alone is not enough) follow from the stated assumptions; I found no internal
  inconsistency in the steps that could be followed in the working paper's text. Several displayed equations are
  partly illegible in the scanned working paper, so I relied on the surrounding text for their content.
- The growth rate's independence from $`L`$ is presented as a correction to Romer (1987), where growth increased in
  $`L`$. The model keeps a scale effect in human capital, which is the property Jones (1995) later tested.
- The paper is explicit that $`H`$ and $`L`$ are held fixed for tractability and that only balanced growth paths are
  characterized. Welfare comparisons are along balanced paths, not including transitions.
- The cross-good symmetry of the model means every design earns the same markup. A cross-industry test that relates
  margins to research intensity is an extension of the free-entry logic, not a prediction the paper states.

## Unanswered questions

- How should $`H_A`$ be measured in data: researchers, R&D spending, or spending deflated by skilled wages? The
  paper's definition of human capital (years of education and training) does not settle it.
- Does the linearity of equation 3 in $`A`$ survive, or does research productivity fall as the stock of ideas grows?
  Bloom et al. (2020) report it falling in the aggregate and in every micro setting they study.
- What determines the split of rents between the research sector and the intermediate producer when design and
  production occur in the same firm, as the paper allows?
- How large is the gap between the equilibrium and optimal growth rates for plausible parameter values?

## Items requiring expert verification

- The exact typeset form of equations 14, 15 and 19 in the published *JPE* version, since the working-paper scan is
  partly illegible at those equations; the forms given here are consistent with the surrounding text and with
  standard textbook statements of the model.
- Whether page and equation numbering in the published version match the working paper.
- Whether Sokoloff (1988) and Sokoloff and Khan (1989) as cited support the model's mechanism to the degree the
  paper suggests; I did not read them.

No published correction or comment documenting an analytical error in the paper was found in the sources I read.
Reporting gaps (no calibration, no numerical examples of magnitudes) are a matter of the paper's purpose rather than
errors.

The modern rerun in this repository does not reproduce anything in the paper, which has no data. It tests the two
predictions above with US time series and 2022 industry data, and finds no proportional link between research effort
and productivity growth, and margins that rise less than one for one with research intensity across industries.
