[A265]

Closes #75

Status: REVIEW READY. Implementation, documentation, required gates, mutation controls, and area comparison complete. The commit is local only.

## Revision

- Branch: `75-slew-active`.
- Base: `e5dcea6e351abff18a27a00f8e345f3251bdbd8f`.
- Head: `49d23b20fcad15a3c03554476d8b8c9116b3b375`.
- Tree: `804cd0dae42b46a2a85656f6e49781687ba671e6`.
- Subject: `Export the PHC policy slew interval`.
- One commit, one-line subject, no body or trailers. Working tree and index clean.

## Authority

Read [issue #75 and its assignment](https://github.com/Mister-M-alt/FPGA-gPTP/issues/75#issuecomment-5816647338), [parent #545](https://github.com/kebag-logic/milan-fpga/issues/545), its [prior handoff](https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5816629893), and [the manager decision](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5816509317). Their full public bodies and comments are retained as `issue-75.json`, `issue-545.json`, and `issue-387.json`.

## Implementation and completion rule

`phc_slew_active_o` is a registered, synchronous policy level. A non-stepping pair outside ±100 ns starts or continues transient correction. Two consecutive consumed pairs inside that inclusive band complete it. Ordinary PI tracking inside the band stays inactive, including nonzero frequency trims.

The issue did not specify a settling tolerance, and the base had no completion state. The ±100 ns/two-pair definition is an explicit implementation choice for review, not a previously recorded owner threshold. An optional clarification was requested; no different preference was received. The 20 us/100 us step thresholds, PI arithmetic and ±200 ppm clamp are unchanged.

The generator publishes its verdict through PHC word 2. A nonzero verdict asserts before the affected addend. A zero verdict clears only with the replacement addend, covering the complete interval between pairs. Reset clears both the output and qualification independently of retained scratch.

- Missing Sync holds the applied rate and level; receipt timeout restarts qualification.
- Missing Follow_Up discards the pending pair and holds the level.
- asCapable loss holds the affected rate and level; qualification restarts.
- A grandmaster identity change holds the level and restarts qualification.
- A replacement step retains an existing level through the step, then clears it with the integral-only rate. A step alone never asserts it.
- Becoming grandmaster explicitly retires an active correction through PHC word 3: integral-only rate and level clear occur together.
- A consumer must reset its retained rate with the engine and align this level with the effective PHC rate, independently of publication commits.

The engine, generator, integration/development/test guides, interface check and engine harness are updated. The bench instantiation explicitly leaves the new output unconnected. No parent code was changed.

## Required gates

There are no tracked CI workflow files in this checkout. The root Makefile defines the full local gate. Its complete default run returns **0**, with no skipped suites. All gate invocations ran in the foreground, with output written directly to logs and return codes preserved. Commands and times are in `gates.tsv` and the named logs.

| Gate | Result | Evidence |
|---|---|---|
| Complete default gate | rc 0 | `all.log` |
| PHC interface contract | PASS | `all.log` |
| MicroCPU | 768/768 | `all.log` |
| Parser | 268/268 | `all.log` |
| Engine: ordinary, request-seeded, Sync-seeded images | 1532/1532 each | `engine-final.log`, `all.log` |
| Engine negative controls | 30/30 caught; positive control passes | `engine-mutation-proof.txt`, `all.log` |
| Adapters | 81/81; 4/4 mutants caught; positive control passes | `all.log` |
| Independent packet-generator cross-check | 288/288; 3/3 mutants caught; positive control passes | `all.log` |
| Bench timestamp-tag simulation | PASS, both tags carried | `all.log` |
| Engine and bench lint | rc 0 | `all.log` |
| Diagram check and self-test | PASS, 10 self-test arms | `all.log` |
| Documentation check and self-test | PASS, 10 self-test arms | `all.log` |
| Base and candidate OOC recipes | rc 0 each | `baseline-ooc.log`, `candidate-ooc-final.log` |
| Base-to-head whitespace check, clean tree/index | rc 0 | `final-verification.txt` |

The three new mutants fail their named checks:

| Mutant | Required failing check |
|---|---|
| Output tied low | `slew: policy decision starts at +101 ns` |
| Clear after the first in-band pair | `slew: first in-band pair cannot clear` |
| Clear before the replacement rate | `slew: no clear precedes the replacement rate` |

Directed tests cover both tracking-band boundaries, exactly 100 us, start before the affected rate, completion with its replacement, continuous between-pair coverage, ordinary nonzero-rate tracking, steps, reset, lost capability and recovery, missing Sync and Follow_Up, identity changes, and both directions of mastership transition. Real closed-loop jumps have one uninterrupted active interval each.

## ROM and area

All four tracked ROM images were regenerated by the repository generator and independently reproduced. Hashes are in `rom-sha256.txt`; no ROM-digest ledger exists here. The generator uses 1008 real words (1009 seeded) in the same 1024-word ROM. Shared legs use the formerly unused prefix; dispatch entries and ROM depth are unchanged.

Measurements use the repository OOC recipe, `xc7a100tfgg484-2`, 100 MHz, at the stated base and final source.

| Resource | Base | Candidate | Delta |
|---|---:|---:|---:|
| LUTs | 4773 | 4853 | +80 (+1.68%) |
| Registers | 3646 | 3652 | +6 |
| Memory LUTs | 466 | 466 | 0 |
| Block RAM tiles | 1.5 | 1.5 | 0 |
| DSPs | 4 | 4 | 0 |
| Post-synthesis WNS | +2.249 ns | +1.773 ns | -0.476 ns |

Raw base/candidate utilization and timing reports and `area.json` are included. This is OOC measurement, not routed or board evidence.

## Duration and downstream work

The manager decision's 0.5 s maximum is not supported by the unchanged PI loop. The existing integration contract already says 0.5 s or more. With a master 140 ppm fast, real ±90 us jumps hold the level for 6,138,826 and 3,833,378 cycles at 2 MHz: **3.069413 s and 1.916689 s**. Final offsets are 0 ns and -1 ns, with ordinary +140 ppm tracking continuing. There is no completion timer. Missing trustworthy measurements can hold an affected interval indefinitely.

The read-only parent consumer is `$LANES/545-crf-servo-slew/hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv`: `KL_gptp_engine` begins at **652**, `u_engine` at **655**, and PHC connections at **677–680**. Add `.phc_slew_active_o (phc_slew_active_o)` beside those connections, export the wrapper level, and carry it through the datapath to the CRF servo. Align it with the effective rate and staged sample; discard and count every partly overlapped window, including its tail after deassertion, while remaining LOCKED. The parent pin/connection and consumer validation belong to #545 and were not run here. Its instantiation file hash is unchanged in `parent-consumer-sha256.txt`.

No push, PR action, merge, delegation, parent edit, private transcript access, or hardware operation occurred. `PR-BODY.md` is ready for review. `candidate.patch`, source hashes, ROM hashes, gate logs and the packet manifest identify the complete local result.
