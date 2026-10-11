https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6104874774
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
