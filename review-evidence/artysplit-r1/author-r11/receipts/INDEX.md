# Round 11 receipt index

Head `c0b625d1792e61b8e99944daea65b842e6b9dcde` on branch `arty-int-1127`, four commits on round 10's `640699e68`.
No product image changes; the census, its extract and the egress row stand as round 10 measured them.
Prepared locally; nothing has been posted or pushed.

[MANIFEST.json](MANIFEST.json) lists the 337 receipt files with each one's bytes and SHA256 before and after redaction.
Every file here passes the publication scrub unchanged.

## The bare-metal gate's five findings (`ea73a3f74`)

- [baremetal/baremetal-before-640699e6.log](baremetal/baremetal-before-640699e6.log): at `640699e6`, `check_baremetal_only.py --check` fails with the five findings: three `[T] retired-stack term 'Linux'`, two `[R] ... '/sys'`.
- The rewording keeps each meaning:
  - section 15 and `ctrl_loop.h`: no host's scheduling profile is part of this FPGA point;
  - the harness README: #983's host point;
  - `arty_grade.py`: `CPU (sys domain) clock`;
  - `egress_ledger.py`: `CPU and system clock`.
- [baremetal/gate-baremetal.log](baremetal/gate-baremetal.log): 0 findings across 1,981 files at the head; [baremetal/gate-baremetal-selftest.log](baremetal/gate-baremetal-selftest.log): 867 arms.

## Three more gate failures the local CI found, and their fixes

- **Test-evidence ratchet** ([findings/docs__docs-gates-0-37.log](findings/docs__docs-gates-0-37.log)): round 10's `egress_mii.py` reads `milan_datapath.sv` (the gasket's `GAP_CYCLES`) with no disposition. `22adb80ed` records why the read is not an implementation-derived oracle: its waits are the census's measured departures, held to the testbench's C++ queue.
- **Firmware coverage ratchet** ([findings/rtl-fast__firmware-unit-leg2-12.log](findings/rtl-fast__firmware-unit-leg2-12.log)): `ctrl_plat_console.c` covered 97 of 98 branches against a stale record of 68/68. The `lat` command added 30 branches.
  - The uncovered arc is infeasible: `lat` requires `c->len == 15`, and the name walk compares `at <= 3` with it. It is the same arc under the CI image's gcc 13.3.0 ([coverage/cov13-check.log](coverage/cov13-check.log)) and the host's gcc 16.2.1 ([coverage/cov-check.log](coverage/cov-check.log)).
  - `5469c8dc5` adds the exclusion row (`arc 2 of 4`; the table now has seventeen rows) and records the console at 154/154 lines and 97/97 branches. That is the figure `--write` records under gcc 13 ([coverage/cov13-write.log](coverage/cov13-write.log)).
  - [coverage/chk-v13.log](coverage/chk-v13.log) and [coverage/chk-v16.log](coverage/chk-v16.log): `--selftest` and `--check` pass under both compilers.
  - The removal of the redundant bound, which would change every image, was not taken.
- **Register reference freshness** ([findings/docs__docs-gates-0-attempt1-51.log](findings/docs__docs-gates-0-attempt1-51.log)): `248d85c14` had edited the generated `REGISTER_MAP.md` by hand.
  - `c0b625d17` moves that prose into `scripts/register_descriptions.json` and regenerates.
  - The page comes out byte-identical to the committed one, plus the three `GPTP_*_LAT` parameter rows the RTL adds, and the RTL fingerprint is refreshed.

## Every CI job a pull request runs, locally, at the head

[ci-final/results.json](ci-final/results.json): 67 jobs, all PASS, 212 gate steps run, none nonzero:
- docs: 7 jobs;
- elaborate: 5;
- rtl-fast: 23;
- rtl-full: 32 (the preflight, 27 Verilator shards, 4 Yosys shards).

Each job's step logs are under [ci-final/](ci-final/); [ci-runner/run_ci.py](ci-runner/run_ci.py) is the runner.

How it ran, and where it differs from a hosted run:
- `act` replays only a pushed PR head, and this head is not pushed. So each job's `run:` steps ran as the workflow files state them: bash `-eo pipefail`, matrix values and step conditions applied, each job in its own copy of a clean clone at the head with its submodules at their pins.
- The base is the live `dev-soft-core`, `0b594023`, fetched read-only into a scratch mirror.
- Setup, cache, evidence-recording and cancellation steps were not run. The pinned tools stood in:
  - Verilator v5.050, sv2v v0.0.12 and Yosys 0.66;
  - the RV32 SDK;
  - a Python 3.12 venv built with CI's own install, LiteX-pin, patch-series and VexiiRiscv commands ([ci-runner/venv312-setup.log](ci-runner/venv312-setup.log)).
- `nproc` reported 4, as on a hosted runner.
- Jobs that only read other jobs' artifacts (the aggregators, case unions, manifest and fail-fast) were not run.
- `rtl/physical-gptp` runs only on `schedule` or `workflow_dispatch`, so it was stopped; it is not a pull-request job.

## Product images

- [identity/product-identity.json](identity/product-identity.json): every shipping product ELF, built from clean clones of `640699e6` and of the head, is byte-identical:
  - `endstation_arty_split` `f17d1a9d…`, the published image;
  - `endstation_ax7101_8x8` `0f1450ac…`;
  - `endstation_ax7101_1x1_tdm8` `6e0a5412…`.
  It was checked at `ea73a3f74` too ([identity/product-identity-ea73a3f74.json](identity/product-identity-ea73a3f74.json)).
- [identity/](identity/): `ctrl_loop.h` at both heads, comment-stripped (`gcc -fpreprocessed -dD -E -P`), is byte-identical (SHA256 `26be07bc…`) with the same 667 lines. Nothing compiled, line tables included, can differ.
  Since `640699e6`, the only changes under `sw/`, `hdl/`, `configs/` and the submodules are that comment and two coverage files that are not compiled.

## The census, its extract and the egress row

- [consistency/extract-regrade.log](consistency/extract-regrade.log): round 10's published extract regrades at the head, 159/159, worst pass 143,181 cycles, line for line as round 10's.
- [consistency/extract-egress.log](consistency/extract-egress.log): the 100 Mb/s row from the same extract is 505.738 us of 1 ms.
- No re-measurement: the images are identical.

## Standalone gates at the head

[gates/gates11.rc](gates/gates11.rc): all 23 exit 0:
- the ten documentation and idiom gates;
- eight standalone self-tests and `arty_grade.py`;
- the bare-metal gate and its self-test;
- the test-evidence ratchet;
- the register reference.

[source/round11-commits.patch](source/round11-commits.patch): the four commits.
