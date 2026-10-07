[R526] POSITIVE - exact head af5be4710c3516cc247c353213d6939fa8d23f57

Independent composition pass recorded before opening prior public review bodies.
No composition defect found. This is the initial independent verdict and ledger;
the final REPORT.md will additionally reconcile prior public findings and record
the final checkout-integrity check.

The ordered parents are 72d3780d23a0b96362f8ae64059311b866ff5776 and
04e1435a218908d2b12b4053e5dab2c2dcac2ebf. The tree is
c2aaa434de409dd97074d71567c2df41d38af65e. The source base is
6714181d0c8a16e2983f85b724f4d688f5111835.

The sole additional-predecessor overlap is docs/testing/CI_WORKFLOWS.md.
Raw three-way composition reproduces its candidate bytes. The other 14 PR
entries retain source bytes and modes; all paths outside the PR delta retain
predecessor entries. Historical FT overlap was already in the source base.
Six deadline/default cases and their explicit overrides match the document.
The SDK installation precedes both required RV32 arms and their controls.
All 15 focused repository gates passed; composition_probe.py also passed.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composition touches CI acceptance: issue #679 and ruling 6022358702; REQUIREMENTS.md:306; .github/workflows/rtl-fast.yml:273; CI_WORKFLOWS.md:42. Required arms and object-only evidence boundary retained. | R526-3 composition; source behavior covered by R526-2 and R527-2 as assigned | af5be4710c3516cc247c353213d6939fa8d23f57; source 04e1435a218908d2b12b4053e5dab2c2dcac2ebf |
| RTL | CLEAN | Composition does not touch the PR's RTL scope: 15-path parent-to-candidate diff, hdl subtree and gitlinks retained from predecessor; firmware behavior and shipping inputs unchanged. Predecessor AAF change retained exactly. | R526-2 and R527-2 source coverage; R526-3 proves no new RTL interaction | source 04e1435a218908d2b12b4053e5dab2c2dcac2ebf; retention af5be4710c3516cc247c353213d6939fa8d23f57 |
| Robustness | CLEAN | Composition touches CI failure/timeout contracts: scripts/run_all_suites.sh:245; scripts/ci_events.py:7763; firmware required flags and gate inventory. Object dependency checks retain reviewed source bytes. | R526-3 composition; R526-2 and R527-2 source coverage | af5be4710c3516cc247c353213d6939fa8d23f57; source 04e1435a218908d2b12b4053e5dab2c2dcac2ebf |
| Tests | CLEAN | Composition touches gate scheduling/registries: scripts/ci_scope.py:22; scripts/measure_test_evidence.py; scripts/suite_shards.py; ci_events check/selftest; documentation and NVM record checks. Source tests retain bytes. | R526-3 composition; R526-2 and R527-2 source coverage | af5be4710c3516cc247c353213d6939fa8d23f57; source 04e1435a218908d2b12b4053e5dab2c2dcac2ebf |
| Docs | CLEAN | Composition directly touches CI_WORKFLOWS.md:42 and :188; sw/firmware/gtest/README.md:347; docs_check, TOC, anchors, paths, style, feature status, and em-dash gates passed. | R526-3 | af5be4710c3516cc247c353213d6939fa8d23f57 |

Limits: composition only. Source campaigns and full builder/native banks were
not rerun. The supplied R1 public packet is historical source evidence, not a
candidate bank. Hosted/local-replica acceptance and the final current-dev merge
turn remain manager duties. Physical calibration was NOT RUN; field skips and
static frames do not establish hardware or whole-program stack bounds.
