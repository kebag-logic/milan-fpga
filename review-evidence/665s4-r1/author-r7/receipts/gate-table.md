| Gate | rc | Result |
|---|---:|---|
| The reviewer's `nomap_probe.sh`, unedited | 2 at its link, as required | `no-map link rc=2`, the named refusal, no ELF |
| The plat page's command, as written | 0 | no stand-in load in `ls_*`; 39.0 tiles; its map equals the run's |
| The design page's command, as written | 0 | no stand-in load in `ls_*`; 59.0 tiles, ledgered |
| `firmware_boundary --without verilator` | 0 | `ctrl_boundary: PASS`; its `ctrl_plat_image.py` runs stopped at their link |
| `firmware_boundary --only verilator` | 0 | `ctrl_boundary: PASS` |
| S3's split boot, 1x1 | 0 | `ctrl_split_boot: PASS (0 finding(s))`, 84.372 ms, 18 of 18 writes |
| S3's split boot, 8x8 | 0 | `ctrl_split_boot: PASS (0 finding(s))`, 184.622 ms, 18 of 18 writes |
| S3's self-test | 0 | `6 of 6 native controls as required; 2 of 2 plants caught; 0 placement controls wrong` |
| `--placement-controls`, 1x1 and 8x8 | 0 | `ctrl_split_boot placement controls: 8 of 8 as required` at each |
| `ctrl_image_selftest.py --require-rv32` | 0 | `ctrl_image self-test: 37 checks PASS` |
| The nine literal mutants | 0 | `mutants: 9 planted, 0 escaped; clone clean after: True` |
| The reviewers' `refusal_probe.py`, `portable_checks.sh` | 0 | `misses: 0`; each of its checks rc 0, `guard on the real map: []` |
| `check_nvm_capture.py` | 0 | `PASS: capture census, clocks, both timing arms and receipt agree` |
| `check_py_idiom.py` | 0 | no new finding |
| `docs.yml`, every job, each on a fresh clone with an empty `HOME` and a new virtual environment | 0 | 71 steps ran, each rc 0; 24 not run, each with its reason; all three SDK steps downloaded the archive, verified `d42680e9...` and printed `SDK fresh installation: verified` |
| `git diff --check a68536fa`, merge bases | 0 | rc 0; one merge base, `a68536fa`, still `dev-soft-core`'s tip |
| The privacy check | 0 | `0 private line(s) in a68536fa..HEAD` |
| `rg '13\.863'` | | only `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`, where it records history |
