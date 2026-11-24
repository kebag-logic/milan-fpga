[R883] NEGATIVE - exact head 44c566399002db32bf8a6ad3ce719488d418bcb0

# R883-4: internal independent delta re-review, issue #884 / PR #966

Exact head `44c566399002db32bf8a6ad3ce719488d418bcb0`, tree `ec7081348db64e19247dc8ac7a4e1d2f327ae59c`
(`884-gptp-firmware` -> `dev-soft-core-optimisation`). Delta reviewed: `165476c7..44c56639`, five commits
(`17bd60c6`, `e48ff320`, `edd31d4d`, `7ad1e7df`, `44c56639`). The previously reviewed head `165476c7` met the bar
(R884-4 POSITIVE). The scope is the manager's ruling on #872 (issuecomment-7124686692, item 1): repair the coverage
gate with tests only and lower no recorded figure.

All five lenses applied. I finished my own pass over the diff before reading any prior public review finding.

**Why NEGATIVE:** one MINOR (F1, Tests) is open. One of the new AECP face tests covers the software-gPTP
AS_CAPABLE line for coverage, but it cannot fail when the line's mask is lost: the datapath's AS_CAPABLE bit
then leaks through under a firmware gPTP owner. Every other claim in the brief holds at this head. There are also
three RESIDUE items and one SUGGESTION.

## Verified claims (the brief's items 1 to 5)

| # | Claim | Result | Evidence |
|---|---|---|---|
| 1 | No product source changed | **Holds.** `git diff --stat 165476c7..44c56639` over `sw/firmware/ctrl/**/*.{c,h}`, `sw/firmware/ctrl_nvm`, `hdl`, `configs`, `third_party`, the processor submodules, `sw/mailbox` and `sw/litex` is empty. The ten changed paths are tests, test plumbing, the ratchet and two READMEs. No gitlink moved. | `receipts/delta-scope.log` |
| 2 | `fw_coverage --check` passes; no figure lowered | **Holds, at the exact head.** My own run gave `firmware coverage: PASS (42 files)`, rc 0. `aecp_face.c` is 229/229 lines and 204/204 branches. `mbx.c` is 384/384 and 202/202. `ctrl_plat.c` is 224/224 and 110/110 after exclusions, with the stale `gate()` row gone. `gptp.h` is 2/2 and 0/0. `gptp.c` is 665/704 and 346/437, which is 94.46 % and 79.18 %. The run parsed the final `gtest/README.md` exclusions, so the author's README-identity argument is superseded. The ratchet diff changes five rows: three rise and two are new. None falls. | `receipts/coverage-check.log`, `.rc`; ratchet rows in `receipts/delta-scope.log` |
| 3 | New AECP face tests and mailbox gPTP mutations kill planted defects | **Holds for the four declared plants. Two of ten extra plants escape.** At the head, unplanted, all four new tests run and pass (one and two interfaces). Each declared plant is caught on its own named test and words. Of the extras, eight are caught. Two escape: `x-face-datapath-capable-bit-kept` (**F1**) and `x-pub-gptp-every-interface-block-0` (**S1**; the two-interface closed loop catches that one). | `receipts/mutants-baseline.log`, `mutants-control.log`, `mutants-aecp.log`, `face-wide-probe.log`, `gptp-sim-planted.log` |
| 4 | The gPTP simulation honours `STACK_DIR`, has its pin prerequisite and is registered; both campaigns are classified | **Holds.** A supplied `STACK_DIR` reaches every compile's include path, and the default tree is not used (7 against 0 in the dry run). `stack-pin` accepts the pinned clone. It refuses an edited `include/adp.h` and another revision, and `build` stops before any object compiles. `ctrl_configs.py:139-141` registers `tb/verilator/gptp_sw/Makefile build` as a Verilator builder. `gptp_mutants.py` and `gptp_sw_mutants.py` are in `SUITES` (`ctrl_configs.py:337-340`). The author's Verilator boundary leg records `make -C tb/verilator/gptp_sw: exit 0`, five passing `tb/verilator/gptp_sw/Makefile` pin controls and `ctrl_boundary: PASS`. Its census reports `199 pin`, the README's figure. My full closed loop at the head (slave, master, flood) passes with the pinned 5.050. | `receipts/stack-pin-probe.log`, `gptp-sim-plain.log`; published `firmware-verilator-edd31.log:7,255-259`, `firmware-boundary-edd31.log:354,368` |
| 5 | Four firmware shards and the previously cancelled hosted jobs pass at this head | **Local evidence holds and transfers. Hosted evidence at this exact head does not exist yet.** All four shards ran at `17bd60c6` and returned rc 0. They catch 828 of 828 control plants, which include both new driver plants, and both new face plants. The diff `17bd60c6..44c56639` touches none of the firmware gate's inputs. `ctrl_configs.py` is named only in a docstring of `test_ctrl_firmware.py`, and neither README nor the gPTP Makefile is read by that gate. My serialisation of `ctrl_mutants.MUTANTS` at `17bd60c6` and at the head matches: 828 entries, sha256 `470f936c...4afd`, the new entry at index 783 in both. The boundary legs ran at `edd31d4d`; later commits change only the extracted table (identical) and `gtest/README.md`. Hosted runs at `44c56639` (`rtl-fast`, `rtl-full`, `elaborate`, `docs`) were still queued or in progress when this report was written, and no firmware job had reported. | published `fw-shard-{0..3}-final.log*`, `input-equivalence.json`; `receipts/table-identity.log`, `hosted-workflow-runs.tsv`, `hosted-check-runs.tsv` |

Launch heads in the packet: the gPTP simulation baseline ran at `ee9b42b1`, a predecessor that is not an ancestor
of the head and whose Makefile differs by one line. My own closed-loop run at the exact head replaces it. The
mutant campaign ran at `e48ff320`, whose Makefile is the head's.

## Findings

### R883-4-F1 | MINOR | Tests | `sw/firmware/ctrl/test/test_aecp.cpp:4647-4685` (with `:4433` and `sw/firmware/ctrl/aecp/aecp_face.c:212`) | The software-gPTP AVB test cannot catch the datapath's AS_CAPABLE bit leaking through

- **Authority/evidence:** `aecp_face.c:212` exists to replace bit 0 (AS_CAPABLE, IEEE 1722.1-2021 7.4.40.2) with
  the firmware owner's asCapable: `(out->flags & ~1u) | (as_capable ? 1u : 0u)`. The datapath's bit 0 is a live
  value, not a constant. `KL_ptp_clock_validity.sv:143` drives `GET_AVB_INFO flags[0]` from the active owner's
  asCapable, and the fabric owner stays in the split image until a later phase. The fixture's datapath answers
  flags `0x7a`, bit 0 clear (`test_aecp.cpp:4433`). So `capable ? 0x7b : 0x7a` (`:4675`) holds whether or not
  the mask is applied.
  - I planted `out->flags | (as_capable ? 1u : 0u)` (no mask). It escapes the new test. It also escapes the
    whole AECP app suite at one and two interfaces, the debug suite at two interfaces, and the platform boot at
    one and two interfaces, all rc 0 with no failure (`receipts/mutants-aecp.log`, `receipts/face-wide-probe.log`).
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect", and tests must not
    merely reproduce implementation assumptions. The test is new in this delta and was added to cover this exact
    line.
- **Impact:** a regression that drops the mask would go unseen. GET_AVB_INFO would then report AS_CAPABLE set
  while the firmware gPTP owner says the port is not asCapable, whenever the datapath's bit is set (fabric owner
  present, or a stale bit at a transition).
  - The product code at the head is correct, so this is a test-strength defect, not a behavioural one. I did not
    attribute it to Conformance or Robustness, because those lenses judge the implementation and it behaves
    correctly.
- **Required outcome:** in this test (or one beside it), make the datapath answer AS_CAPABLE set. For example,
  flags `0x7b` while the snapshot says not capable, and expect `0x7a`. Also cover the reverse case, datapath
  bit clear with snapshot capable. Add a planted row for the unmasked OR to `aecp_face_mutants.py`.
- **Verification:** at the fixed head, the new plant fails the named test on its own words in the AECP campaign.
  The existing two face plants are still caught, and coverage stays at 229/229 and 204/204.

### R883-4-R1 | RESIDUE | Docs | PR body "Coverage and local workflow repair" section; `sw/firmware/gtest/README.md:237-240` | The unmet 100 % target for `gptp.c` is not stated as owed

- Wording only. The README says "The floor does not change the target", and the PR body says "No recorded floor
  is lowered". Neither says that `gptp.c` misses Mark II's 100 % target, or that the gap must close before the
  optimisation-to-dev-soft-core PR (#872 ruling, item 1).
- **Exact fix (PR body):** after "...`gptp.c` at 665/704 lines and 346/437 branches.", add: "`gptp.c` is below
  Mark II's 100 % target. The recorded figure is a floor that must not fall, and the gap must close before the
  optimisation-to-`dev-soft-core` PR (#872)."
- **Exact fix (README):** in the same place, add: "the gap is owed before the optimisation line merges to
  `dev-soft-core` (#872)."

### R883-4-R2 | RESIDUE | Docs | `sw/firmware/ctrl/test/aecp_face_mutants.py:3-9` | Module docstring does not name its two new rows

- Wording only. The docstring lists GET_AS_PATH, AS_PATH_CHANGED and SET_STREAM_FORMAT. It omits the
  software-gPTP GET_AVB_INFO and GET_AS_PATH forwarding rows that this delta adds at `:25-31`.
- **Exact fix:** after "(#897; IEEE 1722.1-2021 7.4.41)", add: "; under a firmware gPTP owner (#884),
  GET_AVB_INFO's gPTP fields and AS_CAPABLE come from its snapshot while the link flags and SR class stay the
  datapath's (7.4.40), and GET_AS_PATH forwards the owner's answer and refusal with no window read".

### R883-4-R3 | RESIDUE | Docs | `sw/firmware/ctrl/test/test_unit_driver.cpp:157` | Field name differs from the contract

- Wording only. The comment says `valid[21]`, but the contract names that field `OK`
  (`sw/mailbox/mailbox.yaml`, TIMESTAMP word 1).
- **Exact fix:** change `valid[21]` to `ok[21]`.

### R883-4-S1 | SUGGESTION | Tests | `sw/firmware/ctrl/test/test_unit_driver.cpp:362-381` | "On its own interface" cannot be tested at one interface

- The unit arm builds the tracked contract (`MBX_N_IF 1u`). The loop therefore checks interface 0 only, and the
  needle's claim "on its own interface" cannot fail there. The same holds for `interface = flags % MBX_N_IF` at
  `:153`.
- I planted every interface's GPTP_STATE written into interface 0's block. The unit arm missed it (rc 0). The
  two-interface closed loop caught it: `SLAVE if1 the words the datapath takes are the snapshot's, its GEN last
  got=0 exp=4261412866` (`receipts/gptp-sim-planted.log`, rc 2). That loop runs in the `gptp_sw` suite.
- Optional: name that closed-loop check as a second kill for the publication row, or word the needle so it
  claims no interface-specific behaviour.

### Source-comment rule

I scanned the added lines of the delta and found no new lane label, lane name, review round, reviewer ID or
issue-comment ID. The existing `issuecomment` link at `sw/firmware/ctrl/README.md:426` predates the delta.

## Prior public findings at this head

The delta touches none of the artifacts these findings rest on: `gptp.c`, `gptp.h`, `KL_mbx_cdc.sv`,
`milan_datapath.sv`, `tb/verilator/milan_dp/Makefile`, `tb_cdc_pub.sv`, `test_builder.py`, `docs/`, `sw/litex/`.
`git diff --quiet 165476c7 HEAD -- docs sw/litex` holds.

| Finding | Status at `44c56639` | Evidence |
|---|---|---|
| R883-3-F1, MINOR, Docs (memory-ledger keys) | RESOLVED, retained | `docs/design/SPLIT_CONTROL_MEMORY.md:141-142` give `image_gptp` 1,104 B and 2,152 B, limits 59.0 and 64.0; file unchanged since `165476c7` |
| R883-3-F2, MINOR, Docs (plain-image identity claim) | RESOLVED, retained | `docs/design/GPTP_SOFTWARE.md:153-155` say plain images exclude the owner and the relearn changes both layouts (+8 B ROM); unchanged |
| R884-3-F1, MINOR, Docs | RESOLVED, retained | same rows as R883-3-F1 |
| R883-3-R1 / R884-3-R1, RESIDUE (source-comment IDs) | RETAINED on the residue checklist (#746) | no new instance in this delta |
| R883-1-F1 to F4, R883-2-F1 and F2, R884-1-F1 to F5, R884-2-F1 and F2 | RESOLVED at earlier heads, retained | resolutions recorded at R883-3 and R884-4; their artifacts are untouched by this delta |
| R883-1-S1 to S5, R883-2-S1 to S4 (SUGGESTION) | Unchanged (taken or retained as previously recorded) | their artifacts are untouched |

## Lens ledger (reviewer-owned)

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `coverage.ratchet` rows against the #872 ruling (item 1), by `receipts/coverage-check.log`. `test_unit_driver.cpp:145-177` against `mailbox.yaml` TIMESTAMP words 1 to 3 (SEQUENCE_ID[15:0], MSG_TYPE[19:16], EGRESS[20], OK[21], NS_LO, NS_HI). `test_unit_driver.cpp:362-382` against `mbx.h:122-126` (GPTP_STATE written last). `test_aecp.cpp:4647-4734` against `aecp_face.c:208-213,346-347` and `aecp_face.h:59-65`. No product behaviour changed (`receipts/delta-scope.log`). | R883-4 | `44c566399002db32bf8a6ad3ce719488d418bcb0` |
| RTL | CLEAN | No `hdl/` path in the delta (`receipts/delta-scope.log`). `tb/verilator/gptp_sw/Makefile`: the `RTL` list and `VFLAGS` are unchanged, and only `INC`, the object prerequisites and `stack-pin` changed. The closed loop builds and passes at the head with pinned Verilator 5.050 (`receipts/gptp-sim-plain.log`). | R883-4 | `44c566399002db32bf8a6ad3ce719488d418bcb0` |
| Robustness | CLEAN | `stack-pin` refuses an edited header and a moved revision, and the build stops first (`receipts/stack-pin-probe.log`). New tests exercise an invalid interface (`MBX_N_IF`, `~0u`) with no write, ring wrap, an all-ones reserved word-1 field, a silent datapath refusing the whole observation with no owner call, and the owner's path refusal with count untouched and no window read. All pass at the head (`receipts/mutants-baseline.log`). | R883-4 | `44c566399002db32bf8a6ad3ce719488d418bcb0` |
| Tests | **UNCLEAN (F1)** | `test_aecp.cpp:4647-4734`, `test_unit_driver.cpp:145-177,362-382`, `aecp_face_mutants.py:25-31`, `gptp_driver_mutants.py`, `ctrl_mutants.py:33,682`. Ten reviewer plants (`receipts/mutants-*.log`, `face-wide-probe.log`, `gptp-sim-*.log`). Table identity (`receipts/table-identity.log`). Shard receipts. Coverage at the head. | R883-4 | `44c566399002db32bf8a6ad3ce719488d418bcb0` |
| Docs | CLEAN (R1 to R3 are RESIDUE) | `sw/firmware/gtest/README.md:234-247`, whose 21 exclusions are parsed by the passing coverage run. `sw/firmware/ctrl/README.md:155-161`, where "four" Verilator builders matches `ctrl_configs.py:136-141`. `:253`, where 199 matches the boundary census figure control. `ctrl_configs.py:103-110,334-340`. Packet `PR-BODY.md` and the live PR body (identical apart from one blank line). | R883-4 | `44c566399002db32bf8a6ad3ce719488d418bcb0` |

## Real limits

- I ran no full firmware shard, boundary leg, builder, Yosys, LiteX or parent bank. Shard and boundary evidence
  is the author's published receipts (launch heads `17bd60c6` and `edd31d4d`), transferred to the head by the
  input analysis above, not re-executed.
- My mutant probes reuse the repository's own planting and grading functions on disposable copies. I graded the
  extra plants on any failure of the named test (empty needle), not on specific words.
- I did not run `fw_coverage --selftest`. That the ratchet refuses a drop below the `gptp.c` floor rests on the
  author's `coverage-selftest.log` and on the tool's documented `--check` semantics.
- Hosted contexts at `44c56639` were queued or in progress, with no firmware job reported, when this report was
  written. I make no hosted claim.
- I did not run Docker, act or any host runner. No physical calibration was run, and field skips are not hardware
  proof. No manager source bank exists at this head, and none is claimed or inferred.
- Two simulation logs had the pinned tool's host path replaced with `<PINNED_VERILATOR_IMAGE>`. Nothing else was
  edited.

## Pending manager duties

- Hosted acceptance at `44c56639`: `firmware-unit`, the four firmware shards, `firmware-boundary`,
  `firmware-verilator`, `verilator-suites` (including `gptp_sw`), `yosys-portability`, docs and elaborate, plus
  the act replica.
- The current-dev merge candidate (source base `59b09884`, live dev `e275d795`), with builder and native banks
  at the merge turn.
- F1 needs a fixing commit and a delta re-review.
- Carry R1 to R3 and the retained source-comment residue (#746) on the residue checklist.

## Clone state after probes

The clone holds HEAD `44c56639` and tree `ec708134`. `diff-index` and the worktree are clean, the index matches
`ls-tree` in mode, blob and path, and the status is empty, ignored files included (bytecode caches from the
runs were removed). The six gitlinks match HEAD (`efeb541a`, `1616fc8f`, `801ef228`, `08ee86e8`, `715589c1`,
`48ff7a7e`), and the initialised submodules are clean (`receipts/restore-check.log`). All probes worked on
copies under this packet's `scratch/`.

Probe scripts: `probe_mutants.py`, `probe_face_wide.py`, `probe_gptp_sim.sh`, `probe_stack_pin.sh`,
`probe_table_identity.py`.

R883-4 FINISHED
