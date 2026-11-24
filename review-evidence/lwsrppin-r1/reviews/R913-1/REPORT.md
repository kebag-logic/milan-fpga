[R913] NEGATIVE - exact head dbba60e68a6e4a46f80e381c30ff823ee4ff7484

Round R913-1, internal independent review of kebag-logic/milan-fpga PR #992 (`20-lwsrp-pin-d1bb4f4` -> `dev-soft-core`, Closes #991).
Head `dbba60e68a6e4a46f80e381c30ff823ee4ff7484`, tree `1e85cc2bb2ba13643ce6ae7cfb14a49a5a838c6c`, source base `aa30d77f75cd97b3a29878ca0ed68010a7629266`.
All five lenses were applied. Four are clean. `Tests` is unclean on one MINOR (F1), which is why the verdict is NEGATIVE.
Everything else the brief asked me to verify held. I reproduced the red and green runs myself, and the firmware shards, twin and plants match the packet figures.

## Reconstruction (in order)

1. AGENTS.md, CONTRIBUTING.md (sections 3, 5, 6, 6.1), docs/README.md.
2. Issue #991: body (objective, references, scope, two acceptance criteria). It has no comments. PR body, live at this head and checked against the packet's `PR-BODY.md`: the live body adds `Closes #991` and the owner-delegated LUT/FF ruling and drops the "open decision" wording. PR comments: two review-start notices only. There were no prior review findings to resolve.
3. Authorities, read in my own extraction of the standards: IEEE 802.1Q-2022 10.7.5.7 to 10.7.5.9, 10.7.6.6, Tables 10-3, 10-4, 10-5 and 10.8 NOTE 2. IEEE 802.1Q-2018 10.7.4.3, 10.8.2.5, 10.8.2.6 and 10.8 NOTE 2. Milan v1.2 Table 4.3 (joinTime 200 ms, max 240 ms; LeaveTime 5000 ms). lwSRP `d1bb4f4e` `doc/developer.md:272-278` records the public ruling of lwSRP #20.
4. `git diff aa30d77f..dbba60e6` (18 files) and its four commits, plus the lwSRP delta `08ee86e8..d1bb4f4e` (`src/core/mrp_mad.c` +23/-18).
5. The evidence packet at `c8dd5709:review-evidence/lwsrppin-r1/author`: REVIEW-READY, PR-BODY, HANDOFF-r1, receipts/INDEX.md and the receipts named below. Exact-head hosted check runs were listed read-only.

## Findings

### F1 - MINOR - Tests - `tb/verilator/milan_dp/twin_mrp.py:188-190` (txLAF! outcome), self-test `twin_mrp.py:398-441` (`omission-from-full`, `:425-428`)

- **Requirement/evidence:**
  - `opportunity()` adds the txLAF! outcome with two halves. The Applicant goes to its Table 10-3 txLAF! next state. The Registrar takes the sLA's rLA!, so IN goes to LV (docstring `:186-187`, README `:1398-1406`).
  - The self-test's only txLAF! case (`omission-from-full`) runs with the Registrar MT throughout, so the Registrar half is never exercised.
  - I planted one fault: `part.registrar["rLA!"].get(registrar, registrar)` replaced by `registrar` (mutant `txlaf-registrar-kept`, `scripts/twin_mutants.py`). It passes `twin_mrp.py --selftest` ("OK (10 checks)", `receipts/twin-mutants/selftest-mutants.txt`).
  - The mutant is not equivalent. A Domain at QA receives a JoinIn (Registrar IN), is left out of a full own LeaveAll, then sends JoinMt. The correct grade reports 0 findings; the mutant reports "JoinMt ... from VP with the Registrar IN, Table 10-3's tx! sends JoinIn" (`receipts/twin-mutants/txlaf-registrar-probe.txt`, `scripts/txlaf_registrar_probe.py`).
  - No real capture reaches this branch. No LeaveAll frame in either half is full: full=0 in both halves, least spare 1,359 octets in the split's MSRP (`receipts/twin/leaveall-room.txt`). So the self-test is the only coverage of txLAF!, and README `:1404-1406` presents it as holding that case.
  - My other eight planted faults were all caught (old rLA! after/before, unconditional txLAF!, txLAF! QA kept, txLA! QA bracketed, 1514 room, vector without header, MVRP final EndMark).
- **Impact:** a regression in the Registrar side of txLAF! has no gate. It would grade the message after a full own LeaveAll with the wrong Registrar state: a legal JoinMt refused, or a wrong JoinIn accepted.
- **Required outcome:** `twin_mrp.py --selftest` fails when the Registrar does not take the sLA's rLA! at txLAF!. One way is a full-omission case with the Registrar IN beforehand.
- **Verification:** rerun `scripts/twin_mutants.py <root> <scratch>`. `txlaf-registrar-kept` must be CAUGHT, the other eight still CAUGHT and the control PASS. `make twin` stays at 0 findings and `make twin-plants` still refuses 16 of 16.
- **Lens attribution:** Tests only. The code is correct against Table 10-4 and 10.7.6.6 (Conformance clean), and it behaves correctly at the full boundary (Robustness clean). What is missing is a test that can fail for this defect.

### S1 - SUGGESTION - Docs - `sw/firmware/ctrl/test/test_ctrl_firmware.py:72-79`

The gate docstring's `srp` entry names its notable suites (#895 `srp_talker.cpp`, #930 `srp_listeners.cpp`) with their shapes. The new `srp_own_leaveall.cpp` arms (lwSRP #20, 8x8/1if every input and 1x1/1if) are wired in at `:211` but are not described there. Optional.

No RESIDUE and no comment-rule residue. The added lines carry no lane labels, review rounds, reviewer IDs, issue-comment IDs, tool or model names, or host details (scan of every added line). No U+2014 in any added line.

## Lens results

```text
[R913] PASS Conformance - srp_own_leaveall.cpp:1-276; twin_mrp.py:13-38,82-90,180-192,293-341; README.md:1390-1407; lwSRP d1bb4f4e mrp_mad.c:766-782,1505-1534 - the own-LeaveAll reading against 802.1Q-2022 10.7.5.8/10.7.5.9/10.7.6.6, Tables 10-3/10-4/10-5 and the lwSRP #20 ruling; both acceptance criteria
[R913] PASS RTL - diff aa30d77f..dbba60e6 (no hdl/ file); packet ledger/image-deltas.txt, ledger/margins.md, ooc/{base,head,head2}.tsv; lwSRP mrp_mad.c delta - firmware and memory-architecture effect of the pin
[R913] PASS Robustness - srp_own_leaveall.cpp:141-275 (every input, offsets 5-200 ms plus 129/189/191, both stations' LeaveAlls); twin_mrp.py:293-341 (room boundary, MVRP walk); receipts/probe-before/probe.log - boundary, ordering and configuration paths
[R913] UNCLEAN Tests - twin_mrp.py:398-441 vs :188-190 (F1); srp_own_leaveall.cpp red at 08ee86e8 / green at d1bb4f4e (receipts/own-leaveall/*); twin and plants (receipts/twin/*); firmware shards 0 and 3 (receipts/firmware/*)
[R913] PASS Docs - SUBMODULES.md:26; MAILBOX_SPLIT.md:454; ctrl/README.md:644-649; ctrl/srp/README.md:76-77,594; milan_dp README.md:1390-1407,1524; Makefile:37-38; twin_compare.py:91; twin_plants.py:234; drawio/svg/png + PNG_MANIFEST.json; live PR body vs packet - pins, permalinks, generated artifacts and claims
```

### Conformance (CLEAN)

- **Acceptance criterion 1** (reproduction red at `08ee86e8`, green at `d1bb4f4e`, at 1x1/1if and 8x8/1if). I ran the two `own_leaveall_arms` myself with `scripts/run_own_la.py`.
  - **Base:** the tree at `3fb8cc76` (gitlink `08ee86e8`) against lwSRP `08ee86e8`. At 8x8/1if, 351 of 387 withdrawals were never sent; at 1x1/1if, 78 of 86. Each arm failed 39 of 44 tests.
  - The only Lv sent at the base came at offsets 190, 191, 195 and 200 ms, 11 withdrawals at each (9 inputs + 2 inputs). Those are the withdrawals made after the rejoin tx!, which fits the VP to Lv! to VO mechanism the PR describes.
  - **Head:** `dbba60e6` against `d1bb4f4e`. 387 of 387 and 86 of 86 sent, worst delay 190 ms (bound 240), the peer deregistering at each Lv, 44 of 44 tests passing in each arm.
  - **No-withdrawal leg:** 90,190 ms, 5 board and 2 peer LeaveAlls, every Listener registered, no Lv, at both base and head. It is a guard that the fix deregisters nothing, not a discriminating reproduction.
- **Acceptance criterion 2:** see Tests and Docs. Tiles are unchanged per the packet's margins.md.
- **The twin grade against the clauses:**
  - 10.7.6.6 says the sLA's rLA! goes "against all instances of the Applicant state machine, or the Registrar state machine", which is ambiguous. The PR's reading, one Applicant event (txLA! or txLAF!) with the rLA! reaching the Registrar only, is the public ruling of lwSRP #20. The issue's scope adopts it.
  - It is also the only reading under which Table 10-3's txLA! next states matter. The txLAF! row equals the rLA! row in every state but LA, so txLAF! already is the "no room" substitute.
  - TXLA and TXLAF (`twin_mrp.py:80-85`) match Table 10-3 of 802.1Q-2022 cell by cell. Table 10-4 has no txLAF! row, and its "rLv! || rLA! || txLA!" row takes IN to LV, as coded.
  - `MRPDU_ROOM = 1500` matches `MBX_FRAME_BYTES_MAX` 1514 less 14 (`mbx_contract.h:1401`). FirstValue widths come from `srp_wire_compare.MSRP` (25/34/8/4) and VID 2.
- **The grade does not merely legalize the device:**
  - The device omits a value as txLAF! whenever it is left out (lwSRP `mrp_mad.c:1513-1514`). The grade allows txLAF! only where the frame is full, which is stricter than the device. For the states whose txLA! cell is bracketed (VO, LA, AO, QO, LO), the txLA! and txLAF! next states are identical, so the two descriptions agree there.
  - Mt at the own LeaveAll stays illegal (`mt-at-own-leaveall`).
  - Run against the real captures (`receipts/twin-mutants/capture-probes.txt`), making txLAF! unconditional lets `leave-all-omission` ESCAPE, so the room check is what refuses that plant. The old "rLA! after txLA!" model still reports 0 findings on the head captures, which confirms the PR's statement that the old grade passed only because the stimulus has no withdrawal within a JoinTime of the LeaveAll.
- **Citations:** the reproduction's comments are correct: Milan v1.2 Table 4.3 (240 ms joinTime maximum, LeaveTime 5 s), 802.1Q-2018 10.8.2.5 (JoinIn 1, JoinMt 3, Lv 5), 10.7.4.3 (draw under 1.5 x LeaveAllTime = 15 s) and 10.8 NOTE 2.

### RTL (CLEAN)

- No file under `hdl/` changes. Applied to the firmware and memory architecture the pin changes:
  - The lwSRP delta moves the sLA's rLA! from every Applicant and Registrar (`broadcast_event`) to every Registrar (`sla_registrars`). Each Applicant takes its own txLA!/txLAF! in `mrp_transmit`, and nothing else in the transmit path changes.
- **Image delta** (packet `ledger/image-deltas.txt`):
  - +60 B `.text` in every image, all of it `mrp_mad.o` (13,155 to 13,219 B). No other section or object changes.
  - ROM +56/+64 B. The 8x8/1if ROM moves from 40 to 104 B into its third 2,048 B bank, leaving 1,944 B. SRAM 0. RAMB36 tiles unchanged at every point (`ledger/margins.md`).
- **Out-of-context map** (`ooc/base.tsv`, `head.tsv` = `head2.tsv`):
  - RAMB36 and RAMB18 unchanged.
  - ROM-top LUT/FF change: 8x8/1if 51/14 to 65/27, 8x8/2if 146 to 169 LUT, 1x1 down.
  - This is ACCEPTED by the owner-delegated ruling as content-driven mapping. The routed 8x8/1if build (fit plus the #818 floor, totals in the PR body) is a merge condition, not a review finding, and I record it under pending duties.
- Widths and indexing in the new grade code: the MVRP 13-bit NumberOfValues mask, (n+2)/3 ThreePacked and (n+3)/4 FourPacked counts (in the test's parser) are correct.

### Robustness (CLEAN)

- **Reproduction coverage:**
  - Every input at 8x8/1if (9 sinks) and at 1x1/1if (2).
  - 43 offsets from 5 to 200 ms, including 189 and 191 around the 190 ms join timer.
  - The no-collateral check on every later input, and a 2 s settle proving nothing re-declares after its Lv.
  - The LeaveAlls of both stations.
- **Twin grade boundaries:**
  - `>` against spare is the right comparison: frame + vector = 1500 fits, and this is held by `msrp-room-for-a-domain`, spare 7 against vector 7.
  - A Listener's FourPacked octet is counted.
  - The MVRP walk is bounded by the frame length.
- **Extra probe, outside the issue's scope** (`receipts/probe-before/probe.log`, `scripts/probe_before_leaveall.inc`):
  - Withdrawals 5, 50, 100, 150, 200 and 400 ms before the board's first own LeaveAll at head, at both points. Each sent its Lv 1 ms later and the peer deregistered at once.
  - In this fixture the LeaveAll leaves at its timer when no join timer runs, so the window between leavealltimer! and a delayed LeaveAll MRPDU was not reached. I report this as a limit, not as evidence either way.

### Tests (UNCLEAN: F1)

- **Reproduction:** it fails for the defect it names. I ran it red myself at `08ee86e8` and green at `d1bb4f4e` (figures above).
  - Its frame reader is independent of both lwSRP parsers (`srp_own_leaveall.cpp:49-80`). The peer is lwSRP's own Milan Registrar, so a second, independent decoder decides "sent as Lv".
- **Twin:** I ran `make twin` with the pinned Verilator 5.050 (identity checked: "Verilator 5.050 2026-07-01 rev v5.050") and got rc 0. The self-test reported OK (10 checks), and "twin: 0 finding(s)".
- **Plants:** `make twin-plants` twice, rc 0 both times. All 16 plants were REFUSED twice in each run (`receipts/twin/plants-{1,2}-refusals.txt`).
- **Firmware gate, shard 0/4** (`--require-rv32 --self-test --jobs 4`): rc 0. 90 arms `[ok]`, 0 not ok, 2,244 cases in PASS verdicts, both own-LeaveAll arms `[ok]`.
- **Firmware gate, shard 3/4:** rc 0, 543 `[ok]` catches, 0 FAIL/MISSED/ESCAPED. The pin controls name `d1bb4f4e`: an edited `src/core/mrp_mad.c` and `97677fcb` are both refused.
- **Packet only:** shards 1 and 2 (832/832, 392), the load and flip grades, the harness, `plat_ledger` and `test_ctrl_memory`. Their receipts match the PR body:
  - loads 0.512/0.70 and 0.744/0.75;
  - last notice 127.43 ms; ACMP 29.15/30; txL 47.98/49; THE TRANSMIT 77 against 76.81, byte-identical to the base;
  - the harness at 1x1/1if and 8x8/1if, including answering-every-port and answering-later, 0 passes over THE SHARE.
- **Open:** F1, the self-test's txLAF! case does not test the Registrar half.

### Docs (CLEAN)

- **Pin sites** (`git grep` at HEAD for `08ee86e8`/`d1bb4f4e`): every pin site moved:
  - the gitlink;
  - `ctrl_arms.LWSRP_REV` and its checkout comment;
  - SUBMODULES.md;
  - the drawio, SVG and PNG diagrams and PNG_MANIFEST.json;
  - the prose pins in MAILBOX_SPLIT.md, ctrl/README.md and ctrl/srp/README.md;
  - the two lwSRP permalinks.
- **Permalinks:** I checked them at the pin. `integrator.md#L327-L329` holds the same three sentences that `08ee86e8` had at 324-326. `mrp.h#L292-L294` is unchanged.
- **Historical records left as they should be:** `ci/image/exec-audit-receipt.json:4184` (a receipt of commit `54fbcba6`) and `SPLIT_CONTROL_MEMORY.md:491` (the figures of `8ab2b539`).
- **lwSRP pin:** `d1bb4f4e` is on lwSRP `origin/main`, descends from `08ee86e8`, and its tree is `ba42b837`, equal to `25b5a740^{tree}`.
- **Gates run in a copy:**
  - `submodule_boundaries.gen.py --check` and `--selftest`, `check_diagram_pngs.py`, `check_submodule_docs.py`: rc 0 each.
  - `docs_check.py`: 0 findings.
  - `check_py_idiom.py` and `--selftest` (54/54), `check_cpp_idiom.py` and `--selftest` (83/83): rc 0.
  - `check_em_dash.py` refused to judge because the pinned renderer is not installed here. My direct scan found 0 added lines with U+2014.
- **README text:** the twin README, plant words, Makefile header and plant docstring agree with the code.
- **PR body:** every figure in it that I checked matches the packet and my own runs.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | srp_own_leaveall.cpp; twin_mrp.py:13-38,80-90,180-192,293-341; milan_dp README.md:1390-1407; lwSRP d1bb4f4e mrp_mad.c:766-782,1505-1534; 802.1Q-2022 10.7.5.7-9, 10.7.6.6, Tables 10-3/10-4/10-5; Milan v1.2 Table 4.3; own red/green runs | R913-1 | dbba60e68a6e4a46f80e381c30ff823ee4ff7484 |
| RTL | CLEAN | full diff (no hdl/); lwSRP 08ee86e8..d1bb4f4e mrp_mad.c; packet image-deltas.txt, margins.md, ooc base/head/head2.tsv (LUT/FF accepted by owner ruling; routed build is a merge condition) | R913-1 | dbba60e68a6e4a46f80e381c30ff823ee4ff7484 |
| Robustness | CLEAN | srp_own_leaveall.cpp:141-275; twin_mrp.py:293-341; receipts/probe-before/probe.log; receipts/twin/leaveall-room.txt | R913-1 | dbba60e68a6e4a46f80e381c30ff823ee4ff7484 |
| Tests | UNCLEAN (F1 MINOR open) | twin_mrp.py:398-441 vs :188-190; receipts/own-leaveall/*; receipts/twin/*; receipts/twin-mutants/*; receipts/firmware/gate-{0,3}.log | R913-1 | dbba60e68a6e4a46f80e381c30ff823ee4ff7484 |
| Docs | CLEAN | SUBMODULES.md, MAILBOX_SPLIT.md, ctrl/README.md, ctrl/srp/README.md, milan_dp README.md, Makefile, twin_compare.py, twin_plants.py, diagrams + manifest; receipts/docs/*; live PR body vs packet | R913-1 | dbba60e68a6e4a46f80e381c30ff823ee4ff7484 |

## Real limits

- **Firmware shards 1 and 2** (mutation campaigns), the load and flip grades, the CPU budget harness arms, `plat_ledger`, `test_ctrl_memory` and the out-of-context map were not rerun. They are verified from the packet's receipts only. Shards 0 and 3 were rerun.
- **Where the author's gates ran:** firmware, harness, ledger and OOC at `402834ac`. `402834ac..dbba60e6` changes only `twin_mrp.py` docstrings (8 lines), which none of those gates read. My twin, plants, docs gates and shards 0 and 3 ran at `dbba60e6`.
- **Base run setup:** it used an extracted tree of `3fb8cc76` (the reproduction commit, gitlink `08ee86e8`) with the processor, gPTP, verilog-axis and tsn-c-stack trees archived at their gitlinks. My runner omits the processor-harness reuse cut that only `test_acmp_mbx.cpp` needs; the head log came from the first copy of the runner, which still made that cut.
- **Em-dash gate:** `check_em_dash.py` was not run (no pinned renderer). A direct U+2014 scan of the added lines stands in for it.
- **Probe-before window:** the probe did not reach a withdrawal between leavealltimer! and a LeaveAll MRPDU held back by a running join timer (see Robustness).
- **Not done:** no manager source bank, no hosted or act acceptance, no hardware. Physical calibration NOT RUN. Field skips are not hardware proof.
- **Hosted checks at this head, when I looked:** only `changes`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability` and `Prepare pinned Yosys` had succeeded. The rest were queued or in progress.
- **Receipt redaction:** my receipts have host and home paths replaced by placeholders (`<packet>`, `<clone>`, `$HOME`, `<pinned-verilator-root>`). They are otherwise raw.
- **Clone restored:** the clone was restored to the exact head: index and worktree equal HEAD, 1,937 tracked blobs hash to their index ids, no index flags, and the 5 gitlinks are at their pins with clean checkouts. The only residue, three bytecode caches from my head run, was removed.

## Pending manager duties

- Carry F1 to the author lane and re-review the corrected head (Tests at minimum).
- The routed 8x8/1if build of this head against the base is a merge condition: fit, the #818 timing floor, and its LUT/FF totals added to the PR body.
- The current-dev merge candidate (live dev `e275d795`) needs builder and native banks.
- Exact-head hosted and act acceptance.
- #990 (srptx red at the base, same kinds) stays out of scope.
- Process observations, for triage and not graded here:
  - Issue #991's body names no executor or reviewer and no exact validation command, and the issue has no takeover comment (AGENTS section 4/5).
  - The published packet's logs carry lane scratch paths, while `receipts/INDEX.md:4` says host paths "are not published".

R913-1 FINISHED
