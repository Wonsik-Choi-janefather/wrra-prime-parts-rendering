# Address 105 finite prime-parts case study

Wonsik Choi · sole author · ORCID [0009-0001-4263-9772](https://orcid.org/0009-0001-4263-9772) · janefather@gmail.com  
Version 1.0.0 · 2026-10-04

- [Case paper DOI](https://doi.org/10.5281/zenodo.23137504)
- [Separate dataset DOI](https://doi.org/10.5281/zenodo.23137540)
- [Prior reviewed collection 0.1–0.12](https://doi.org/10.5281/zenodo.23134716)

## Assessment path

**Verified inputs:** the published finite assembler and recorded neutron/proton/electron rest energies. Address 105, K15, the two traversal orders, prime readouts and source preparation are fixed configuration choices.

**WRRA transformation:** prime-labelled assembly → retained component identities → declared nucleon readouts → a common source ledger including unused components and full daughter energy budgets.

**Outputs:** small-first selects 11 components (`105 = 2+3+5+7+11+13+17+19+23+2+3`), read as 1 n and 10 D; large-first selects 4 (`105 = 47+43+13+2`), read as 1 n and 3 D. D is a complete proton/electron/electron-antineutrino bundle. Large-first retains seven source baryons. Both have total B=11 and energy 10335.21964134 MeV.

**Falsifiers:** a fixed-rule result mismatch or failed additive-address/Q/B/L/energy balance.

This case executes static assembly, declared readouts and a shared source budget. Physical preparation dynamics, individual spectra, time-dependent nuclear reactions, photon transport and cosmic abundance inference are not executed by this dataset. The source comparison and scalar reproduction pass. Check counts are implementation/conservation audit items.

## Paper

The paper is two pages in each language, with editable Word counterparts.

- [Korean PDF](paper/WRRA_Prime_Parts_105_Case_Study_v1_0_KO_2026_10_04.pdf)
- [English PDF](paper/WRRA_Prime_Parts_105_Case_Study_v1_0_EN_2026_10_04.pdf)
- [Korean Word](paper/WRRA_Prime_Parts_105_Case_Study_v1_0_KO_2026_10_04.docx)
- [English Word](paper/WRRA_Prime_Parts_105_Case_Study_v1_0_EN_2026_10_04.docx)

## Separate dataset

- [Download dataset ZIP](WRRA_Prime_Parts_105_Dataset_v1_0_2026_10_04.zip)
- [Korean data documentation](dataset/README_KO.md)
- [English data documentation](dataset/README_EN.md)
- [Assembly visits](dataset/data/assembly_trace.csv)
- [Selected component instances](dataset/data/component_instances.csv)
- [Per-prime counts](dataset/data/component_counts.csv)
- [Two source ledgers](dataset/data/case_ledger.csv)
- [Results and scalar checks](dataset/data/results.json)
- [Upstream comparison evidence](dataset/audit/source_comparison.json)
- [Review record](REVIEW_105.json)

```sh
cd dataset
python reproduce.py --check
```

Python 3.9+ with no external dependencies. Generated files go to a separate `reproduced/` directory and are compared byte-for-byte with the five reference result files. The dataset contains 45 traversal visits, 15 selected components, 30 per-prime records and two ledgers. All 28 scalar checks and 13 upstream assembly comparisons pass. The ZIP was extracted, reproduced and hash-verified separately before publication.

Copyright (C) 2026 Wonsik Choi. CC BY 4.0, consistent with the Zenodo records.
