[R310] NEGATIVE - exact head 29840136bb2d21bc0fbe92c7c533368f40837ff6

# R310-1 internal independent review: processor issue #113 / PR #115

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `29840136bb2d21bc0fbe92c7c533368f40837ff6`, tree `03bdccaf528aa94098544cf04f5598292fe855c8`
- Source base: `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b`. The diff is one commit, 15 files, +132/-12.
- Reviewer: [R310], internal role, cleared context, isolated detached clone. There were no source edits, commits, pushes or GitHub writes.
- Scope authorities: issue #113 body; the manager decision on issue #113 (comment 5821292534); the PR #115 body; Milan v1.2 consolidated (2023-11-30) §5.4.5.2 with Table 5.22; the repository's own contracts, which are 06 F06.13 and §7, 10 §6.4, 02 event catalog and REQ-NOT-003.

## Verdict summary

The RTL change is correct, minimal and conformant:
- A committed per-sink change of the accumulated-latency latch raises exactly one unsolicited GET_STREAM_INFO for that Stream Input, through the existing per-descriptor pending bit.
- An unchanged refresh raises none, and other sinks are not notified.
- Registration and FailureInformation changes on the same write coalesce into one push.
- The strobe reaches nothing but the notification OR.
- The top-level port list is byte-identical to the base.

I confirmed all of these with the head's own tests and with reviewer probes.

One MINOR finding is open. The new test's documented claim that its values "exercise the full comparison width" is false. A comparator truncated to bits [15:0], [30:0], [31:30] or [2:0] passes all 614 GI checks at the head. This leaves Tests and Docs unclean, so the verdict is NEGATIVE.

## Independent reconstruction

1. **Repository conventions.** The repository has no AGENTS.md or CONTRIBUTING.md. I used README.md and docs/README.md. They require single-source docs, `make check` doc gates and one self-checking suite per module.
2. **Frozen acceptance (issue #113 plus manager decision 5821292534).** The decision is to implement. The trigger is a change of the latched `acc_latency[sink]` after a Talker refresh, not the refresh itself. It must reuse the existing per-descriptor path with no new rate limit. The required tests are response-level:
   - a latency-only refresh gives exactly one unsolicited response carrying the new value;
   - an unchanged refresh gives none;
   - another sink is not notified;
   - a mutant that removes the trigger fails the first test.

   The docs to update are F06.13, the §06 live-event list and the compliance row. The PR must also report an area delta at the default shape and a parent consumer check.
3. **Clause, verified directly.** I checked the local Milan v1.2 consolidated PDF, sha256 `6bb902be…3bba8`, the same hash the author's provenance records. §5.4.5.2 (printed p. 62) says: "the unsolicited notifications listed in Table 5.22 shall be sent asynchronously of any command when the state of the entity changes". In Table 5.22 (printed p. 63), the GET_STREAM_INFO row reads "Sent when one of these pieces of information changes: … MSRP accumulated latency (Stream Input only) …". Only the GET_COUNTERS row carries the one-per-descriptor-per-second restriction, so adding no rate limit is correct. Receipt: `receipts/static-spec.txt`.
4. **Prior public review findings on PR #115.** At review time there were none: no reviews, no inline comments, and the only PR comment is the review-start notice. Nothing needs to be resolved or retained.

## Lens results

### Conformance: CLEAN
- The trigger matches Table 5.22's GET_STREAM_INFO row for Stream Inputs. The notification is raised on the change of the reported state, and a same-value refresh stays silent (§5.4.5.2: "when the state of the entity changes").
- No new rate limit is added (the limit applies to GET_COUNTERS only).
- The pushed value is the one a solicited read returns. The head's test checks this byte-exact, and my probes checked it again with 4 more single-bit transitions and 4 coalesced writes.
- MSRP_ACC_LAT_VALID is defined as "registering a matching talker attribute" (06 F06.13 flags paragraph). The pre-existing silent clear of the latch on A15/A8 therefore changes no valid reported field, and the ACMP status path notifies those transitions.

### RTL: CLEAN
- `hdl/srp/KL_srp_listener_fsm.sv:738`: `evt_tk_latency_chg_o[s] <= (lat_r[s] != evt_acc_latency_i)` sits in the same registering branch that re-latches `lat_r[s]`, so the pulse and the new latch land on the same edge. It defaults to 0 every cycle (`:711`) and at reset (`:701`), which makes it a one-cycle pulse. It uses one 32-bit comparator per sink, which is correct even when sinks entered registration at different times.
- `hdl/top/protocol_processor_top.sv:3146`: the pulse is ORed into `ntfy_stri_in_w[k]` with the same-index registration, unregistration and fail-change strobes, all registered on the same attribute write. `KL_aecp_notify.sv:758` sets one pending bit per sink, and the bit clears at emission pick (`:987`). The gather reads owners live after the pick, so a coalesced or same-edge update is reported with its new value.
- Fan-out: the strobe's only consumer is the stri OR. It is not read inside the listener FSM, so no applicant or declaration logic sees it, and it appears in no `evr_strobe_w` entry (`receipts/static-rtl.txt`).
- The `protocol_processor_top` port header is byte-identical at base and head (sha256 `e7470860…b5a9` for both). Every instantiation of `KL_srp_top` and `KL_srp_listener_fsm` is updated (the top and two testbench wrappers).
- Scoped lint with the pinned 5.050 simulator is clean: `KL_srp_listener_fsm`, `KL_srp_top` and `protocol_processor_top` all have rc 0 and zero warnings or errors (`receipts/scoped-lint.txt`).
- The area figures agree exactly with the published OOC reports:

  | Measure | Base | Head |
  |---|---:|---:|
  | Slice LUTs | 28,649 | 28,643 |
  | Registers | 31,095 | 31,123 |
  | RAMB36 / RAMB18 / DSP | 23 / 2 / 4 | 23 / 2 / 4 |
  | `KL_srp_listener_fsm` LUTs / registers | 1795 / 2328 | 1868 / 2336 |
  | WNS | -10.089 ns | -8.192 ns |

  All 45 HDL sha256 values in the OOC provenance match the exact-head blobs, and the OOC recipe is unchanged between base and head (`receipts/static-area.txt`). The README's attribution of the −6 total LUTs to remapping is consistent with the per-instance deltas.

### Robustness: CLEAN
- **Same-cycle ACMP settle or teardown (`ctl_acc_w`) with a registering hit on the same sink.** A pulse may fire while the latch ends at 0. This is at worst one extra notification that coalesces with the ACMP transition and carries the current state. It is benign, and the base already behaved this way for registration strobes.
- **Unregistration (rLv or leavetimer).** The latch is retained, as before this change. A later re-registration raises the registration strobe whatever the latency, so no change is lost.
- **Event landing on the pick cycle.** An event that lands on the same cycle as the pending-bit pick is absorbed by the live gather that follows. No stale value can be pushed, because the pulse and the latch update share an edge.
- **Behavioural checks (probe `golden-plus`, 763 checks, 0 failures):**
  - a latency-only change sends no Listener New on the wire, so the applicant is untouched;
  - a FailureInformation change together with a latency change gives exactly one push carrying both new values;
  - an Advertise→Failed swap and a Failed→Advertise swap, each with a changed latency, give exactly one push each;
  - nothing else is pushed.

### Tests: UNCLEAN (F1)
Real and adequate:
- The GI latency section drives real Talker JoinIn MRPDUs through the MAC/SRP path to two settled sinks, one Advertise and one Failed.
- It grades complete 94-byte responses byte-exact, including sequence IDs.
- It checks exact unsolicited counts, silence on an unchanged refresh, other-sink isolation and solicited agreement.
- It uses latch values with bit 31 set (0x81234567, 0xABCDEF01), zero and all ones.

My reruns (pinned simulator, exact-head archive, 8 CPUs):

| Run | Result |
|---|---|
| GI focused suite | 614 checks, 0 failures |
| `tb/pp_top` full suite | 2,074/2,074 |
| `tb/srp_top` | 1,531/1,531 |
| `tb/srp_stream_fsms` | 1,087/1,087 |

Mutants (`receipts/probes/probes.jsonl`):

| Mutant | Outcome |
|---|---|
| Author's trigger removal | Killed by `GI LATENCY-CHANGE: exactly one unsolicited response`: 4 exact-count failures reporting 0, 594 checks, 8 failures |
| Always pulse | Killed |
| Wrong sink (k^1) | Killed |
| Broadcast to all sinks | Killed |
| Comparator narrowed to [2:0], [15:0], [30:0] or [31:30] | **Survives**; see F1 |

### Docs: UNCLEAN (F1)
Accurate and complete for the required scope:
- F06.13 msrp_accumulated_latency row (`docs/architecture/06_aecp_engine.md:303`), with the clause;
- the §7 live-event list (`06_aecp_engine.md:735-745`), including the coalescing statement and the absence of a GET_COUNTERS-style limit;
- 10 §6.4, with the latch contract and two state-diagram self-edges;
- the 02 event catalog row `TK_LATENCY_CHANGE{sink}` (02:400), marked "wired directly and not routed";
- REQ-NOT-003 evidence text. The status stays P, which is correct because other triggers are still partial.

The `syn/ooc/README.md` area section matches the reports. Links (856), matrix (115 REQ / 17 GAP) and modmatrix (92 rows, 0 untested) gates pass locally. The hosted docs-gates job succeeded at the exact head.

The false coverage claim in `tb/pp_top/README.md:64-66` is F1.

## Findings

### F1: MINOR (Tests, Docs). The latency comparator's width is not covered, and the README claims it is
- **Where:** `tb/pp_top/gsi_internal.hpp:305-310`, the value sequence in `latency_changes()`. The claim is at `tb/pp_top/README.md:64-66`: "Distinct values, bit 31, zero and all ones exercise the full comparison width and sink selection". The PR body repeats it.
- **Evidence:**
  - The four latency transitions the head tests are 0x00012345→0x81234567, 0x00012345→0xABCDEF01, 0x81234567→0x00000000 and 0xABCDEF01→0xFFFFFFFF. Each differs in bits [2:0] and in bits [31:30] alike, so no bit is ever the only one that changes.
  - The comparator at `hdl/srp/KL_srp_listener_fsm.sv:738` is the new logic under test. Replaced with `lat_r[s][15:0] != evt_acc_latency_i[15:0]`, or with slices [30:0], [31:30] or [2:0], it still passes all 614 GI checks: probes `cmp-low16`, `cmp-no-bit31`, `cmp-high2` and `cmp-low3`, all "614 checks, 0 failures".
  - A 16-bit truncation is a realistic defect. It would miss any latency step that is a multiple of 65,536 ns, and then a registered controller keeps the old latency, which is exactly what issue #113 describes.
- **Impact:** the named-check test does not protect the property it claims to protect. A regression that narrows the comparison would ship undetected against Milan Table 5.22, and the committed test documentation overstates the coverage.
- **Required outcome:**
  - Add latency-only refreshes whose old and new values differ in a single high bit and in a single low bit. At minimum bit 31 alone, and preferably bit 0 and one middle bit such as bit 15.
  - Each must require exactly one unsolicited response.
  - Preferably retain a comparator-narrowing mutant in `gsi_mutants.py` with a named failing check.
  - Alternatively, reword `tb/pp_top/README.md:64-66` and the PR text so they claim only what is covered.
- **Verification:**
  - Probe `golden-plus` adds 0→0x80000000, 0xFFFFFFFF→0x7FFFFFFF, 0x80000000→0x80000001 and 0x7FFFFFFF→0x7FFF7FFF to the head's own `latency_refresh()`. It passes on the unmodified RTL: 763 checks, 0 failures.
  - With those additions, all four narrowed comparators fail `GI LATENCY-CHANGE: exactly one unsolicited response`: probes `cmp-*-plus`, verdict KILLED-BY-NAMED.
  - Rerun with `scripts/r310_probes.py` (see Reproduction).

### S1: SUGGESTION (Docs). Integrator-facing note
`docs/guides/integrator.md:290` and the GET_STREAM_INFO paragraph below it could say that the processor now notifies input latency changes from the raw `srp_acc_latency_o` latch. The integrator's STREAM_INPUT selector 3 answer must therefore be derived live from that port, plus the constant ingress delay, for the pushed value to be the new one. The current text implies this ("read live … like your own words") without tying it to the new trigger. This does not affect the verdict.

### S2: SUGGESTION (Docs). Scope of "a write that changes this sink's latch"
`docs/architecture/10_srp_engine.md:391-398` could add that the A15/A8 clear of `acc_latency[sink]` raises no latency strobe. That transition is reported by the ACMP status notification, and MSRP_ACC_LAT_VALID is 0 once unregistered. This does not affect the verdict.

### S3: SUGGESTION (RTL, area). Optional comparator sharing
The FailureInformation detector already uses one comparator on the lowest hit sink, justified by all candidates sharing a registration lineage. The same argument would let the latency change use one 32-bit comparator instead of eight, with MT-state sinks covered by the registration strobe. The current +73 LUTs is small, so this is optional.

## Reviewer ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan v1.2 §5.4.5.2 and Table 5.22 (printed pp. 62-63, local PDF sha256 verified); issue #113 plus decision 5821292534; F06.13 and §7; value path through gather selector 3 | R310-1 | 29840136bb2d21bc0fbe92c7c533368f40837ff6 |
| RTL | CLEAN | `KL_srp_listener_fsm.sv` (match, indication and registrar planes), `KL_srp_top.sv`, `protocol_processor_top.sv` (stri_events, gsi owner read, evr map, port header), `KL_aecp_notify.sv` (intake and pick clear); scoped lint; OOC util/util_hier/timing reports and provenance | R310-1 | 29840136bb2d21bc0fbe92c7c533368f40837ff6 |
| Robustness | CLEAN | Same-cycle ctl/registering interplay, rLv/leavetimer retention, pick-cycle event absorption, reset and pulse defaults; probe `golden-plus` (coalescing, wire silence, isolation) | R310-1 | 29840136bb2d21bc0fbe92c7c533368f40837ff6 |
| Tests | UNCLEAN (F1) | `gsi_internal.hpp`, `sim_main.cpp` fold, `pp_top_wrap.sv`, `gsi_mutants.py`; GI 614 and pp_top 2,074 reruns; srp_top 1,531 and srp_stream_fsms 1,087 reruns; 14 reviewer probe variants | R310-1 | 29840136bb2d21bc0fbe92c7c533368f40837ff6 |
| Docs | UNCLEAN (F1) | 00 REQ-NOT-003, 02 catalog, 06 F06.13 and §7, 10 §6.4 plus diagram, `syn/ooc/README.md`, `tb/pp_top/README.md`, integrator guide; links, matrix and modmatrix gates; hosted docs-gates result | R310-1 | 29840136bb2d21bc0fbe92c7c533368f40837ff6 |

## Evidence consulted (public)
- The author evidence packet at `kebag-logic/milan-fpga@b0a26b65…/review-evidence/pp113-r1/author/`, specifically AREA.md, the area-base and area-head reports, `ooc-*.json`, `provenance.json`, PARENT-COMPARISON.md, `parent-comparison.json`, and the tails of the control and candidate consumer logs.
  - **Parent consumer:** 7/7 commands return rc 0 at both the control (processor a8f8ce81, parent 9947af73) and the candidate (processor 29840136, parent dd8b228b), on dev 573f0052. The consumer passes 371 checks with 0 failures at each pin. The same four front-end findings appear at both pins.
  - **Builder:** one historical resource-calibration arm is unrun at both pins because an input is missing. That is not hardware evidence.
  - I did not rerun the parent consumer check, per the review rules. I found no separate manager-bank receipts inside that tree, only the author subtree, so the manager's bank result is taken from the review brief.
- **Hosted checks at the exact head:** docs-gates, suites and portability all completed with success in two workflow runs, 6 of 6 executed jobs (`receipts/hosted-check-runs.txt`). No skipped contexts are listed. The manager owns hosted/act acceptance.

## Real limits
- I ran focused suites and probes only. I did not run the full PP, parent, gPTP, Yosys or builder banks, the OOC synthesis, Docker/act or hardware.
- I did not run the mermaid and wavedrom doc lints locally. The only diagram edit is two stateDiagram-v2 self-edges in 10 §6.4, and hosted docs-gates passed at the exact head.
- The area figures come from the author's published reports, which I cross-checked against the head blobs via provenance. I did not resynthesize.
- Physical calibration was NOT RUN. Field skips are not hardware proof. There is no routed-timing claim, and both OOC builds have negative slack.
- The probes build a disposable `git archive` of the exact head. The reviewer test additions are probes only and are not proposed patches.

## Pending manager duties
- The final current-dev candidate build and banks at the merge turn: source base a8f8ce81, live dev 573f0052.
- Hosted/act acceptance.
- The second independent review ([R311]).
- The parent re-pin as a separate lane after merge.
- Disposition of F1 in a new round.

## Reproduction
- `scripts/r310_probes.py --repo <clone> --commit 29840136bb2d21bc0fbe92c7c533368f40837ff6 --work <scratch> --out <dir> --verilator <verilator 5.050> --cpus 0-7 golden golden-plus trigger-removed always-pulse wrong-sink broadcast cmp-low3 cmp-high2 cmp-no-bit31 cmp-low16 cmp-low3-plus cmp-high2-plus cmp-no-bit31-plus cmp-low16-plus`. Each variant needs about one minute to build and run.
- `scripts/r310_static_checks.sh <clone> <copy of review-evidence/pp113-r1> <pdftotext -layout of Milan v1.2> <out>`
- **Clone integrity after all probes** (`receipts/clone-integrity.txt`): HEAD and tree are exact. There are no modified, untracked or ignored files. Index modes and blobs equal the HEAD tree, and worktree bytes equal the HEAD blobs. The repository has no submodule gitlinks.
- **Tool identity** (`receipts/tools.txt`): the pinned simulator reports 5.050 rev v5.050. The wrapper and wrapped-binary sha256 values are recorded there.

R310-1 FINISHED
