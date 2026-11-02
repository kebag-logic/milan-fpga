[R754] NEGATIVE - exact head ef7dc9850827e0eadae5ae098d5db3dc91d29b3d

Round R754-5, external independent review of kebag-logic/milan-fpga PR #825 (issue #797). Head `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d`, tree `b0ae22190efb307eb997f3f8ff896c2657a88747`. Delta reviewed: `79fdea05..ef7dc985` (`f24695e4`, `ef7dc985`): `docs/reference/REGISTER_MAP.md` +4/-4, `scripts/register_descriptions.json` +2/-2, `scripts/register_read_sweep.py` +82/-21. No RTL change.

**Why NEGATIVE:** one MINOR is open, F1 (Tests). R753-4 F1 is resolved. The page, the descriptions and the RTL agree in every state I drove, including one the sweep does not drive. But one of the four clears the new clause names, the clear on a provisioning `STRMW_CTRL` write (`milan_csr.sv:3128`), is never separated by a swept state. An RTL mutant that deletes it passes the sweep with 0 disagreements. Adding one state kills that mutant, and the head still passes with the state added.

## Findings

### F1 - MINOR - Tests - `scripts/register_read_sweep.py:345-362`, `:17-20` - no swept state separates the `STRMW_CTRL`-write clear the clause now names

- **Authority:**
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect."
  - The sweep's own contract (`register_read_sweep.py:7-10`, `:23-27`) is to read each clause as the page prints it.
  - `f24695e4` names four clears of the SRP-served word: a later write answer, a selection write, a `STRMW_CTRL` write, and another master's beat. This round's focus (1) is "every case that clears the word per `milan_csr.sv:3108-3133`".
- **RTL:** `srp_fresh_r` has five clears: reset (`:3109`), a write answer (`:3113-3115`), `sel_wr_w` (`:3119`), `srp_prov_w` (`:3128`) and `i_srp_ctx_stolen` (`:3132`).
- **Evidence:** I deleted each clear in turn in a disposable copy and swept it against the head page (`receipts/patches/m*.rtl.diff`):

  | Mutant | Clear removed | Sweep rc | Disagreements | Receipt |
  |---|---|---:|---:|---|
  | m1 | stolen beat, `:3132` | 1 | 144 | `receipts/sweep_m1.log` |
  | m2 | write answer, `:3115` (set instead of clear) | 1 | 288 | `receipts/sweep_m2.log` |
  | m5 | `STRM_SEL` write, `:3119` | 1 | 96 | `receipts/sweep_m5.log` |
  | **m4** | **provisioning `STRMW_CTRL` write, `:3128`** | **0** | **0** | `receipts/sweep_m4.log` |

- **Cause:** no swept state reads the word while a poll answer comes before a `STRMW_CTRL` write and the write is still unanswered.
  - Mode 2/3 always answers the write it posts (`:355-358`).
  - Mode 4/5 answers the poll only after the write fires (`wr_ctrl_answered`, `:282-297`).
  - So the write-answer clear always hides whether the `STRMW_CTRL` clear exists.
  - In the missing state, the page's clause ("latest answer ... was a poll, after the last `STRM_SEL`/`STRMW_CTRL` write") predicts 0, and the m4 RTL returns `{16'd0, i_srp_ctx_rd_stat}`.
- **Docstring:** the docstring says the answers are driven "in either order around the write" (`:17-18`). The modes cover a poll after the write fires, both before and after its answer. They never cover a poll before the write.
- **The page is right:** I added a mode 8 to a disposable copy of the sweep (`receipts/patches/sweep_mode8.diff`, 3 lines): a poll answered, then a `STRMW_CTRL` write left unanswered. Results:
  - Head RTL: rc 0, 0 disagreements (`receipts/sweep_mode8_m6.log`).
  - m4 RTL: rc 1, 144 disagreements (`receipts/sweep_mode8_m7.log`). Example: `STRMW_SRP 0x85C ... srpw=1 srppoll=0 ... read 0x00004444: row 'any other case' says 0x00000000`.
- **Why not RESIDUE:** this is a test that cannot fail for the defect in one clause it claims to read. It is not wording.
- **Why not Conformance, RTL or Docs:** the RTL matches its comments. The printed rows and `register_descriptions.json:4086-4087` hold in the missing state (mode 8 at head is 0).
- **Why now:** the gap predates the delta, because the old clause also named `STRMW_CTRL`. The delta rewrites the clause as an explicit list of clears, and rewrites the harness to read it "as the page words it" from a record of `STRM_SEL`/`STRMW_CTRL` writes (`:238-253`, `:363-368`). The sweep is the evidence that the list is true, so each named clear needs a state that can expose it.
- **Impact:** a regression that drops the provisioning clear passes the instrument whose job is to prove the page's words. Software reading `STRMW_SID_LO`/`_HI`/`STRMW_SRP` between a provisioning write and its answer would then get the pre-write snapshot as a fresh answer, while the page says 0.
- **Required outcome:** the sweep drives a state where a poll is answered, then a provisioning `STRMW_CTRL` write is posted and left unanswered, then the words are read. The docstring describes the orders the modes actually drive.
- **Verification:**
  - The sweep exits 0 on both builds at the fixed head.
  - The m4 mutant (`receipts/patches/m4.rtl.diff`) makes it exit 1.
  - m1, m2 and m5 still exit 1.
  - Putting back the round-4 wording still exits 1.

### Suggestions (optional, no effect on coverage)

- **S1 - Tests - `scripts/register_read_sweep.py:349-350`, `:361`:** the comment defines `srp` as "the table answered since the selection". Modes 4 and 5 compute it as `at_ans > at_selwr`, and `at_selwr` also moves on a `STRMW_CTRL` write. The column is only logged, no clause reads it, and no answer falls between the selection and the write in those modes, so nothing differs today. "since the last `STRM_SEL`/`STRMW_CTRL` write" would match the code.
- **S2 - Robustness, Tests:** coverage of one case. A grant and a steal on the same edge read 0 in the RTL, because the steal clear comes last (`:3130-3132`). The harness's `at_steal > at_ans` would record that as no steal. Today this cannot happen: `CSR_REGISTER_NOTES.md:958` says the steal marks a yielded poll beat, so the window is not granted on that beat. A port-contract sentence saying the two never coincide would close it.
- Prior suggestions not taken stay optional: R754-4 S1 and S2, R753-4 S1-S4.

### Residue

None new.
- The delta's added source comments carry only `#797`. They have no bench lane labels, lane names, review rounds, reviewer IDs or comment IDs: a grep of the added lines `79fdea05..HEAD` finds none.
- Both commits are one line with no trailers.
- `git diff --check 79fdea05 HEAD` is clean.

## Focus results

| Item | Result | Evidence |
|---|---|---|
| (1) The `srp_fresh_r` pair states every clear, with its negation, generator-fresh | **Met.** All four rows and the JSON pair carry the same words. The positive form maps exactly onto `:3108-3133`. A poll grant sets the word. A later write answer clears it ("latest answer was a poll"). A selection write or a provisioning `STRMW_CTRL` write clears it ("after the last ... write", including the same edge, since those clears follow the grant in the block). A steal clears it ("no other master ... since"). Reset leaves the word 0 and the selection at PARK, where every row is "any other case". A `STRMW_CTRL` write that does not provision cannot follow a fresh poll at the same selection, so the broader wording is harmless (as R753-4 said). The negation is the exact logical complement. | `REGISTER_MAP.md:3462,3483,3639,3640`; `register_descriptions.json:4086-4087`; `receipts/gen_check.log` "fresh (203 registers, 34 modules, 240 files)" rc 0; `receipts/gen_selftest.log` 61/61 rc 0 |
| (2) The sweep drives a poll then a write answer, and a steal after a poll answer, and the harness comment states the page's words | **Met.** Modes 4 and 6, plus 5 and 7 as controls. The comments at `:345-350` and `:363-368` state the page's clause. One named clear is still unseparated: F1. | `register_read_sweep.py:238-253,282-297,345-368`; `receipts/sweep_head.log` rc 0, 48,007 reads per build, 0 disagreements on ship and 2x2 |
| (3) The old wording planted back makes the extended sweep exit 1 | **Met.** The page at `79fdea05` gives rc 1 with 288 disagreements (48 ship, 240 2x2). 144 are `srpw=1 srppoll=0 srpsince=1` (poll then write answer) and 144 are `srppoll=1 srpsteal=1` (poll then steal). The old JSON pair planted in a copy makes `--check` exit 1 (STALE). | `receipts/sweep_oldpage.log`, `receipts/gen_check_oldjson.log`; this matches the author's `plants/` receipts to the count |
| (4) The reviewer's probe states agree with the new rows | **Met.** 25 states, 0 disagreeing, rc 0. The four marked states (A len2/off1, len3/off0, len3/off1, and B) read 0 with `new_clause=0`. The probe's `new_clause` comes from the head harness's own record, so it is not independent of the sweep. My mutants m1/m2 and the mode-8 run carry the independent check. | author `receipts/probe/probe_marked_states.log` (hash-verified) |
| (5) Nothing else on the page changed | **Met.** `git diff 79fdea05..HEAD -- docs` changes exactly the four rows. The JSON changes exactly the two pair strings. `--check` is fresh. | `receipts/clone_integrity.txt` (diff stat) |

## Prior findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R753-4 F1 (SRP-served clause omits the write-answer-after-poll and stolen-beat clears) | **Resolved.** The required wording (with "with" for ", and", which keeps a read-table cell one conjunction) and all four verification items are met. | Focus (1)-(4) |
| R753-3 RES2 (`REGISTER_MAP.md:4503`) | Retained, RESIDUE | Line unchanged at head |
| R753-3 RES3 (`CSR_REGISTER_NOTES.md:974`) | Retained, RESIDUE | `docs/design` unchanged in the delta |
| R754-3 R1 (`CSR_REGISTER_NOTES.md:78`) | Retained, RESIDUE | Unchanged |
| R754-4 S1, S2; R753-4 S1-S4 | Not taken, optional | PR body says suggestions are not taken |

## Lens results

```text
[R754] PASS Conformance - docs/reference/REGISTER_MAP.md:3462,3483,3639,3640; scripts/register_descriptions.json:4086-4087 against hdl/common/csr/milan_csr.sv:1109-1110,2528,2543-2576,2915,3086-3133 - every clear, its same-edge priority, reset and non-provisioning CTRL writes; head sweep 0/0 on both builds; mode-8 sweep at head 0
[R754] PASS RTL - hdl/common/csr/milan_csr.sv:3104-3134,624-631; hdl/milan/milan_datapath.sv:3010 - no RTL in the delta; mutants m1/m2/m5/m4 confirm each clear's observable role (receipts/sweep_m*.log); prior lens verdict holds
[R754] PASS Robustness - receipts/sweep_head.log, sweep_mode8_m6.log, author probe_marked_states.log - poll/write ordering both ways, write left unanswered, stolen beat before and after a poll, reset to PARK; same-edge grant+steal not reachable per CSR_REGISTER_NOTES.md:958 (S2)
[R754] UNCLEAN Tests - scripts/register_read_sweep.py:17-20,345-362 - F1: the provisioning-CTRL clear (milan_csr.sv:3128) survives the sweep (receipts/sweep_m4.log rc 0); other three clears killed; old-wording plant rc 1 (288)
[R754] PASS Docs - REGISTER_MAP.md delta (4 rows), register_descriptions.json delta (2 strings), gen --check fresh and --selftest 61/61, PR body Round 5 rows f24695e4/ef7dc985, author REVIEW READY - claims match the receipts; no new residue
```

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 4 page rows and the JSON pair against `milan_csr.sv:3086-3133` and the read mux `:2543-2576`; head and mode-8 sweeps | R754-5 | `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d` |
| RTL | CLEAN | `milan_csr.sv:3104-3134`, port comment `:624-631`, datapath tie-off `:3010`; 4 clear mutants | R754-5 | `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d` |
| Robustness | CLEAN | Ordering, unanswered-write, steal, reset and non-provisioning paths (sweep, mode 8, author probe) | R754-5 | `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d` |
| Tests | UNCLEAN (F1) | `register_read_sweep.py` delta; head sweep; old-page plant; mutants m1, m2, m4, m5; mode-8 variant | R754-5 | `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d` |
| Docs | CLEAN | Page and JSON delta, `--check`, `--selftest`, PR body, REVIEW READY, receipts index | R754-5 | `ef7dc9850827e0eadae5ae098d5db3dc91d29b3d` |

## Evidence verification

- **Published author receipts:** `review-evidence/797r1-r1` at `5f1367c330396e36efe019660c66550ee593df70`.
  - 167/167 `author-r5/` files match `MANIFEST.json` `published_sha256`. The manifest's sha256 is `534c52ca...65b0` (`receipts/evidence_manifest_check.txt`).
  - The evidence commit itself carries no signature, so integrity rests on the manifest hashes.
  - All 63 author gate and lane rc files read 0. The plants read rc 1 as claimed.
- **My own runs:** the pinned Verilator wrapper reports `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/verilator_version.txt`).
  - The generator needs `wavedrom==2.0.3.post3`. It is missing on the host, where the first `--check` refused (rc 2), so I installed it into a scratch-local venv. The recorded `gen_*` receipts are the venv runs.
  - The receipts agree with the author's to the count: 48,007 reads per build, 288 = 48 + 240.
- **Clone restored:** HEAD, write-tree and HEAD^{tree} all equal `b0ae2219...`. The index equals the HEAD tree in mode, blob and path (sha256 `6a6661cc...`). No untracked or ignored files remain: I removed the bytecode caches my runs created. The six gitlinks are unchanged (`receipts/clone_integrity.txt`).

## Real limits

- **Block level only:** the shipping datapath ties the SRP grant and `i_srp_ctx_stolen` to 0, so no shipping-SoC read differs in any of these states.
- A grant and a steal on the same edge are not driven (S2).
- Not run: Verilator suites, Yosys, behave suite, parent/PP/gPTP/builder banks, Vivado, hardware. Physical calibration was not run. Field skips are not hardware proof.
- No manager source bank exists at this head, and none is claimed or inferred. The source-head execution evidence is the author's published receipts, spot-checked and reproduced above.
- **Hosted checks:** at snapshot (`receipts/hosted_checks_snapshot.txt`), `docs-check-no-git` and `wire-accountability` had completed with success. The docs, elaborate and fail-fast jobs were in progress or queued. I did not wait on them.
- **Bases:** the lane's diff base given is `1e80128f`. The author's merge-base with `origin/dev` is `1f29f189`, a descendant of `1e80128f` and an ancestor of head. Live dev `503bc97c` is not merged.

## Pending manager duties

- Re-review the F1 fix at its new head. Rerun the m4 mutant and the old-wording plant against it.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts.
- Accept the hosted and act contexts at the exact head.
- Carry the residue checklist: R753-3 RES2 and RES3, R754-3 R1.

R754-5 FINISHED
