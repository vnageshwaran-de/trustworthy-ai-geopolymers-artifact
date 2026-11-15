# trustworthy-ai-geopolymers-artifact

Research artifact for the systematic review *From Property Prediction to Clean-Technology Deployment: A Systematic Review and Roadmap for Trustworthy AI in Low-Carbon Geopolymer Development* (PRISMA 2020; 669 unique primary studies).

Archived on Zenodo, all versions: [10.5281/zenodo.24253216](https://doi.org/10.5281/zenodo.24253216). Licence: CC BY 4.0.

This repository holds only the data and scripts that the article and its Supplementary Materials refer to. No abstract text from the reviewed articles is included; records are identified by DOI or Scopus EID and title.

## Screening and corpus
| File | Content |
|---|---|
| `corpus_screening.csv` | Screening ledger: per-record decisions and exclusion codes |
| `corpus_master.csv` | Records identified (Scopus and supplementary sources) |
| `corpus_fallback_only.csv` | Records from the supplementary search |
| `duplicate_audit.csv` | Duplicate-report evidence, including the 12 Nov 2026 amendment |
| `excluded_records.csv` | Record removed after the freeze (SD292) |

## Coded corpus and audits
| File | Content |
|---|---|
| `extraction_master.csv` | Coded corpus: 729 records, 728 included, 669 unique studies. Duplicates are flagged in `duplicate_of`; `post_freeze_status` marks the 12 Nov 2026 changes |
| `extraction_pilot.csv`, `extraction_deep.csv` | Full-template extractions (4 pilot and 12 deep-tier studies) |
| `physics_type_verification.csv` | Claimed-versus-verified physics audit (Supplementary Table S11) |
| `carbon_lca_audit.csv` | Environmental-evidence ladder, 122 classified studies (Table S12, Fig. 4) |

## Coding reliability (Table S9)
| File | Content |
|---|---|
| `recode/RECODE_INSTRUCTIONS.md` | Codebook given to the blind recoders |
| `recode/recode_worksheet_blind_70.csv` | The 70-study, year-stratified sample (abstract column removed) |
| `recode/recode_worksheet_human_completed.csv`, `recode/recode_procedural_blind_completed.csv` | The two completed blind recodes |
| `recode/recode_answer_key.csv` | Original codes of the 70 sampled studies, taken from `extraction_master.csv` |
| `recode/score_recode.py` | Agreement and Cohen's κ; run `python3 score_recode.py <completed_recode.csv>` from `recode/` |

Table S9 was computed on 31 Aug 2026 against a snapshot of the original codes. The answer key here is taken from the released `extraction_master.csv`, so a few κ values differ from Table S9 in the second decimal place.

## Keyword classifier, version 1.2 (Table S16)
| File | Content |
|---|---|
| `keyword_classifier/keyword_classifier.py`, `keyword_classifier/lexicon.json` | Deterministic classifier and its lexicon |
| `keyword_classifier/keyword_codes.csv` | Classifier output for the 729 frozen records |

## Full-corpus recode (Table S17)
| File | Content |
|---|---|
| `full_corpus_recode/full_corpus_recode.csv` | Per-record decisions: original and recoded task and environmental codes, whether each record was adjudicated, eligibility (with reason), the physics rescreen and carbon-ladder additions |
| `full_corpus_recode/recode_rules.py` | Deterministic screen that flagged records for adjudication |

## Documents cited in the Supplementary Materials
`documents/Stage2_Protocol.md` (protocol; S2), `documents/Stage3_Corpus_Report.md` (S2), `documents/Stage4_Taxonomy.md` (S4), `documents/Stage6_Research_Gaps.md` (S6), `documents/springerlink_sample_screen.md` (Note S7).
