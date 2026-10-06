[A539] REVIEW READY

Round 3 (assignment 6009196984). Not pushed.
Commit: `0f3d37dbffc4ca3f0e0f69499de80fc256a7db57`, three commits on `5747a8cb`:

- `c79c178e`: `--no-ff` merge of dev `a1e9839e` (#666, #668). There was no conflict.
- `e8f7d247`: moves `DUT_READER_DISPOSITIONS` unchanged into `scripts/measure_test_evidence_readers.py`.
- `0f3d37db`: `--no-ff` merge of dev `423ac5d9` (#669). #669 merged just after this round started, and I merged it before handing off. There was no conflict: #669 touches none of the lane's files.

Changed:
- `scripts/measure_test_evidence_readers.py` is new (154 lines): an SPDX header, a docstring, then the table.
  - The table is byte-identical to lines 596-730 at `c79c178e`: 135 lines, 35 entries, sha256 `ad10ad7a...c193` on both sides.
  - It also equals the base dict parsed from `c79c178e`, in the same order.
- `scripts/measure_test_evidence.py` goes from 1002 to 869 lines. It imports the table beside its other local imports. The section-3 comment names the new module. No other line changed.
- `docs/development/CODE_QUALITY.md:1761` now names the new module as the home of the live disposition list.

Registration: no gate needs an entry, so none was added.
- `scripts/ci_scope.py` has no per-script list. Every path under `scripts/` is relevant: `printf 'scripts/measure_test_evidence_readers.py\n' | python3 scripts/ci_scope.py` prints `true`. Its selftest passes.
- No script inventory or docs page lists helper modules. `lint_rtl_policy.py` and `measure_test_evidence_selftest.py` are named only by the script that imports them.

Validation, on clean worktrees with Verilator 5.050:
- `python3 scripts/check_py_idiom.py`: rc 0 at the head, with `long module: 10 <= 10`. `scripts/py_idiom.budget` is untouched and `--selftest` passes 54/54.
  - The tree before the move fails with rc 1 and `long module 11 > ratchet 10`. That holds both at `c79c178e` and with `423ac5d9` merged into it (a scratch merge, not committed).
- `python3 scripts/measure_test_evidence.py`, `--check` and `--selftest`: rc 0 for each, and the output before and after the move is byte-identical (`cmp`). That holds at `c79c178e` vs `e8f7d247`, and again with `423ac5d9` vs `0f3d37db`.
  - `--check`: PASS, with 0 unexplained readers and no stale disposition.
  - `--selftest`: 101/101.
- The 48-command builder bank at `0f3d37db` (base `423ac5d9`): 48 of 48 rc 0. It also passed 48 of 48 at `e8f7d247` (base `a1e9839e`).
  - Five commands need the pinned Markdown renderer, which this host's system interpreter lacks: `gen_toc.py` x3 and `check_em_dash.py` x2. On that interpreter they exit rc 2 with "renderer not installed". They pass with a venv of `tools/markdown/requirements.txt` first on PATH, with matching pins.
  - `xvlog_gate.py --check` ran under the Vivado lock and reports 2 findings, equal to the ratchet (0 in `hdl/`).
  - `test_builder.py` reports "ALL GATES PASS EXCEPT 1 NOT RUN". Gate 11 needs the mf48 place report, which is not on this host, as in round 2.
- What dev's merged files feed, all rc 0:
  - `sw/mailbox/gen_mailbox.py --check --crosscheck`: 0 findings. `--selftest`: 0 arms failed.
  - `make -C tb/verilator/mbx`: Wishbone 134/0, AXI4-Lite 179/0, cosim 13/0, quick mutants 4 of 4.
  - `make -C tb/verilator/mbx mutants`: both positive controls ok, 46 of 46 caught.
  - `sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <lwSRP 19f5796b>`: 51 of 51 caught, both pin arms ok, PASS.
  - `syn/yosys/run.sh`: 58 of 58 tops, including the three mailbox tops. Tap purity PASS.
  - `scripts/run_litex_sims.sh --selftest`: 10/10. The aggregate passes 4 of 4 with `MILAN_LITEX_PYTHON` set; see the first risk below.
  - `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test`: OK across 5 shapes, 42 checks, all 82 planted defects reddened.
  - `scripts/check_nvm_capture.py`: PASS. `scripts/check_nvm_record_space.py --self-test`: 0 findings.
  - `sw/builder/test_builder.py --require-elaboration --require-rv32`: as the bank's run, and no elaboration arm was skipped for a toolchain reason. This ran at both heads.
  - I ran the #666/#668 rows at `e8f7d247` and did not rerun them. Nothing they read changed in #669: it touches `sw/firmware/ctrl_nvm/` and two docs pages only, and no file those rows read names it.
- The lane's own suites were not rerun. Since `5747a8cb`, `git diff` touches `hdl/` only in `hdl/milan/mailbox/` and `README-tests.md` files, and moves no pin. `milan_datapath` instantiates no mailbox module, so the round-2 results stand.
- Area: I regenerated the OOC ship point. None of its sources or included HDL changed since `5747a8cb`, so the round-2 area figures stand.

Acceptance criteria (round 3):
1. Met: `c79c178e` and `0f3d37db`.
2. Met: identical output, and every ratchet is unchanged.
3. Met: nothing needed adding, with the evidence above.
4. Met: the bank and every feeder pass, all rc 0.

Open risks/questions:
- This one was already present at dev `a1e9839e`; I have not changed it. `scripts/run_litex_sims.sh:121-122` finds the sweep venv with a `sed` pattern anchored at column 0, but `sw/litex/sweep.sh:30` is indented.
  - So on a host whose `python3` lacks LiteX, every simulation is a declared skip (rc 90) unless `MILAN_LITEX_PYTHON` is set.
  - `test_builder.py:22611` uses an unanchored search and finds the venv. Hosted CI installs LiteX into `python3`, so it is unaffected.
  - It is a candidate for a separate issue.
- #645 adds entries to the table's old place in `measure_test_evidence.py`. After this lands, those entries belong in `scripts/measure_test_evidence_readers.py`.
- An updated PR body is ready for the manager to apply.
