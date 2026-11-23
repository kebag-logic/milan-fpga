# HANDOFF r2: milan-fpga #983 / PR #986, [A830]

**Status: REVIEW READY at `66b4def34dcbc0d371ce4eb339d3d0226875befa`. Committed locally on `pf-linuxprof-1`, NOT pushed. The remote branch is still `677d605f`.** All three R900-1 items are addressed. The `[A830] REVIEW READY` is posted on #983: https://github.com/kebag-logic/milan-fpga/issues/983#issuecomment-7100207805

## What was done

- **F1 (MINOR):** `load_config` reads `board.target` with `_req(brd, "target", "board")`. A `board` of `[]`, `""` or `["ax7101"]` raises `ConfigError: board: missing required key 'target'` again, as at the base. Gate 42 gains these three rows (31 refusals). The rows fail under `677d605f`'s builder.
- **F2 (MINOR), decision:** the rule is the widest advertised format, at IEEE 802.1Q-2018 35.2.2.8.4 a) and 35.2.2.8, with Milan v1.2 4.3.3.2 Table 4.4 per format. The firmware declares one fixed TSpec per source, and SET_STREAM_FORMAT moves an idle output to any advertised format without re-declaring. The code is unchanged; docs section 6 and the `load_config` comment now state the rule.
  - Gate 41's new `_check_host_tspec` requires 217 octets, not 73, for a talker with a 2-channel current format that advertises 2 and 8. It fails under a current-format mutant.
  - **The board's `endstation_pb2_bridge.yaml` image does not change** (5784 bytes, the same sha256, MaxFrameSize 217 at both heads).
- **R1 (RESIDUE):** the PR body Status uses the reviewer's sentence, plus one clause that round 2's head is local until pushed.
- **Identity:** 245/245 FPGA artifacts are byte-identical across base, `677d605f` and `66b4def3` (R900-1's own probe: 5 configs x own/split/all-fabric).
- **Gates at `66b4def3`:** 32, 41, 42 and `test_bad_configs_rejected` pass. The 24 docs and quality gates are all rc=0.

## For the manager

- **Publish:** push `pf-linuxprof-1` (`66b4def3`). Then replace the PR #986 body with [PR-BODY.md](PR-BODY.md). After the push, the Status paragraph's "becomes the published head when it is pushed" clause can be shortened to name `66b4def3` as published. The push restarts the hosted gates (the PR is not a draft), and act must be run from a trusted dev worktree.
- **Re-review:** R900 should re-review `66b4def3`. The internal cleared-context review is still unassigned.
- **Still owed** (not run this round): the full builder suite at `66b4def3`, gate 1b, the firmware shards and mutation campaigns, and candidate-merge validation against current `dev`.
- **Possible new Issue** (not filed): `board: null` or an integer raises TypeError at the base and at the head. That is pre-existing and outside F1.
- **Process notes:**
  - An intermediate commit `fb021a13` failed `check_py_idiom` (`load_config` grew to 101 lines) and was amended. That is disclosed in [receipts/INDEX.md](receipts/INDEX.md).
  - The em-dash gate needed the pinned renderer, which was installed with `--require-hashes` into `receipts/scratch/venv`.
  - The board YAML was fetched read-only into `download/`.
  - One read-only `git status` was run in `$LANES/pb2-aecp` to confirm it was untouched. No file there was edited.

Files: [REVIEW-READY.md](REVIEW-READY.md), [PR-BODY.md](PR-BODY.md), [receipts/INDEX.md](receipts/INDEX.md).

REVIEW READY 66b4def34dcbc0d371ce4eb339d3d0226875befa
