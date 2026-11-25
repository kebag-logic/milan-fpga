[A834] REVIEW READY
Commit: 67838b379f9e9ecb6cf6fbd0f162a5bb852ca570 (one commit on 507bce7f; local, not pushed)
Changed: the held-egress ledger at 8x8/1if is restated as the ruling on this PR decides
(https://github.com/kebag-logic/milan-fpga/pull/992#issuecomment-7146658362, item 1). Three paths changed, no firmware,
RTL, configuration or test input:
- `tb/verilator/ctrl_service_budget/egress_ledger.py`: two named measurements of `backlog-owed`'s seven rows at
  8x8/1if, arm A, to 10 ns: `TRAIN` (the flip train's image at `2509db68`, `74f8d3c7…`) and `PINNED` (this PR's
  merge image at `507bce7f`, `eed56acc…`). `MEASURED` is the largest of the five per row, and the figures follow the
  unchanged rule (`figure`): hold + largest + 5 %, rounded up to 0.01 ms. The section 13 parser reads the two new
  columns (`DOC_HEAD`, `DOC_ROW`), and the control "section 13's five measurements are the five images'" replaces the
  three-image control. Three new mutants: a figure at the first three images' measurements, a figure at the train's
  where the pin merge's is larger, and `service.aecp.last` at the pin merge's where the train's is larger.
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 13: a bullet that restates the ledger by the ruling, with each
  head's share stated separately (the train's per #1005, this PR's +0.086..0.094 / -0.223 ms), and the table's two
  new columns and new figures.
- `tb/verilator/ctrl_service_budget/README.md`: the `MEASURED` sentence names the five measurements and their
  rulings, and the mutant count is eighteen. It said fourteen and two measurements, which was already stale at
  `507bce7f`, where there were 15 mutants and three measurements.

## Validation (receipts/INDEX.md)

| Check | Command | Result |
|---|---|---|
| Figures | `egress_ledger.py`'s `LEDGER`, against the rule computed separately in `Decimal` and the ruling's expected figures (`tools/derive.py`) | all 7 equal: 64.31, 64.51, 64.71, 64.91, 65.11, 63.29 (set by `507bce7f`), 63.23 (set by `2509db68`). No rounding step differs from the ruling |
| Measurements | `TRAIN` and `PINNED` against round 4's `results/backlog-owed.json` (sha256 `260f3c64…`, `0d0b3ff3…`) | both EQUAL, to 10 ns |
| Self-test | `python3 -I egress_ledger.py --selftest` | rc 0. 72 of 72 controls PASS (36 in its own process, 36 as a separate process), 18 of 18 mutants caught |
| The leg, merge head | `egress_ledger.py --point 8x8-1if <r4>/b-8x8-1if/results` | rc 0, PASS. 974 instances, all measured; every row is under its figure by 0.16008 to 0.38237 ms |
| The leg, from the log | `egress_ledger.py --point 8x8-1if <r4>/run-8x8-1if.log` | rc 0, PASS (held at the log's microsecond plus half) |
| The leg, train image | `egress_ledger.py --point 8x8-1if <r4>/b-base-8x8-1if/results` | rc 0, PASS, under by 0.15947 to 0.33171 ms |
| Image identity | `plat_ledger.py --build-dir` at `67838b37` (porcelain 0 before and after), sha256 of every ELF, bin and hex, against round 3's same build at `507bce7f` | rc 0, PASS at every point. 28 of 28 files are byte-identical, `eed56acc…` (8x8/1if) and `79c5326c…` (1x1/1if) among them, which are round 4's harness images. `git diff --name-only 507bce7f 67838b37` lists the three paths above, and no harness `build.json` names any of them |
| Docs gates | `docs.yml` steps as in round 3/4 (`tools/docs5.sh`), the em-dash gate as a push from `507bce7f` | 46 of 46 rc 0, both end-station builder legs included, porcelain 0 before and after. The em-dash gate, run as a push from `507bce7f`: 0 findings over 15 added lines in 2 Markdown pages. The contents gate, the no-git docs gate and the Python idiom gate (54 of 54 checks) pass. The steps that need a hosted runner's event were not run (`receipts/docs/run.log`) |
| Base move | `git merge-tree --write-tree 67838b37 origin/dev-soft-core` (`2f2a8152`) | rc 0, no conflict. Not merged here, as the brief instructs |

Acceptance criteria (issue #991 AC2, the harness part): the egress ledger leg at 8x8/1if is now met under the
ruling. Everything else is as round 4 reported. The six harness runs and the self-test are rc 0 on images that are
byte-identical to this head's, and `kept_grade` PASS. The single pass over THE SHARE is `srp-bound`'s, owed to #977
by #969's amended ruling (https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7116192252, item 2).
That ruling grades it OWED, not raised, so "0 passes over THE SHARE" holds everywhere except that one owed pass. The
PR body names it.

The ruling's conditions: section 13's columns and shares (done), the self-test and the leg pass (done), the images
stay byte-identical to `507bce7f`'s (done, proven by rebuild), and one delta reviewer covers the change (open: it
needs a reviewer).

Open risks/questions:
- #1005 criterion 3 says that "from now on" restating these rows needs a per-PR cost or phase attribution. This
  restatement is the one that ruling decides inside #992, and the attribution of the train's share stays with #1005.
  A reviewer may want that ordering confirmed.
- The head is not pushed. The hosted gates and the local CI replica have not run at `67838b37`, and they start once
  it is pushed.
- The R1 residue (the docstring's "sent as Lv") is unchanged and out of this round's scope.
