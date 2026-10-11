[R597] POSITIVE - exact head 49b437f445e34b558106c8799c1ffc0a5dc844cf

# R597-1: external independent review of PR #718 (issue #711)

- Role: cleared-context external reviewer `[R597]`, round R597-1.
- Exact head: `49b437f445e34b558106c8799c1ffc0a5dc844cf`, tree `3bb600ec7a1e16887bed81cdf7f36e1d55f6a793`, on source base dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (two commits, `55ef91b75` and `49b437f44`).
- Verdict: **POSITIVE**. All five lenses CLEAN at the exact head. There are no open BLOCKER, MAJOR, MINOR or RESIDUE items. One SUGGESTION (S1) is non-blocking.
- Closes #711: justified. Acceptance items 1 to 5 are met. For items 3 and 5, the issue's premises ("the firmware digest moves", "the documented digest") did not hold. The author said so publicly, and the invariant each item protects is met (see Conformance).
- No manager source bank ran at this head, and none is claimed or inferred. The execution evidence below is my own, at the exact head and base, plus the author's published receipts where I say so.

## What I read, in order

1. `AGENTS.md`, `CONTRIBUTING.md` (review bar, commit rule), `docs/README.md`.
2. Issue #711 body (acceptance 1-5), the assignment comment (STOP on any decoded SRP behaviour change, lost coverage or lost kills; capture comparison model), TAKEN and REVIEW READY.
3. lwSRP issue #17, its acceptance (the reference end station's layout: one Message per AttributeType, one VectorAttribute per value, NumberOfValues 1, ascending FirstValue, no "+k" packing, LeaveAll flagged per type as before), and lwSRP PR #18 (merged at `08ee86e8`, two positive reviews at `a44eeedf`).
4. The PR body, then `git diff e8454e27..49b437f4` and both commits.
5. Executable evidence: my own runs (below) and the author's packet `review-evidence/711-r1` at `643de7f0` (HANDOFF.md, decoded, capture, export, route, firmware summaries, scripts).
6. Prior public review findings on PR #718: I checked after my own pass. At the time of writing, the PR has only two "review started" notices, so there was nothing to resolve or retain.

## Findings

### S1 - SUGGESTION - Tests - `sw/firmware/ctrl/test/srp_latency.cpp:76-84` - the end-of-walk assertion cannot see a walk that forgets the Message EndMark skip

- Evidence: probe `mut-noendskip-newpin` drops `off+=2;` at line 81, the skip over the Message EndMark. The arm still passes at IF=1 and IF=2 (`receipts/walk/mut-noendskip-newpin.log`, rc 0). MVRP has a single AttributeType (802.1Q-2018 11.2.3.1), so a grouped MVRP MRPDU has exactly one Message. Its Message EndMark sits immediately before the MRPDU EndMark, and a walk that stops on the first of the two zero pairs satisfies `!f->bytes[off] && !f->bytes[off+1]`.
- What the assertion does prove: the probe `mut-vecsize-newpin` (vector size `n/3`) fails. The base walk with the new assertion fails at `08ee86e8`. A planted lwSRP encoder that drops the MRPDU EndMark (`receipts/walk/lwplant-noend.patch`) fails the head walk at IF=1 and IF=2. The base walk misses that same plant (rc 0). So the shipped walk does require lwSRP's MRPDU EndMark, as the PR claims.
- Impact: none on the firmware or on the LeaveAll timing verdict. This weakness only matters if the test's own walk is later edited.
- Optional change: also require that the walk has consumed the whole MRPDU (for example `off+2==f->len`, since `send_pdu` adds no padding: `sw/firmware/ctrl/srp/srp_mbx.c:502-516`). Alternatively, assert the Message EndMark explicitly before skipping it.
- Verification: the `noendskip` variant of `scripts/r597_walk_variants.py` must then fail.

No other finding. The trailing-octet frames that my decoder flags are not lwSRP output. They come from the test harness at both pins (`receipts/decoded-trailing.log`):

- empty-MRPDU filler records in `srp_mbx`, `test_acmp_mbx` and the model suite;
- the maximum-record frames of `srp_app` (`srp_app.cpp:127-136`).

They decode with no difference between base and head.

## Lens results (clean lines with evidence)

### Conformance: CLEAN

`[R597] PASS Conformance - third_party/lwSRP gitlink, sw/firmware/ctrl/test/srp_latency.cpp:68-84, receipts/decoded-*, receipts/lwsrp-pin-provenance.txt - acceptance 1-5 of #711 and IEEE 802.1Q-2018 10.8.1.2 / 10.8.2.8-10.8.2.10 / 35.2.2 / 11.2.3.1`

- **Acceptance 1.** The gitlink moved `9197193e -> 08ee86e8`. That is the only submodule change, and `.gitmodules` is unchanged.
  - `08ee86e8` is on lwSRP `main` first-parent. It is the merge of PR #18, with parents `9197193e` and `a44eeedf`, and its tree `67b35af9` equals the reviewed head `a44eeedf`.
  - Compiled-source change: `src/core/mrp_mad.c`, transmit functions only (hunks at 1285, 1336 and 1370). `src/include/shish_lan/mrp.h` changes in a comment only. `mrp_pdu.c`, `src/ports` and `src/modules` are unchanged, so the receive path is identical.
- **Acceptance 2.** The firmware arms pass, including the F4 SRP set at IF=1 and IF=2, and every campaign keeps its kills. Coverage is 30 files at 100 % with a table identical to base (see Tests).
  - The byte-level expectation change is `srp_latency.cpp:76-84`. It is cited to 802.1Q-2018 10.8.1.2 and listed in the packet's HANDOFF.md ("Byte-level SRP expectations", lines 39-44).
  - It is the only one. I enumerated every test consumer of transmitted SRP bytes. The fixture's own capture walker (`srp_fixture.hpp:76-127`) already walks every VectorAttribute to each EndMark, using AttributeListLength for MSRP. `srp_mbx`, `srp_walk`, `test_acmp_mbx` and `srp_shape` read decoded declarations through it.
- **Walk claims.** My walk matrix (`receipts/walk/summary.txt`) reproduces each claim at both interface counts:

  | Walk | lwSRP pin | Result (IF=1 and IF=2) |
  |---|---|---|
  | Base walk + new assertion | `08ee86e8` | FAIL: "walk must end on the MRPDU EndMark" |
  | Base walk + new assertion | `9197193e` | pass |
  | New walk (exact head) | `08ee86e8` | pass |
  | New walk (exact head) | `9197193e` | pass |
  | Exact base walk, no assertion | `08ee86e8` | pass (the old check was blind) |

- **Decoded SRP behaviour is unchanged.** I used my own decoder (`scripts/r597_mrpdu.py`), written from 10.8.1.2, 10.8.2, 35.2.2 and 11.2.3.1, which shares no code with lwSRP, the fixtures or the author's decoder. I fed it with my own TX hook on the host mailbox model (`scripts/r597_dump_hook.py`, probe copies only), running every firmware arm at base (lwSRP `9197193e`) and head (`08ee86e8`).
  - Results: 4,186 MRPDUs; 2,201 byte-identical; 1,985 layout-only; **0 decoded differently**; 8,278 values; 173 LeaveAll types; 289,969 / 285,067 octets; 122 non-MRPDU frames, all unchanged. Every frame has the same interface and time at both pins.
  - These totals equal the author's table, and every per-arm figure matches (`receipts/decoded-summary.txt`).
  - Decoder controls (`receipts/decoder-selftest.log`, 15 of 15):
    - grouped, split and "+k" packed forms decode equal;
    - a swapped event, a dropped vector, a dropped LeaveAll, a changed FirstValue and a changed FourPackedEvent decode differently;
    - descending order and a missing MRPDU EndMark are reported as not grouped;
    - a truncated vector and a wrong AttributeListLength are refused.
- **Grouped layout versus the reference end station.** Every head MRPDU has:
  - one Message per AttributeType, in type order;
  - the LeaveAll vector first, with NumberOfValues 0;
  - one VectorAttribute per value with NumberOfValues 1, in strictly ascending FirstValue;
  - no "+k" packing;
  - an MRPDU EndMark.

  Zero departures apart from the harness-made trailing octets above. This is the reference's layout as published on lwSRP#17. The base had 647 MRPDUs with a type split across Messages, and no multi-value vectors at either pin.

  On decoding: the receive path is unchanged between pins. lwSRP#17 acceptance 4 covers receiving all three valid forms upstream. In this tree, `srp_walk.cpp:19-29` feeds a certified switch's two-value Domain vector through the firmware.
- **Acceptance 3.** lwSRP is not in the capture firmware. `tb/verilator/nvm_capture_cpu/firmware.py:71,108` builds from `sw/firmware/milan_baremetal/milan_baremetal.c` alone, `lwsrp_table.json` is the builder's reservation table (`sw/builder/endstation_builder.py:5833`), and no capture input reads `third_party/lwSRP`.
  - The diff touches no capture input.
  - `scripts/check_nvm_capture.py` passes at head and base (`receipts/docs/16b-system-python.log`, `16c-base.log`).
  - The author's nine `capture.log` files are byte-identical base against candidate (`capture--compare.json`).
  - The invariant (candidate logs equal base logs apart from lwSRP-caused changes) holds with nothing to attribute.
- **Acceptance 4.** The pin-derived records are:
  - the ledger row (`check_submodule_docs.py` OK, 5 exact gitlinks);
  - the generated diagram (`submodule_boundaries.gen.py --check` OK; PNG manifest `check_diagram_pngs.py` OK);
  - the arm pin `ctrl_arms.LWSRP_REV`, enforced by the pin-refusal arms;
  - the prose pins.

  The two re-pointed contract permalinks quote text byte-identical to the old line ranges. The one remaining `9197193e` (`sw/firmware/ctrl/srp/README.md:292`) is a correct historical statement ("merged as PR #15 at `9197193e`").
- **Acceptance 5.** The shipping firmware is `sw/firmware/milan_baremetal` only (`sw/litex/milan_soc.py:3991-3993`). Nothing in the builder, LiteX, syn or HDL reads the lwSRP gitlink, and the diff touches none of them.
  - The author's exports show identical ROM and image digests at base, head and a second base (1x1 `a14e34e7…`, 8x8 `cf2c371f…`).
  - Their `route-1x1` gate is PASS with zero delta. The route reports are identical apart from the date line. The differing build files are path-embedding noise that is equally present base-to-base.
  - No prior tracked digest existed. The PR now documents the measured ones.

### RTL: CLEAN

`[R597] PASS RTL - git diff e8454e27..49b437f4 (file list) and gitlinks protocol-processor 2ad2f845, gptp-processor 5dce647a, verilog-axis 48ff7a7e, external efeb541a - no RTL, constraint, synthesis or RTL-submodule input changed`

- No `hdl/`, `syn/`, `tb/`, `sw/litex/` or `sw/builder/` file is in the diff. The RTL-relevant gitlinks are identical at base and head (`receipts/lwsrp-pin-provenance.txt`).
- `hdl/common/csr/gen/lwsrp_csr_defaults.svh` comes from the builder's configuration, not from the lwSRP submodule.
- The author's `route-1x1` receipts show identical utilization and timing (WNS 0.299 ns, WHS 0.031 ns). I did not rerun Vivado.

### Robustness: CLEAN

`[R597] PASS Robustness - srp_latency.cpp:69-84 bounds, srp_mbx.c:502-523,800 capacity and parse path, receipts/walk/lwplant-*, receipts/fw/arms-log-diff-base-head.txt - malformed/truncated walk input, capacity and MTU split, self-parse of grouped MVRP`

- **New walk bounds.** Every read is guarded (`off+2<=f->len` before each header). A width or count that jumps past the frame ends the loop, and the assertion short-circuits on `off+2<=f->len`.
- **MRPDU EndMark.** A frame with no MRPDU EndMark fails, as shown by the planted lwSRP defect.
- **Capacity.** `srp_mbx.c:800` passes `sizeof(frame)-14` to `mrp_transmit`, and lwSRP's new contract (`mrp.h:260-266`) needs only one value's Message plus the LeaveAll preamble. With 4,186 MRPDUs, no frame count or timing changed, so no split moved.
- **Self-parse of grouped MVRP.** `send_pdu` licenses VIDs by parsing its own grouped MVRP PDU with the unchanged parser (`srp_mbx.c:519-522`). VLAN registration tests pass at IF=1 and IF=2.
- **Mailbox cost.** The only behavioural log differences are fewer accesses on the SRP transmitting poll (48 to 46 at IF=1, 91 to 89 at IF=2, bounds 770 and 1540), from shorter frames, plus the encoder's object size.

### Tests: CLEAN

`[R597] PASS Tests - receipts/fw/head-selftest.log, receipts/fw/*-dump-arms.log, receipts/fw/{head,base}-coverage-check.log, receipts/walk/* - exact-head firmware unit job with planted defects, base/head arm and coverage equality, walk sensitivity probes`

- **Exact-head firmware unit job.** Command: `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4`, with the pinned RV32 SDK installed from its verified archive into scratch (`receipts/sdk-install.log`) and `third_party/lwSRP` at its gitlink. Result: rc 0, `test_ctrl_firmware: PASS`.
  - 59 arms `ok`, 0 FAIL.
  - Planted defects: control 471 of 471; AECP 74 `[ok]`; SRP 237 `[ok]` (the 169 + 68 split); both lwSRP pin refusals `[ok]` (an edited `src/core/mrp_mad.c`, and `9197193e` checked out). That is 784 of 784, with 0 `[FAIL]` lines.
- **Base against head arms (no planted defects).** Both rc 0. The verdict lines are identical (59 `ok` each). The tallies are identical: 65 tallies, 1,412 checks, 0 failures on my counting basis, which sums every `checks:` line. The author's 1,191 cases are a different basis.
  - The only differences in the full logs are `core_mrp_mad.o` text 12,709 to 13,309 (+600) at every RV32 shape and the two SRP transmitting-poll access counts above (`receipts/fw/arms-log-diff-base-head.txt`).
  - The mutation tables (`ctrl_mutants.py`, `aecp_mutants.py`, `srp_mutants.py`) are untouched by the diff, so the base totals equal the head totals.
- **Coverage.** `fw_coverage.py --check --jobs 4` passes at head and base (30 files). The 30-row table, including numerators and denominators, is byte-identical (`receipts/fw/coverage-compare.txt`).
- **The new test can fail for its defect.** See the walk matrix (Conformance) and S1. The vector-size mutant fails, and the planted lwSRP EndMark drop fails at head and passes the base walk. The surviving Message-EndMark-skip mutant is S1 (SUGGESTION).

### Docs: CLEAN

`[R597] PASS Docs - docs/reference/SUBMODULES.md:26,229, docs/design/MAILBOX_SPLIT.md:295, sw/firmware/ctrl/README.md:340-342, sw/firmware/ctrl/srp/README.md:75-76,292-293,343-345, docs/diagrams/submodule_boundaries.*, PNG_MANIFEST.json, receipts/docs/summary.tsv - pin prose, permalinks, generated records, and documentation gates at the exact head`

- **Focused gates at the exact head** (`receipts/docs/summary.tsv`), all rc 0:
  - `submodule_boundaries.gen.py --check` and `--selftest`;
  - `check_submodule_docs.py` and `--selftest`;
  - `check_diagram_pngs.py`;
  - `check_em_dash.py --base e8454e27`;
  - `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`;
  - `gen_toc.py --check` and `--verify-anchors`;
  - `DOC_MAP.gen.py --check`;
  - `check_cpp_idiom.py`, `check_py_idiom.py`, `check_hygiene.py --check`, `measure_test_evidence.py --check`.

  `check_nvm_capture.py` exited 1 only because the markdown environment lacks PyYAML (line 16). Rerun with the system interpreter it passes at head and base.
- **Prose accuracy.** The new sentences in `srp/README.md:343-345` match the measured behaviour. `MAILBOX_SPLIT.md:295`'s claim about the port layer still holds, because `src/ports` is unchanged between pins. No tracked record carries a control-firmware size that the +600 octets would stale: `ctrl_image.py`'s table does not link lwSRP (`rv32_image/image_main.c:15,53`).
- **Commits.** Both commits have one-line messages with no trailers.
- **Cold-reviewer reconstruction.** The PR, the issue and the packet's HANDOFF.md are enough for another cold reviewer to reconstruct the change.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gitlink and lwSRP `9197193e..08ee86e8` src diff; `srp_latency.cpp:68-84`; independent decode of 4,186 MRPDUs from all firmware arms at base and head; capture and shipping input independence; #711 acceptance 1-5 | R597-1 | `49b437f445e34b558106c8799c1ffc0a5dc844cf` |
| RTL | CLEAN | diff file list; RTL-relevant gitlinks at base and head; builder-generated SRP CSR defaults; author's route-1x1 receipts | R597-1 | `49b437f445e34b558106c8799c1ffc0a5dc844cf` |
| Robustness | CLEAN | walk bounds and EndMark plant; `srp_mbx.c` capacity and self-parse; frame count, timing and split equality; mailbox access deltas | R597-1 | `49b437f445e34b558106c8799c1ffc0a5dc844cf` |
| Tests | CLEAN (S1 SUGGESTION only) | exact-head self-test (59 arms, 784 of 784 defects); base/head arm logs and tallies; base/head coverage tables; 8-probe walk matrix plus 2 lwSRP-plant probes | R597-1 | `49b437f445e34b558106c8799c1ffc0a5dc844cf` |
| Docs | CLEAN | 17 focused documentation gates; pin prose and permalinks; generated diagram and manifest; HANDOFF listing; commit format | R597-1 | `49b437f445e34b558106c8799c1ffc0a5dc844cf` |

## Real limits

- **Reference capture.** The reference end station's capture is not a public artifact in either repository. I compared the head layout with the layout lwSRP#17 publishes for that capture, not with the capture itself.
- **Not run by me:**
  - the saved-state capture re-measure, the shipping export, the Vivado route and `xvlog_gate.py`;
  - the Yosys and Verilator sweeps, `tsn_fuzz`, and the full `docs.yml` (17 of its commands were run);
  - act and any hosted job.

  For acceptance 3 and 5 I relied on static input independence, which I verified, plus the author's published receipts. These are inspected, not reproduced.
- **Planted defects at base.** I did not run the base planted-defect campaign. Base totals follow from the unchanged mutation tables.
- **Dump hook.** The decoded comparison covers every SRP-channel record the host mailbox model sends in the normal (non-mutant) arm runs. Build-only RV32 shapes emit no frames.
- **Shared host.** The host was shared with other heavy jobs (load about 28 on 16 cores). No result depended on timing.
- **Hosted checks.** A snapshot at exact head (`receipts/hosted-checks-snapshot.tsv`) shows some contexts complete and `docs-check`, `elaborate`, `firmware-unit` and four Verilator shards in progress. The `Physical gPTP` context was skipped, which is not hardware evidence. Physical calibration was NOT RUN. Hosted acceptance belongs to the manager.

## Pending manager duties

- Hosted exact-head gates (`rtl-fast`, `verilator-suites`, `yosys-portability`) and the act replica on the pushed head.
- Candidate-merge validation on live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5` (builder and native banks), with receipts linked on the PR.
- Acknowledging the two premise notes on #711 acceptance 3 and 5. The invariants are met. The premises "digest moves" and "documented digest" did not hold.
- The PR's unchecked Definition-of-Done items, including posting the self-test evidence in a PR comment.
- Merge authorization, post-merge containment, and closing #711 and moving it to Done.

## Reproduction

The scripts live under `scripts/`. Probe copies and builds are under `scratch/`, which is not published.

- `r597_env.sh`: environment for the scripts.
- `r597_dump_hook.py`: TX hook for probe copies.
- `r597_mrpdu.py`: `selftest`, and `compare <base dump> <head dump> <out.json>`.
- `r597_trailing.py`: classifies frames with trailing octets.
- `r597_walk_variants.py`: probe edits.
- `r597_latency_arm.py`: runs the `srp_latency` arm at IF=1 and IF=2.
- `r597_walk_matrix.sh`: the walk matrix.
- `r597_docs.sh`: the documentation gates, with `CHECKOUT` set to the exact-head checkout.

The exact-head checkout was verified clean after all probes:

- index equals the tree;
- no modified, untracked or ignored file;
- gitlinks exact, with `third_party/lwSRP` at `08ee86e8` and an unmodified `src/`.

See `receipts/exact-clone-integrity.txt`.

R597-1 FINISHED
