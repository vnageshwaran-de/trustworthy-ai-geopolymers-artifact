# Stage 4 — Taxonomy: candidates, selection and coding rules

*Compiled for artifact v1.2 from the manuscript (v1.1 and revised versions), the coder instructions in `recode/RECODE_INSTRUCTIONS.md` and the classifier lexicon. The criterion-by-criterion scoring sheet for the three candidates is not part of this archive; only the summary result below is reported.*

## 1. Why a new organization was needed

Earlier reviews sort studies by algorithm family or by predicted property. Neither grouping shows whether a study can be trusted, transferred or used. The questions this review asks (how trustworthy, how physically grounded, how environmentally quantified, how close to deployment) are independent of one another: a study may place carbon inside an optimization while reporting no uncertainty. A single hierarchy cannot carry them.

## 2. Candidate taxonomies

Three candidates were developed and scored against six criteria: novelty, scientific value, interpretability, coding stability, journal relevance and downstream usefulness.

| Candidate | Structure | Outcome |
|---|---|---|
| A. AI-maturity ladder | One ordered axis: ML prediction, optimization, explainable AI, uncertainty-aware AI, physics-informed AI, inverse design, adaptive experimentation, autonomous discovery | Not adopted as the coding instrument; kept as a view of the coded corpus (Figure 2 of the paper) |
| B. Six-axis faceted classification | Each study receives a profile on six independent axes (Section 3) | **Adopted.** Highest total score, 52 of 60 |
| C. Clean-technology translation pipeline | Seven functional stages: understand, predict, trust, design, green-assess, adapt, discover | Not adopted as the coding instrument; kept as an ordering of the synthesis |

Candidates A and C are projections of candidate B. The ladder is obtained from the task, trust and physics codes; the pipeline from the task and environmental codes. Because all three are views of one coding, a disagreement about where a study sits can be settled by inspecting its released profile.

## 3. The six axes

| Axis | Values | Rule |
|---|---|---|
| **M** Material system | fly-ash, slag, FA-slag, metakaolin/clay, red-mud, tailings, biomass-ash, recycled-aggregate, one-part, stabilized-soil, mixed/other-AAM | Multi-label; shares sum to more than 100% |
| **T** AI task | experiment-selection > inverse-design > multi-objective-optimization > optimization > classification > microstructure/image-analysis > prediction | One primary label; the highest applicable label in this priority order wins |
| **R** Trust practices | explainability, uncertainty quantification, calibration, robustness, out-of-distribution evaluation, external validation, physical consistency, reproducibility | A flag is set only on concrete evidence of the practice |
| **P** Physics integration | Type I data only; Type II chemical quantities used as ordinary inputs; Type III domain knowledge shapes model structure; Type IV physical relations embedded in loss or architecture; Type V ML coupled to mechanistic simulation | Ambiguous cases take the lower type; author labels are audited, not accepted |
| **E** Environmental function | none-explicit, waste-valorization, durability, cost, carbon, LCA | Multi-label; quantification required. Calling a mix sustainable earns nothing |
| **D** Deployment maturity | laboratory prediction, externally validated model, formulation recommendation, process optimization, pilot, adaptive, autonomous | Furthest stage reached; adaptive work is marked simulated or physical |

## 4. How the axes are coded in this release

| Axis | Corpus-wide coding (669 studies) | Study-by-study coding |
|---|---|---|
| M, T, E | Keyword classifier (`classifier/`) | Human recode of 70 studies (`recode/`) |
| R | Keyword classifier for six flags: explainability, uncertainty, calibration, external validation, out-of-distribution, repository. Robustness and physical consistency cannot be coded from keywords | Human recode; full-text extraction rows |
| P | Keyword classifier assigns I, II or "III+ flag" | Physics audit of 32 studies (`physics_type_verification.csv`) |
| D | Not coded corpus-wide | Full-text extraction rows (`extraction_deep.csv`, `extraction_pilot.csv`) and the human recode |

The terms matched for each code are in `classifier/lexicon.json`.

## 5. Capability stages used in Figure 2

Each study is placed at the highest stage whose vocabulary it carries, tested in this order:

1. Stage 7, adaptive: task is experiment-selection
2. Stage 6, inverse design: task is inverse-design
3. Stage 5, physics-informed (flagged): physics code is "III+ flag"
4. Stage 4, uncertainty-aware: uncertainty or calibration flag
5. Stage 3, explainable AI: explainability flag
6. Stage 2, optimization: task is optimization or multi-objective optimization
7. Stage 1, ML prediction: everything else

Stage 8, autonomous, has no studies. The rule is implemented in `figures/make_figures.py`.
