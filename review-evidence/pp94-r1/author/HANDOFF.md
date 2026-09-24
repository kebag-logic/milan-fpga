[A245] Author handoff — issue #94

Head: `4f525eb55b310d6b9bc2f1a000254cb2dd483665`  
Branch: `94-desc-mem-guard`  
Base: `008edbbf486598ae237414273d75e385cf0e1a56`  
Workspace: `$LANES/pp94-desc-mem-guard`  
Date: 2026-09-24

## Scope and implementation

Implemented [the assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/94#issuecomment-5810666541).
`KL_aecp_desc_mem_guard` retains one accepted burst's debt until a consumed
`last` or `err`. While owed, request valid toward memory and ready toward the
store are both low; responses pass through unchanged. It has one synchronous
active-low hard reset and no watchdog, rollback input or software clear.

The guard is instantiated in `protocol_processor_top`, between the AECP engine's
exported descriptor-store master and `desc_mem_*`. Its `debt_o` is published as
`desc_mem_debt_o`, the documented D3 interface. The store's functional RTL and
watchdog are unchanged; its only edit is a banner explaining the integration.
The existing immediate error on the first locate after a fetch-response timeout
is preserved and explicitly exercised.

The memory must respond after request acceptance, end a burst on `last` or `err`
without sending more beats for it, and flush pre-reset work on hard reset.
A store-only or future rollback reset must never reset the guard.

Documentation updates cover architecture §07, the single-source status dictionary
F02.10, integrator §4.1, and the two existing descriptor-path diagrams. Both edited
SVGs were rendered and visually checked; [descriptor-fetch.png](descriptor-fetch.png)
and [rtl-dataflow.png](rtl-dataflow.png) preserve the inspection artifacts.

Source-list inventory: the hand-kept processor-top suite list and portability top
list include the new guard; the new guard suite and OOC script list it explicitly.
HDL lint, portability conversion and timer-map shape elaboration discover all RTL
files automatically, so their source lists include it without another literal
copy. The generated module matrix now covers 46 modules/packages with none untested.
The existing bare-store suite still tests the store directly.

## Reproduction first, before product RTL changes

Read the entire issue and assignment, repository documentation/house style and
store suite. No repository-local AGENTS.md or CONTRIBUTING file was present; the
supplied workspace instructions applied. The immutable T9 draft, guard prototype,
V23 stimulus/oracle and queued-memory model were fetched with git at
`c1ee27d81c4a1e98f9584e979b73a88acfe238b3` into a scratch directory under `/tmp`.
Only the designated evidence tree was extracted. That scratch repository and
extracted evidence have been deleted; see [evidence-read.txt](evidence-read.txt).

The first completed regression ran against the unmodified store with no guard.
[baseline-rtl.diff](baseline-rtl.diff) is empty, recorded before the run.
The FIFO accepted a new request while the timed-out STREAM_OUTPUT burst remained
owed. Its response was then served as STREAM_INPUT:

```text
third locate bytes: 00060000deadbeef cafef00d01234567
expected:           0005000011223344 5566778899aabbcc
FAIL: third locate late_beats_never_served: STREAM_INPUT received another burst's bytes
18 checks: 17 PASS, 1 FAIL
```

At the default 4,096-cycle watchdog: old request accepted at cycle 80; late first
beat at 6,080 and terminal at 6,083; third locate presented at 4,185. The unguarded
memory accepted one overlapping request. The guard held it for 1,895 cycles,
accepted no overlap, served its own bytes, then served another locate after drain.

Commands from the workspace (all foreground, never piped):

```sh
rtk proxy make -C tb/desc_mem_guard baseline
rtk proxy make -C tb/desc_mem_guard
rtk proxy python3 tb/desc_mem_guard/mutate.py --output $MANAGEMENT/2026-09-23/pp94-a245
```

The baseline is intentionally nonzero. The first build attempt exposed unused
wrapper pins; those were wired to explicit taps before the completed reproduction.
No product RTL was changed before the wrong-byte result.

## Mutation and acceptance table

| Build / case | Result | Evidence |
|---|---|---|
| Original store, guard absent | simulation rc 1 / make rc 2; 17 PASS, 1 FAIL; wrong STREAM_OUTPUT bytes | [baseline-late.log](baseline-late.log) |
| Guard, identical late scenario | rc 0; 18 PASS, 0 FAIL; correct complete STREAM_INPUT bytes and recovery | [guard-late.log](guard-late.log) |
| Guard, only both request holds deleted | simulation rc 1 / make rc 2; 17 PASS, 1 FAIL; same completed wrong-byte assertion | [mutant-no-hold.log](mutant-no-hold.log) |
| Mutation controller | rc 0 only because the exact completed assertion and wrong bytes were detected; build failures/crashes are refused | `tb/desc_mem_guard/mutate.py` |
| Full guard suite | rc 0; 77 PASS, 0 FAIL | [guard-suite.log](guard-suite.log) |
| Stuck burst after one nonterminal beat | five later locates all error; longest 4,102 cycles vs bound 4,160; debt stays set; no extra request accepted | [guard-suite.log](guard-suite.log) |
| Store-only reset / hard reset / terminal err without last | debt survives store-only reset, drains while store remains reset; hard reset clears it with queue flushed; terminal error permits recovery | [guard-suite.log](guard-suite.log) |
| Handshake cases | stalled request creates no debt; invalid or backpressured terminal cannot clear it; payload pass-through; hold remains through terminal cycle | [guard-suite.log](guard-suite.log) |
| Existing store suite | rc 0; 584 PASS, 0 FAIL | [full-simulation-bank.log](full-simulation-bank.log) |
| Product-top suite | rc 0; 1,454 PASS, 0 FAIL across both builds; A12 late response and A13 stuck burst checked through real MAC READ_DESCRIPTOR commands | [full-simulation-bank.log](full-simulation-bank.log) |

The mutant source is [KL_aecp_desc_mem_guard.no_hold.sv](KL_aecp_desc_mem_guard.no_hold.sv).
It is a separate source file; the product checkout was never mutated for the control.

## Out-of-context area

Used the repository's `syn/ooc` flow: the same synthesis mode, part,
clock and report commands as `ucpu_ooc.tcl`, with the guard itself as top and all
ports retained. Added the reproducible `syn/ooc/desc_mem_guard_ooc.tcl` entry point.

```sh
rtk proxy bash -c 'cd $MANAGEMENT/2026-09-23/pp94-a245/area && $WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin/vivado -mode batch -source $LANES/pp94-desc-mem-guard/syn/ooc/desc_mem_guard_ooc.tcl -nojournal -log ooc.log'
```

| Metric | T9 estimate | Measured |
|---|---:|---:|
| Slice LUTs | 5 | 4 |
| Flip-flops | 1 | 1 |
| RAM / DSP | — | 0 / 0 |

Synthesis rc 0, reference part `xc7a100tfgg484-2`, release 2026.1.
The mapped logic is two LUT2, one LUT4, one LUT5 and one FDRE.
[util.rpt](area/util.rpt), [util_hier.rpt](area/util_hier.rpt),
[timing.rpt](area/timing.rpt), [ooc.log](area/ooc.log).
Timing is OOC and has unconstrained I/O; no routed timing or hardware claim is made.

## Gate table

Read `.github/workflows/hdl.yml`, the repository's sole CI workflow. Every validation
command it invokes was run locally, foreground, with no pipeline around the gate.
`run_gate.py` captures each subprocess's exact return code and full output with a
7,200-second timeout; [gates.jsonl](gates.jsonl) records commands and timings.
The workflow's historical `refs/pull/13/head` fetch also completed with rc 0 before
the NVM figure gate ([fetch log](ci-history-fetch.log)).

| Gate command | rc | Result | Log |
|---|---:|---|---|
| `python3 scripts/check-links.py` | 0 | 840 links | [ci-links.log](ci-links.log) |
| `python3 scripts/check-matrix.py` | 0 | 115 REQ rows, 17 GAP findings | [ci-matrix.log](ci-matrix.log) |
| `python3 scripts/render-wavedrom.py --check` | 0 | 18 blocks | [ci-wavedrom.log](ci-wavedrom.log) |
| `make stale` | 0 | exports current | [ci-stale.log](ci-stale.log) |
| `./scripts/lint_hdl.sh` | 0 | every RTL module, including guard and processor top | [hdl-lint.log](hdl-lint.log) |
| `bash scripts/run_suites.sh` | 0 | 32 suites; 15,894 checks; zero failing | [full-simulation-bank.log](full-simulation-bank.log) |
| `python3 scripts/gen_matrix.py --check` | 0 | 46 modules/packages, zero untested | [ci-traceability.log](ci-traceability.log) |
| `make -C tb/nvm_port figures` | 0 | 46 builds; all measured figures agree | [nvm-figures.log](nvm-figures.log) |
| `./syn/yosys/run.sh` | 0 | all listed tops, including guard; engine Xilinx RAM inference assertions | [portability.log](portability.log) |
| `make check` | 0 | 41 Mermaid + 18 WaveDrom blocks; links, matrices, staleness | [docs-check.log](docs-check.log) |
| `git diff --cached --check` | 0 | no whitespace errors | [diff-check.log](diff-check.log) |

An initial documentation run caught two missing anchors; both were corrected and
all final gate records above are green. Local versions are recorded in
[versions.txt](versions.txt): the simulation release was 5.052 (the repository's
floor is 5.050; CI installs 5.050), conversion v0.0.13 and synthesis 0.66 for the
portability gate. No remote CI run was triggered.

## Deferred to the D3 lane

The D3 restore writer does not exist at this integration base. Holding restorable
owners while `debt_o` is set, deadline-to-CLOSED policy, the 5,000/16,000-cycle
rollback cases, stage-1-only/full-slot rollback cases and the early-owner-release
mutant remain in the D3 lane. This change publishes their debt interface; it does
not claim rollback implementation or validation.

## Delivery

One local commit, one-line subject, no body or trailers. The working tree is clean.
No push, PR creation/edit, merge, hardware work, additional checkout or delegation
was performed. No private transcripts or management files outside this output
directory were read. [PR-BODY.md](PR-BODY.md) is ready for the manager's PR action.
