[A809] REVIEW READY
Commit: 0d80f0ed2a880c3a3b2429c669f104801203ec05 (`pf-951-943n-1`, on the flip train's head `15168e14`, PR #945; for `dev-soft-core`). Covers #956 and #957.
Code head `8845364d`: every code gate below ran there. The commits after it change no image:
- `0818deb1`, `03d9d519` and `0d80f0ed`: docs.
- `b8890724`: the CPU budget harness's `declaring-outputs` check of output 0 and its self-test controls, and two Python
  idiom fixes. The latter regroup `srp_talker_mutants.py`'s rows; the same 63 rows.
- `5d8cfd62`: the harness's 8x8/1if `record.maap` statement, restated by the rule (below), and docs.

Changed:
- **#956**, `sw/firmware/ctrl/srp/srp_mbx.c:40-47`. By the owner's decision of 2026-11-21, `SRP_REDECLARE_CS` is two
  longest LeaveAll periods **less** the JoinTime and THE TRANSMIT's term: 2,977 cs at 1x1/1if, 2,973 at 8x8/1if and
  2,970 at two interfaces (#951: 3,023, 3,027 and 3,030).
  - The count still starts at the Leave's request. So the changed destination is declared two longest periods less
    both terms after it, and is on the wire no later than 30.0 s after it.
  - On the model's wire: 29,770 ms (1x1/1if) and 29,700 ms (8x8/2if) after an aligned request, and 29,995 ms at the
    latest at both.
  - The Talker tests, the composed MAAP conflict test (held at 29 s, on the model's wire by 30 s), the plants and the
    docs that stated about 30.2 s are restated.
- **#957**, `srp_mbx.c:205-214, 228-229` and `srp_mbx.h:62-65`. `listener` records each change of the Listener
  declaration lwSRP indicates for a source's stream (Ignore at a registration's end) in #936's `noticed`, while the
  source's DA gate is open on the interface. That record becomes one unsolicited GET_STREAM_INFO of the output to every
  registered controller, with the new flags.
  - New tests: `Talker.ListenerRegistrationChangeIsNoticed` (1x1/1if, 8x8/2if) and
    `AppOutputs.ListenerRegistrationChangeIsItsStreamOutputsNotice` (every output; 1x1 at one and two interfaces, 8x8
    at one; real Listener MRPDUs, notices read on the wire).
  - Plants: `talker-registration-*` (5) and `registration-notice-*` (3).
- Comments only: `ctrl_app_aecp.c`, `ctrl_loop.h`, the CPU budget harness's texts.
- The harness:
  - `declaring_outputs.py`'s check now expects output 0's Listener notice to every registration after the declared
    Talker's. It encoded the pre-#957 silence.
  - `load_grade.py` states 8x8/1if's own `record.maap` at 185 us (180 before), by the rule.
- Docs: the SRP and AECP READMEs, `MAILBOX_SPLIT.md`, `FR_NFR.md`, `SPLIT_CONTROL_MEMORY.md` section 13.
- No RTL, mailbox-contract, lwSRP, bound or memory-budget change.

Validation (receipts in the author packet; its `INDEX.md` lists them):
- Firmware gate, `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard k/4`, k = 0 to 3, at `8845364d`:
  PASS.
  - Shard 0: 75 verdicts, none failed.
  - Plants caught: control 826, AECP 388, SRP 563 (with the pins). None escaped.
  - The new rows among them: 18 of #956 and #957 at each SRP campaign (13 hold-off, 5 registration), and 3 in the AECP
    campaign.
- The new and restated tests fail on the train's code (receipts `956-tests-fail-at-train-value.txt`,
  `957-final-tests-fail-at-train-firmware.txt`).
- `fw_coverage.py --selftest` (29 of 29) and `--check` (40 files): PASS.
- Twin, twin-plants, twin-maps and twin-maps-plants: PASS.
- `plat_ledger.py`: PASS, 0 findings. 8x8/1if rom 139,248 of 139,264 B (the train's head: 139,208).
- 20 images, base against head: `listener` +40 B. Otherwise only 8x8's field offsets in three objects.
- Release (all-fabric) image: byte-identical but for LiteX's generation times and the CPU netlist's per-run name.
- CPU budget harness `run.py --self-test`: 0 failures at `5d8cfd62` (and at `b8890724`).
- CPU budget harness, the legs the change reaches, base `15168e14` against head:
  - The legs: arm A's `srp`, `backlog-owed`, `aecp`, `datapath-events` (and `aecp-largest-notice` at 1x1/1if),
    `srp-talker-held`, `srp-talker-loss` and `aecp-outputs`.
  - Probes paired: 71 at 1x1/1if and 95 at 8x8/1if.
  - In both: no verdict changed, arm A's seven known `backlog-owed` misses on each side and no other, no pass over the
    share, and all 66 stated costs measured within by the rule at the final head's tables.
  - One is restated there. 8x8/1if's own MAAP record measures 17,259 cycles in `srp-talker-loss` (base 16,176, the
    train's full-pass maximum), 185 us over its 180.
    - The record runs none of the change's code. The 8 bytes each 8x8 interface's SRP state grew move the data after
      it; at 1x1 it is 10,001 on both sides.
    - `load_grade.py --check`, `flip_grade.py --check` at 1x1/1if and 8x8/1if, and `shape_costs.py --check` pass.
      8x8/1if's load stays 0.744 of 0.75, and THE TRANSMIT's row by every source is 76.86 of its 77 ms (76.81 before).
  - The head's `declaring-outputs` legs pass with the arm's restated check (output 0's declared Talker notice, then
    its Listener's, one to every registration each; three planted orders refused in the self-test).
- Docs workflow steps at `0d80f0ed`: 104 of 104, tracked files unchanged after them. End-station builder legs at `5d8cfd62`:
  both `ALL GATES PASS EXCEPT 1 NOT RUN` (leg 0's MAKEFLAGS mutation arm, which the tree declares has nothing to detect here; leg 1's calibration gate, whose real report needs a build tree not on this host).
- Not run: the formal CPU measurement (below), the full Verilator suite sweep (no RTL change), act and the hosted
  gates.

Acceptance criteria:
#956:
- `SRP_REDECLARE_CS` is derived from the named LeaveAll constant with both terms inside: met (`srp_mbx.c:40-47`).
- Tests restated, declared at or after 29.x s and at or before 30.0 s on the model's wire: met. Talker tests at
  29,770 / 29,700 ms declared and 29,995 ms at the latest; the composed test held at 29 s and on the wire by 30 s.
- A plant putting #951's value back fails by name: met, on three tests at both campaigns.
- The bench measures 29 to 30 s at 1x1/1if and 8x8/1if: not done. It needs bench access, which this lane did not
  have; the model predicts about 29.7 s Leave to Talker at 8x8/1if.

#957:
- One unsolicited response with the new flags per registration change, at every output and both shapes, none when
  nothing changed: met in the model, at every output of the 1x1 shape at one and two interfaces and of the 8x8 at one.
- A test that fails on the current code: met.
- The CPU rows at 1x1/1if and 8x8/1if re-measured within their bounds: met on the legs the change reaches, base
  against head. One stated cost is restated by the rule (8x8/1if `record.maap`, 185 us); no bound changes. The
  formal full pass is not run (below).

Open risks/questions:
- **The formal CPU measurement is not run.** Every arm and group at a point is about 70 core-hours at this host's
  load, and no range was bookable for it. Four measured stated costs sit at their statement by the rule, so a group
  not run could hold one over it:
  - `centisecond` at 1x1/1if: 16,064 cycles, 170 of 170 us.
  - `record.srp` at 8x8/1if: 35,273, 375 of 375.
  - `item.acmp_declined` at 8x8/1if: 2,386, 30 of 30.
  - `record.maap` at 8x8/1if: 17,259, 185 of 185 as restated.
  The next formal pass should re-measure them.
- **The 8x8/1if product image's rom** has 16 bytes left under its ledgered 58 RAMB36. Two earlier forms of #957 (296 and
  152 B) did not fit; the commits show both.
- **Changed from TAKEN: #957 depends on the DA gate.** The notice follows the output's DA gate, the face's
  "declaring", not "whatever the Talker's declaration" as the TAKEN said. Behind a closed gate the answer shows
  neither flag, and that cost no rom. A link reset records no Listener change (as #936 records no Talker change
  there).
- **#956's lower bound** holds from a request made on a centisecond. Mid-centisecond, the count (#895's, unchanged)
  can end up to 1 cs sooner.
- **The TAKEN came after the first edits, not before them.**
- **Seen beside it, not changed** (for a new Issue if wanted). Under a held loop's burst of ticks in the model
  (8x8/2if), THE TRANSMIT's resume slice can clear an interface's due that a join timer's expiry re-set between two
  slices, so lwSRP's declaration waits for the next periodic transmission. Not shown reachable in real time.
