# HANDOFF r5: [A814] PR #966 / #884 documentation corrections

Local commit: `165476c755e4728a044c12ea6bc33ce0a0a9d28f` on `opt-gptp-sw-1`.
Parent: `8267b8951616cfd570baf690835d4b0d38f14596`. Working tree clean.
Scope: R883-3-F1/F2 and R884-3-F1, as assigned for round 5. PR target remains
`dev-soft-core-optimisation`. The manager publishes the local commit and requests re-review.

## Changed lines and reasons

| File:line | Change | Reason |
|---|---|---|
| `docs/design/SPLIT_CONTROL_MEMORY.md:141` | `image_gptp` 1,096 -> 1,104 B; 59.0 RAMB36 retained | R883-3-F1 / R884-3-F1: the current fixture identity includes the 8 B `local_off` field for its one port |
| `docs/design/SPLIT_CONTROL_MEMORY.md:142` | `image_gptp` 2,136 -> 2,152 B; 64.0 RAMB36 retained | Same findings: the two-port identity includes 8 B per port |
| `docs/design/GPTP_SOFTWARE.md:153` | Plain images exclude the firmware gPTP owner; byte-identity claim removed | R883-3-F2: the shared hot-list relearn changes both variants' layout |
| `docs/design/GPTP_SOFTWARE.md:154` | States the shared layout change | Distinguishes optional ownership from the shared linker ordering |
| `docs/design/GPTP_SOFTWARE.md:155` | Gives measured plain ROM before/after at `a6323318` / `631dc544`: 126,632 -> 126,640 B at 1x1/1if; 140,952 -> 140,960 B at 8x8/2if | The claim now names the measured revisions and artifacts; SRAM and allocated tiles are unchanged |

These are the only repository hunks. Other lanes may meet these documentation paragraphs;
there is no new source, interface, mailbox, RTL, hot-list or budget merge surface.
`receipts/documentation.diff` is the complete diff. `receipts/source-equivalence.txt`
proves it is byte-identical to the worktree diff tested before commit and that every
other tracked path equals the parent. No code or approved bounds changed.

## Evidence reconciliation

`receipts/evidence-reconciliation.md` records `ctrl_memory.LEDGERED`,
`ctrl_memory_ledger.IMG_GPTP_1/2`, the platform key 20,160 B, the unchanged 59/64/62
RAMB36 entries, and both plain-image measurements. The three original round-4 logs
are copied byte for byte into `receipts/prior-memory/`. Their revision labels remain
unchanged. The five original `631dc544` platform ELF artifacts were regraded; their
sizes and SHA-256 values are recorded rather than copying build artifacts into this packet.

## Gate results

The four requested documentation checks and focused ledger checks ran on the exact
contents subsequently committed as `165476c7`. The source-equivalence receipt binds
the pre-commit worktree to that commit. Commands run from the candidate checkout with
its LiteX Python environment, except the em-dash check uses an isolated pinned renderer.

| Command / scope | Result | Receipt |
|---|---|---|
| `python3 -B scripts/docs_check.py` | PASS, 0 findings; 23/23 scrub controls, 4/4 routing arms | `receipts/docs_check.log` |
| `python3 -B scripts/check_doc_style.py` | PASS, 25 current documents | `receipts/check_doc_style.log` |
| `python3 -B scripts/check_doc_paths.py` | PASS, 1,773 cited paths and 10 line anchors | `receipts/check_doc_paths.log` |
| `python3 -B scripts/docs_inventory.py --check` | PASS, inventory fresh | `receipts/docs_inventory.log` |
| `python3 -B <packet>/receipts/run_ledger_tests.py` | PASS, 150 assertions, 16/16 ledger plants and 3/3 mapper mutants caught | `receipts/ledger_tests.log` |
| `python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <prior-images> --regrade --self-test` | PASS, five points and 9/9 controls; original `631dc544` images | `receipts/plat_ledger_regrade.log` |
| `python3 -B scripts/check_em_dash.py --base 8267b8951616cfd570baf690835d4b0d38f14596` | PASS, 5 added lines; 339/339 controls | `receipts/check_em_dash.log` |
| `git diff --check 8267b8951616cfd570baf690835d4b0d38f14596 HEAD` | PASS | `receipts/source-equivalence.txt` |

The ledger runner calls the existing `test_ctrl_memory.check_arms`,
`ledger_plant_arms` and `ctrl_memory_ledger.mapper_arms`; it adds no test oracle or mutant.
It includes the ledger's good images, wrong identity, missing override, other-point and
half-tile-over refusals. Full memory simulation, firmware and synthesis banks were not
rerun for this prose-only change; no new image build is claimed.

Existing plants remain meaningful: removing `image_gptp` from either identity accepts
an image the override must refuse; raising its tiles changes the accepted tile tuple.
Those produce `PLANTED ledger ... is caught`, with `exit codes` or the measured tuple.
The three mapper plants (ignored override, override on every image, accepted stray tag)
produce `MUTANT ... is caught by the mapper's facts`, with wrong exit codes. The platform
controls produce `KEY`, `LINK`, `TILES` or `LEDGER` at the expected points. Full diagnostics
are in the two fresh ledger receipts. No new check needs a new planted defect this round.

The em-dash check first refused the incomplete shared renderer environment. The initial
refusal is retained as `receipts/check_em_dash-setup-refusal.log`; the locked packages
were installed under external scratch, recorded by `receipts/renderer-setup.log`.

## Review handoff

`REVIEW-READY.md` contains the one [comment posted on #884](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7092240935). `PR-BODY.md` is the updated
local description for the manager; the PR itself was not edited. Publication of the
comment succeeded and is recorded in `receipts/issue-comment.txt`.
Independent Docs re-review remains required; this author report supplies no review verdict.
The source-comment residue R883-3-R1 / R884-3-R1 stays on the manager's checklist,
outside the explicit two-statement scope. No push, merge, rebase, bench access or
sub-agent work was performed.

REVIEW READY 165476c755e4728a044c12ea6bc33ce0a0a9d28f
