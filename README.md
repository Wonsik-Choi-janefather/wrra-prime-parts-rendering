# WRRA Prime Parts Rendering Followup 0.1–0.12 — reviewed collection

Wonsik Choi (sole author), ORCID 0009-0001-4263-9772. 2026-10-04.

**Reviewed collection DOI:** [10.5281/zenodo.23134716](https://doi.org/10.5281/zenodo.23134716) · [Zenodo record](https://zenodo.org/records/23134716).

This repository is devoted to the prime-parts followup. It does not combine this series with WRRA_M upstream/downstream synthesis. The antecedent exploratory synthesis is [DOI 10.5281/zenodo.23128482](https://doi.org/10.5281/zenodo.23128482).

## Review result

Verified inputs → WRRA transformation → outputs → falsifiers are laid out in the Korean and English reviewed manuscripts. The ten historical 0.1–0.10 calculations replayed in isolation; 0.1–0.2 agree numerically despite changed JSON serialization, 0.3–0.10 agree byte-for-byte. Stage 0.11 passes 47 cross-stage and 26 independent checks. Stage 0.12 passes 44 internal and 12 separate checks, and regenerates identical output bytes in a fresh directory. These are computational audits, not independent measurements.

At the chosen K15 finite-pool, linear-site, six-direction, ten-contact preparation, 0.12 gives 134.812677 expected first-generation fusion-photon absorptions and 133.477884 recaptures. The site occupancy independence and post-180-second pulse are model choices. Secondary capture photons are recorded but not spatially propagated. The collection ends at 0.12 as an executed, scoped model; no additional stage is required by this release.

## Files and reproduction

- `WRRA_Prime_Parts_0_1_to_0_12_Reviewed_EN.pdf` and `_KO.pdf`: bilingual scope and correction edition.
- `WRRA_Parts_Followup_0_11_Reproducibility.zip`: originals for stages 0.1–0.6, retained stage sources for 0.7–0.10, stage replay, 0.11 synthesis, inputs, results, audit.
- `WRRA_Parts_Followup_0_12_Reproducibility.zip`: finite-pool first-generation spatial model, source snapshots, checks, narrative, hashes.
- `REVIEW_LEDGER.json`: source and correction provenance, pass counts, acceptance scope.

Unpack each ZIP into its own directory. In the 0.11 directory run `OPENBLAS_NUM_THREADS=1 python3 replay_early.py`, then `OPENBLAS_NUM_THREADS=1 python3 replay_late.py`, `python3 compute.py`, and `python3 verify.py`. In the 0.12 directory run `OPENBLAS_NUM_THREADS=1 python3 compute.py` and `python3 verify.py`. Requires Python, NumPy, SciPy.

The historical stage results are snapshots and are not silently rewritten. This collection makes the correction to the 0.12 pool energy ledger explicit: the `initial_beta_budget_MeV` is already included in the electron and antineutrino records and must not be added a second time. The final `compute.py` checks absolute closure against the original common-source energy.

Model/empirical distinction: rest masses and neutron lifetime are inherited measured inputs; alpha/beta weights and spatial/coupling choices are calibrated/declared. WRRA originality lies in the executed structural ledger. Fixed-input outputs are conditional WRRA predictions, not independent measurements or a derivation of all microscopic forces.

## Focused case study of address 105

The separate two-page case paper and dataset explain finite assembly order, nucleon readouts and common source accounting with one worked example.

- [Case paper and reproducible dataset](case_studies/address_105/v1_0/README.md)
- Paper DOI: https://doi.org/10.5281/zenodo.23137504
- Dataset DOI: https://doi.org/10.5281/zenodo.23137540
