[A560]

## Contents

- **[Status](#status)** -- Candidate and validation.
- **[Linked Issue / roles](#linked-issue--roles)** -- Task and independent review.
- **[Description](#description)** -- Bare-metal SRP behavior.
- **[Round 6](#round-6)** -- Receive recovery and F2 composition.
- **[Round 7](#round-7)** -- Bound retained input and account for linked size.
- **[Round 8](#round-8)** -- Merge F3 and verify four-module composition.
- **[Round 9](#round-9)** -- Deliver ACMP bindings and strengthen access-bound evidence.
- **[Round 10](#round-10)** -- Registration feedback, permanent refusal parking and independent bound terms.
- **[Round 11](#round-11)** -- Ordered withdrawal feedback and current registration kind.
- **[Round 12](#round-12)** -- Callback contract compliance and discriminating feedback checks.
- **[Round 13](#round-13)** -- Failed-kind intra-PDU tests and named plants.
- **[Round 14](#round-14)** -- Trusted replay dependency manifest and refusal controls.
- **[Authoritative references](#authoritative-references)** -- Applicable contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Dependencies and environment.
- **[How to validate](#how-to-validate)** -- Commands and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Integration and release evidence.
- **[Definition of Done](#definition-of-done)** -- Remaining merge bar.

## Status

Round 14 candidate: `fe1cd0679f5028c749af7242c903a82ca2b3d692`; `665-f4-srp` -> `dev`.
Assigned Round 14 verification passes: all 87 final command receipts return 0.
The builder resource-calibration arm remains NOT RUN because its place report is absent.
Prior round evidence is retained below.
Controlled calibration and compiler-absent omissions are recorded below.
Corrected-head independent reviews and hosted acceptance remain pending.
Reviewers own closure and verdicts.

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
This participant recovery policy does not enlarge the 10 ms service budget.

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

## Round 9

The explicit composition now owns ACMP-to-SRP delivery. The ACMP callback
copies the latest request per sink; a separate poll uses the configured interface
and retries adapter refusals. Unbind and replacement supersede pending intent.
The original environment observes requests, while every callback remains serialized.
Attachment validates shape and poll capacity and refuses repeated wiring.

Real ACMP inputs test bind, receive/TX refusal and recovery, retained-input expiry,
unbind, replacement and interface/sink isolation at one and two interfaces.
Named mutations discriminate each path. Per-term SRP access measurements include
an actual transmitting poll and maximum-size RX/TX records.
The A0 source-count fixture controls the extra byte a relaxed guard would inspect;
the named assertion fails under AddressSanitizer without an overflow.

The three-module MAAP bound is attributed to `CTRL_APP_THREE_PASS_MAX`.
Composition and pool wording are corrected, and mutation claims name their scope.
Binding delivery adds zero mailbox accesses; the four-module bound remains
3,128 / 3,977 at IF=1/2. Fresh linked spans are 78,784 / 91,488 bytes for 1x1 at IF=1/2 and
93,488 / 120,960 for 8x8. Growth over Round 8 is 1,408 / 1,424 bytes:
544 bytes of static request/environment storage and 864 / 880 text bytes.
The reserved stack remains 8,192 bytes. The image reaches the binder through
ACMP; no separate forced binding entry remains. Earlier rounds above describe their respective heads.

The complete campaign catches 469 control plants, 129 SRP plants at IF=2,
28 additional IF=1 plants and two pin controls. Saved-state verification passes
435 tests across five shapes and catches all 109 plants. Coverage remains 100%
for all 22 files after unchanged exclusions. Builder, compiler audits, both
linked-image auditors, mailbox, differential, harness and documentation gates
all exit 0. Explicit unavailable-calibration and compiler-absent declarations
retain their stated scope; they are not hardware or compiled-firmware evidence.

## Round 10

The composition now returns per-sink, per-interface Talker registration to ACMP
in its deferred delivery poll. Advertise registers with `failed=false`, Failed
with `failed=true`, and withdrawal invokes unregistration. Registration stops
the no-Talker deadline; refreshed listeners remain SETTLED_RSV_OK beyond 10 s.
Delivery runs after SRP returns, preserving serialization and preventing reentry.
Repeated unchanged registration is not delivered again.

VID 0 and VID >= 4095 set readable `srp_requests[sink].parked`. An invalid
replacement first retires any accepted older binding, including a temporarily
refused unbind. Once retired, the parked request permits sleep until ACMP
replaces or withdraws it. Transient receive/output refusals retain their retries.
Header indentation and lifecycle prose are corrected; the test fixture names
service without the delivery poll.

Tests independently fund fixed poll reads, real send-callback cost, both
participant calls per interface, event-record words and two receive records.
The test-only transmit shim pads a real PDU to the maximum frame length while
preserving the production send callback. Reset and retained reception are
alternative branches whose measured increments form a conservative envelope;
the figures do not claim one simultaneous worst-case trace. All eight escaping
reviewer plant kinds are detected where non-equivalent. Replacing MBX_N_IF with
1 is equivalent at IF=1; the standing factor plant is detectable at both counts.

Nineteen new named plants cover feedback, parking and individual terms at both
interface counts. The complete campaign catches 469 control plants, 147 SRP
plants at IF=2, 46 additional IF=1 plants and two pin controls. Saved-state,
mailbox, builder/compiler, differential, image, sanitizer, harness and all
round-9 documentation gates pass. Delivery coverage is 75/75 lines and 60/60
branches; all 22 ratcheted files remain at 100% after unchanged exclusions.

Feedback adds a conservative 64 mailbox accesses per application pass, giving
3,192 / 4,041 at IF=1/2. SRP itself remains 1,596 / 2,366; the independently
measured poll envelope is 770 / 1,540. CPU work and external callbacks remain
excluded. Linked RAM spans are 79,536 / 92,240 for 1x1 and 94,224 / 121,712 for
8x8 at IF=1/2, increases of 736–752 bytes over Round 9. BSS is unchanged; the
parking flag fits existing padding. The stack reservation remains 8,192 bytes.
No mailbox, register-map, RTL, dependency pin, default build or shipping-image
change was required. Earlier round sections describe their respective heads.

## Round 11

A settled listener could retain an obsolete REGISTERING_FAILED flag.
A withdrawal followed by re-registration could disappear before composition service.
The adapter now retains each binding's first withdrawal and preceding kind.
Wire AttributeEvent boundaries preserve Lv/New inside one PDU.
Atomic JoinIn/JoinMt kind replacement remains continuous registration.
Expiry followed by receive also preserves the withdrawal.

The composition delivers registration, kind change and withdrawal in order.
`acmp_tk_kind_changed` updates only a SETTLED_RSV_OK view.
It does not replay Table 5.30's registration event or reprobe.
The interface extension follows the explicit round-11 decision on #665.
Pending replacement blocks obsolete feedback; accepted replacement retires it.
Identical stream identities follow the same supersession rule.

Standing tests cover both kinds, withdrawal sequences, isolation and supersession.
Transient refusal and pending-replacement guards have named discriminating plants.
Discovered withdrawal measures the funded timer path at IF=1/2.
Registration then withdrawal also measures both timer actions.
The feedback allowance becomes six accesses per sink, at most 96.
Four-module bounds become 3,224 / 4,073 accesses, excluding CPU work.
Updated timing tables preserve the target-calibration limitation.

Coverage writer and checker pass: all 22 files remain at 100%.
No coverage exclusion changed. Nine applicable reviewer probes pass at IF=1/2.
The mailbox suite and complete documentation bank also pass.
GCC and Clang plain/AddressSanitizer controls pass, including the named A0
plant and composed SRP suites at IF=1/2. Firmware and test objects are
instrumented; lwSRP library objects retain their ordinary harness flags.
The pinned RV32 compiler audit passes.
The complete control/SRP campaign, compiler-absence controls and builder bank
also pass. The campaign catches all 471 control plants, 160 SRP plants, two
pin controls and 59 selected SRP repeats at IF=1. The two new core plants
and thirteen new SRP plants are included. All four named round-10 plants
are caught at IF=1/2. The independent reviewer cases are 9/9 at each count.

| Shape / IF | Text | Read-only | Data | BSS | Reserved stack | RAM span | Delta round 10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1 TDM8 / 1 | 45392 | 2878 | 0 | 23440 | 8192 | 79904 | +368 |
| 1x1 TDM8 / 2 | 46676 | 2878 | 0 | 34808 | 8192 | 92576 | +336 |
| 8x8 / 1 | 45444 | 2878 | 0 | 38200 | 8192 | 94736 | +512 |
| 8x8 / 2 | 46820 | 2878 | 0 | 64328 | 8192 | 122240 | +528 |

The runtime archives are unchanged verified inputs from round 10.
Reserved stack does not establish a measured call-chain bound.


The builder receipt uses `803e8c3c9e7506c4f004d562437ae4f374fbad8e`.
Its sole difference from the final candidate is the ACMP mutation oracle's
entry number, outside builder inputs. Production, positive executable tests,
coverage and linked-image inputs are byte-identical. The complete firmware
campaign and final documentation checks use the final candidate.

## Authoritative references

- Issue #665 assignments 6030279477, 6038730087, 6040189958, 6045716528, 6047209532 and 6048644347; validation ruling 6036016117; R532-6 and R533-6 reports.
- Round 13 assignment 6051940062; R532-12 report 6051937140; R533-12 report 6051926602.
- `REQUIREMENTS.md` section 1; `docs/design/MAILBOX_SPLIT.md`; `docs/reference/FR_NFR.md`, NFR-SCOUT-02/03/08 and SRP hooks.
- Milan v1.2 4.2.7.2.2, 4.3.2, 5.5.2.7 and Table 4.3; IEEE 802.1Q-2018 Tables 10-3/10-4, 10.7.11, 35.1.2.2, 35.2.2.7.2 and 35.2.6.
- #608, #678, #679 and processor #134; `sw/firmware/ctrl/srp/README.md` records the selected processor differences.

## How to get into the same state

Use this checkout recipe. Set the
installation-specific disk-scratch and tool locations before exporting them:

```sh
git fetch origin 665-f4-srp
git switch --detach 154722e14781c7373f3229420b6e007f9bcf9835
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
inner build jobs. The public dependency is available at its recorded gitlink.

## How to validate

Round 13 runs the full ctrl campaign, coverage, sanitizer suites, named plants,
original reviewer probes and documentation gates. The broader lane commands
below also reproduce retained earlier-round evidence; their complete banks
were not rerun for this tests-only delta.

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
git diff --check 82a79638405c3365e4078da471be56758f8dd679 HEAD
```

The packet includes the exact reviewer inputs and portable sanitizer/probe
helpers. Copy these small files into disk scratch before running them from the
candidate checkout. For Round 13:

```sh
mkdir -p "$SCRATCH/round13-checks"
cp -R "$PACKET/round13-helpers/." "$SCRATCH/round13-checks/"
run_gate round13-probes python3 "$SCRATCH/round13-checks/review_probes.py"
run_gate round13-plants python3 "$SCRATCH/round13-checks/new_plants.py"
run_gate round13-sanitizers python3 "$SCRATCH/round13-checks/asan.py"
```

Earlier-round probes remain reproducible with their original helpers:

```sh
mkdir -p "$SCRATCH/review-checks"
cp -R "$PACKET/round12-helpers/." "$SCRATCH/review-checks/"
run_gate reviewer-probes python3 "$SCRATCH/review-checks/review_probes.py"
run_gate round11-probes python3 "$SCRATCH/review-checks/review11.py"
run_gate round12-probes python3 "$SCRATCH/review-checks/review12.py"
run_gate feedback-plants python3 "$SCRATCH/review-checks/new_plants.py"
run_gate feedback-bounds python3 "$SCRATCH/review-checks/check_bounds.py"
run_gate sanitizers python3 "$SCRATCH/review-checks/asan.py"
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
run_gate builder env MAKEFLAGS=-j8 python3 sw/builder/test_builder.py --require-rv32
run_gate compiler-pinned python3 sw/builder/test_firmware_compiler.py --sdk-destination "$SDK" --audit "$SCRATCH/rv32-pinned.jsonl"
cd "$SOURCE"
```

The full builder exits 0 with one explicit `NOT RUN` for an unavailable
pre-existing calibration report; no board access is part of this evidence.
The compiler-absent control intentionally reports unavailable compiler
instruments as `NOT RUN`; it does not claim compiled firmware evidence.
The builder's ordinary selector records its selected compiler. The additional
audit substitutes only that selector's executable with the verified CI-pinned
SDK and preserves all other arguments. This proves SDK compatibility, not
hosted selector adoption. Both linked-image
auditors and the firmware RV32 suites use the CI-pinned SDK above.

`ROUND13-GATES.md` expands the 75 documentation-bank commands and current
checks. Its JSON receipt binds exact commands to exit codes, durations and log
hashes. `ROUND13-PLANTS.json` maps the three new plants to the original review
replacements and their named failures at each interface count. `HANDOFF.md` contains the file:line change table, coverage, gates and
remaining integration work. Earlier round packets remain historical evidence.

Expected: every final gate exits 0; every plant fails its named observable;
all 22 portable files remain at 100% after inherited exclusions. Firmware
positives include both interface counts, five entity shapes, required target
builds and ADP/ACMP/SRP processor-wire differentials. The MAAP differential
also checks its 16 planted defects.

## Round 12

The MSRP receive filter previously entered its owning application through
`mrp_attr_visit`, contrary to the dependency callback contract. Talker indications
now copy matching registration kinds into static per-sink state. The next filter
observes the completed preceding event from those copies. Registrar visits run
outside callbacks, before/after receive, after ticks and in the poll.
Atomic kind replacement remains continuous; Lv followed by New retains withdrawal.
The lwSRP pin and contract remain unchanged.

Standing composition cases cover an identical-identity rebind after an undelivered
withdrawal, settled link down and down/up with re-registration before delivery,
and retention of the pre-withdrawal kind. The three named reviewer plants are
`p11-supersession-kind-stale`, `p11-reset-withdrawal-lost` and
`p11-postwithdrawal-kind-overwrite`. Additional single-PDU cases discriminate lost
Advertise/Failed indication copies and stale identity matching. Every case uses
mailbox ingress and the composition poll at IF=1/2.

Merged authorized dev `99e4eb6c14462aafa84bb1ac597fd241abc1a240` with two parents,
preserving SRP and the adopted processor pin in regenerated dependency documents.
The builder and compiler audits freeze `7b47f333ecde4af16e32ca95730f56c3c454d0eb`;
the final commit adds only the `p11-*` selection to the standing IF=1 mutation
pass. Their source inputs are unchanged; the full firmware campaign, coverage
and final documentation checks pass at the candidate above. Contract citations
name exact dependency lines and remain usable in source archives without
submodule contents.
The service-access bounds remain 3224/4073 at IF=1/2; the documentation separately
names per-event sink scans and boundary registrar visits for target calibration.

Coverage regeneration returns 0: all 22 portable files remain at 100% after
unchanged exclusions; the adapter covers 515/515 lines and 478/478 branches.
The complete firmware and saved-state campaigns, both compiler audits, sanitizers,
linked images, mailbox, differential and documentation gates return 0. The full
standing campaign catches each of the three `p11-*` plants at IF=1 and IF=2.
All 25 named feedback/review plants are caught at both counts, and all 13
independent probes pass at both counts. The complete composition suite passes
49 tests at each count. First-party sanitizer checks pass with both host compiler
families; dependency objects retain ordinary harness flags.

The Round 12 packet records all 114 final gate receipts, the mapping from the
113 Round 11 gates, exact commands and hashes, test-to-plant checks, coverage,
linked sizes and final source integrity. The initial archive-citation failure
and earlier passing runs before the standing-pass addition are preserved as
superseded evidence. No test or exclusion was weakened.

## Round 13

Three standing mailbox/composition cases cover Failed Lv then New in one PDU,
a Failed replacement withdrawn before Advertise returns in that PDU, and Failed
leaving while Advertise stays registered. The first two must reprobe; the third
retains the settled reservation and reports Advertise through GET_RX_STATE.
Each case confirms one received PDU and runs for both sinks at IF=1/2.

The three named plants are `feedback-leave-clears-advertise-only`,
`feedback-failed-indication-as-advertise` and `feedback-change-clears-both-kinds`.
They match q04, q13 and q06 and fail their named behavioral assertions at IF=1/2.
The existing `feedback-` selection includes all three in both standing passes.
The original three reviewer probe cases also pass at IF=1/2.

The mailbox design now cites lwSRP `9197193e47a6bb1c45a56d90a18c1784123aba44`.
Firmware and dependency contents are unchanged. R532-12-S1 remains an optional
production guard suggestion outside this tests-only delta; no new production
defect was demonstrated. Re-review of R532-12-F1 remains required.

Validation: the complete ctrl campaign catches 471 control plants, 169 SRP
plants at IF=2 and 68 at IF=1, plus both pin-refusal controls. Each new plant is
caught at each count in the full campaign and the focused run. The composition
suite passes 52 cases per count; the original reviewer probes pass three per
count. Fourteen sanitizer arms pass 140 tests per count. All 22 coverage files
remain at 100% lines/branches after unchanged exclusions. The 75-command docs
bank and five final docs/contract checks return zero.

Only two test files and the stale pin citation change. The follow-up commit
wraps one Python line with an identical syntax tree. No firmware, dependency,
coverage exclusion, RTL, register map or shipping-image input changes.

## Round 14

The trusted replay previously refused the candidate because its approved
submodule inventory omitted `third_party/lwSRP`. The manifest now includes the
exact existing name/path/HTTPS URL. Initialization derives four public pinned
dependencies, and the CI contract records five gitlinks including the inactive
SSH-only dependency.

The self-test uses an independent expected manifest, checks the initialization
arguments, and rejects removed, duplicate, extra or redirected lwSRP entries
and missing or extra gitlinks. Two standing controls plant candidate-controlled
trust and require their refusal checks to fail. A disposable source-mutation
audit catches eight named check/plant pairs covering five distinct faults,
including the original missing manifest entry. The unchanged baseline passes.

The committed runner's complete offline self-test passes in a disposable job.
The CI contract passes 1741 items and 2362 controls; all 75 documentation
commands and both source-archive checks return zero. The complete ctrl suite
passes 51 arms and 1252 checks, including required RV32 checks at IF=1/2.
The builder returns zero with one explicit resource-calibration omission: the
physical place report is absent. The separate CI-pinned SDK audit passes all
retained firmware checks with 2146 compiler invocations and zero omitted arms;
its negative controls pass too. All 87 final command receipts return zero.
Firmware coverage remains the unchanged Round 13 measurement: 22 files at
100% lines and branches after the same exclusions.
Only the runner manifest/self-tests and its enumerating CI contract change.

## Known limitations / out of scope

- F3 is now present. The composition owns SRP binding delivery, registration feedback, retries and permanent-refusal parking; live MAAP/stream updates and fabric licence output remain target integration.
- Timing remains a conditional host envelope. Original arrival/deadline budgets are retained; an 11 ms exhaustion or TX stall is rejected. Expired allocation refusal is discarded. Target scheduling and physical timing remain separate evidence.
- Linked RAM spans are 80368 / 93024 bytes for 1x1 at IF=1/2 and 95168 / 122672 for 8x8. They include alignment and an 8192-byte stack reservation, not a whole-call-chain bound. The fixtures are not booted images.
- Imported mailbox/RTL changes are assigned dev content. The feedback fix adds no RTL or register-map changes and does not change default placement or shipping-image inputs. Full processor-only SRP suites were not rerun; the firmware processor-wire differential was.
- The manager owns publication, fresh reviews, hosted gates, trusted workflow replication, candidate validation and containment. No hardware validation or merge approval is claimed.

Historical Round 9 resource note: service memory briefly peaked at 9053396992 bytes,
53396992 bytes above the 9000000000-byte working watermark. Flushing cached
products from completed tests reduced current use below 3 GB. The excursion
is recorded in the Round 9 handoff and integrity receipt; it is not a passed limit check. Round 10 peak service memory is 8766693376 bytes, below the watermark; disk stays above the 30 GB floor.

Round 11 peak service memory is 7723220992 bytes, below 9000000000;
the minimum sampled free disk space is 165787316224 bytes, above the 30 GB floor.

Round 12 peak service memory is 7083560960 bytes, below 9000000000;
minimum sampled free disk is 114278535168 bytes, above the 30 GB floor.

## Definition of Done

- [ ] Linked Issue acceptance criteria are fully satisfied after integration
- [x] New or changed behavior has self-checking tests
- [x] Assigned Round 10 verification passes
- [x] Assigned Round 11 verification passes
- [x] Assigned Round 12 verification passes
- [x] Assigned Round 13 verification passes
- [x] Assigned Round 14 verification passes, with the stated calibration omission
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
