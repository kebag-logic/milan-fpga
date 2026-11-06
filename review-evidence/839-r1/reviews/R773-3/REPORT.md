[R773] POSITIVE - exact head 3c22947861e5c057a6195ad46e1a379d67592559

Round R773-3: internal independent review of PR #841 (issue #839). Exact head `3c22947861e5c057a6195ad46e1a379d67592559`, tree `03d9de984aa5c1796aae715abe50abe8e88cfee4`. The PR's GitHub head is the same SHA. Source base `604899c08ff1cd1830e1dd08b733109ef852400c`.

Scope follows the round 3 assignment on issue #839 (issuecomment-6672288408). It covers the delta `ba56827b..3c229478`, two commits (`ba1da8b6`, `3c229478`), README text and check names only. I checked three things:

1. R774-2 F1: the milan_dp README states exactly what the leg checks, line by line against `sim_boot_sa.cpp:759-830` and `:549-618`.
2. The renamed checks say what they compare, and `bootsa` and `bootsa-mutants` still pass with every control caught.
3. No RTL, harness logic or receipt figure changed.

Code the delta does not touch keeps its prior lens verdicts (R773-2 at `ba56827b`, R773-1 at `992c3d7b` for the RTL). Nothing those verdicts depend on changed. I applied all five lenses to the delta.

Verdict: no open BLOCKER, MAJOR or MINOR, and no RESIDUE in the delta. R774-2 F1 (= R773-2 RES-1) is resolved at its cause, with the exact replacement texts. R773-2 S1 / R774-2 S4 and R773-2 S2 were taken. The three suggestions not taken are retained as optional. This round adds three optional wording SUGGESTIONS.

## 1. Delta scope (assignment item 3)

`receipts/delta-gates.txt`:

- `git diff --stat ba56827b..3c229478` touches exactly two files: `tb/verilator/milan_dp/README.md` (+9 -6) and `tb/verilator/milan_dp/sim_boot_sa.cpp` (+3 -2).
- Nothing changed under `hdl/`, `syn/`, `sw/`, `configs/`, scripts, the Makefile, `bootsa_mutants.py` or any submodule gitlink.
- Linear history: `3c229478` has parent `ba1da8b6`, which has parent `ba56827b`. No rebase.
- `git diff --check` is clean (rc 0) both for the delta and for `604899c0..HEAD`.
- The `sim_boot_sa.cpp` change (`:811-816`) only changes the string passed to `check_.dec()`. It adds a ternary on `k` that picks between two literals. The values compared (`wrong_da[i]`, `seen[Other]`) and the expected 0 are unchanged, so no harness logic changed.
- Receipt figures are unchanged against the round-2 author and reviewer figures:
  - 67 checks, 0 failures;
  - 868 first-boot frames (MSRP 36, MVRP 1, gPTP 1, ADP 5, AECP 1, ACMP 2, MAAP 5, AAF 31, CRF 786);
  - early-enable boots: 847 and 3 frames after the pair, 0 left while held;
  - stamp: 93 frames, 3556 octets compared, 0 changed.

  Source: `receipts/bootsa.log:492-575`.

## 2. README against the code (assignment item 1)

`grade()` runs once, at `sim_boot_sa.cpp:862`, after `controller()` (`:849`) and `probe_tx()` (`:861`), and before `pair_order()` (`:863-864`) and `early_enable()` (`:865-866`). `reset()` does not clear `sent_`: each later boot starts its own range at `from = sent_.size()`. So at `:862`, `sent_` holds exactly the first boot's frames, including the controller's and the listener's exchanges. README `:1183-1184` ("every frame of the first boot (through the controller's and the listener's exchanges)") is exact.

| README line | Statement | Code | Match |
|---|---|---|---|
| 1186-1187 | processor offered before the MAC write | `:796-797` `pp_offered_early_` | yes, and now first, in code order |
| 1188 | no all-zero source | `:798` | yes |
| 1189 | no CSR-addressed frame before both halves | `:799-800` (`before_mac && kind != Gptp`) | yes |
| 1190 | each protocol's source is the station MAC | `:801-807` (nine kinds plus `other`) | yes |
| 1191-1192 | destinations: own for MSRP, MVRP, gPTP, ADP, ACMP, MAAP; the controller's MAC for AECP | `:774-775`, `:808-815`; `protocol_da()` `:178-189` | yes (wording, S2) |
| 1193-1195 | EtherType at 12-13 or 16-17 behind a C-TAG; AVTP subtype one of the graded kinds | `classify()` `:151-169`, `:816-817` | yes |
| 1196-1197 | eight kinds required; CRF where the config declares the CRF Media Clock Output | `:818-827` (`kCrfOutputDeclared`) | yes |
| 1198 | `A_TXARB_DIAG` clean | `:828-830` | yes |
| 1200-1203 | octet comparison through the stamp in every boot | `grade_stamp()` `:621-629` at `:867` | yes (unchanged) |
| 1205 | "grades instead" | `early_enable()` makes none of `grade()`'s destination, known-protocol, sent-and-graded or processor-offered checks | yes |
| 1207-1210 | offered while held: MAAP and CRF (MAAP on), AAF and CRF (MAAP off), CRF where declared | `:600`, `:604`, `:608-609` | yes |
| 1211 | no frame of that source before the pair | `:601`, `:605`, `:610` | yes. AAF is not a required offerer with MAAP on, and its early frames are still counted by `early_csr` (`:590`, `:613`) |
| 1212-1213 | MAAP, AAF and CRF frames after the pair (AAF and CRF with MAAP off), CRF where declared | `:602`, `:607`, `:611` | yes |
| 1214-1215 | no CSR-addressed early frame, no all-zero, the station MAC on every frame, `A_TXARB_DIAG` | `:613-617` | yes |

The three texts the round 3 assignment requires are present verbatim:

- `:1183-1184`, the first boot named;
- `:1205`, "grades instead";
- `:1210` and `:1213`, "(CRF where the config declares the CRF Media Clock Output)".

The PR body's "two README lists against the code" table cites the same line ranges as above. I checked every row at this head and each is correct.

## 3. Renamed checks and the campaigns (assignment item 2)

- AECP's name is now "every AECP frame's destination address is the controller's MAC". It compares `s.da` with `kControllerMac` (`:774`), which is what it says.
- The other six names are now "every <kind> frame's destination address is its protocol's". They compare against `protocol_da(kind)`.
- "every frame's EtherType (and, for AVTP, subtype) is a graded protocol's" counts `Kind::Other`. `classify()` assigns `Kind::Other` exactly when the EtherType (after an optional C-TAG) is not one of the four graded ones, or the AVTP subtype is not one of the six graded ones. So the name says what the check compares.
- Neither old parenthetical remains anywhere in the tree. A grep for "untouched" and "known protocol" across `tb/verilator/milan_dp`, `scripts`, `docs` and `CHANGELOG.md` finds only unrelated uses and the README's own prose at `:1193`.
- `bootsa_mutants.py:65-66` (`MSRP_DA`, `ADP_DA`) still name "... is its protocol's". `verdict()` matches by substring (`name in line`). These names were substrings of the old names and are now equal to the new ones.

Reviewer runs on the exact head, using Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`, identity checked):

| Run | Result | Receipt |
|---|---|---|
| `make -j16 bootsa` | rc 0, `== bootsa: checks: 67   failures: 0 ==`, `RESULT: PASS`, 49 s | `receipts/bootsa.log`, `receipts/bootsa.rc` |
| The 12 `MUTATIONS` arms of `bootsa_mutants.py` plus its positive control, through the tree's own `run_mutant()` / `verdict()`, 4 arms at a time (`run_mutants_parallel.py`, `VERILATOR_JOBS=4`) | rc 0, clean leg `pass`, 12/12 caught by every named check, 4 min 14 s | `receipts/bootsa-mutants.log`, `receipts/bootsa-mutants.rc` |

The destination-octet control is caught by "every MSRP frame's destination address is its protocol's", and the last-beat control by "every ADP frame's destination address is its protocol's". Both use the renamed names. This agrees with the author's REVIEW READY on issue #839 at this head (issuecomment-6673486928): 67/0 and "13 checks: 13 PASS, 0 FAIL".

## 4. Prior findings, resolved or retained at this head

| Prior item | State at 3c229478 | Evidence |
|---|---|---|
| R774-2 F1 (MINOR, Docs) = R773-2 RES-1 (RESIDUE): the "grades every frame" list read as covering every boot; "also"; CRF unconditional | **Resolved at its cause**, option (a), with R774-2's exact texts | README `:1183-1184`, `:1205`, `:1210`, `:1213`; section 2 table |
| R773-2 S1 / R774-2 S4 (SUGGESTION): check names saying "untouched" | **Taken** | `sim_boot_sa.cpp:811-816`; section 3 |
| R773-2 S2 (SUGGESTION): CRF condition in the early-enable list | **Taken** | README `:1210`, `:1213` |
| R773-2 S3 = R774-2 S3 (SUGGESTION): `gen_boot_fw.py:112` `body ="".join(...)` | Not taken (outside the round 3 assignment). **Retained, optional** | `gen_boot_fw.py:112` unchanged |
| R774-2 S1 (SUGGESTION): name every check a control is known to fail (`OFF_CRF` for the all-three arm; `OCTETS` for the destination and last-beat arms) | Not taken. **Retained, optional** | `bootsa_mutants.py:116-118` unchanged |
| R774-2 S2 (SUGGESTION): use the exported offsets instead of `0x108`/`0x10C`/`0x784` literals | Not taken. **Retained, optional** | `sim_boot_sa.cpp:617`, `:828`, `:863-864` |
| R773-2 S4 (SUGGESTION, no change required): PM2 is an equivalent mutant | No change; nothing it depends on moved | no `hdl/` delta |

## 5. Findings of this round

No BLOCKER, MAJOR, MINOR or RESIDUE.

The comment-rule scan of the delta's added lines finds:

- no lane label, round, reviewer ID or comment ID;
- no em or en dash.

Source: `receipts/docs-spot.log`.

### S1 - SUGGESTION - Docs - tb/verilator/milan_dp/README.md:1205 - "instead" follows the stamp paragraph

- **Evidence.** "In each early-enable boot it grades instead:" comes straight after the stamp paragraph (`:1200-1203`), not after `grade()`'s list. "Instead" is meant to replace the first-boot list (`:1183-1198`). The stamp paragraph itself says "in every boot", so the meaning holds, and the code is exact.
- **Optional text.** "In each early-enable boot it grades, instead of the first boot's list:".

### S2 - SUGGESTION - Docs - tb/verilator/milan_dp/README.md:1191-1192 - AECP grouped under "fixed-address"

- **Evidence.** "each fixed-address protocol's destination ... is its own for MSRP, MVRP, gPTP, ADP, ACMP and MAAP, and the controller's MAC for AECP" makes AECP read as a fixed-address protocol. The code takes AECP's address from the controller (`:774`). This text predates the delta, and its meaning is correct.
- **Optional text.** "each frame's destination (octets 0 to 5) is its protocol's own for MSRP, MVRP, gPTP, ADP, ACMP and MAAP, and the controller's MAC for AECP;". This matches the new check names.

### S3 - SUGGESTION - Docs - tb/verilator/milan_dp/README.md:1210 - where the CRF condition sits

- **Evidence.** The parenthetical ends the sentence after "the MAAP-off boot", so it can read as qualifying only that boot. The code applies it in both boots (`:568`, `:608`). The text is exact for the shipping config, which declares CRF.
- **Optional text.** Put it at the head of the list item: "that each source it requires (CRF where the config declares the CRF Media Clock Output) offered a frame ...".

## 6. Per-lens results

```text
[R773] PASS Conformance — tb/verilator/milan_dp/README.md:1183-1215 and sim_boot_sa.cpp:549-618,759-830,849-867 at 3c229478 against the round 3 assignment (issuecomment-6672288408) items 1-2 and R774-2 F1's required texts; issue #839 acceptance unchanged by a delta with no hdl/ or harness-logic change (receipts/delta-gates.txt); figures unchanged (receipts/bootsa.log:492-575)
[R773] PASS RTL — receipts/delta-gates.txt: delta ba56827b..3c229478 touches no hdl/, syn/, configs/ or submodule gitlink; the RTL verdicts of R773-1 (992c3d7b) and R773-2 (ba56827b) carry, since nothing in RTL scope changed; bootsa_mutants.py fragments still match the RTL exactly once (12/12 arms planted and built, receipts/bootsa-mutants.log)
[R773] PASS Robustness — sim_boot_sa.cpp:808-817 at 3c229478: the only code change is the per-kind name literal (ternary on k); counters, expected values, reset handling (:496-497) and early-enable ordering are byte-identical to ba56827b (receipts/delta.diff); both early-enable boots and both pair-order boots pass (receipts/bootsa.log)
[R773] PASS Tests — receipts/bootsa.log (67 checks, 0 failures, rc 0, renamed names at :521-528) and receipts/bootsa-mutants.log (clean leg pass, 12/12 arms caught by every named check, the two destination arms by the renamed names) at 3c229478; bootsa_mutants.py:62-73 and verdict() substring match against the new names
[R773] PASS Docs — tb/verilator/milan_dp/README.md:1183-1215 line by line against sim_boot_sa.cpp (section 2 table); PR #841 body Round 3 section and its README/code table; receipts/docs-spot.log (check_doc_style rc 0, docs_check rc 0 with 0 findings, manual em-dash and comment-rule scan of the delta clean); S1-S3 optional
```

## 7. Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round 3 assignment items 1-2; R774-2 F1's required texts; README `:1183-1215` against `grade()`, `early_enable()` and `run()`; figures in `receipts/bootsa.log` | R773-3 | 3c22947861e5c057a6195ad46e1a379d67592559 |
| RTL | CLEAN | `receipts/delta-gates.txt` (no RTL-scope change); the mutant fragments still match the RTL | R773-3 (delta). R773-1 and R773-2 for the unchanged RTL | 3c22947861e5c057a6195ad46e1a379d67592559 (RTL last covered at ancestor `ba56827b`; untouched since) |
| Robustness | CLEAN | `receipts/delta.diff` (no logic change); `bootsa` pair-order and early-enable boots at the head | R773-3 | 3c22947861e5c057a6195ad46e1a379d67592559 |
| Tests | CLEAN (retained R774-2 S1, S2 and R773-2 S3 optional) | `sim_boot_sa.cpp:808-817`; `bootsa_mutants.py:62-73`, `verdict()`; `receipts/bootsa.log`; `receipts/bootsa-mutants.log` | R773-3 | 3c22947861e5c057a6195ad46e1a379d67592559 |
| Docs | CLEAN (S1-S3 optional) | milan_dp `README.md` `:1183-1215`; PR #841 body Round 3 section; `receipts/docs-spot.log` | R773-3 | 3c22947861e5c057a6195ad46e1a379d67592559 |

## 8. Real limits

- **No manager source bank at this head.** No manager source bank ran at this exact head, and I do not claim one. Source-head execution evidence is the author's published receipts plus my own two runs (`bootsa` and the 12-arm campaign).
- **Parallel driver, not the shipped entry point.** The campaign ran through the tree's own `run_mutant()` / `verdict()` in a parallel driver (`run_mutants_parallel.py`), not through `make bootsa-mutants`. The arms, the plants, the build recipe and the catch rule are identical. Only the scheduling differs.
- **Doc gates partly run.** I did not run the docs workflow end to end.
  - `check_em_dash.py` could not run, because its pinned renderer (html5lib) is not installed and installs are not allowed. A manual scan of the delta's added lines found no em or en dash.
  - `check_doc_style.py` and `docs_check.py` ran: rc 0.
  - For the full docs set I rely on the author's receipt ("64 steps ran, 31 not run with a reason, 0 bad"), which I did not re-execute.
- **CRF-off path not exercised.** The `kCrfOutputDeclared == false` branch is not exercised: the shipping config declares CRF. The README's CRF condition is checked against the code, not against a run.
- **No round-3 author receipts in the evidence tree.** The published evidence tree at `f2049361` holds the author's round-2 and the round-1 review packets. It has no round-3 author receipts. That commit is unsigned (`verification.reason: unsigned`). I used the author's REVIEW READY figures on issue #839 and matched them with my own runs.
- **Hosted checks not finished.** Exact-head hosted checks at snapshot time were 12 success, 1 skipped, 15 in progress, 24 queued, 0 failed, of 52 (`receipts/hosted-checks-snapshot.txt`). That is not a hosted verdict. Skipped contexts are not executed evidence.
- **No hardware evidence.** Physical calibration was NOT RUN, and field skips are not hardware proof. Acceptance 3 and 4 rest on the maintainer decision record (issuecomment-6655611611). The PR body says "Relates to #839", not a closing keyword.

## 9. Pending manager duties

- Build and validate the current-dev merge candidate (source base `604899c0`, live dev `cc204c6f`) with the builder and native banks, and link the receipts on the PR.
- Own hosted and act acceptance at the exact head, once the 39 in-progress or queued contexts finish.
- Collect the second positive review (R774-3) and confirm the full completion bar before any merge. Only a maintainer can authorise the merge.
- Optionally carry S1-S3 and the retained suggestions (R774-2 S1, S2; R773-2 S3) to a later docs pass. None of them blocks.

## 10. Clone integrity after probes

`receipts/clone-integrity.txt`:

- HEAD is `3c229478`; HEAD's tree and the index tree are both `03d9de98`;
- 0 status lines, with ignored files included; build products removed;
- `git diff HEAD` is empty;
- the six gitlinks are as recorded, and checked-out submodules sit at their gitlinks (`external` is uninitialized, as found).

R773-3 FINISHED
