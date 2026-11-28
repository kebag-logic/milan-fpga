# A869 public-source privacy forward fix: HANDOFF

**Status (15:52 CET 2026-11-28): REVIEW READY.** There are 3 local branches, one commit each. All gates pass at base and at head, the firmware is byte-identical, and the A868 rescan is clean except 2 documented literals per milan-fpga tree. Nothing was pushed, posted or commented.
**ETA:** none. The work is done. What remains is the manager's decisions in NEEDS-MANAGER.md and opening the 3 PRs.

## Heads

| repo | branch | base | head |
|---|---|---|---|
| kebag-logic/milan-fpga | `privfix-bench-names` | dev-soft-core `c1c42843` | `0715cb206050c49a1745dd2d11e2fc0e1b74116b` |
| kebag-logic/milan-fpga | `privfix-bench-names-dev` | dev `e275d795` | `e7974868ef362f521e59fb82446ff54a19886bfa` |
| Mister-M-alt/FPGA-gPTP | `privfix-bench-names` | main `5ab111e3` | `e3fde4489655b1f7771cdfdf114485d237a86b75` |

- At 15:50 the upstream bases were unchanged, so each branch is one commit on the current upstream head.
- Worktrees: $LANES/privfix-1128 and $LANES/privfix-1128-dev, both added from $LANES/postmerge-0923. That clone's own checkout and its other worktrees were not touched.
- FPGA-gPTP clone: $LANES/fpgagptp-privfix.
- Commit subject on all three: "Remove bench-specific names from documentation and tools" (FPGA-gPTP: "…from documentation"). One line, no body and no trailer. The brief's commit rule replaced the default attribution trailer.

## What changed

**milan-fpga.** The same 21 files and the same 66 diff lines on both branches.
- The tap product becomes "inline capture tap", or `capture-tap` as a fixture label.
- The two bench host names become "controller bench host" and "a second bench host". The second one is not matched by rules.py and was fixed by hand.
- The switch becomes "the AVB switch".
- Two fixture IPs become RFC 5737 addresses: the `check_baremetal_only.py` ssh arm, and a mock gateway in an `act_ci.py` self-test.
- A path into the private test repo that was named after the two hosts now names the directory and describes the script.
- Touched Markdown lines lost their em dashes (gate rule). REGISTER_MAP_CLASSES.md's 3-entry Contents block moved to `--` as a whole, because gen_toc keeps one separator per block.
- No identifier, CLI option, wire or file-format literal changed. The 28-octet tap header handling and `--tap` are untouched, and only prose, help text, comments, one scenario title and one fixture label moved. Nothing under hdl/, sw/, syn/, configs/, avdecc/, ci/ or any submodule was touched.

**FPGA-gPTP.** `docs/history/v1/BENCH_FIRSTLIGHT.md`: `--ftdi-serial <serial>`, one line.

## Verification (receipts/INDEX.md)

- **Gates.** 32 gates per milan-fpga tree, base and head, under the same conditions (5 public submodules, pinned md-venv). They cover the doc checks (check_doc_style, the em-dash gate, docs_check, toc, anchors, inventory and the rest), the hygiene and idiom gates, the avtp_wire_truth and torture_campaign self-tests, act_ci `--selftest`, check_baremetal_only `--check` and `--selftest`, behave on the 3 touched features and the full behave suite. Result: **0 changed and 0 failing in both trees**. FPGA-gPTP `make docs` passes at base and at head.
- **Byte identity.** `test_ctrl_firmware.py --require-rv32 --build-only` was built at base and at head into the same path, and every output was hashed. dev-soft-core: 149 RV32 ELFs, 1,489 host ELFs and 5,664 other files, identical. dev: 235, 939 and 3,236, identical. The generated-doc `--check` gates pass. Limit: no LiteX or bitstream build (NEEDS-MANAGER §6).
- **A868 rescan of the committed heads.** milan-fpga has 2 hits per tree, both the act-slot pool self-test pins (NEEDS-MANAGER §1). FPGA-gPTP has 0. Commit messages and branch names: 0. The PR bodies scan clean under both the rules and a broader pattern. The rules' own false positives (`pw1_w`, the IEEE clause numbers, `archlinux:latest`) remain, as intended.

## Things that went wrong

- **One rm ran before it was logged:** `rm -rf /tmp/a869-fw-build` at 15:17, on a path that did not exist, so nothing was removed. It is recorded in disk-cleanup.log as a breach, and every later rm was logged first.
- **The first baseline is not comparable:** no submodules and no pinned renderer, so 12 gates refused at setup. I reran the baseline (base2) under the head's conditions. The first baseline is kept, marked superseded.

## Decisions for the manager (details in NEEDS-MANAGER.md)

1. The act-slot Docker pool literal stays: production `act_ci.py:739` and two self-test pins. Accept it as a false positive, or make the pool configurable in a separate PR.
2. The switch's and the peer's clock identities (with the vendor OUI) in the #117 evidence page are outside A868's list and were not changed.
3. milan-fpga's `gptp-processor` pins still point at FPGA-gPTP commits that carry the serial. Removing it needs a pin bump, which runs the RTL gates.
4. The ci/image snapshots still hold the old digest of `check_baremetal_only.py`. 168 of 378 inventory inputs were already stale at the base, so I did not regenerate them.
5. The owner's "force push everything necessary" conflicts with this brief's no push. I followed the brief.
6. The PR bodies carry no tool footer (removed by the manager before publishing).

## To open the PRs (manager, after review)

From each worktree or clone: push the branch, then
`gh pr create --base <dev-soft-core|dev|main> --head <branch> --body-file PR-BODY-<x>.md`.

REVIEW READY milan-fpga:privfix-bench-names@0715cb206050c49a1745dd2d11e2fc0e1b74116b milan-fpga:privfix-bench-names-dev@e7974868ef362f521e59fb82446ff54a19886bfa FPGA-gPTP:privfix-bench-names@e3fde4489655b1f7771cdfdf114485d237a86b75
