## Gates

All at `b7fe6a777e562359d2a5693f3f4285fb6bd8f1ce`, each on a clean clone, every clone clean after. Receipts in `receipts/`, indexed in `receipts/INDEX.md`. The first five rows are the ruling's; the rest are additions.

| Gate | rc | Result |
|---|---:|---|
| `ctrl_image_selftest.py --require-rv32` | 0 | `ctrl_image self-test: 40 checks PASS` |
| `firmware_boundary --without verilator` | 0 | `ctrl_boundary: PASS`; four `ctrl_plat_image.py` runs stopped at their link; `ctrl_image_selftest.py: exit 0` |
| `firmware_boundary --only verilator` | 0 | `ctrl_boundary: PASS`; four `ctrl_plat_image.py` runs stopped at their link |
| `docs.yml`, every job, each on a fresh clone with an empty `HOME` and a new virtual environment | 0 | 71 steps ran, each rc 0; 24 not run, each with its reason; all three SDK steps downloaded the archive, verified `d42680e9...` and printed `SDK fresh installation: verified`. Its two builder legs print `ALL GATES PASS EXCEPT 16 NOT RUN` and `EXCEPT 1 NOT RUN`, the counts round 7's printed; this round has no separate builder run behind them |
| `git diff --check` and the privacy check | 0 | rc 0 against `a68536fa` and `37e03930`; `0 private line(s) in a68536fa..HEAD`; one merge base, still `dev-soft-core`'s tip |
| The fifteen literal mutants | 0 | `mutants: 15 planted, 0 escaped; clone clean after: True` |
| The reviewer's `partial_map_probe.sh`, unedited | 0 | as above |
| `map_edges.sh` | 0 | as above |
| S3's split boot, 1x1 | 0 | `ctrl_split_boot: PASS (0 finding(s))`, 84.372 ms, 4,218,617 CPU cycles, 18 of 18 writes |
| S3's split boot, 8x8 | 0 | `ctrl_split_boot: PASS (0 finding(s))`, 184.622 ms, 9,231,088 CPU cycles, 18 of 18 writes |
| `check_py_idiom.py` | 0 | no new finding |

The two boundary modes ran concurrently on two clones (`wt-bnd`, `wt-bnd2`), beside the docs replay. There is no `seq_boundary.sh` this round, so nothing published disagrees with what ran (R737-4-S1's point).

## Not done
