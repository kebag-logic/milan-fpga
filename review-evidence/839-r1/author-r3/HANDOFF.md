# HANDOFF: issue #839, round 3 (docs only), author A731c

Status: REVIEW READY at `3c22947861e5c057a6195ad46e1a379d67592559`; every round-3 gate rc 0. Not pushed (the manager pushes).

- Base: dev `604899c08ff1cd1830e1dd08b733109ef852400c` (the merge base; `git merge-base HEAD origin/dev`)
- Round-2 head: `ba56827bbfe4acadb84ca220616a76ad74611e7d` (pushed, PR #841)
- Round-3 head: `3c22947861e5c057a6195ad46e1a379d67592559`, two commits on `ba56827b`, no rebase, no force. Not pushed.
- Origin: `https://github.com/kebag-logic/milan-fpga.git`. No submodule touched, no git command run inside a submodule.
- TAKEN: issue #839 issuecomment-6672403928 (text: `taken.md`).
- REVIEW READY: issue #839 issuecomment-6673486928 (text: `review-ready.md`). It points to "the lane's
  handoff" for the per-item table. That table is also in `PR-BODY.md`'s Round 3 section, so it becomes
  public with the body.
- PR body: `PR-BODY.md` is the live body of #841 (at `ba56827b`), with these changes: the first line is
  `[A731c]`, a Round 3 contents entry and section (one paragraph and the README-to-code table), the
  round-3 status, the round-3 executor, and the reviewer rounds R773-2 and R774-2. The manager applies it.
- Commits (one-line subjects, no body, no trailers):
  - `ba1da8b66c` Say in the bootsa README that grade()'s list covers the first boot and the early-enable list replaces it, in the leg's order, with CRF where the config declares the CRF Media Clock Output (#839)
  - `3c22947861` Name the bootsa destination and EtherType checks by what they compare, the controller's MAC for AECP, instead of untouched octets (#839)

## Assignment

The round 3 [A10] comment on #839 (2026-11-05T23:32:54Z), docs only:

1. R774-2 F1, option (a): `tb/verilator/milan_dp/README.md` states what the leg checks, with R774-2's
   exact replacement texts at `:1183`, `:1204` and `:1207-1210`; the lists match `sim_boot_sa.cpp:759-830`
   and `:549-618` line by line.
2. Suggestions taken as text or check-name only: R773-2 S1 / R774-2 S4 (rename the two check names that
   still say "octets 0 to 5 untouched" and "octets 12 and 13 untouched"); R773-2 S2 (CRF's condition, as 1).

No RTL, harness logic or receipt figure changes. Not taken (not in the assignment): R774-2 S1, S2, S3;
R773-2 S3, S4.

## Changes

| Commit | File:line | What | Authority |
|---|---|---|---|
| `ba1da8b6` | `tb/verilator/milan_dp/README.md:1183-1184` | "It grades every frame on valid/ready at `m_axis_mac_tx`:" becomes R774-2's exact text "It grades every frame of the first boot (through the controller's and the listener's exchanges) on valid/ready at `m_axis_mac_tx`:" (wrapped over two lines) | R774-2 F1 (a); R773-2 RES-1 |
| `ba1da8b6` | `README.md:1186-1198` | The list is put in `grade()`'s order: the "processor offered" item moves from seventh to first. No item's wording changes | [A10] item 1, "line by line" |
| `ba1da8b6` | `README.md:1205` | "In each early-enable boot it also grades:" becomes R774-2's exact "In each early-enable boot it grades instead:" | R774-2 F1 (a) |
| `ba1da8b6` | `README.md:1210`, `:1213` | "(CRF where the config declares the CRF Media Clock Output)" added after the offered bullet and after the left-after bullet, the two that name CRF (R774-2's `:1207-1210`) | R774-2 F1 (a); R773-2 S2 |
| `3c229478` | `tb/verilator/milan_dp/sim_boot_sa.cpp:811-813` | The destination checks' names drop "(octets 0 to 5 untouched)". AECP's now reads "every AECP frame's destination address is the controller's MAC" (it is compared with `kControllerMac`, `:774`); the six others keep "every X frame's destination address is its protocol's" (compared with `protocol_da()`) | R773-2 S1 / R774-2 S4 |
| `3c229478` | `sim_boot_sa.cpp:816` | "every frame is a known protocol's (octets 12 and 13 untouched)" becomes "every frame's EtherType (and, for AVTP, subtype) is a graded protocol's", which is what `classify()` reads (`:151-169`: EtherType at 12-13, or 16-17 behind a C-TAG; AVTP subtype) | R773-2 S1 / R774-2 S4 |

What a check computes, its count and its verdict are unchanged: 67 checks at both heads.
`bootsa_mutants.py` matches a check by substring. Its `MSRP_DA` and `ADP_DA` names
(`bootsa_mutants.py:65-66`) are prefixes of the renamed names, so the campaign needs no change. It
still catches both controls that name them (the bootsa-mutants receipt). No other file quotes either
old name: a tree grep for "octets 0 to 5 untouched" and "octets 12 and 13 untouched" at the head is
empty.

### The README lists against the code, line by line (at `3c229478`)

First-boot list, `grade()` (`sim_boot_sa.cpp:759-831`, run once at `:862`, after `probe_tx()` and before the four later boots):

| README | Code |
|---|---|
| `:1186-1187` processor offered before the station MAC | `:796-797` `pp_offered_early_` |
| `:1188` no all-zero source | `:798` |
| `:1189` no CSR-addressed frame before both halves | `:799-800` (`before_mac`, gPTP excluded, `:773`) |
| `:1190` each protocol's source is the station MAC | `:801-807` |
| `:1191-1192` destination for MSRP, MVRP, gPTP, ADP, ACMP, MAAP; controller's MAC for AECP | `:808-815` (`:774-775`) |
| `:1193-1195` EtherType (12-13, or 16-17 behind a C-TAG) and AVTP subtype | `:816-817` (`classify()`, `:151-169`) |
| `:1196-1197` required kinds; CRF where declared | `:818-827` (`kCrfOutputDeclared`, `:820`) |
| `:1198` `A_TXARB_DIAG` | `:828-830` |

Early-enable list, `early_enable()` (`sim_boot_sa.cpp:549-618`):

| README | Code |
|---|---|
| `:1207-1210` each required source offered while unwritten: MAAP and CRF (MAAP on), AAF and CRF (MAAP off), CRF where declared | `:600` (MAAP, under `if (maap)`), `:604` (AAF, `else`), `:609` (CRF, under `if (kCrfOutputDeclared)`, `:608`) |
| `:1211` no frame of that source left before the pair | `:601`, `:605`, `:610` |
| `:1212-1213` MAAP, AAF and CRF frames after it (AAF and CRF with MAAP off), CRF where declared | `:602` (MAAP on), `:607` (both boots), `:611` (CRF, `:608`) |
| `:1214-1215` no CSR-addressed early frame, no all-zero, every frame the station MAC, `A_TXARB_DIAG` | `:613`, `:614`, `:615`, `:616-617` |

## New checks and planted mutants

None this round. No check is added or removed, and the twelve controls are unchanged. The renamed
names fail where they did. "the stamp lands on the destination, octets 0 to 5" fails "[BOOTSA] every
MSRP frame's destination address is its protocol's", and "the stamp's beat position survives a frame's
last beat" fails "[BOOTSA] every ADP frame's destination address is its protocol's" (the
bootsa-mutants receipt).

## Gates

This round's gate set comes from the round 3 [A10] comment: the docs gates, `bootsa`, `bootsa-mutants`
and `git diff --check`. The full sweep was not run, as the assignment says. Everything ran at head
`3c22947861e5c057a6195ad46e1a379d67592559` on clean clones of the committed head: one `clone_at.sh`
clone for the lane gates, and one fresh clone per `docs.yml` job. Nothing was piped. Each gate has one
log and one rc, and each log's first line names the head. Receipts are under `receipts/gates/`.

| Gate | Command (as run) | rc | What the log shows | Receipt |
|---|---|---:|---|---|
| The leg | `make -C tb/verilator/milan_dp bootsa` | 0 | `== bootsa: checks: 67   failures: 0 ==`, `RESULT: PASS`. The renamed checks: `[ ok ] [BOOTSA] every AECP frame's destination address is the controller's MAC got=0 exp=0`, `[ ok ] [BOOTSA] every frame's EtherType (and, for AVTP, subtype) is a graded protocol's got=0 exp=0`. The figures match round 2's: 868 first-boot frames; early-enable "847 frames after the pair" (MAAP on) and "3 frames after the pair" (MAAP off), each with "0 frames left" | `gates/lane/bootsa.log`, `.rc` |
| The leg's planted controls | `make -C tb/verilator/milan_dp bootsa-mutants` | 0 | `13 checks: 13 PASS, 0 FAIL`: the clean leg passes, and all twelve controls are caught by every check they name, the two destination controls by the renamed names | `gates/lane/bootsa_mutants.log`, `.rc` |
| Every `run:` step of `docs.yml` | `run_docs_yml.py <head> <job> <root>` for each of its nine jobs, then `verify_docs_yml.py` (`tools/docs_jobs.sh`) | verify 0 | `64 steps ran, 31 not run with a reason, 0 bad`; all nine jobs `failed 0`. Every clone is clean after its job, and `docs-check-no-git` removes its own `.git` by design. The 31 not run are hosted-only steps (records, uploads, cancels, apt and sudo installs), each with its reason in `tools/not_run.json`. The builder legs read `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`, as in round 2 | `gates/docsyml/docs-yml-table.md`, `verify.rc`, per-step logs |
| `scripts/docs_inventory.py --check` | NOT RUN: `git ls-tree` finds it neither at the head nor at the base | n/a | `scripts/docs_inventory.py is in neither tree: NOT RUN` | `gates/lane/docs_inventory_absent.*` |
| `git diff --check` against the merge base | `git diff --check 604899c08ff1cd1830e1dd08b733109ef852400c HEAD` | 0 | no output | `gates/lane/diffcheck.*` |

The lane clone was clean after its gates (`gates/lane/tree-after.txt` is empty).

Diagnostic, not a gate (before the commit, in the lane worktree): `check_doc_style.py` `documentation
style: OK`, `check_cpp_idiom.py` all ratchets at 0, `measure_test_evidence.py --check`
`TEST-EVIDENCE RATCHET: PASS`. The same three ran again as `docs.yml` steps at the head, above.

Tools: `receipts/gates/tools/` holds round 2's runner, verifier, `clone_at.sh`, `collect.py`,
`make_index.py` and `gate_table.py`, copied unchanged except for this round's scratch root and home.
`lane_gates.sh` is this round's gate list. The runner uses round 2's docs venv (pyyaml, the pinned
Markdown renderer, `wavedrom==2.0.3.post3`), read-only.

Redaction: `collect.py` replaces the host path prefixes with `<home>`, `<management>`, `<lanes>`,
`<scratch>`, `<data>` and `<slots>`. Afterwards the SDK and LiteX install prefixes in the copied logs
became `<sdk>` and `<litex>`. One log is over 200 KB: `docs-gates-2__gate_41.log`, 353,498 bytes, sha256
`9516367623c8fa384b39fcda18009fb4af7f4590ed4d23decb62714bffa57292`. It is listed in
`gates/docsyml/LARGE-LOGS.txt`, with its last 120 lines kept beside it.

## Not changed, and why

- `hdl/`, `syn/`, `sw/`, `configs/`, submodules: untouched (`git diff --stat ba56827bbfe4 HEAD` touches only
  `tb/verilator/milan_dp/README.md` and `sim_boot_sa.cpp`). The area figure stands, as in round 2.
- `CHANGELOG.md`'s "It grades every frame's source past ENTITY_AVAILABLE." is about the first boot, so it
  is already accurate. The assignment names only the README.
- R774-2 S1 (name every check a control is known to fail), S2 (exported offsets) and S3 (spacing), and
  R773-2 S3 and S4: not in the round 3 assignment.

## Acceptance

Unchanged from round 2. Acceptance 1 and 2 are met with simulated evidence. Acceptance 3 and 4 are read
as the maintainer accepted on 2026-11-05 (issuecomment-6655611611). No hardware capture exists yet, so the
PR relates to #839 and does not close it.
