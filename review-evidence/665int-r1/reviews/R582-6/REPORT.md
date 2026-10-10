[R582] POSITIVE - exact head 67c1285b3b28b12a3af4f3f3aae6e92befd5febb

# R582-6: internal cleared-context review of PR #704 (#665 F-INT PR 1)

Head `67c1285b3b28b12a3af4f3f3aae6e92befd5febb`, tree `dd07654c71dc292cd5055793bd038691f06fa1a0`, base of the lane's
own delta dev `554e61d2` (44 commits, 63 files; the assigned source base `7c1b52be` adds F5, already in dev). Round 7
answers assignment 6100024293 with five commits on `0a8f700f` (`a2e14de6`, `480e5fe9`, `cb63ff0a`, `49e59dee`,
`67c1285b`). No BLOCKER, MAJOR or MINOR is open. One RESIDUE (PR body) and three SUGGESTIONs are recorded. Every
finding of rounds 1 to 5 is resolved at this head (section 4).

## 1. Scope as reconstructed

- Issue #665 rules: default all-fabric placement, no shipping-image change, host-tested firmware, per-path service
  bounds, portable C11.
- Assignment 6087047553 and ruling 6088423771 split F-INT into two PRs. PR 1 is the publication block in the mailbox
  window (contract 2.2) and its RTL simulation with plants. It also carries the firmware writers, each before the
  response that promises its value, with ordering tests and three plants per writer. The all-fabric image must stay
  byte-identical, and the firmware size and mailbox area are measured.
- Rulings 6092086337 (round 3), 6094461419 (round 4), 6095125193 (round 4b), 6095903333 (round 5) and 6097292237
  (round 6) add the started level, the Talker declarations, the completeness census, and its netlist form.
- Round 7 (6100024293) is the acceptance under review:
  1. the census covers every shape the builder builds, with parameters taken from the builder, the cross-shape
     rule, and the plants S1, S2, S3, B and E;
  2. one plant per rule, with a standing mutation check;
  3. its own `rtl-fast` job, required by the aggregate, pinned by `ci_events.py`, at most 60 % of its timeout at
     the head, with a cold-cache estimate;
  4. pinned-tool refusal;
  5. the R583-5-R1 text.

## 2. Findings

### R582-6-R1 - RESIDUE - Docs, Conformance - PR #704 body (Status, Round 7 table row "Item 3", Known limitations)

- Authority/evidence: round-7 item 3 says "The PR body records the measured hosted figures at the head, not
  estimates". The PR body still reads "The hosted figures at this head are the manager's to report after the push"
  and "No hosted run of this head exists, since it is not pushed". The hosted run at this exact head exists:
  - `rtl-fast` run 38076540233, job `publication-census` 114284711008, warm Yosys cache;
  - the job ran 18:42:48 to 18:56:56Z, 14 min 08 s of its 45 (31 %);
  - the census step ran 13 min 54 s: `--check` in 105 s and the self-test in 727 s, at `--jobs 4`;
  - receipts: `receipts/hosted_rtl_fast_38076540233_jobs.tsv` and
    `receipts/hosted_publication_census_114284711008_excerpt.txt`.
- Impact: wording only. The measurement exists and meets the 60 % bar. No figure the body states is wrong, and no
  verdict, test or code depends on the text.
- Exact fix:
  - Round 7 table, row "Item 3": replace "The hosted figures at this head are the manager's to report after the
    push; none is estimated here" with "Hosted at `67c1285b` (run 38076540233, job 114284711008, warm Yosys
    cache): the job 14 min 08 s of its 45 (31 %), its census step 13 min 54 s (`--check` 105 s, the self-test
    727 s, at `--jobs 4`)".
  - Known limitations, the "Round 7 changes no RTL" bullet: replace "No hosted run of this head exists, since it is
    not pushed: the hosted figures of `publication-census` are the manager's to report." with "Hosted at this head,
    `publication-census` ran 14 min 08 s of its 45 (job 114284711008)."
  - Status: replace "No review of this head has run yet." with "R582-6 and R583-6 review this head.", and delete
    the bullet "The review of this head has not run."
- Verification: a diff of the PR body against job 114284711008's log.

### R582-6-S1 - SUGGESTION - RTL, Robustness, Tests - `sw/mailbox/publication_census.py:234-244,358-375`; `hdl/common/csr/milan_csr.sv:2309-2395,2547,2876-2979`

- The census stops a cone at two blackbox cells: `csr` (on a `CSR_READBACK` input) and `pp_shadow` (on a
  `PROCESSOR_FACE` input). Ruling 6097292237 item 2 sanctions this.
- What happens inside `milan_csr` is not checked. Probe CP1 (`scripts/census_probe.py`, receipt
  `receipts/census_probe_CP1.log`) plants `assign o_aaf_enable = aaf_ctrl[0] | i_lwsrp_status[0];` in
  `milan_csr.sv`. That edit carries the status read `pp_cd_srp_over_limit_w -> lwsrp_over_limit` onto the AAF talker
  enable, which is on the wire. The census accepts the planted copy with 0 findings.
- Nothing escapes today. I traced all eight `CSR_READBACK` inputs inside `milan_csr.sv`: each feeds only `live_mux`,
  the stream-window mux or the 0x800 snapshot, as the comment at `publication_census.py:234-236` says.
- Optional outcome, either:
  - a census rule that elaborates `milan_csr` and requires each `CSR_READBACK` input to reach only its bus read
    data (the same cone code, one more netlist); or
  - one line in the PR body's limits and the census docstring that the read-back face is trusted to stay read-back.

### R582-6-S2 - SUGGESTION - Conformance, Docs - `hdl/milan/milan_datapath.sv:1407,1948-1949,2008-2011,7167-7188`; `docs/design/MAILBOX_SPLIT.md:1030-1037`

- Decision 1 of ruling 6088423771 removes the parent `KL_maap` in the split placement.
- The datapath reads two of its outputs on the wire:
  - `maap_addr` and `maap_addr_valid` select `eff_aaf_dmac`, the AAF framer's `dest_mac_i`;
  - `maap_addr_valid` is a term of `aaf_gate`.
- These are not processor class-D outputs, so the census population (the `pp_shadow` class-D ports) and the block
  (`DA_GATE` is a validity bit, not an address) do not cover them. The ruling's list and the documents scope
  completeness to class-D, so PR 1 is consistent.
- The design page names the wrapper's other faces that PR 2 must connect, but not these two signals.
- Optional outcome: record, beside the AECP faces on the design page and in the PR's limits, that PR 2 must source
  the talker destination address and the MAAP gate term in the split build. Two routes exist: the CSR `AAF_DMAC`
  with `MAAP_CTRL.en` clear, or a block field.

### R582-6-S3 - SUGGESTION - RTL, Docs - `docs/design/MAILBOX_SPLIT.md:1043-1047`; `sw/litex/milan_soc.py:811,2550-2551`

- `KL_mbx` runs on the `sys` clock (`milan_soc.py:2551`). `milan_datapath` runs on the `milan` domain (`:811`).
- The page says a half-written stream_id never reaches the datapath because it takes `pub_sid_o` only while
  `pub_sid_valid_o` is set. That holds across the crossing only if PR 2 uses an approved CDC pattern in which
  `SID_LO`/`SID_HI` are quasi-static before the synchronised `SID_VALID` rises. The same applies to each field's
  ordering against the response.
- "Open items" mentions the tap's crossing in general, not the publication block's.
- Optional outcome: one sentence in "The publication block" stating the ports' clock domain and the crossing PR 2
  owes.

## 3. Lens results (exact head `67c1285b`)

```text
[R582] PASS Conformance - rulings 6088423771, 6092086337, 6094461419, 6095125193, 6095903333, 6097292237, 6100024293 items 1-5; sw/mailbox/census_elab.py:166-196,237-245; publication_census.py:568-594; census_rules.py; census_selftest.py; .github/workflows/rtl-fast.yml:244-303,370-390; scripts/ci_events.py:1259,2353-2378; sw/builder/endstation_builder.py:4950-4995 vs milan_soc.py:921-1096; hosted job 114284711008 (14 min 08 s of 45, 31 %); writer order in acmp.c:198-213 and its transmit/finish calls, maap_mbx.c:62, srp_mbx.c:64-83,188-189,259,349,651,736-743,822,831 - every round-7 item met; the cross-shape rule compares a read's classes of end, a reading made public in the PR body that keeps the per-shape off-wire rule and that I accept (manager to confirm); RESIDUE R582-6-R1 only
[R582] PASS RTL - hdl/milan/mailbox/KL_mbx.sv:59-72,159-176,271-321,351-358 (decode, field masks, sync reset, full-strobe write, holes and absent interfaces, read mux); KL_mbx_pkg.sv; sw/litex/milan_soc.py:2534-2571 (port widths); hdl/ unchanged since 4274a205 (git diff 4274a205..HEAD -- hdl empty); receipts/mbx_make.log (pinned Verilator 5.050: 402/447/32/404/449/389 checks, 0 failures, 6 of 6 quick plants); receipts/mbx_mutants_full.log (175 of 175) - no defect; SUGGESTIONs S1, S3
[R582] PASS Robustness - KL_mbx partial strobe, holes, sink past 16, interface past N_IF, reset (bench P1-P5 and their plants); mbx.c pub writers' range refusals; srp_mbx.c reset/destroy/owed-stop paths (receipts/fw_probe_owedstop.log: the owed-stop publish removed is caught at one and two interfaces); census refusal of unpinned tools (receipts/census_pins.log), of a shape header missing a file (census_elab.py:189-193), of builder errors (:171-175) - no defect; SUGGESTION S1
[R582] PASS Tests - receipts/census_check_selftest.log (6 shapes, 234 checks, 0 failures; 0 of 120 arms failed, R583-5 S1/S2/S3/R1/R2, R582-5 B/E and the four round-7 rule plants refused by their words; 0 of 31 rules unproven); hosted job 114284711008 (same); receipts/hosted_elaborate_114284598759_gate23m_excerpt.txt (gate 23m 5 elaborations, 3/3 cuts); receipts/hosted_firmware_unit_114284710904_excerpt.txt (506 of 506, PASS, coverage 30 files); receipts/fw_probe_control.log (12 SRP arms PASS); receipts/mbx_mutants_full.log (175 of 175) - each new test can fail for its defect
[R582] PASS Docs - docs/design/MAILBOX_SPLIT.md:802-1120 (shapes table checked against the census's bound parameters, 31 rules, 116+2 plants, 120 arms); docs/ARCHITECTURE_HW_SW_SPLIT.md:88-98,192; docs/testing/CI_WORKFLOWS.md:42-43,62-64,144-157 (matches rtl-fast.yml and ci_scope); tb/verilator/mbx/README.md:23-51 and Makefile:7-17,63-74; census docstrings; receipts/quick_gates.log (gen_mailbox --check/--crosscheck/--selftest, ci_events --check, check_py_idiom, module matrix, check_em_dash 0 findings over 679 lines, git diff --check: rc 0) - accurate; RESIDUE R582-6-R1 (PR body)
```

## 4. Prior public findings at this head

All of these were read after my own pass over the diff.

| Finding | At this head | Evidence |
|---|---|---|
| R582-1-F1 (MAJOR), R582-1-F2 = R583-1-F1, R582-1-F3, R583-1-F2, R583-1-F3 | Resolved | No contract, RTL, generator or writer source changed since `4274a205`. The mbx bench, the 175 RTL plants, hosted firmware-unit (506/506) and the SRP arms pass |
| R582-2-F1 = R583-2-F1 | Resolved, superseded by the netlist census | Population from the `pp_shadow` cell (`publication_census.py:451-485`); R582-2 and R583-2 forms are self-test plants, refused |
| R582-2-R1 (RESIDUE) | Resolved (applied) | `mbx_model.h:161-162` and `mbx_model.c:27` carry the exact fix text. R583-5's "retained" note quotes the fixed sentence, which the fix itself contains |
| R582-2-S1 = R583-2-S1 | Optional, not taken | `maap_mbx.c:62` defined at 16 sources (`mailbox.yaml` `sources: 16`) |
| R583-2-S2 (required) | Resolved | `srpcmp` arm in every gate run (hosted) |
| R582-3-F1 = R583-3-F1, R582-3-F2, R582-3-F3, R583-3-S1 | Resolved | Netlist cone; B13 with its plant; the adoption and failed-creation tests with their plants (hosted firmware-unit 506/506 and the SRP table) |
| R582-4-F1, R583-4-F1, R583-4-F2, R582-4-S1 | Resolved | Their forms are refused self-test plants (local and hosted logs); the `srpcmp` arm names its 5 controls and 18 plants |
| R582-5-F1 = R583-5-F1 (MINOR, one shape) | Resolved by option (a) | All six shapes elaborated with builder parameters; S1, S2, S3, arm B and arm E refused by their own words at shapes that build them |
| R583-5-F2 (MINOR, unplanted rules) | Resolved | 31 registered rules, a plant each; mutation check 0 of 31 unproven (local and hosted) |
| R582-5-F2 = R583-5-F3 (MINOR, budget) | Resolved | The round-6 row states the measured hosted figures (10 min 08 s; 24 min 36 s of 30). The census moved to its own job: 14 min 08 s of 45 at this head. The missing round-7 hosted record is R582-6-R1 |
| R582-5-S1 (pins) | Resolved | `census_elab.py:237-245`; `receipts/census_pins.log` |
| R583-5-R1 (RESIDUE) | Resolved (applied) | PR body round-3 table row "Item 3" carries the exact text |

## 5. Executed evidence

These commands ran in this clone and in disposable clones under the packet's `scratch/`. The tools were:

- sv2v v0.0.12, from the release zip, with its sha256 checked against the `rtl-fast.yml` pin;
- the host's Yosys 0.66;
- the pinned Verilator 5.050.

Tool identities are in `receipts/environment.txt`.

| Command | Result | Receipt |
|---|---|---|
| `publication_census.py --check --selftest --jobs 8` | rc 0; 6 shapes, 234 checks, 0 failures; 25 nets, 4 unread, 39 reads of 21; 0 of 120 arms failed; 0 of 31 rules unproven; 12 min 12 s wall, 1.2 GB peak per process | `census_check_selftest.log` |
| `publication_census.py --list --jobs 6` | rc 0; the 39 reads with their classes, the same in each shape | `census_list.log` |
| `census_probe.py` CP0 (control) / CP1 (CSR read-back routed to `o_aaf_enable`) | ACCEPTED / ACCEPTED (S1) | `census_probe_CP0.log`, `census_probe_CP1.log` |
| `census_elab.toolchain()`, host sv2v v0.0.13, then pinned | refused with both pins named / accepted | `census_pins.log` |
| `make -C tb/verilator/mbx` (pinned Verilator) | rc 0; 402, 447, 32, 404, 449, 389 checks, 0 failures; 6 of 6 plants | `mbx_make.log` |
| `tb/verilator/mbx/mutants.py --jobs 8` | rc 0; 175 of 175 caught | `mbx_mutants_full.log` |
| `fw_probe.py` control: the 12 SRP arms (6 suites, 1 and 2 interfaces) | PASS | `fw_probe_control.log` |
| `fw_probe.py` with the owed-stop `publish_licence(i)` removed (`srp_mbx.c:822`) | caught by `Srp.PubLicenceIsSetAndClearedBeforeEachChangeIsReported` at 1 and 2 interfaces; restored | `fw_probe_owedstop.log` |
| gen_mailbox `--check`/`--crosscheck`/`--selftest`, `ci_events --check`, `check_py_idiom`, module matrix, `check_em_dash`, `git diff --check` | rc 0 each | `quick_gates.log` |
| Hosted, exact head: rtl-fast 38076540233 (6 jobs + aggregate success), elaborate 38076540267 (gate 23m), docs 38076540254 | success | `hosted_*` |
| Clone integrity after probes | index (1280 entries, modes, blob ids), tree, worktree, submodule gitlinks and checkouts identical to the pre-review baseline; caches the review created removed | `clone_integrity.txt` |

## 6. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (R582-6-R1 RESIDUE; S2 optional) | rulings 6087047553 to 6100024293; census code and rules; rtl-fast.yml; ci_events.py; builder `datapath_params` and gate 23m; writer order in acmp/maap/srp adapters; hosted job 114284711008 | R582-6 | `67c1285b3b28b12a3af4f3f3aae6e92befd5febb` |
| RTL | CLEAN (S1, S3 optional) | `KL_mbx.sv`, `KL_mbx_pkg.sv`, `milan_soc.py:2534-2571`, `milan_csr.sv` read-back paths, `milan_datapath.sv` reads; mbx bench and 175 RTL plants | R582-6 | `67c1285b3b28b12a3af4f3f3aae6e92befd5febb` |
| Robustness | CLEAN (S1 optional) | block strobe/hole/range/reset paths; driver refusals; SRP reset, destroy and owed-stop; census tool, header and builder refusals | R582-6 | `67c1285b3b28b12a3af4f3f3aae6e92befd5febb` |
| Tests | CLEAN | census self-test (120 arms) and mutation check (31 rules); gate 23m and its 3 cuts; firmware plants (hosted 506/506, reviewer owed-stop plant); 175 RTL plants | R582-6 | `67c1285b3b28b12a3af4f3f3aae6e92befd5febb` |
| Docs | CLEAN (R582-6-R1 RESIDUE; S2, S3 optional) | `MAILBOX_SPLIT.md`, `ARCHITECTURE_HW_SW_SPLIT.md`, `CI_WORKFLOWS.md`, mbx README and Makefile, census docstrings, PR body; docs gates | R582-6 | `67c1285b3b28b12a3af4f3f3aae6e92befd5febb` |

## 7. Real limits

- No manager source bank ran at this head, and I claim none. The local census used the host's distribution build
  of Yosys 0.66. The hosted job used the tag build from cache, and both report `Yosys 0.66`.
- Not rerun locally:
  - the firmware gate in full (`test_ctrl_firmware.py --self-test`), the coverage ratchet, `test_ctrl_nvm.py` and
    the builder suite. For these I relied on hosted `firmware-unit` and `elaborate` at this head. Locally only the
    12 SRP arms and one plant ran;
  - the all-fabric export, the firmware image size, the out-of-context area and Vivado. Their inputs are unchanged
    since `4274a205`, and round 7 changes only tests, READMEs, census, builder function, CI and docs there.
- Hosted runs are `pull_request` runs whose head SHA is this head; GitHub builds its merge ref. `rtl-full` 38076540228
  was still in progress at review time: Verilator shard 1/5 was running, every other shard had succeeded, and
  physical gPTP was skipped. A skipped context is not hardware proof. Physical calibration was NOT RUN.
- The census's guarantee is bounded by its stated limits: the shapes the builder builds, `SYNTHESIS` only, a class-D
  face read from section headings, reads from outside the datapath unseen, and the trusted CSR and answer-face
  terminals (S1).

## 8. Pending manager duties

- Hosted and act acceptance at the exact head, including the `rtl-full` completion (`verilator-suites`,
  `yosys-portability`) and the round-7 60 % bar: 31 % measured, R582-6-R1.
- Validate the current-dev merge candidate (source base `7c1b52be`, live dev `f88df731`) with the builder and native
  banks, and link the receipts.
- Confirm the public reading that the cross-shape rule compares a read's classes of cone end, not each end's port
  (PR body, Round 7).
- Carry R582-6-R1 to the residue checklist. Decide whether S1, S2 or S3 are taken (optional).

R582-6 FINISHED
