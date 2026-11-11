[A683zj] REVIEW READY

Commit: `e7e2b7444a9859b058deff0d9edb575f2fb1946f` (branch `665-s2b-cycles`, two commits on round 26's `0b37f3d2`; no merge, rebase, force or amend; not pushed). PR target `dev-soft-core`.

Changed:
- `e5baac61` (#882, ruling item 1): the CPU budget harness's `get_avb_info` row sends GET_AVB_INFO `0x0027` on AVB_INTERFACE 0 with its four-byte command (IEEE 1722.1-2021 7.4.40.1), not GET_AS_PATH `0x0028` on AVB_INTERFACE 9. Every row that ends at a response states its command or message type and its status (`tb/verilator/ctrl_service_budget/answers.py`). The grader holds the probe's own response, found by its sequence_id, to both; another type or status fails the run. A row that states a status other than SUCCESS is a refusal row, named `<row>, refused <status>`, and the run refuses a row that states no response. SUCCESS is asserted in arm B (`answering-ports`), whose observation ports answer; arm B's `aecp` group is now one of the load gate's legs at both points. Eighteen self-test checks and ten mutants, the plant restoring the refused command among them.
- `e7e2b744` (items 4 and 6): the lane splits. `load_grade.py --check` holds 1x1/1if for merge. 8x8/2if moves to `flip_grade.py`, a separately invoked check read at the pin's column, with its own `--selftest` (six controls, the over-ceiling row among them) and four more mutants in the harness self-test. The README and `docs/design/SPLIT_CONTROL_MEMORY.md` section 13 state the rows' rule, the baseline, the cut and the split.
- No firmware, RTL, mailbox contract, donor or submodule change.

Validation (on clean clones of the head, never piped):
- Every `run:` step of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml` that a pull request to `dev-soft-core` triggers: 139 steps rc 0, 226 not run (each with its reason), 0 bad. Among them: `firmware-unit` (`test_ctrl_firmware.py --require-rv32 --self-test` PASS, `fw_coverage.py --check` PASS over 38 files), `firmware-control-mutants` 672 of 672, `firmware-aecp-mutants` 220 `[ok]`, `firmware-srp-mutants` 340 `[ok]`, `firmware-boundary` and `firmware-verilator` `ctrl_boundary: PASS`, `bdd-conformance` 508 scenarios.
- The full sweep, four shard units: 65 of 65 suites passed, 2,613,726 checks, 0 failures; every preflight PASS.
- The harness self-test: 0 failures. `load_grade.py --selftest` 23 of 23 and `--check` PASS. `flip_grade.py --selftest` 6 of 6. `flip_grade.py --check` exits 1 by design: `OVER 8x8/2if: the load 0.815 at the pin is over the flip ceiling 0.70`.
- The harness at both points, every recorded group regraded at the head: 0 refusals; 6 misses of 996 (8x8/2if) and of 945 (1x1/1if) probe instances, all on the three egress-held paths (tsn-c-stack#26); 0 work passes over the share.
- `test_builder.py --require-rv32` (all gates pass, the same two arms not run as in round 14), `cd tests && behave`, `test_ctrl_nvm.py --require-rv32 --self-test`, the `ctrl_split_boot` runs and plants, `twin`, `gen_mailbox`, `lint_rtl`, the idiom and docs gates, and `git diff --check` against the merge base `1d6bf555`: all rc 0.

Acceptance criteria (the round 27 ruling, issuecomment-6788828284):
1. #882: met (its three acceptance items). The baseline, on unchanged firmware: each of round 26's legs rebuilt byte-identical; the `aecp` group run again in arm A, in arm B and with tsn-c-stack#32 at both points; every other group regraded under the new checks. 0 refusals, round 26's tallies, and no stated cost moves.
   - The changed rows: at 8x8/2if `get_avb_info` 0.338 ms (arm A, refused ENTITY_MISBEHAVING; 0.316 before) and 0.341 ms (arm B, SUCCESS); at 1x1/1if 0.118 and 0.143 ms.
2. One cut: the baseline gap at 8x8/2if was 0.019, so the cut of this tree's share of SRP's record was made. It was **measured on a scratch image and not committed**, so there is no firmware mutant. That is a deviation, for the manager to accept or overturn.
   - The heaviest SRP record went from 34,361 to 33,741 cycles, which puts 8x8/2if at about 0.713 with tsn-c-stack#32 and 0.809 at the pin, over 0.70 either way.
   - Its +160 B take arm A's image with tsn-c-stack#32 to 122,936 B, over the 8x8/2if ledger of 122,880 B.
3. The full gate pass at the head, once: every gate rc 0 but the flip check.
4. 8x8/2if over and 1x1/1if under, so the lane splits.
   - 1x1/1if: 0.450 with tsn-c-stack#32 (0.463 at the pin), held for merge.
   - 8x8/2if: 0.815 at the pin (0.719 with tsn-c-stack#32), held by the flip check, which fails at this head.
   - The flip-gate issue's text is in the handoff, for the manager to open.
5. The tripwire fires. The memo's figures: the baseline 0.719 / 0.815; after the cut about 0.713 / 0.809; between images on the same groups, the heaviest work pass moved -15,987 to +2,056 cycles.
6. tsn-c-stack, lwSRP and the donor clone untouched; the flip check reads the pin.
7. #870's `KL_mbx` round had not landed by the measurement, so the grade uses the harness's own access cycles and the flip-gate issue carries #870's.

Open risks/questions:
- D2: the cut is not committed (item 2 above).
- D1: GET_AVB_INFO's SUCCESS is asserted in arm B only. In arm A, the image as linked, the face's window is unanswered, so GET_AVB_INFO and GET_COUNTERS are named refusals. No arm measures the window reads answered.
- Firmware finding for its own issue: `aecp.c:428` keeps 14 bits of the AEM command_type, so `0x7FF0` is answered under `0x3FF0`.
- No row measures a talker's PROBE_TX answered SUCCESS.
