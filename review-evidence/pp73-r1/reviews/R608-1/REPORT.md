[R608] NEGATIVE - exact head 39cac060f6f3730cf8172adc6424c275cd268517

# R608-1 independent review: issue #73 / PR #174, one AECP command model

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #174 (`Closes #73`)
- Exact head 39cac060f6f3730cf8172adc6424c275cd268517, tree c132228346eddff8f248281d0c8d702e51ae18fd
- Source base main 2cbed0a987c1e68402658d69459ab7e5aa571adc (an ancestor of the head; 6 commits)
- Parent: kebag-logic/milan-fpga live dev ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5, `protocol-processor` gitlink 2ad2f845
- Role: internal independent reviewer, cleared context, own detached clone
- Verdict: **NEGATIVE**. 4 MINOR findings are open: F1 and F2 (Tests), F1 and F3 (Docs), F2 and F4 (Robustness). Conformance and RTL are clean. The PR's core claims reproduce: the ROMs and the elaborated engine are byte-identical, both ROM digests equal the parent ledger's rows for pin 2ad2f845, the gate runs in CI, and the planted drifts fail by name. What keeps the verdict NEGATIVE: the record of what is generated, gated and still hand-written (acceptance 4) overstates the gate's reach, and the by-name guarantee has a gap from the real input path. So `Closes #73` is not yet earned.

## 1. Reconstruction (order followed)

1. Governance. Neither AGENTS.md nor CONTRIBUTING.md exists in this repository. Read instead: `README.md` (build and check commands, consumption contract) and `docs/README.md` (single-source rules; `make check` is the CI docs-gates job; editing workflow).
2. Issue #73 body: acceptance 1-4. Owner comments: re-scope by the Mark II decisions (the single model generates the fabric ROMs and the firmware tables), and the lane comment's frozen scope and proof list. Neither the issue nor the PR had prior public review findings at this head, only the two review-start notices. Those were read after my own pass.
3. Authorities: REQ-VER-002 and GAP-11 (`docs/00_MILAN_COMPLIANCE_REVIEW.md:535`, column key :355), F06.14 and 06 §8 / §8.1, 09 §1 / §7 / §8.10. Consumers: `KL_aecp_engine.sv`, `KL_aecp_ucpu.sv`, `ucpu_pkg.sv`, `KL_aecp_notify.sv`, `KL_pp_scoreboard.sv`, `pp_pkg.sv`, `protocol_processor_top.sv`. IEEE 1722.1-2021 Table 7-141 and the AEM command and response field layouts were used for the size and status arithmetic.
4. `git diff 2cbed0a9..39cac060` in full: 8 files, +2041/-63, and no `.sv/.svh/.v/.hex/.mem/.tcl/.xdc` change. All 6 commits were reviewed.
5. Public evidence: kebag-logic/milan-fpga@140d1b7e `review-evidence/pp73-r1`. It holds `MANIFEST.json`, `author/HANDOFF.md` and `author/PR-BODY.md`, and the digests match the manifest (`receipts/evidence_fetch.txt`). It is a narrative record only: no raw logs are published. There was no manager evidence comment beyond the lane comment.

## 2. Findings

### F1 - MINOR - Tests, Docs - the engine's per-command decode and dispatch are held to no table, yet the record says the table drives them

- **Where:**
  - `hdl/aecp/KL_aecp_engine.sv:1366` (decode wire `sclks_w` on `OP_SET_CLOCK_SRC_C`) and `:3481` (dispatch arm `upc_r <= UPC_SCLKS_C`). Every served command has the same pattern.
  - `scripts/check_aecp_commands.py:506-596` (`check_engine`) and `:711` (DISPATCH comparison).
  - `hdl/aecp/ucode/gen_ucode.py:2438-2444` (DISPATCH).
  - Claims: `hdl/aecp/ucode/aecp_commands.json:7,11`; `docs/architecture/09_verification.md:465`, the §8.10 table (:470-484) and its held-to-no-table list (:492-499); `docs/architecture/06_aecp_engine.md:1205` and `:1423-1425`; `docs/00_MILAN_COMPLIANCE_REVIEW.md:535` (REQ-VER-002 Arch cell).
- **Evidence:** I planted two independent probes in head copies (`receipts/drift_probes/q1_*.txt`, `q2_*.txt`):
  - q1 redirects SET_CLOCK_SOURCE's success arm to `UPC_GCLKS_C`, a program that never reaches CHECK_LOCK. The command is lock-protected.
  - q2 keys SET_CLOCK_SOURCE's decode on `OP_GET_CLOCK_SRC_C`.

  Both pass the gate with rc 0: `aecp commands: 31 commands, 84 entries walked, F06.14 41 rows, OK`. `check_engine` checks only three things: that each table entry has a `UPC_<e>_C`, that every `UPC_*_C` is claimed by some command, body or shared entry, and the GET_DYNAMIC_INFO sub-decode. It does not check which program the engine actually selects for which opcode. `DISPATCH` is built from the table and changes no ROM word (the ROMs are byte-identical). Its comparison at `:711` is the table compared with itself through the generator. Its one effect is the "placed program" assertion.
- **What the docs claim:**
  - The table's `about` (:11) and 09 §8.10 (:465) say `entries` are "the µPC programs the engine dispatches the command to".
  - 06 §8 (:1205) and REQ-VER-002 say the µcode "takes ... its per-command dispatch map from the command table".
  - 06 (:1423-1425) says the decode stages' per-opcode content (hazard class, minimum length, response-size id, lock/GDI/notify flags) "already has one source: the command table". Yet 09 §8.10 itself lists the command-length floors as held to no table.
  - The held-to-no-table lists in 09 §8.10 and REQ-VER-002 omit the engine's per-command decode and dispatch arms, and REQ-VER-002 also omits the length floors.
  - 09 §8.10 lists the µprograms both as "hand-written µprograms, gated" (its table) and as "the µprograms themselves ... held to no table" (:492) without saying which properties are gated.
- **Impact:** Acceptance 4 ("record what is generated and what is still hand-written") is overstated. The gate's ROM-walk guarantees (exactly the lock-protected commands reach CHECK_LOCK; status set; sizes) hold for the programs the table names, not for the programs the engine dispatches. A rewired dispatch arm or decode passes `aecpcmd`. Only the dynamic suites can catch it.
- **Required outcome:** do one of the following.
  - (a) Extend `aecpcmd` to hold each served command's decode term (`txn_w.opcode == OP_X_C`, MVU sub-decode included) and its `upc_r` dispatch arms to the table's `entries`, with self-test plants for both.
  - (b) Correct the record in 09 §8.10, REQ-VER-002 Arch, 06 §8 (:1205 and :1423-1425) and the table's `about`. The engine's per-command decode and dispatch arms and the command-length floors are hand-written and held to no table. `entries` are the programs the table assigns, checked only to exist and be claimed. `DISPATCH` is a placed-program assertion, not a dispatch source. The PR body's "DISPATCH ... read when it generates the ROM" wording should follow.
- **Verification:** for (a), re-run probes q1 and q2: each must fail by name. For (b), the docs must state the above with `make check` green, and acceptance 4 must be re-read against it.

### F2 - MINOR - Tests, Robustness - the self-test plants generator-read table defects only in memory, so the gate's real path for them is untested and can be nameless

- **Where:** `scripts/check_aecp_commands.py:1351-1373`. `selftest` mutates `Inputs.table` after `load()` has already run the generator on the clean table. The two cases are "a message type that is neither AEM nor MVU" (`:1153-1155`) and "an entry the engine cannot dispatch to" (`:1053-1055`). On the generator side: `hdl/aecp/ucode/gen_ucode.py:141` (`next(...)` with no default) and `:2443` (`assert`).
- **Evidence:** I applied the self-test's own fixtures to the table file (`receipts/drift_probes/`):
  - p5e: GET_MILAN_INFO `message` set to `AAU`. Result: rc 2, `AECP COMMAND GATE: REFUSED - hdl/aecp/ucode/gen_ucode.py did not generate: StopIteration()`. This names neither the command nor the consumer. p5 (`AA`) and p5b (`--write`) give the same.
  - p8: the `SCFGRUN2` entry. Result: rc 2, a generator assertion, not the engine finding (rc 1) the self-test expects.
  - Meanwhile `--selftest` reports `89 planted defects, 89 caught by name`.
  - Control: p5c sets an AEM row's `message` to `AA` and gets the named schema finding with rc 1.
  - `receipts/selftest_coverage.txt` confirms that every finding site and all 16 refusal sites are hit by name in memory. The gap is only between the in-memory plant and the file path.
- **Claims:**
  - `check_aecp_commands.py:40`: "Every line of a failure names the command and the consumer that disagree".
  - 09 §7 row `aecpcmd` (:127): "Each disagreement names its command and consumer".
  - The PR body says the same.
- **Impact:** The gate fails closed (never a pass). But the "unrepresentable message type" refusal, a planted drift this round must see fail by name, is nameless end to end on the only MVU row. The self-test cannot detect this kind of divergence for any table field the generator reads.
- **Required outcome:** fix both sides.
  - The generator's table reads, or a schema check run before the generator loads, must refuse with a line naming the command and the field.
  - The self-test must plant the table defects the generator reads (message type, entries, status codes, the MVU row) in a file copy, as `planted_copy` already does for four refusals, so that the generator re-runs.
- **Verification:** probes p5e and p8 print a line naming GET_MILAN_INFO / GET_CLOCK_SOURCE and the consumer, and the self-test covers both through a file copy.

### F3 - MINOR - Docs - generated F06.14 cells print doubled plurals

- **Where:** `scripts/check_aecp_commands.py:784` (`f", N {r['unit']}s"`) applied to already-plural units in `aecp_commands.json` (`msrp mappings`, `path entries`, `mappings`). The output is in `docs/architecture/06_aecp_engine.md:274,275,277,278,279`: "N msrp mappingss", "N path entriess", "N mappingss".
- **Impact:** Wrong text in a normative, generated table. The fix changes generator code and a generated artifact, so under the owner rule this is not RESIDUE.
- **Required outcome:** stop appending `s` (or store singular units), run `--write`, and keep `make check` green.
- **Verification:** `grep -c 'mappingss\|entriess' docs/architecture/06_aecp_engine.md` returns 0, and the gate passes.

### F4 - MINOR - Tests, Robustness - the new generator input is missing from the suites' `ucode.hex` rules

- **Where:** `tb/pp_top/Makefile:236` and `tb/ucpu/Makefile:20`. Both list `gen_ucode.py` alone as the prerequisite. Since this PR, `gen_ucode.py` also reads `aecp_commands.json` (status codes and MVU command_type, which reach ROM words).
- **Evidence:** in a scratch clone after a build, touching the table leaves `make -q ucode.hex` at rc 0 (up to date); touching `gen_ucode.py` gives rc 1 (`receipts/ucode_prereq_probe.txt`).
- **Impact:** An incremental local suite run after a table edit simulates the stale ROM and can report a false pass. CI is unaffected because it builds from a fresh checkout. The PR records this as a known limitation (09 §8.10 :501-503) and defers the fix as "outside this lane's file scope". No owner decision on #73 limits the lane's files.
- **Required outcome:** add the table as a `ucode.hex` prerequisite in both rules, or record an owner decision on #73 that accepts the deferral.
- **Verification:** after touching the table, `make -q ucode.hex` is non-zero in both suites.

### Suggestions (do not affect the verdict)

- **S1 (Docs):** The parent export is named and consumable, but its fields are described only in the table's `about` strings, 09 §8.10 prose and the gate's `REQUIRED` tuple. A cross-repository consumer (the Mark II firmware tables) would benefit from a field reference or a JSON Schema beside the `aecp-command-table/1` tag. That reference should mark which fields are machine semantics and which are F06.14 prose (`doc`, `clause`, `notify.doc`).
- **S2 (Robustness):** `gen_ucode.py:2443` uses `assert` for its only DISPATCH check, so it vanishes under `python3 -O`. A raised error would hold under any interpreter flag.

### Prior public findings at this head

None. PR #174 and issue #73 carry only the two review-start notices, so there is nothing to resolve or retain.

## 3. Focus items and acceptance

| Item | Result | Evidence |
|---|---|---|
| One machine-readable command table (acceptance 1) | met. `aecp_commands.json` (schema `aecp-command-table/1`): 31 served commands with opcode, rtl constant, cmd/resp cdl, status set, hazard class, lock, notify, GDI and oversize flags, entries | file review; gate clean run |
| gen_ucode.py takes status codes, MVU command_type and dispatch map from it; F06.14 generated (acceptance 2) | status codes and MVU command_type: met. F06.14: met (`--write` is idempotent, probe q3). Dispatch map: generated but consumed by no ROM word, and the engine's real dispatch is ungated (F1) | `gen_ucode.py:41-53,141,2438`; probes q1-q3 |
| Gate in make check and in the CI docs-gates job (acceptance 3) | met. `Makefile:15,48-50`; `.github/workflows/hdl.yml:30-35`. At exact head, push run 38103534048 docs-gates executed `aecp commands selftest: 89 planted defects, 89 caught by name, OK` and `aecp commands: ... OK` | `receipts/hosted/docs-gates_push_job114364185692.log:245-246` |
| REQ-VER-002 Cov/Arch and 09 §8 record what is generated and hand-written (acceptance 4) | **not fully met**: the record overstates what the table drives (F1) | F1 |
| Byte identity | met. `ucode.hex` 518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8 and `ltn_rom.hex` 23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956, identical at base and head (`cmp`). No RTL or ROM input changed, so the elaborated engine is identical. All 27 `tb/` mutation patches naming `gen_ucode.py` pass `git apply --check` at head | `receipts/rom_digests.txt`, `receipts/source_identity.txt` |
| ROM digests equal the parent ledger for pin 2ad2f845 | met. `syn/yosys/rom_digests.tsv` at parent dev ac2c5e77 lines 15-16 hold the same two digests | `receipts/parent_rom_digests_ac2c5e77.tsv` |
| Planted drifts fail by name (at least two re-applied independently) | I re-applied 7 drifts independently of the author's fixtures. Table opcode only (SET_NAME 0x0010->0x0012): rc 1, named. Doc size only (GET_COUNTERS Resp. size): rc 1, named row and column. RTL `OP_GET_COUNTERS_C` only: rc 1, named. Missing command (START_STREAMING): rc 1, named. Generator status source: rc 1, named. `make aecpcmd` on a drift: rc 2. Status code in the table only: rc 1, named. Unrepresentable message type: named on an AEM row (rc 1), nameless refusal on the MVU row (rc 2, F2) | `receipts/drift_probes/` |
| Every finding and refusal has a planted drift | met in memory: 66 finding sites plus the empty-table return, and 16 refusal sites, each hit by name (`receipts/selftest_coverage.txt`). File-path fidelity gap: F2 | coverage script |
| Parent export named (format and path) and consumable | met. `protocol-processor/hdl/aecp/ucode/aecp_commands.json`, JSON, schema tag. The gitlink path `protocol-processor` exists at parent dev ac2c5e77. The parent gate is a follow-up lane (S1) | 09 §8.10 :505-507; parent tree query |
| Closes #73 only if acceptance 1-4 are met | not yet: acceptance 4 (F1), with F2-F4 open beside it | above |

**Conformance arithmetic (clean).**
- The corrected F06.14 sizes match the IEEE 1722.1-2021 field layouts:
  - SET/GET_SAMPLING_RATE: type, index, rate gives cdl 20, so 32 B.
  - SET/GET_CLOCK_SOURCE: type, index, source index, reserved gives cdl 20.
  - GET_AUDIO_MAP: 12 octets of header fields plus 8 per mapping gives cdl 24 + 8·N, so 36 + 8·N B.
  - GET_COUNTERS: cdl 148. GET_AVB_INFO: cdl 32 + 4·N. GET_AS_PATH: cdl 16 + 8·N. ENTITY_AVAILABLE (2021 form): cdl 32. MVU GET_MILAN_INFO: cdl 20/32.
- The status codes equal Table 7-141.
- The gate's µCPU model agrees with the RTL: `KL_aecp_ucpu.sv:257,700-719` (CHECK_LOCK 3, CHECK_ARG 7/11, MAP_VALID 7, faces 2/7/10, BR_STATUS 0 on SUCCESS).
- The F06.14 lead-in claim that a voided MVU answer is NOT_IMPLEMENTED matches `KL_aecp_engine.sv:3734-3741,3786-3794`.

## 4. Executed checks (source head; this reviewer)

Toolchain: Verilator 5.050 through the scoped pinned wrapper (`receipts/focused/*.verilator-version.log`); the host default 5.052 was not used. Python 3.14.7.

| Check | base 2cbed0a9 | head 39cac060 | Receipt |
|---|---|---|---|
| `make check` | 0 | 0. Identical to base apart from `links 1187->1188`, `ids 563->564 files` and the two `aecpcmd` lines | `receipts/focused/*.make-check.*` |
| `scripts/check_upc_map.py` | 0 | 0, same | `*.upc-map.*` |
| `scripts/check_m9_opcodes.py` | 0 | 0, same | `*.m9.*` |
| `tb/ucpu` | 0, 437/437 | 0, 437/437; log identical after path filtering | `*.ucpu.*` |
| `tb/pp_top` (7 builds) | 0, 10470/10470 | 0, 10470/10470; check lines identical | `*.pp_top.*` |
| ROM generation | as above | as above | `receipts/rom_digests.txt` |
| drift and coverage probes | - | as above | `receipts/drift_probes/`, `receipts/selftest_coverage.txt` |

During the head pp_top run, my prerequisite probe touched `gen_ucode.py`'s mtime in the scratch clone, so the `interfaces` build regenerated `ucode.hex`. The content was unchanged (the generator is deterministic) and the tallies are identical to base.

**Hosted, exact head** (`receipts/hosted/exact_head_runs.txt`, queried 2026-10-11T03:03Z):
- push run 38103534048 and pull_request run 38103536339 (merge 7c9d434 onto base 2cbed0a9): docs-gates success and portability success in both;
- `suites` was still in progress in both, so it is not evidence here.

**Clone integrity** (`receipts/clone_integrity.txt`):
- the review clone is at the exact head and tree, with an empty `status --porcelain --ignored`;
- the index blob ids and modes equal the HEAD tree;
- this repository has no gitlinks. The parent's `protocol-processor` gitlink was only read (2ad2f845).
- All probes ran in disposable copies.

## 5. Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | F06.14 sizes and status sets against IEEE 1722.1-2021 field layouts and Table 7-141; MVU GET_MILAN_INFO; the µCPU status semantics the gate models (`KL_aecp_ucpu.sv`); the MVU refusal form in the engine | R608-1 | 39cac060f6f3730cf8172adc6424c275cd268517 |
| RTL | CLEAN | no `.sv`/`.svh`/`.v`/`.hex` change; `ucode.hex` and `ltn_rom.hex` byte-identical at base and head and equal to the parent ledger for 2ad2f845; `tb/ucpu` and `tb/pp_top` identical at base and head; uPC-map and M9 gates | R608-1 | 39cac060f6f3730cf8172adc6424c275cd268517 |
| Robustness | UNCLEAN (F2, F4) | gate refusal paths (unreadable, non-JSON, stale pattern, generator failure) on file copies; generator table reads; suite build prerequisites | R608-1 | 39cac060f6f3730cf8172adc6424c275cd268517 |
| Tests | UNCLEAN (F1, F2, F4) | `scripts/check_aecp_commands.py` in full; self-test coverage of every finding and refusal site; 7 independent planted drifts plus 2 coverage probes; `make check` locally and in hosted docs-gates; mutation-patch applicability | R608-1 | 39cac060f6f3730cf8172adc6424c275cd268517 |
| Docs | UNCLEAN (F1, F3) | 06 §6 F06.14 (generated rows and lead-in), 06 §8 and §8.1, 09 §1/§7/§8.10, REQ-VER-002 row, Makefile and CI comments, PR body, published handoff | R608-1 | 39cac060f6f3730cf8172adc6424c275cd268517 |

## 6. Real limits

- I did not run the full processor suite bank (`run_suites.sh`), `lint_hdl.sh`, the mutation campaigns, `syn/yosys/run.sh` or any parent bank. These are outside this review's allowance. Coverage for them rests on unchanged RTL, identical ROMs, my focused `tb/ucpu`/`tb/pp_top` runs and the hosted portability success, and the author's published narrative.
- The published executable evidence is narrative (HANDOFF.md, PR-BODY.md) with no raw logs. The author's base/head campaign and Yosys equalities, and the scratch-parent run at dev e8454e27, are unverified by this reviewer.
- At query time the hosted `suites` job at the exact head was still running. No completed hosted suites result is claimed.
- There is no manager source bank at this head, and none is inferred. Physical calibration was NOT RUN. No hardware was used, and field skips are not hardware proof.

## 7. Pending manager duties

- Donor and consumer banks at parent dev ac2c5e77 with the gitlink at the head: AECP inventory and BDD tiers, `ooc.sh --record-rom-digests` / ROM-digest verify, `pp_srcs.py`. Also the current-dev merge candidate (builder and native banks) at the merge turn, receipts linked on the PR.
- Hosted/act acceptance, including the exact-head `suites` job's final result.
- The follow-up parent lane that holds the Mark II firmware's AECP tables to `protocol-processor/hdl/aecp/ucode/aecp_commands.json`.
- There is no RESIDUE item for the residue checklist this round.

R608-1 FINISHED
