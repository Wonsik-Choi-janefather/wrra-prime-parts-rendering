# WRRA Address 105 Prime Parts Case Study Dataset

Wonsik Choi · sole author · Independent Researcher, Seoul  
ORCID 0009-0001-4263-9772 · janefather@gmail.com  
Version 1.0.0 · 2026-10-04

Dataset: https://doi.org/10.5281/zenodo.23137540  
Associated paper: https://doi.org/10.5281/zenodo.23137504  
Case repository: https://github.com/Wonsik-Choi-janefather/wrra-prime-parts-rendering/tree/main/case_studies/address_105/v1_0  
Prior reviewed collection: https://doi.org/10.5281/zenodo.23134716

## Scope and assessment

Verified inputs are the published assembler and its recorded particle rest energies. Address 105, the first 15 primes, the two traversal orders, the 5/47 neutron assignment, the inactive source reserve and the common budget are fixed model choices. The WRRA transformation is finite prime-labelled assembly → identity-preserving nucleon readout → shared source accounting including reserves and nonrest budgets. The outputs are 11 components (1 n + 10 D) versus 4 (1 n + 3 D), with common total B=11 and energy 10335.21964134 MeV. A failure of the fixed-rule result or address, charge, baryon, lepton or energy conservation falsifies this executed construction.

These are deterministic model outputs, not laboratory measurements, observed particle counts or samples of cosmic energy fractions. Each traversal visits every prime once and selects it if it fits the current remainder. Repeat full traversals while the remainder is at least 2. The pool is reusable between traversals; repeated components retain occurrence indices. A complete D bundle contains a proton, electron, electron antineutrino and the associated energy budget. This dataset executes static assembly/readout/source accounting; it does not execute microscopic preparation, individual spectra, time-dependent nuclear reactions or photon transport.

## Files and units

The `data/` directory contains five generated files: `assembly_trace.csv` (45 visits), `component_instances.csv` (15 selections), `component_counts.csv` (30 per-prime records), `case_ledger.csv` (two ledgers), and `results.json` (outputs and 28 checks). `inputs.json` records fixed inputs; `data_dictionary.json` defines every CSV column. `audit/source_comparison.json` records 13 upstream-code comparison checks, source hashes and provenance. `audit/upstream_assembly_excerpt.txt` preserves the exact upstream loop executed in that comparison. `metadata.json` records authorship, DOI links and scope. `SHA256SUMS` covers distributed files other than itself.

CSV files are UTF-8 with LF newlines. Dimensionless address labels, component/particle counts, electric charge in elementary-charge units, baryon/lepton numbers and MeV energies remain distinct. Each ledger is per prepared address-105 case. Decimal strings retain the supplied input precision, not newly estimated experimental uncertainty.

## Reproduction

Python 3.9+ and no third-party packages are required. Decimal energy calculations use precision 40.

```sh
python reproduce.py --check
```

This writes to the separate `reproduced/` directory and compares recalculated bytes with all five distributed files in `data/`. It does not overwrite reference data. Select another destination with `--output`.

The 28 checks cover address identities, each traversal step, selected components, source/particle accounting and deliberately incomplete or duplicated ledgers. The 13 upstream checks execute the original assembly AST for address array [105] and weight [1], compare the K15 readouts and verify that the four original K15/K16 assemblies have common maximum count 11. They do not rerun the complete one-million-address population or later reaction calculations. Check counts are implementation/conservation audits, not independent observational confirmations.

## Energy and reserve semantics

Both additive address residues are zero, while large-first retains seven **source** baryons. The two concepts must not be conflated. Address 105 is not a baryon count, MeV energy or spatial coordinate.

The common source energy is 11 × 939.56542194 = 10335.21964134 MeV. A D has proton-plus-electron rest energy 938.78308838069 MeV and an unresolved antineutrino/kinetic/recoil budget of 0.78233355931 MeV. Record that budget once; it is not automatically photon energy. Inactive reserves are a stipulated source preparation, not observed free neutrons made stable. Different assignments share total budgets; this dataset does not establish dynamics from one identical microscopic preparation to both outcomes.

## Rights and citation

Copyright (C) 2026 Wonsik Choi. Creative Commons Attribution 4.0 International. https://creativecommons.org/licenses/by/4.0/

Wonsik Choi (2026). *WRRA Address 105 Prime Parts Case Study Dataset* (1.0.0). Zenodo. https://doi.org/10.5281/zenodo.23137540
