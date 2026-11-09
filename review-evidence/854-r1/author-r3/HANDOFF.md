# 854-a756c HANDOFF (round 3, text only)

**Status: REVIEW READY. Every round 3 gate is rc 0 on a clean clone of the head.** Lane `854-shadow-drop-count`, base `dev`
`ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36` (the live `dev` tip, so the head is its own merge result). Round 2 head
`de71984e4fc1b568065dffec483ea3ff51518604`; round 3 head **`a853461dd57f8e493ca079e0faa1f07229c3cb16`** (two commits
on `de71984e`, no rebase or amend). Nothing pushed. TAKEN posted on #854 (issuecomment-6744251794; text
`TAKEN-COMMENT.md`). REVIEW READY posted (issuecomment-6745967653). `PR-BODY.md` is ready for the manager, with `Closes #854`.

## 1. Authority

The round 3 ruling on #854 (issuecomment-6743871886), on R803-2 (PR #862 issuecomment-6743685710) and R804-2
(issuecomment-6743864788). It replaces every earlier assignment item and GATES paragraph.

| Ruling item | Met by |
|---|---|
| 1. FF attribution (R803-2-F1 = R804-2-F1): the change carries +10 FF (count, `last_kept_r`, the FIFO's overflow register), the other +3 at ExtraPostPlacementOpt is SoC placement replication (AltSpreadLogic_high +10); everywhere the claim appears, PR body included | `8d6b623b`: `234_PP_SHADOW_AREA_BASELINE.md:110-113`, `AREA_BUDGET.md:256-257` and `:697-698`; `PR-BODY.md` "The change at one directive" |
| 2. LUT share (R804-2-S1): the change in the wrapper's remainder, because the hierarchy's LUT totals are not additive there; the FF share stays exact | `8d6b623b`: `234_...:116`, `:124`, `:126-128`; `AREA_BUDGET.md:259-261`; `PR-BODY.md` "The tap's own share" |
| 3. Docstrings (R804-2-R1), the exact fix | `a853461d`: `drops_mutant.py:25-26`, `:111` |
| 4. Residue to #495: a hosted `RXFILT=0 --drops-only` run | not lane work; named in `PR-BODY.md` limitations |
| Nothing else: no route, record, JSON or RTL change | `git diff --name-only de71984e a853461d`: the two pages and `drops_mutant.py` only |

Where the claim does **not** recur, checked: `CHANGELOG.md:78` ("Against #851's route it grows 106 LUTs and 13 FFs":
the image's figure against the record, no attribution); `syn/ooc/pp_resource_baseline.json`'s `measured` note ("this
route at ExtraPostPlacementOpt moved by ... +13 FF": the route's figure; the ruling forbids a JSON change anyway);
`234_...:92` and `:105` and `AREA_BUDGET.md:246` (tables and gate figures, not attributions). The round 2 REVIEW
READY comment on #854 also states the +13; existing comments are not edited.

## 2. Changes (round 3)

| File:line | Change | Evidence |
|---|---|---|
| `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:110-113` | "the flip-flop figure, +13 at both, is the change's" becomes: both figures move with placement; the change carries +10 FF (8-bit count, `last_kept_r`, the FIFO's overflow register), as measured out of context and at the wrapper (20,038 FF at all three directives); the other +3 at ExtraPostPlacementOpt is placement replication in the SoC, in the DMA write bridge's `aligner` (146 against 143), outside `milan_datapath` (43,435 at all three); at AltSpreadLogic_high the route moved +10 (54,837 to 54,847) | `receipts/area/hier-attribution.txt` |
| `234_...:116`, `:124`, `:126-128` | the tap's share is the change in the wrapper's remainder; the FF share is exact (remainder = own-cell row: 332 / 340 / 341); the LUT share is the change in a remainder that is not a cell count (own-cell row 18, 17 at 8x8; total less children +1, 0, 0, -5, -6) | the same receipt |
| `docs/design/AREA_BUDGET.md:256-257` | "the change moved by +151 LUTs, +13 FFs" becomes "the route moved by"; a sentence: the change carries +10 FF, the other +3 is SoC placement replication, as the AltSpreadLogic_high +10 shows | the same receipt |
| `AREA_BUDGET.md:259-261` | the remainder wording; FF share exact, LUT share not a cell count | the same receipt |
| `AREA_BUDGET.md:697-698` (the sixteenth ledger entry) | "the change moved" becomes "the route moved"; the +10 / +3 split | the same receipt |
| `tb/verilator/pp_shadow/drops_mutant.py:25-26` | "Exit 0 = both clean controls passed and every arm was caught by its named check; 1 = otherwise." | R804-2-R1's exact text |
| `drops_mutant.py:111` | "The two clean controls, then every arm; 0 when each arm was caught." | R804-2-R1's exact text |

No standard clause is affected: the counter is a project diagnostic (the counted set is IEEE 1722-2016 EtherType
0x22F0 carrying IEEE 1722.1-2021 clauses 6, 8 and 9, and IEEE 802.1Q-2022 35.2 MSRP and 11.2 MVRP), and round 3
changes no behaviour.

**Attribution receipt** (`receipts/area/hier-attribution.txt`, from `receipts/scripts/hier_check.py` over record 16's
published hierarchy reports, sha256 in the receipt, and the baseline JSON at `ac0a01e3` and at `de71984e`):

- route FF: EPPO 54,850, ASLH 54,847, ETO 54,847; `milan_datapath` 43,435 and the wrapper 20,038 in all three;
- EPPO minus ASLH, FF: only `VexiiRiscvLitex_*` / `dma_bridge_write_bridge` / `aligner`, +3 (146 against 143);
- wrapper total less children: LUT +1 / 0 / 0 (routes), -5 / -6 (standalone), own-cell row 18 / 18 / 18 / 18 / 17;
  FF equal to the own-cell row (332, 332, 332, 340, 341);
- gate scopes, record 16 minus record 15: wrapper +35 / +10 (route), +10 / +10 (both standalone); the remainder
  +8 / +9, +7 / +9, +6 / +9.
- Record 15's directives (`234_...` fifteenth section): ASLH 54,837, EPPO 54,837, ETO 54,838 FF.

## 3. New checks

None: round 3 adds or changes no check. The existing `[DR]` checks and the eight `drops-mutant` arms are unchanged and
re-run at the head (section 4): both clean controls pass; count-removed 7 failing checks, count-from-tready 7,
counts-refused 3, misses-second-beat 3, wraps 2, diag-tied-off 7, misses-oversize 1, counts-runts 2, each KILLED by
its named check (the same counts as round 2).

## 4. Gates (clean clone `fclone` of `a853461d`, units `milan-854-a756c-gates` and `milan-854-a756c-docs`, CPUs 8-15, this session's own booked range; the host had no other free range)

| Gate | Command | rc | Log shows |
|---|---|---:|---|
| diff check | `git diff --check ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36 HEAD` | 0 | no output |
| docs inventory | `python3 scripts/docs_inventory.py --check` | 0 | `documentation inventory: OK (547 lines, docs/DOCUMENTATION_AUDIT.md is fresh)` |
| drops-mutant | `make -C tb/verilator/pp_shadow drops-mutant` | 0 | `PASS: [DR] catches every arm (8 of 8); both clean controls pass` |
| check-baseline (extra: `pp_resource_gate.py` reads `AREA_BUDGET.md`'s policy table, which round 3 does not change) | `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | `baseline PASS: 3 endpoints` |
| resource gate self-test (extra) | `python3 syn/ooc/pp_resource_gate.py --selftest` | 0 | `resource gate selftest: 312 arms and 500 generated cases PASS` |
| resource gate mutants (extra) | `python3 -X cpu_count=4 syn/ooc/pp_resource_gate_mutants.py` | 0 | `resource gate mutants: control passes, all 236 mutants fail` |
| docs.yml | every `run:` step, each job on its own fresh clone (`receipts/scripts/docsyml_all.sh`, `run_docs_yml.py`, `verify_docs_yml.py`, `not_run.json`, round 2's runner and verifier with this lane's paths) | 0 | `65 steps ran, 31 not run with a reason, 0 bad`; `verify.rc` 0; every job runner rc 0; every job's tree clean after it (`docs-check-no-git` removes `.git` by design) |

Receipts: `receipts/gates/final/` (the four ruling gates and the resource gate, one log and rc each;
`tree-after.txt` and `tree-after-b.txt`: only ignored build products, the two generated ROM images and `syn/ooc/__pycache__`, nothing tracked changed; `fclone.txt`: the clone's head and submodules) and
`receipts/gates/docsyml-a853461d/` (`progress.txt`, `verify.txt`, `verify.rc`, every runner log and step log; one
log over 200 KB by sha256 and size in `logs/LARGE-FILES.sha256`). `receipts/area/hier-attribution.txt` with its
script `receipts/scripts/hier_check.py`; its JSON inputs were `git show ac0a01e3:syn/ooc/pp_resource_baseline.json`
and `git show de71984e:...` (unchanged at `a853461d`), sha256 in the receipt. `receipts/INDEX.md` is generated from
the files present by `receipts/scripts/collect_receipts.py`.

Not re-run in round 3, per the ruling: the `pp_shadow` suite in every leg (round 2 at `de71984e`: base 738, vid73
738, crf 778, pending 317, 0 failures), the gate's `check` on the measured endpoints, the full sweep and the firmware
gates. No input of theirs moved: `git diff --name-only de71984e a853461d` is the two pages and `drops_mutant.py`; the
suite reads no documentation page and runs `drops_mutant.py` only under `drops-mutant`.

## 5. Timeline (CET, 2026-11-09)

- 16:38: round 3 started; read both reports and the ruling.
- 16:4x: TAKEN posted; attribution figures re-derived from the published reports; commits `8d6b623b`, `a853461d`.
- 16:48: gates launched on `fclone`; 16:52 diff check, inventory and drops-mutant rc 0.
- 16:53: resource gate and docs.yml launched; resource gate rc 0 by 16:53.
- 17:52: docs.yml done, 65 ran, 0 bad; receipts collected; REVIEW READY posted on #854 (issuecomment-6745967653; text `REVIEW-READY.md`). Round complete; nothing pushed.
