STATUS: STOP: 64x64 two-hart firmware does not build. Updated 2026-11-24 12:46 CET.

# [A837] two-hart scale, round 1

#966 is locally review-ready at `44c566399002db32bf8a6ad3ce719488d418bcb0`. No push or PR edit was made.

## Source and measurement identity

The scale branch is `opt-hart2-a837-r1` in `/data-2/milan/lanes/opt-hart2`, head `fe009fa2c7741b8612bdbc74fe70909d57931503`, based on the #966 repair. It composes int4 `3f36b457`, A808’s scale ports, the interface-specific probe repair `fcad6d10`, tsn-c-stack `115df0bec6d45269979d4d7a9cebc4cd727b9fe1`, and lwSRP `0757869e6cd9af6ea4fd04824e3a501664698a39`. The scale-only transmit cap is 16 values and the attribute bucket count is 16. Zbb remains off.

The two 32x32 models were built at `368c2d1e9898e43849873bd242fba482924817f0`. Later edits affect self-tests, documentation and the native input manifest. The recorded source inputs and native executables remain byte-identical. The original manifest omitted the passive cost-observer header; the original manifests remain unchanged, and `scale-input-equivalence.json` supplies its build-head hash and compiler dependency evidence. The corrected builder refuses reuse without that header recorded.

The one-hart 32x32 ELF is byte-identical before and after the new observer/cache-selection changes: 196024 bytes, SHA-256 `2b05feba4c2c7ff44f0eda69dadf9dc882124b553ada835e7e93db9a0add1cc7`. This compares the composed scale baseline at `32d78e99` with `368c2d1e`; it does not assert identity across the earlier accepted fold and scale ports. Both two-hart cache arms use the same 211544-byte ELF, SHA-256 `c96b345a11fac7fb27aa656664c19c57a0b39e274c9e71292f761f7a12e9a553`.

## 32x32/2if: nine Arm A groups

Both harts run at 100 MHz. Hart 1 has 16 KiB instruction cache in both arms, with no data cache or 8 KiB data cache as named. Worst pass includes completed work passes and the maximum of idle-pass runs. THE SHARE is 2.0 ms (200000 cycles). These are Arm A measurements without staged firmware gPTP; its long-window charge is shown separately.

| Group | D$0 H0 ms | D$0 H1 ms | D$8 H0 ms | D$8 H1 ms | D$0 grade / strict | D$8 grade / strict |
|---|---:|---:|---:|---:|---:|---:|
| srp | 0.83224 | 0.53844 | 0.83225 | 0.40948 | 0 / 0 | 0 / 0 |
| backlog-owed | 0.81531 | 0.87266 | 0.81534 | 0.66448 | 0 / 1 | 0 / 1 |
| backlog-adp-refill | 0.81531 | 0.91832 | 0.81531 | 0.68439 | 0 / 0 | 0 / 0 |
| control | 0.37355 | 0.72704 | 0.37355 | 0.53609 | 0 / 0 | 0 / 0 |
| adp-link | 0.66434 | 0.72704 | 0.66437 | 0.53609 | 0 / 0 | 0 / 0 |
| acmp-noresp | 0.37355 | 0.79730 | 0.37355 | 0.78905 | 0 / 0 | 0 / 0 |
| maap | 0.37355 | 0.53607 | 0.37356 | 0.40948 | 1 / 1 | 1 / 1 |
| aecp | 0.37355 | 0.72704 | 0.37355 | 0.53609 | 0 / 0 | 0 / 0 |
| acmp-notk | 0.39648 | 0.79730 | 0.39648 | 0.78905 | 0 / 0 | 0 / 0 |

The original commands record budget and SHARE findings; their exit codes do not waive recorded findings. The strict grades additionally make those findings fail. Every finding and original command is retained in the receipts. The quoted budget messages give total measured latency: for example, 64.226 ms is compared with 20 ms, not an additional 64.226 ms beyond it.

32-d0: original matrix command rc 1; strict matrix rc 1. Work passes H0/H1 [3727, 8122]; idle passes [286410, 103320]; over-SHARE work passes plus idle runs [0, 0].

32-d0 nonzero grades / findings:

- backlog.owed.if0: 64.226 ms over its budget 20 ms
- backlog.owed_behind0.if0: 64.561 ms over its budget 20 ms
- backlog.owed_behind1.if0: 64.895 ms over its budget 20 ms
- backlog.owed_behind2.if0: 65.229 ms over its budget 20 ms
- backlog.owed_behind3.if0: 65.563 ms over its budget 20 ms
- backlog-owed.service.acmp.last.if0: 61.947 ms over its budget 20 ms
- backlog-owed.service.aecp.last.if1: 63.867 ms over its budget 20 ms
- maap: the periodic timer's run-out at 1159.100 ms (if1 MVRP): its owner's first frame or build 769.512 ms after the owner's transmit opportunity at 1159.100 ms, past THE TRANSMIT's 49 ms (late)
- maap: the periodic timer's run-out at 1159.127 ms (if1 MSRP): its owner's first frame or build 769.196 ms after the owner's transmit opportunity at 1159.127 ms, past THE TRANSMIT's 49 ms (late)

32-d8: original matrix command rc 1; strict matrix rc 1. Work passes H0/H1 [3720, 6441]; idle passes [285829, 143975]; over-SHARE work passes plus idle runs [0, 0].

32-d8 nonzero grades / findings:

- backlog.owed.if0: 63.503 ms over its budget 20 ms
- backlog.owed_behind0.if0: 63.762 ms over its budget 20 ms
- backlog.owed_behind1.if0: 64.022 ms over its budget 20 ms
- backlog.owed_behind2.if0: 64.286 ms over its budget 20 ms
- backlog.owed_behind3.if0: 64.549 ms over its budget 20 ms
- backlog-owed.service.acmp.last.if0: 61.656 ms over its budget 20 ms
- backlog-owed.service.aecp.last.if1: 63.227 ms over its budget 20 ms
- maap: a join interval of 180.928 ms (if1 MSRP), outside 181.0 to 239.0 ms
- maap: a join interval of 180.929 ms (if1 MVRP), outside 181.0 to 239.0 ms
- maap: the periodic timer's run-out at 1157.053 ms (if1 MVRP): its owner's first frame or build 749.885 ms after the owner's transmit opportunity at 1157.053 ms, past THE TRANSMIT's 49 ms (late)
- maap: the periodic timer's run-out at 1157.079 ms (if1 MSRP): its owner's first frame or build 749.569 ms after the owner's transmit opportunity at 1157.079 ms, past THE TRANSMIT's 49 ms (late)

The cached MAAP run also has two join intervals of 180.928 and 180.929 ms, below 181.0 ms; these remain unwaived. The MAAP periodic-opportunity findings are retained. In each cache arm the reported interface-1 timer expiries predate that interface’s link-up; first subsequent MSRP and MVRP builds start within 0.55 ms. The current grader retains LINK timestamps but drops LINK values. This is diagnostic context, not a protocol verdict or a bound waiver.

## Per-hart long-window load and gPTP placement

These are demand-model loads, not measured CPU occupancy or a closed worst-case proof. The inherited arrival-rate equations are evaluated using sampled two-hart costs where available; each sample maximum receives 5% and rounds up to 5 us. Inclusive polls can only proxy individual owed items. All transferred terms remain listed below. The generated 32x32 shape has 33 slots; the conservative per-interface sink count is 17 and it has 68 counter-bearing descriptors.

| Hart 1 D$ | gPTP charged to | H0 load | H1 load |
|---|---:|---:|---:|
| 32-d0 | 0 | 0.599170 | 0.397682 |
| 32-d0 | 1 | 0.594970 | 0.401882 |
| 32-d8 | 0 | 0.596170 | 0.390626 |
| 32-d8 | 1 | 0.591970 | 0.394826 |

The transferred charge is 0.0042 for both gPTP ports together, applied to each hart in turn. The #884 placement rule requires the 64x64 measured worst-pass comparison and load no greater than 0.70 on the selected hart. No placement decision is inferred from a 32x32 result alone.

Largest demand-model terms (fraction of one hart):

- 32-d0, H0: srp 0.246500, item.mrpdu 0.157579, builds 0.113789, item.reclaim 0.025526, ticks 0.022500, item.walk 0.013684.
- 32-d0, H1: item.aecp 0.078320, item.acmp 0.075200, rec.acmp 0.050000, timers 0.049138, notices 0.037400, steps 0.034333.
- 32-d8, H0: srp 0.246500, item.mrpdu 0.157579, builds 0.113789, item.reclaim 0.025526, ticks 0.019500, item.walk 0.013684.
- 32-d8, H1: item.aecp 0.078320, item.acmp 0.068150, rec.acmp 0.053000, timers 0.049132, notices 0.037400, steps 0.034333.

## Cost samples and unmeasured terms

Inclusive completed-call shares below divide total completed-call cycles by total simulated CPU cycles across the nine groups. Nested calls overlap and must not be summed as occupancy. Unfinished calls and tail-call paths are not complete samples.

- 32-d0, H0 inclusive top calls: srp_mbx:poll 27.92%, ctrl_loop:dispatch_ticks 2.33%, srp_mbx:build_mrpdu 0.17%, srp_mbx:receive 0.03%, srp_mbx:apply_receive 0.03%, srp_mbx:on_event 0.03%.
- 32-d0, H1 inclusive top calls: maap_mbx:poll 36.47%, ctrl_loop:round_of 5.64%, ctrl_app_aecp:deliver 5.00%, aecp_mbx:poll 3.77%, adp_mbx:on_poll 1.24%, acmp_mbx:on_poll 0.95%.
- 32-d8, H0 inclusive top calls: srp_mbx:poll 27.93%, ctrl_loop:dispatch_ticks 2.33%, srp_mbx:build_mrpdu 0.17%, srp_mbx:receive 0.03%, srp_mbx:apply_receive 0.03%, srp_mbx:on_event 0.03%.
- 32-d8, H1 inclusive top calls: maap_mbx:poll 31.33%, ctrl_loop:round_of 6.77%, ctrl_app_aecp:deliver 5.24%, aecp_mbx:poll 4.24%, adp_mbx:on_poll 1.51%, acmp_mbx:on_poll 0.71%.

MAAP’s poll refreshes demand by walking sources. The declaring bitmap-clearing loop has no demand bits in this Arm A invalid-destination fixture. ACMP bitmap scans are not separately attributed. These samples do not establish a Zbb benefit; Zbb stays off.

| Term | D$0 us / provenance | D$8 us / provenance |
|---|---|---|
| base | 570 / unmeasured transfer | 570 / unmeasured transfer |
| build | 10810 / unmeasured transfer | 10810 / unmeasured transfer |
| build_one | 875 / measured | 875 / measured |
| centisecond | 960 / unmeasured transfer | 960 / unmeasured transfer |
| event.ACMP | 170 / measured conservative proxy | 185 / measured conservative proxy |
| event.ADP | 70 / measured conservative proxy | 55 / measured conservative proxy |
| event.AECP | 20 / measured conservative proxy | 25 / measured conservative proxy |
| event.GM | 30 / unmeasured transfer | 30 / unmeasured transfer |
| event.MAAP | 220 / measured conservative proxy | 165 / measured conservative proxy |
| event.TICK | 45 / unmeasured transfer | 45 / unmeasured transfer |
| events_none | 20 / unmeasured transfer | 20 / unmeasured transfer |
| item.acmp | 160 / measured conservative proxy | 145 / measured conservative proxy |
| item.acmp_declined | 0 / unmeasured transfer | 0 / unmeasured transfer |
| item.aecp.notice | 350 / unmeasured transfer | 350 / unmeasured transfer |
| item.aecp.probe | 65 / unmeasured transfer | 65 / unmeasured transfer |
| item.aecp.response | 95 / measured conservative proxy | 80 / measured conservative proxy |
| item.mrpdu | 7485 / unmeasured transfer | 7485 / unmeasured transfer |
| item.reclaim | 25 / measured | 25 / measured |
| item.retained | 865 / unmeasured transfer | 865 / unmeasured transfer |
| item.walk | 65 / measured | 65 / measured |
| record.acmp | 250 / measured | 265 / measured |
| record.adp | 130 / measured | 155 / measured |
| record.aecp | 160 / measured | 145 / measured |
| record.maap | 180 / measured | 130 / measured |
| record.srp | 320 / measured | 320 / measured |
| step | 1030 / unmeasured transfer | 1030 / unmeasured transfer |

Every transferred model cost is marked in the table. The historical centisecond entry is replaced in the final per-hart tick term by measured dispatch maxima: H0/H1 180/5 us without D$ and 150/5 us with 8 KiB D$, each plus the transferred 45 us event overhead. Additional unmeasured assumptions and rates:

- send.* / take.*: 6.4 us from historical 1x1 cross-hart record; not remeasured at scale.
- hart0.steps: PHY 155 us per 125 ms, not staged at scale.
- gptp: 0.0042 per hart for both ports, transferred from gPTP lane; not staged by Arm A.
- ticks: event.TICK overhead transferred; each hart dispatch_ticks maximum measured where nonzero.
- notices: cold-round and notice costs from shape header; item.aecp.notice and item.aecp.probe remain historical transfers because their costs are not separately staged; long notice/declaring arms not staged.
- background: empty-pass base is not a long-window term in the inherited equations; report is demand model, not CPU occupancy.
- stream counts: derived from the generated shape; worst sinks/interface rounded up (17 for the 33-slot 32x32 image).
- unfinished calls: only completed entry-to-return calls contribute maxima; tail calls and unfinished calls are not complete samples. Counts are retained; this is sampled cost evidence, not a proof of WCET.
- 16-value cap: full-declaring chunk counts per JoinTime, and their build, reclaim, walk, owed-send and NOTICED rates, are not validated by these nondeclaring Arm A groups; inherited rates are retained explicitly.
- retained SRP retry: item.retained remains historical: normal apply_receive samples do not stage the refusal, pool-release and retry scheduling paths.
- inclusive overlap: sampled handlers and polls can already include cross-hart sends or redelivery; separate historical record charges are retained and can conservatively double-count that work, with no overlap deduction.
- cross-hart retries: queue-full retries beyond one send/take per admitted record are not separately measured or modeled.
- bus and cache interaction: handler samples include their observed waits; unstaged combinations and empty-loop overhead are not separately bounded.
- bitmap scans: MRP walk is observed; ACMP bitmap scan inside handlers is not separately attributed.
- scope: Arm A nine groups only; saved-state, PHY and live-Talker declarations are not measured here.

The JSON receipts retain every sampled function’s count, sum, maximum, unfinished count and source group, plus each modeled cost’s exact provenance. This analysis does not alter repository cost statements or test floors.

## Memory, controls and outstanding checks

At 32x32 both cache arms require 179804 bytes ROM, 169104 bytes hart-0 SRAM and 153760 bytes hart-1 private RAM. The latter stays at the ruled power-of-two allocation of 262144 bytes, leaving 108384 bytes padding. Firmware memories plus the cross-hart RAM account for 150.5 RAMB36-equivalent tiles; cores, caches, peripheral and datapath memories are excluded. No route or fit is claimed. The largest objects are the hart-0 arena (144832 bytes), hart-1 maps (67584) and hart-1 values (41465).

The dedicated scale suite passes 21/21, including second-core removal from recorded build identities at both scale points and rejection of missing hart-1 execution observations. Second-hart unit checks pass 26/26. The observer passes its clean control and catches removed return observations. Actual completed 32x32 SRP traces also pass clean and fail after deleting hart-1 observations in both cache arms: four checks, zero failures. This last plant removes observations, not a physical core.

The full harness self-test is NOT accepted: rc 1, one failing baseline check containing six imported scale-model conflicts. The mutation campaign is not run on that failed baseline. The old shape model caps slices at 1600 us while the imported scale ports state 1935 us; its retained build-both cost is 10810 us against two 1935-us build-one costs; its built-point and poll tables omit scale points. No guard is relaxed. The composed lane also fails the unchanged Python style ratchet. These open failures are separate from the completed #966 local gates.

## 64x64 and stop condition

The 64x64/2if two-hart firmware build at `fe009fa2c7741b8612bdbc74fe70909d57931503` failed during linking: `.hart1.bss` does not fit `hram`; the region overflows by 92064 bytes. The region is 262144 bytes, so the reported overflow implies a 354208-byte linked span. The image builder returned 2, its link step returned 1, and the foreground wrapper returned 1 after 6.781 s. No executable, native 64x64 run or 64x64 load result is claimed. The user’s explicit “if 64x64 does not build, report 32x32 and STOP” condition applies. No memory limit, layout or cache was changed to bypass it; no route was run.

No REBOOT implementation was made: item 2 did not complete its acceptance conditions. The requested acceptance-time filter ownership exception remains for a later authorized continuation.

## Reproduction and receipts

Exact launch arguments, heads, return codes and durations are in `receipts/scale/*.log.json`. The original native logs and models remain under `/data-2/milan/tmp/opt-a837/scale`; compact grades retain their raw-log hashes. `receipts/reproduce/scale_analysis.py` and `scale_strict_grades.py` generate the cost and strict-grade receipts. The original 32x32 manifests require the supplemental header evidence described above; they are not rewritten for reuse. `receipts/INDEX.md` indexes plain-text receipts smaller than 200 KB, with no compressed files.

No push, PR edit, board access or route occurred. The single results-only [A837 report](https://github.com/kebag-logic/milan-fpga/issues/872#issuecomment-7130585273) is published and verified; `PUBLICATION.md` records its body hash.
