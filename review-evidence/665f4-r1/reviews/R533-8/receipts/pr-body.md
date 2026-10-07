[A560]

## Contents

- **[Status](#status)** -- Candidate and validation.
- **[Linked Issue / roles](#linked-issue--roles)** -- Task and independent review.
- **[Description](#description)** -- Bare-metal SRP behavior.
- **[Round 6](#round-6)** -- Receive recovery and F2 composition.
- **[Round 7](#round-7)** -- Bound retained input and account for linked size.
- **[Round 8](#round-8)** -- Merge F3 and verify four-module composition.
- **[Authoritative references](#authoritative-references)** -- Applicable contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Dependencies and environment.
- **[How to validate](#how-to-validate)** -- Commands and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Integration and release evidence.
- **[Definition of Done](#definition-of-done)** -- Remaining merge bar.

## Status

Round 8 REVIEW READY at `a6e6916826448f81de2b779ca61a87a9f8c47278`;
`665-f4-srp` -> `dev`. This pushed merge joins Round 7
`f74b9403b330ce316eeec6f724846f16def98443` and assigned dev
`d8b355fe0f41d49dca6cae1cd8b3826e2edde364` with `--no-ff`.
All 102 final recorded invocations exit 0. Coverage is 100% across 22 files
under inherited exclusions. All 469 control plants, 108 SRP plants, six additional
IF=1 composition plants, two pin controls and 109 saved-state plants are detected.
The builder reports its absent calibration report as NOT RUN; the additional
pinned-SDK audit has zero NOT RUN and 2,146 actual firmware compilations.
R532-7 and R533-7 were positive at the Round 7 head; fresh review of this merge
is owed. Reviewers own finding closure and verdicts.

## Linked Issue / roles

Relates to #665.

Executor: `[A560]`.
Internal cleared-context reviewer: `[R532]`.
External reviewer: `[R533]`.
Reviewers own verdicts, finding closure and the lens ledger.

## Description

Provide per-interface MSRP and MVRP on the bare-metal mailbox using pinned lwSRP
and entity-sized static pools. Startup declares outputs, Class A Domain and its
VLAN. Bound sinks reconcile Listener declarations; licences follow admission,
registration and committed membership. Refused output and recoverable receive
allocation preserve ordered work. Firmware uses neither an OS nor a heap.

## Round 6

An accepted SRP withdrawal could be lost when lwSRP lacked propagation storage.
The adapter now retains the complete record and retries without another peer
packet. Interface, bytes and arrival time survive repeated refusal and partial
application. Later SRP input and bindings wait; link reset cancels only its own
record. Allocation refusals are counted separately from malformed input.
The unchanged R533 probe passes at IF=1/2, including withdrawal after recovery.
Removing retry fails its required active-state check.

Merged assigned dev `e21c1ca024d37ea188ad15b5c8f9c2dae18628df` with `--no-ff`, preserving F2 MAAP tests and coverage.
The explicit application and linked fixture compose ADP, MAAP and SRP with all
receive/event/tick enables. The debug arm explicitly restores assertions after
F2's shared release flag. Eleven receive, two composition and one added timing
test have twenty new named defect plants.

Pins public lwSRP main `9197193e47a6bb1c45a56d90a18c1784123aba44`, which includes merged PR #15 and its Applicant
note tests. The prior claim that no production adaptation was needed was wrong.
The obsolete timer-removal claim is corrected; future-version and atomic-invalid
PDU behavior has adapter regressions. No dependency source change is made here.

## Round 7

A valid over-capacity Domain record could retain itself indefinitely and block
later withdrawals on every interface. Continuing allocation refusal now expires
1000 ms after its original arrival, at the next eligible receive attempt.
Already-queued input gets no new window; failed participant recreation uses the
same deadline. Successful recovery wins over discard, preserving recoverable
cases. `rx_discarded` counts an expired record once, separately from received and
malformed input. Pending events, ticks and owed output still precede reception.
This local recovery policy does not enlarge the 10 ms service budget.

Six new tests cover real-pool over-capacity input, later-interface withdrawal and
binding progress, boundary recovery, original arrival, clock wrap, unavailable
participants and Domain floods. Twelve new defect plants are caught at IF=1/2.
The original eleven receive regressions and unchanged R532/R533 probes pass.
The README now says pending events and every valid Class A Domain value.

Twelve linked measurements use identical verified runtime inputs at the lane
base, Round 5 and this candidate. Linked spans and deltas in bytes:

| Shape / IF | Text | Read-only | BSS | Stack | RAM span | Delta lane base | Delta Round 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1x1 / 1 | 33560 | 2846 | 18072 | 8192 | 62688 | +43936 | +8096 |
| 1x1 / 2 | 34792 | 2846 | 29424 | 8192 | 75264 | +56016 | +9424 |
| 8x8 / 1 | 33500 | 2846 | 32824 | 8192 | 77376 | +58624 | +8096 |
| 8x8 / 2 | 34744 | 2846 | 58928 | 8192 | 104720 | +85472 | +9424 |

The Round 5 growth includes MAAP composition and its application state, plus
1528 BSS bytes for one shared retained receive record. Round 7 alone adds
112–128 span bytes and no BSS. `ROUND7-SIZE.md` records object/symbol attribution,
reproducible commands and the full twelve-link table; `ROUND7-SIZES.json` records
artifact hashes and sizes. The manager-corrected mailbox recipe below is retained.

## Round 8

F3's ADP, ACMP and MAAP composition and F4's SRP now coexist in the explicit
application. SRP attaches after compose/restore/open and before service. It
preserves ACMP's channel and interrupt, enables its own receive interrupt beside
ADP, MAAP and events, and shares the centisecond tick. ADP, ACMP and MAAP keep
their three disjoint runs of one-shot timer slots.

F3's U6/F6 suite also builds against all four modules at IF=1/2. It checks the
exact filter/IRQ masks, an idle wake caused solely by SRP, attachment order,
timers, full-ring progress and the combined pass bound. Six new plants remove
SRP IRQ/wakeup, lose ACMP's enable, add an unrelated IRQ, omit SRP's cost or
count shared event reads twice. Each runs at both interface counts. The complete
campaign retains 469 control/MAAP/ACMP plants and 108 SRP plants, plus two pin
controls and the six additional IF=1 runs.

`CTRL_APP_PASS_MAX` is 3,128 accesses at IF=1 and 3,977 at IF=2. The ACMP bound
already includes ADP; MAAP and SRP add their costs, with shared event reads
counted once. The updated mailbox design table states the conditional timing:
at 1 us/access only the IF=1 event envelope fits 10 ms. CPU work and external
callbacks are excluded, and the ACMP backlog counts do not bound SRP delivery.

R532-7-R1's README sentence now matches the header: “completes or expires.”
The optional R532-7-S1 clarification says `refused` counts attempts, including
retries. Coverage combines both lanes with their inherited exclusion rules; this merge
adds no new exception.

F3's `ctrl_image.py` auditor is retained unchanged, with its 33 negative controls.
F4's auditor is now `ctrl_srp_image.py`; its fixture retains ACMP as well as SRP.
Both shapes link with the pinned RV32 compiler. The inherited auditor includes
saved-state storage; the four-module fixture excludes it. These are separate
size profiles, not a combined shipping-image budget. Four-module measurements:

| Shape / IF | Text | Read-only | BSS | Stack | RAM span | Delta Round 7 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1x1 / 1 | 43400 | 2878 | 22888 | 8192 | 77376 | +14688 |
| 1x1 / 2 | 44724 | 2878 | 34248 | 8192 | 90064 | +14800 |
| 8x8 / 1 | 43352 | 2878 | 37640 | 8192 | 92080 | +14704 |
| 8x8 / 2 | 44704 | 2878 | 63752 | 8192 | 119536 | +14816 |

No new mailbox, register-map or RTL change was needed beyond importing assigned
dev. The dependency pin and all-fabric shipping configuration remain unchanged.
Earlier Round 6/7 results above describe those heads; Round 8 evidence supersedes
them for the current candidate.

## Authoritative references

- Issue #665 assignments 6030279477, 6038730087 6040189958 and 6045716528; validation ruling 6036016117; R532-6 and R533-6 reports.
- `REQUIREMENTS.md` section 1; `docs/design/MAILBOX_SPLIT.md`; `docs/reference/FR_NFR.md`, NFR-SCOUT-02/03/08 and SRP hooks.
- Milan v1.2 4.2.7.2.2, 4.3.2, 5.5.2.7 and Table 4.3; IEEE 802.1Q-2018 Tables 10-3/10-4, 10.7.11, 35.1.2.2, 35.2.2.7.2 and 35.2.6.
- #608, #678, #679 and processor #134; `sw/firmware/ctrl/srp/README.md` records the selected processor differences.

## How to get into the same state

After the manager publishes the new head, use this checkout recipe. Set the
installation-specific disk-scratch and tool locations before exporting them:

```sh
git fetch origin 665-f4-srp
git switch --detach a6e6916826448f81de2b779ca61a87a9f8c47278
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
export SOURCE SCRATCH SDK DOCS_ENV RUNTIME REVIEW_PACKET CGREEN PACKET PINNED_VERILATOR
mkdir -p "$SCRATCH"
export TMPDIR="$SCRATCH"
export PYTHONDONTWRITEBYTECODE=1
export PATH="$DOCS_ENV/bin:$PATH"
python3 scripts/ci_rv32_sdk.py --destination "$SDK"
export MILAN_RV32_CC="$SDK/bin/riscv32-buildroot-linux-gnu-gcc"
export VERILATOR="$PINNED_VERILATOR"
export VERILATOR_JOBS=2
```

Use HDL compiler release 5.050 and the CI-pinned ilp32d SDK, with the gate's
RV32I/ILP32 freestanding flags. lwSRP uses anonymous HTTPS. Keep products in disk
scratch; campaigns use four workers, with at most two HDL builds and eight
inner build jobs. The public dependency needs no local branch publication.

## How to validate

Use separate log/rc files for long jobs, and wait in foreground intervals under
nine minutes. `run_gate` below waits for completion and preserves the command's
exit code. All products belong in disk scratch.

```sh
run_gate() {
  label=$1
  shift
  setsid nohup sh -c '
    logfile=$1
    rcfile=$2
    shift 2
    "$@" >"$logfile" 2>&1
    result=$?
    printf "%s\n" "$result" >"$rcfile"
    exit "$result"
  ' sh "$SCRATCH/$label.log" "$SCRATCH/$label.rc" "$@" </dev/null >/dev/null 2>&1 &
  job=$!
  while kill -0 "$job" 2>/dev/null; do
    timeout 45 tail --pid="$job" -f /dev/null || :
  done
  wait "$job"
}
run_gate firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$SCRATCH/firmware"
run_gate nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4
run_gate coverage python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$SCRATCH/coverage-check"
run_gate maap-diff python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$SCRATCH/maap-diff"
run_gate f3-images python3 sw/firmware/ctrl/test/ctrl_image.py --out "$SCRATCH/f3-images"
run_gate image-controls python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32
for shape in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  for interfaces in 1 2; do
    run_gate "image-$shape-if$interfaces" python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$shape.yaml" --interfaces "$interfaces" --output "$SCRATCH/image-$shape-if$interfaces" --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
  done
done
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/mailbox/gen_mailbox.py --check
python3 scripts/docs_check.py
python3 scripts/docs_check.py --selftest
python3 scripts/check_doc_style.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 scripts/check_submodule_docs.py
python3 scripts/check_diagram_pngs.py
python3 scripts/check_em_dash.py --base d8b355fe0f41d49dca6cae1cd8b3826e2edde364
git diff --check f74b9403b330ce316eeec6f724846f16def98443 HEAD
```

The runtime archives and their provenance are recorded by the linked-size
receipts; rebuild them using `ctrl_image_runtime.py` when needed. They are not
bundled in the packet.

Run the mailbox gate from a committed tracked scratch export. The four-command
recipe now includes F3's NVM header directory. The compiler variable resolves to
release 5.050 with inner builds limited to eight workers. The outer invocation
below permits only one build at a time.

```sh
git archive --format=tar --output "$SCRATCH/mailbox-inputs.tar" HEAD tb/verilator/mbx tb/common hdl/milan/mailbox sw/firmware/ctrl sw/firmware/ctrl_nvm sw/mailbox
mkdir -p "$SCRATCH/mailbox"
tar -xf "$SCRATCH/mailbox-inputs.tar" -C "$SCRATCH/mailbox"
run_gate mailbox make -C "$SCRATCH/mailbox/tb/verilator/mbx" -j1 VERILATOR_JOBS=1 VERILATOR="$PINNED_VERILATOR"
```

The builder writes generated outputs below its checkout; isolate them in a
scratch worktree at the exact candidate, initialize its recorded dependencies,
and run the builder documentation steps and pinned-SDK compatibility audit there:

```sh
git worktree add --detach "$SCRATCH/builder-tree" HEAD
git -C "$SCRATCH/builder-tree" submodule update --init
cd "$SCRATCH/builder-tree"
run_gate compiler-controls python3 sw/builder/test_firmware_compiler.py --selftest
run_gate compiler-absent python3 sw/builder/test_firmware_compiler.py --absent --audit "$SCRATCH/rv32-absent.jsonl"
run_gate builder python3 sw/builder/test_builder.py --require-rv32
run_gate compiler-pinned python3 sw/builder/test_firmware_compiler.py --sdk-destination "$SDK" --audit "$SCRATCH/rv32-pinned.jsonl"
cd "$SOURCE"
```

The full builder exits 0 with one explicit `NOT RUN` for an unavailable
pre-existing calibration report; no board access is part of this evidence.
The compiler-absent control intentionally reports unavailable compiler
instruments as `NOT RUN`; it does not claim compiled firmware evidence.
The builder's ordinary selector records its selected compiler. The additional
audit substitutes only that selector's executable with the verified CI-pinned
SDK and preserves all other arguments. This proves local compatibility, not
hosted selector adoption. Both linked-image
auditors and the firmware RV32 suites use the CI-pinned SDK above.

`ROUND8-GATES.md` expands the 75 documentation-bank commands and remaining
checks. Its JSON receipt binds exact commands to exit codes, durations and log
hashes. `ROUND8-TESTS.md` maps the complete plant table to the failure each must
detect. `HANDOFF.md` contains the file:line change table, coverage, gates and
remaining integration work. Earlier round packets remain historical evidence.

Expected: every final gate exits 0; every plant fails its named observable;
all 22 portable files remain at 100% after inherited exclusions. Firmware
positives include both interface counts, five entity shapes, required target
builds and ADP/ACMP/SRP processor-wire differentials. The MAAP differential
also checks its 16 planted defects.

## Known limitations / out of scope

- F3 is now present. The integrator's ACMP environment still owns SRP binding-port delivery and retries; live MAAP/stream updates and fabric licence output remain target integration.
- Timing remains a conditional host envelope. Original arrival/deadline budgets are retained; an 11 ms exhaustion or TX stall is rejected. Expired allocation refusal is discarded. Target scheduling and physical timing remain separate evidence.
- Linked RAM spans are 77376 / 90064 bytes for 1x1 at IF=1/2 and 92080 / 119536 for 8x8. They include alignment and an 8192-byte stack reservation, not a whole-call-chain bound. The fixtures are not booted images.
- Imported F3 mailbox/RTL changes are assigned dev content. This round adds no further RTL or register-map changes and does not change default placement or shipping-image inputs. Full processor-only SRP suites were not rerun; the firmware processor-wire differential was.
- The manager owns publication, fresh reviews, hosted gates, trusted local replication, candidate validation and containment. No hardware validation or merge approval is claimed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are fully satisfied after integration
- [x] New or changed behavior has self-checking tests
- [x] Assigned Round 8 local verification passes
- [ ] Complete candidate and hosted verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive at the new head
- [ ] External review is positive at the new head
- [ ] Findings are fixed and re-reviewed at the new head
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

