# Command results for the issue 419 round-3 proposal, revision b

Paths are relative to the checkout root; <CHECKOUT> in a recorded command stands for it.

## Source

- dev 36ee8a3714f511d4717513be28b590da26ce1e4e
- protocol-processor 8f2f58fb2cc26e3d37170744b83f9909786a3105
- gptp-processor c1b617435824929a790739ea8585c3fe1a328cc0
- third_party/verilog-axis 48ff7a7e2ef782cf778d47910cf85835c64b1bce
- tracked changes: none

## Session narrative, revision b (this record)

Revision b answers the contract review of pull request 470 at b6ae45a5 (one
NEGATIVE, one POSITIVE) and the manager direction of issue 419 comment
5743971020. Every command ran in the foreground from the checkout root with
rtk in front; compiling and simulating steps ran under taskset -c 96-127 with
at most 8 workers (run.py adds both to every command it spawns; the CPU list
is run.py's CPUS, 16-31 in the reviewed record).

What changed in the evidence sources: the prototype backend checks RELOAD
(a load flag armed by a re-base with no mutating operation in flight and
cleared by any mutating grant, accepted once per reset, refusal published at
PP_NVM_STAT[11], load pending at [3]); a mutating request in the arm's own
cycle is deferred; PP_NVM_STAT[22] is nvm_pend itself. The prototype writer
re-bases before it loads the window, repeats a refused load (at most four
times), publishes only after an accepted RELOAD, and re-attaches without a
reload when the backend reports no load pending (a writer restart without a
fabric reset). The harness gains cases R1, U4, U5, U6, U7 and W1, A11 now
waits for its WRITE's grant before the arm, and run.py gains the mutants R01,
R02, R03, M19, F07 and F08, the check pending_bit_is_status_bit_22 on every
run, and the rule that no check of any case may grade n/a on a prototype
build. The reviewed record's console logs are kept, unpublished, in
prior-session/round3-reviewed-console/.

| Step | Command | Exit | Result |
|---|---|---|---|
| 1 | remove build/, runs/, logs/, tmp/, results.* (clean state) | 0 | - |
| 2 | python3 -B proposal-evidence/run.py --jobs 8 --phase build | 1 | 30 s; refused: mutant M06's seam missed the grant line that revision b splits in two (console/revb-0-build-seam-failure.log). M06 re-seamed on the whole new line; every seam then checked to hit exactly once |
| 3 | clean state again, then python3 -B proposal-evidence/run.py --jobs 8 --phase build | 0 | 72 s, 37 builds |
| 4 | python3 -B proposal-evidence/run.py --jobs 8 --phase run --builds "prod-*,proto-*,mix-*" | 0 | 55 s, 150 runs |
| 5 | python3 -B proposal-evidence/run.py --jobs 8 --phase run --builds "mut-M*" | 0 | 321 s |
| 6 | python3 -B proposal-evidence/run.py --jobs 8 --phase run --builds "mut-R*,mut-F*,mut-G*,mut-A*" | 0 | 234 s; 1824 runs in all |
| 7 | python3 -B proposal-evidence/run.py --jobs 8 --phase grade | 0 | NO FINDINGS: every expectation holds |
| 8 | python3 -B proposal-evidence/make_command_results.py | 0 | this file |

The run phase was split in three so each foreground call stays inside the
session's command time limit; the split changes nothing a run sees (every
run is its own process and each build's dependent runs follow its own runs).

Stopped steps: NONE. No tool call or step was refused or stopped by an
automatic safety filter in this session. No compiler-callback or binary
instrumentation was used; the only source adaptations are run.py's counted
textual seams (the firmware's two CSR primitives and its three fences, the
single counted replacement of each mutant) and, in the host build of the
prototype writer only, an appended function that models a CPU-only reset (it
returns the writer's file-scope variables to their initial values and runs
the writer's boot again; run.py refuses to build it unless it names every
such variable).

## Session narrative, round 3 as reviewed (history)

Every command below ran in the foreground from the checkout root with rtk in
front; compiling and simulating steps also ran under taskset -c 16-31 with at
most 8 workers (run.py adds both to every command it spawns).

State found at the start: the previous session's results.txt and
results.json predated its own last edits to harness/cosim_cases.cpp and
run.py and its last build and run phases, and no grade followed them, so
they did not describe the sources on disk. They are kept unmodified in
proposal-evidence/prior-session/ (results.txt sha256
16fce8e6b916f9ee479bceeb18d3240fb24f33f3920725e9a1484b4fe90c4fdf). Two draft
files the prototype never included (control_section.svh,
ownership_section.svh) were moved from prototype/ to
prior-session/unused-drafts/, and the empty mutants/ directory was removed
(mutants are defined in run.py).

| Step | Command | Exit | Result |
|---|---|---|---|
| 1 | remove build/, runs/, logs/, tmp/, results.* (clean state) | 0 | - |
| 2 | python3 -B proposal-evidence/run.py --phase build --jobs 8 | 0 | 50 s |
| 3 | python3 -B proposal-evidence/run.py --phase run --jobs 8 | 0 | 1110 runs, 6 min 45 s |
| 4 | python3 -B proposal-evidence/run.py --phase grade --jobs 8 | 1 | DIFFERS from prior-session/results.txt: two findings, C1r deferred_until_certificate:0x21:port and C2r hold_bounded:0x21:port. Cause: the check selected the FIRST port ERASE of record 0x21, which is the base binding flushed before any capture, not the request made inside the hold. Resolved in run.py (held_op: the first request made while a capture is open and uncertified); the request inside the hold was deferred correctly (requested 8 cycles after the arm, granted after the certificate) |
| 5 | python3 -B proposal-evidence/run.py --phase grade --skip-area | 0 | no findings; mutant M06 now fails both real-port checks (the checks are live) |
| 6 | cases added in harness/cosim_cases.cpp and run.py: C2e (real port, erased span under a stale mask), a first gap case, mutants M18 (pending bit stuck) and F06 (ACK after a failed slot), convergence now requires the durable status reading | - | - |
| 7 | clean state, then run.py --phase build, --phase run, --phase grade | 0, 0, 0 | 1252 runs, no findings. The first gap case landed the ARM on the WRITE's request edge, so M02 survived it (B5 still killed M02) |
| 8 | the gap case split into C1a (ARM after ERASE done, on the WRITE request edge) and C1g (copy taken inside the ERASE-to-WRITE gap, ERASE granted before the arm, WRITE held) | - | - |
| 9 | clean state, then run.py --phase build, --phase run, --phase grade | 0, 0, 0 | FINAL: 1278 runs, no findings |
| 10 | M02's named killer changed from B5 to the real-port C1g in run.py; run.py --phase grade | 0 | no findings |
| 11 | the rejected composite-bit alternative added as build mut-A01_composite_durable_bit; run.py --phase build --builds 'mut-A01*', --phase run --builds 'mut-A01*', --phase grade | 0, 0, 0 | FINAL results.txt: 1326 runs, NO FINDINGS |
| 12 | python3 -B proposal-evidence/make_command_results.py | 0 | the reviewed record |

Stopped steps in that session: NONE.

## Final results (proposal-evidence/results.txt)

```
MUTANT A01_composite_durable_bit                killer E1_dyn_change_ack_then_second_change:pending_drives_no_commit@end -> fail; 3 failing checks
MUTANT F01_certificate_not_checked              killer C2_hold_expiry_then_erase_with_stale_mask:last_verified_kept@after:0x21 -> fail; 8 failing checks
MUTANT F02_copies_open_records                  killer B1_erase_error_full_span:last_verified_kept@end:0x20 -> fail; 18 failing checks
MUTANT F03_prefill_from_blank                   killer B1_erase_error_full_span:last_verified_kept@end:0x20 -> fail; 20 failing checks
MUTANT F04_ack_without_identity                 killer A1_stable_no_change:stable_no_churn -> fail; 53 failing checks
MUTANT F05_device_busy_gate_kept                killer B9_abandoned_write_stream:later_record_persists@abandoned:0x20 -> fail; 4 failing checks
MUTANT F06_ack_after_failed_slot                killer F2_reported_flash_failure:converged@end -> fail; 4 failing checks
MUTANT F07_reload_refusal_ignored               killer R1_reload_after_failed_erase:converged@end -> fail; 3 failing checks
MUTANT F08_restart_reloads_window               killer W1_writer_restart_reattaches:converged@end -> fail; 3 failing checks
MUTANT G01_pending_from_edge_detector           killer E1_dyn_change_ack_then_second_change:no_durable_claim_unmaterialized@end -> fail; 3 failing checks
MUTANT M01_open_at_erase_completion             killer B1_erase_error_full_span:last_verified_kept@end:0x20 -> fail; 8 failing checks
MUTANT M02_close_on_any_completion              killer C1g_real_port_copy_inside_erase_write_gap:never_torn_or_erased@after:0x21 -> fail; 8 failing checks
MUTANT M03_close_on_partial_write               killer B10_partial_write_never_closes:later_record_persists@end:0x21 -> fail; 2 failing checks
MUTANT M04_ack_ignores_identity                 killer A6_late_ack_while_new_capture_open:stale_identity_refused@stray -> fail; 3 failing checks
MUTANT M05_ack_retires_live_work                killer A2_write_between_verify_and_ack:ack_retires_only_slot@post_ack:0x20 -> fail; 11 failing checks
MUTANT M06_hold_does_not_defer                  killer C1_request_during_hold_is_deferred:deferred_until_certificate:0x21 -> fail; 10 failing checks
MUTANT M07_hold_never_expires                   killer C2_hold_expiry_then_erase_with_stale_mask:hold_bounded:0x21 -> fail; 8 failing checks
MUTANT M08_certificate_ignores_grant            killer C2_hold_expiry_then_erase_with_stale_mask:last_verified_kept@after:0x21 -> fail; 9 failing checks
MUTANT M09_second_arm_accepted                  killer C5_concurrent_arm_refused:concurrent_arm_refused@stray -> fail; 3 failing checks
MUTANT M10_release_forgets_work                 killer C2_hold_expiry_then_erase_with_stale_mask:later_record_persists@after:0x20 -> fail; 7 failing checks
MUTANT M11_dirty_from_bytes_not_close           killer A12_last_byte_before_arm_done_after:converged@end -> fail; 3 failing checks
MUTANT M12_alarm_not_revoking                   killer B1_erase_error_full_span:alarm_revokes@end -> fail; 9 failing checks
MUTANT M13_report_not_revoking                  killer F2_reported_flash_failure:failure_revokes -> fail; 4 failing checks
MUTANT M14_pending_bit_misses_producer          killer E1_dyn_change_ack_then_second_change:no_durable_claim_unmaterialized@end -> fail; 3 failing checks
MUTANT M15_pending_bit_misses_open_record       killer B5_erase_then_no_write_yet:no_durable_claim@gap -> fail; 8 failing checks
MUTANT M17_hold_expiry_voids_capture            killer C3_hold_expiry_without_producer:slow_copy_certifies -> fail; 3 failing checks
MUTANT M18_pending_bit_stuck                    killer A1_stable_no_change:converged@end -> fail; 28 failing checks
MUTANT M19_arm_edge_grant_not_deferred          killer U4_grant_request_on_arm_edge:arm_edge_request_deferred:0x20 -> fail; 4 failing checks
MUTANT R01_reload_ignores_inflight              killer U5_reload_refused_inflight_at_rebase:reload_refused_inflight_at_rebase@after:0x20 -> fail; 3 failing checks
MUTANT R02_reload_ignores_grant_since_rebase    killer R1_reload_after_failed_erase:last_verified_kept@end:0x20 -> fail; 7 failing checks
MUTANT R03_reload_not_once_per_reset            killer U6_reload_refused_after_boot:held_work_survives_post_boot_reload@reload -> fail; 2 failing checks
AREA tracked-1x1                        LUT=  782 LUTRAM=   0 LUT_TOT=  782 FF= 377 DSP=6 CARRY4=108
AREA tracked-1x1-nodsp                  LUT=  846 LUTRAM=   0 LUT_TOT=  846 FF= 377 DSP=0 CARRY4=134
AREA proto-1x1                          LUT= 1092 LUTRAM=   0 LUT_TOT= 1092 FF= 474 DSP=6 CARRY4=114
AREA proto-1x1-nodsp                    LUT= 1144 LUTRAM=   0 LUT_TOT= 1144 FF= 474 DSP=0 CARRY4=140
AREA tracked-8x8                        LUT=  787 LUTRAM= 128 LUT_TOT=  915 FF= 313 DSP=6 CARRY4=107
AREA tracked-8x8-nodsp                  LUT=  865 LUTRAM= 128 LUT_TOT=  993 FF= 313 DSP=0 CARRY4=133
AREA proto-8x8                          LUT= 1338 LUTRAM= 128 LUT_TOT= 1466 FF= 513 DSP=6 CARRY4=113
AREA proto-8x8-nodsp                    LUT= 1482 LUTRAM= 128 LUT_TOT= 1610 FF= 513 DSP=0 CARRY4=139
AREA tracked-1x1-page-bound-30          LUT=  772 LUTRAM=   0 LUT_TOT=  772 FF= 377 DSP=6 CARRY4=108
AREA tracked-1x1-page-bound-30-nodsp    LUT=  857 LUTRAM=   0 LUT_TOT=  857 FF= 377 DSP=0 CARRY4=134
FWSIZE tracked-1x1    text=9790 data=4 bss=52
FWSIZE proto-1x1      text=11890 data=4 bss=60
FWSIZE tracked-8x8    text=9906 data=4 bss=52
FWSIZE proto-8x8      text=12050 data=4 bss=60
REFUSAL old_writer_new_generator: exit 1 refused True
REFUSAL new_writer_old_generator: exit 1 refused True
NO FINDINGS: every expectation holds
```

## Graded checks

1824 case runs over 37 builds; 8743 graded checks: 8246 pass, 335 fail, 162 not expressible.

| Build class | pass | fail | n/a |
|---|---|---|---|
| mix-newfw-oldgw-1x1 | 2 | 2 | 0 |
| mutants and alternative | 7715 | 273 | 34 |
| prod-1x1 | 123 | 40 | 96 |
| prod-8x8 | 48 | 18 | 32 |
| proto-1x1 | 258 | 1 | 0 |
| proto-8x8 | 98 | 0 | 0 |
| proto-w2-1x1 | 2 | 1 | 0 |

Case-run exit codes: 1822 runs exit 0, 2 runs exit 3. A non-zero exit occurs only on a mutant (its harness aborts, graded as a failing check):

- mut-F04_ack_without_identity C1g_real_port_copy_inside_erase_write_gap: exit 3
- mut-M07_hold_never_expires U3_grant_on_certify_edge: exit 3

## Every recorded command, with its exit code

The case runs themselves are the 'runs' of results.json (exit codes above); every other command run.py spawned is below, from its manifests.

### manifest-build-2026-09-19T190037+0000.json: 113 commands, exit codes {0: 113}

| Exit | Wall s | Command |
|---|---|---|
| 0 | 0.374 | `python3 -B scripts/check_nvm_record_space.py --emit-record-table <CHECKOUT>/configs/endstation_ax7101_1x1_tdm8.yaml -o <CHECKOUT>/proposal-evidence/build/shape-1x1/records.txt` |
| 0 | 0.376 | `python3 -B scripts/check_nvm_record_space.py --emit-record-table <CHECKOUT>/configs/endstation_ax7101_8x8.yaml -o <CHECKOUT>/proposal-evidence/build/shape-8x8/records.txt` |
| 0 | 0.14 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/prod-1x1 -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/prod-1x1/host.o` |
| 0 | 0.141 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mix-newfw-oldgw-1x1 -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mix-newfw-oldgw-1x1/host.o` |
| 0 | 0.154 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/proto-1x1 -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/proto-1x1/host.o` |
| 0 | 0.171 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/proto-w2-1x1 -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/proto-w2-1x1/host.o` |
| 0 | 0.308 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/prod-1x1 -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/prod-1x1/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/prod-1x1/fw.o` |
| 0 | 0.36 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mix-newfw-oldgw-1x1 -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mix-newfw-oldgw-1x1/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mix-newfw-oldgw-1x1/fw.o` |
| 0 | 0.356 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/proto-1x1 -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/proto-1x1/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/proto-1x1/fw.o` |
| 0 | 0.352 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/proto-w2-1x1 -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/proto-w2-1x1/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/proto-w2-1x1/fw.o` |
| 0 | 6.26 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/prod-1x1/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -CFLAGS -std=c++17 -O2 -I<CHECKOUT>/proposal-evidence/harne ...` |
| 0 | 6.284 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mix-newfw-oldgw-1x1/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -CFLAGS -std=c++17 -O2 -I<CHECKOUT>/proposal-evi ...` |
| 0 | 0.141 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/prod-8x8 -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/prod-8x8/host.o` |
| 0 | 0.141 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/proto-8x8 -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/proto-8x8/host.o` |
| 0 | 6.495 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/proto-1x1/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS -std=c++17 -O2 -I<CH ...` |
| 0 | 6.508 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/proto-w2-1x1/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=2 -CFLAGS -std=c++17 -O2 -I< ...` |
| 0 | 0.14 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M01_open_at_erase_completion -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M01_open_ ...` |
| 0 | 0.316 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/prod-8x8 -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/prod-8x8/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/prod-8x8/fw.o` |
| 0 | 0.141 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M02_close_on_any_completion -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M02_close_ ...` |
| 0 | 0.361 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/proto-8x8 -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/proto-8x8/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/proto-8x8/fw.o` |
| 0 | 0.36 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M01_open_at_erase_completion -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M01_open_at_erase_completion/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M01_open_at_erase_completion/fw.o` |
| 0 | 0.357 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M02_close_on_any_completion -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M02_close_on_any_completion/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M02_close_on_any_completion/fw.o` |
| 0 | 6.301 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/prod-8x8/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique -GN_STREAM_IN_P=9 -GN_STREAM_OUT_P=9 -GN_SPORT_IN_P=8 -GN_SPORT_OUT_P=8 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=99 -GCLK_HZ_P=1000000 -CFLAGS -std=c++17 -O2 -I<CHECKOUT>/proposal-evidence/harne ...` |
| 0 | 0.146 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M03_close_on_partial_write -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M03_close_o ...` |
| 0 | 0.367 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M03_close_on_partial_write -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M03_close_on_partial_write/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M03_close_on_partial_write/fw.o` |
| 0 | 6.498 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M02_close_on_any_completion/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAG ...` |
| 0 | 6.535 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M01_open_at_erase_completion/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLA ...` |
| 0 | 0.139 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M04_ack_ignores_identity -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M04_ack_ignor ...` |
| 0 | 0.135 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M05_ack_retires_live_work -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M05_ack_reti ...` |
| 0 | 6.904 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/proto-8x8/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=9 -GN_STREAM_OUT_P=9 -GN_SPORT_IN_P=8 -GN_SPORT_OUT_P=8 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=99 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS -std=c++17 -O2 -I<CH ...` |
| 0 | 0.139 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M06_hold_does_not_defer -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M06_hold_does_ ...` |
| 0 | 0.352 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M04_ack_ignores_identity -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M04_ack_ignores_identity/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M04_ack_ignores_identity/fw.o` |
| 0 | 0.352 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M05_ack_retires_live_work -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M05_ack_retires_live_work/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M05_ack_retires_live_work/fw.o` |
| 0 | 0.357 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M06_hold_does_not_defer -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M06_hold_does_not_defer/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M06_hold_does_not_defer/fw.o` |
| 0 | 6.516 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M03_close_on_partial_write/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS ...` |
| 0 | 0.139 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M07_hold_never_expires -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M07_hold_never_ ...` |
| 0 | 0.368 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M07_hold_never_expires -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M07_hold_never_expires/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M07_hold_never_expires/fw.o` |
| 0 | 6.499 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M05_ack_retires_live_work/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS  ...` |
| 0 | 6.513 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M04_ack_ignores_identity/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS - ...` |
| 0 | 0.147 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M08_certificate_ignores_grant -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M08_cert ...` |
| 0 | 0.147 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M09_second_arm_accepted -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M09_second_arm ...` |
| 0 | 6.513 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M06_hold_does_not_defer/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS -s ...` |
| 0 | 0.142 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M10_release_forgets_work -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M10_release_f ...` |
| 0 | 0.354 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M08_certificate_ignores_grant -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M08_certificate_ignores_grant/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M08_certificate_ignores_grant/fw.o` |
| 0 | 0.357 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M09_second_arm_accepted -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M09_second_arm_accepted/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M09_second_arm_accepted/fw.o` |
| 0 | 0.361 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M10_release_forgets_work -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M10_release_forgets_work/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M10_release_forgets_work/fw.o` |
| 0 | 6.539 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M07_hold_never_expires/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS -st ...` |
| 0 | 0.144 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M11_dirty_from_bytes_not_close -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M11_dir ...` |
| 0 | 0.37 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M11_dirty_from_bytes_not_close -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M11_dirty_from_bytes_not_close/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M11_dirty_from_bytes_not_close/fw.o` |
| 0 | 6.529 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M09_second_arm_accepted/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS -s ...` |
| 0 | 6.56 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M08_certificate_ignores_grant/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFL ...` |
| 0 | 0.14 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M12_alarm_not_revoking -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M12_alarm_not_r ...` |
| 0 | 0.141 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M13_report_not_revoking -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M13_report_not ...` |
| 0 | 6.534 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M10_release_forgets_work/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS - ...` |
| 0 | 0.139 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M14_pending_bit_misses_producer -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M14_pe ...` |
| 0 | 0.362 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M12_alarm_not_revoking -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M12_alarm_not_revoking/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M12_alarm_not_revoking/fw.o` |
| 0 | 0.352 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M13_report_not_revoking -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M13_report_not_revoking/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M13_report_not_revoking/fw.o` |
| 0 | 0.356 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M14_pending_bit_misses_producer -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M14_pending_bit_misses_producer/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M14_pending_bit_misses_producer/fw.o` |
| 0 | 6.611 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M11_dirty_from_bytes_not_close/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CF ...` |
| 0 | 0.146 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M15_pending_bit_misses_open_record -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M15 ...` |
| 0 | 6.54 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M13_report_not_revoking/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS -s ...` |
| 0 | 6.557 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M12_alarm_not_revoking/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS -st ...` |
| 0 | 0.368 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M15_pending_bit_misses_open_record -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M15_pending_bit_misses_open_record/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M15_pending_bit_misses_open_record/fw.o` |
| 0 | 6.501 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M14_pending_bit_misses_producer/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -C ...` |
| 0 | 0.142 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M17_hold_expiry_voids_capture -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M17_hold ...` |
| 0 | 0.146 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M18_pending_bit_stuck -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M18_pending_bit_ ...` |
| 0 | 0.139 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-R01_reload_ignores_inflight -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-R01_reload ...` |
| 0 | 0.354 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M18_pending_bit_stuck -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M18_pending_bit_stuck/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M18_pending_bit_stuck/fw.o` |
| 0 | 0.374 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M17_hold_expiry_voids_capture -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M17_hold_expiry_voids_capture/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M17_hold_expiry_voids_capture/fw.o` |
| 0 | 0.353 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-R01_reload_ignores_inflight -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-R01_reload_ignores_inflight/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-R01_reload_ignores_inflight/fw.o` |
| 0 | 6.578 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M15_pending_bit_misses_open_record/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 ...` |
| 0 | 0.144 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-R02_reload_ignores_grant_since_rebase -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut- ...` |
| 0 | 6.503 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M17_hold_expiry_voids_capture/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFL ...` |
| 0 | 6.575 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M18_pending_bit_stuck/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS -std ...` |
| 0 | 0.354 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-R02_reload_ignores_grant_since_rebase -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-R02_reload_ignores_grant_since_rebase/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-R02_reload_ignores_grant_since_rebas ...` |
| 0 | 6.547 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-R01_reload_ignores_inflight/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAG ...` |
| 0 | 0.146 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-R03_reload_not_once_per_reset -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-R03_relo ...` |
| 0 | 0.154 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M19_arm_edge_grant_not_deferred -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-M19_ar ...` |
| 0 | 0.141 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-A01_composite_durable_bit -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-A01_composit ...` |
| 0 | 0.359 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-R03_reload_not_once_per_reset -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-R03_reload_not_once_per_reset/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-R03_reload_not_once_per_reset/fw.o` |
| 0 | 0.352 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-M19_arm_edge_grant_not_deferred -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-M19_arm_edge_grant_not_deferred/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-M19_arm_edge_grant_not_deferred/fw.o` |
| 0 | 0.364 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-A01_composite_durable_bit -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-A01_composite_durable_bit/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-A01_composite_durable_bit/fw.o` |
| 0 | 6.51 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-R02_reload_ignores_grant_since_rebase/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P ...` |
| 0 | 0.145 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F01_certificate_not_checked -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-F01_certif ...` |
| 0 | 6.571 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-R03_reload_not_once_per_reset/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFL ...` |
| 0 | 0.354 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F01_certificate_not_checked -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-F01_certificate_not_checked/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-F01_certificate_not_checked/fw.o` |
| 0 | 6.567 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-M19_arm_edge_grant_not_deferred/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -C ...` |
| 0 | 6.512 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-A01_composite_durable_bit/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS  ...` |
| 0 | 0.139 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F02_copies_open_records -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-F02_copies_ope ...` |
| 0 | 0.139 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F03_prefill_from_blank -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-F03_prefill_fro ...` |
| 0 | 0.141 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F04_ack_without_identity -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-F04_ack_witho ...` |
| 0 | 0.354 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F02_copies_open_records -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-F02_copies_open_records/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-F02_copies_open_records/fw.o` |
| 0 | 0.352 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F03_prefill_from_blank -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-F03_prefill_from_blank/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-F03_prefill_from_blank/fw.o` |
| 0 | 0.352 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F04_ack_without_identity -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-F04_ack_without_identity/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-F04_ack_without_identity/fw.o` |
| 0 | 6.645 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-F01_certificate_not_checked/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAG ...` |
| 0 | 0.147 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F05_device_busy_gate_kept -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-F05_device_b ...` |
| 0 | 6.551 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-F02_copies_open_records/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS -s ...` |
| 0 | 6.498 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-F04_ack_without_identity/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS - ...` |
| 0 | 6.532 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-F03_prefill_from_blank/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS -st ...` |
| 0 | 0.139 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F06_ack_after_failed_slot -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-F06_ack_afte ...` |
| 0 | 0.358 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F05_device_busy_gate_kept -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-F05_device_busy_gate_kept/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-F05_device_busy_gate_kept/fw.o` |
| 0 | 0.136 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F07_reload_refusal_ignored -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-F07_reload_ ...` |
| 0 | 0.14 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F08_restart_reloads_window -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-F08_restart ...` |
| 0 | 0.364 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F06_ack_after_failed_slot -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-F06_ack_after_failed_slot/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-F06_ack_after_failed_slot/fw.o` |
| 0 | 0.352 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F07_reload_refusal_ignored -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-F07_reload_refusal_ignored/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-F07_reload_refusal_ignored/fw.o` |
| 0 | 0.357 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-F08_restart_reloads_window -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-F08_restart_reloads_window/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-F08_restart_reloads_window/fw.o` |
| 0 | 6.57 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-F05_device_busy_gate_kept/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS  ...` |
| 0 | 0.144 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-G01_pending_from_edge_detector -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -DNVM_HOST_JOURNAL_OFFSET=0xee0000u -DNVM_HOST_AEM_OFFSET=0x400000u -DNVM_HOST_IMAGE_OFF=0xef000u -c <CHECKOUT>/proposal-evidence/harness/cosim_host.c -o <CHECKOUT>/proposal-evidence/build/mut-G01_pen ...` |
| 0 | 6.521 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-F06_ack_after_failed_slot/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS  ...` |
| 0 | 6.519 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-F07_reload_refusal_ignored/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS ...` |
| 0 | 6.503 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-F08_restart_reloads_window/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CFLAGS ...` |
| 0 | 0.355 | `gcc -std=gnu11 -O2 -g -Wall -Wextra -Werror -I<CHECKOUT>/proposal-evidence/build/mut-G01_pending_from_edge_detector -I<CHECKOUT>/proposal-evidence/harness -I<CHECKOUT>/proposal-evidence/harness/stubs -Wno-format -c <CHECKOUT>/proposal-evidence/build/mut-G01_pending_from_edge_detector/milan_baremetal.host.c -o <CHECKOUT>/proposal-evidence/build/mut-G01_pending_from_edge_detector/fw.o` |
| 0 | 6.615 | `verilator --cc --exe --build -j 2 --top-module cosim_top --Mdir <CHECKOUT>/proposal-evidence/build/mut-G01_pending_from_edge_detector/obj -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --x-assign unique --x-initial unique +define+PROTO -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=38 -GCLK_HZ_P=1000000 -GCAP_ID_W_P=16 -CF ...` |

### manifest-run-2026-09-19T190145+0000.json: 2 commands, exit codes {0: 2}

| Exit | Wall s | Command |
|---|---|---|
| 0 | 0.371 | `python3 -B scripts/check_nvm_record_space.py --emit-record-table <CHECKOUT>/configs/endstation_ax7101_1x1_tdm8.yaml -o <CHECKOUT>/proposal-evidence/build/shape-1x1/records.txt` |
| 0 | 0.412 | `python3 -B scripts/check_nvm_record_space.py --emit-record-table <CHECKOUT>/configs/endstation_ax7101_8x8.yaml -o <CHECKOUT>/proposal-evidence/build/shape-8x8/records.txt` |

### manifest-run-2026-09-19T190710+0000.json: 2 commands, exit codes {0: 2}

| Exit | Wall s | Command |
|---|---|---|
| 0 | 0.373 | `python3 -B scripts/check_nvm_record_space.py --emit-record-table <CHECKOUT>/configs/endstation_ax7101_1x1_tdm8.yaml -o <CHECKOUT>/proposal-evidence/build/shape-1x1/records.txt` |
| 0 | 0.382 | `python3 -B scripts/check_nvm_record_space.py --emit-record-table <CHECKOUT>/configs/endstation_ax7101_8x8.yaml -o <CHECKOUT>/proposal-evidence/build/shape-8x8/records.txt` |

### manifest-run-2026-09-19T191108+0000.json: 2 commands, exit codes {0: 2}

| Exit | Wall s | Command |
|---|---|---|
| 0 | 0.383 | `python3 -B scripts/check_nvm_record_space.py --emit-record-table <CHECKOUT>/configs/endstation_ax7101_1x1_tdm8.yaml -o <CHECKOUT>/proposal-evidence/build/shape-1x1/records.txt` |
| 0 | 0.38 | `python3 -B scripts/check_nvm_record_space.py --emit-record-table <CHECKOUT>/configs/endstation_ax7101_8x8.yaml -o <CHECKOUT>/proposal-evidence/build/shape-8x8/records.txt` |

### results.json (grade phase): 32 commands, exit codes {0: 30, 1: 2}

| Exit | Wall s | Command |
|---|---|---|
| 0 | 0.372 | `python3 -B scripts/check_nvm_record_space.py --emit-record-table <CHECKOUT>/configs/endstation_ax7101_1x1_tdm8.yaml -o <CHECKOUT>/proposal-evidence/build/shape-1x1/records.txt` |
| 0 | 0.398 | `python3 -B scripts/check_nvm_record_space.py --emit-record-table <CHECKOUT>/configs/endstation_ax7101_8x8.yaml -o <CHECKOUT>/proposal-evidence/build/shape-8x8/records.txt` |
| 1 | 0.07 | `gcc -std=gnu11 -fsyntax-only -Wall -Wextra -Werror -Wno-format -I<CHECKOUT>/proposal-evidence/build/refusal-old_writer_new_generator -I<CHECKOUT>/proposal-evidence/harness/stubs <CHECKOUT>/proposal-evidence/build/refusal-old_writer_new_generator/fw.c` |
| 1 | 0.042 | `gcc -std=gnu11 -fsyntax-only -Wall -Wextra -Werror -Wno-format -I<CHECKOUT>/proposal-evidence/build/refusal-new_writer_old_generator -I<CHECKOUT>/proposal-evidence/harness/stubs <CHECKOUT>/proposal-evidence/build/refusal-new_writer_old_generator/fw.c` |
| 0 | 0.222 | `riscv64-elf-gcc -march=rv32i -mabi=ilp32 -Os -c -I<CHECKOUT>/proposal-evidence/build/size-tracked-1x1 -I<CHECKOUT>/proposal-evidence/harness/size_stubs <CHECKOUT>/sw/firmware/milan_baremetal/milan_baremetal.c -o <CHECKOUT>/proposal-evidence/build/size-tracked-1x1/fw.o` |
| 0 | 0.014 | `riscv64-elf-size <CHECKOUT>/proposal-evidence/build/size-tracked-1x1/fw.o` |
| 0 | 0.24 | `riscv64-elf-gcc -march=rv32i -mabi=ilp32 -Os -c -I<CHECKOUT>/proposal-evidence/build/size-proto-1x1 -I<CHECKOUT>/proposal-evidence/harness/size_stubs <CHECKOUT>/proposal-evidence/prototype/milan_baremetal.proto.c -o <CHECKOUT>/proposal-evidence/build/size-proto-1x1/fw.o` |
| 0 | 0.013 | `riscv64-elf-size <CHECKOUT>/proposal-evidence/build/size-proto-1x1/fw.o` |
| 0 | 0.211 | `riscv64-elf-gcc -march=rv32i -mabi=ilp32 -Os -c -I<CHECKOUT>/proposal-evidence/build/size-tracked-8x8 -I<CHECKOUT>/proposal-evidence/harness/size_stubs <CHECKOUT>/sw/firmware/milan_baremetal/milan_baremetal.c -o <CHECKOUT>/proposal-evidence/build/size-tracked-8x8/fw.o` |
| 0 | 0.014 | `riscv64-elf-size <CHECKOUT>/proposal-evidence/build/size-tracked-8x8/fw.o` |
| 0 | 0.242 | `riscv64-elf-gcc -march=rv32i -mabi=ilp32 -Os -c -I<CHECKOUT>/proposal-evidence/build/size-proto-8x8 -I<CHECKOUT>/proposal-evidence/harness/size_stubs <CHECKOUT>/proposal-evidence/prototype/milan_baremetal.proto.c -o <CHECKOUT>/proposal-evidence/build/size-proto-8x8/fw.o` |
| 0 | 0.013 | `riscv64-elf-size <CHECKOUT>/proposal-evidence/build/size-proto-8x8/fw.o` |
| 0 | 0.245 | `sv2v --top=KL_nvm_backend -DSYNTHESIS <CHECKOUT>/hdl/milan/KL_nvm_backend.sv` |
| 0 | 4.088 | `yosys -q -p read_verilog <CHECKOUT>/proposal-evidence/build/area/tracked-1x1.v; chparam -set N_STREAM_IN_P 2 KL_nvm_backend; chparam -set N_STREAM_OUT_P 2 KL_nvm_backend; chparam -set N_SPORT_IN_P 1 KL_nvm_backend; chparam -set N_SPORT_OUT_P 1 KL_nvm_backend; chparam -set N_AUDIO_UNIT_P 1 KL_nvm_backend; chparam -set N_CLK_DOM_P 1 KL_nvm_backend; chparam -set N_NAME_P 38 KL_nvm_backend; synth_xili ...` |
| 0 | 0.245 | `sv2v --top=KL_nvm_backend -DSYNTHESIS <CHECKOUT>/hdl/milan/KL_nvm_backend.sv` |
| 0 | 4.089 | `yosys -q -p read_verilog <CHECKOUT>/proposal-evidence/build/area/tracked-1x1-nodsp.v; chparam -set N_STREAM_IN_P 2 KL_nvm_backend; chparam -set N_STREAM_OUT_P 2 KL_nvm_backend; chparam -set N_SPORT_IN_P 1 KL_nvm_backend; chparam -set N_SPORT_OUT_P 1 KL_nvm_backend; chparam -set N_AUDIO_UNIT_P 1 KL_nvm_backend; chparam -set N_CLK_DOM_P 1 KL_nvm_backend; chparam -set N_NAME_P 38 KL_nvm_backend; synt ...` |
| 0 | 0.315 | `sv2v --top=KL_nvm_backend -DSYNTHESIS <CHECKOUT>/proposal-evidence/prototype/KL_nvm_backend.proto.sv` |
| 0 | 6.931 | `yosys -q -p read_verilog <CHECKOUT>/proposal-evidence/build/area/proto-1x1.v; chparam -set N_STREAM_IN_P 2 KL_nvm_backend; chparam -set N_STREAM_OUT_P 2 KL_nvm_backend; chparam -set N_SPORT_IN_P 1 KL_nvm_backend; chparam -set N_SPORT_OUT_P 1 KL_nvm_backend; chparam -set N_AUDIO_UNIT_P 1 KL_nvm_backend; chparam -set N_CLK_DOM_P 1 KL_nvm_backend; chparam -set N_NAME_P 38 KL_nvm_backend; synth_xilinx ...` |
| 0 | 0.325 | `sv2v --top=KL_nvm_backend -DSYNTHESIS <CHECKOUT>/proposal-evidence/prototype/KL_nvm_backend.proto.sv` |
| 0 | 6.956 | `yosys -q -p read_verilog <CHECKOUT>/proposal-evidence/build/area/proto-1x1-nodsp.v; chparam -set N_STREAM_IN_P 2 KL_nvm_backend; chparam -set N_STREAM_OUT_P 2 KL_nvm_backend; chparam -set N_SPORT_IN_P 1 KL_nvm_backend; chparam -set N_SPORT_OUT_P 1 KL_nvm_backend; chparam -set N_AUDIO_UNIT_P 1 KL_nvm_backend; chparam -set N_CLK_DOM_P 1 KL_nvm_backend; chparam -set N_NAME_P 38 KL_nvm_backend; synth_ ...` |
| 0 | 0.248 | `sv2v --top=KL_nvm_backend -DSYNTHESIS <CHECKOUT>/hdl/milan/KL_nvm_backend.sv` |
| 0 | 4.207 | `yosys -q -p read_verilog <CHECKOUT>/proposal-evidence/build/area/tracked-8x8.v; chparam -set N_STREAM_IN_P 9 KL_nvm_backend; chparam -set N_STREAM_OUT_P 9 KL_nvm_backend; chparam -set N_SPORT_IN_P 8 KL_nvm_backend; chparam -set N_SPORT_OUT_P 8 KL_nvm_backend; chparam -set N_AUDIO_UNIT_P 1 KL_nvm_backend; chparam -set N_CLK_DOM_P 1 KL_nvm_backend; chparam -set N_NAME_P 99 KL_nvm_backend; synth_xili ...` |
| 0 | 0.255 | `sv2v --top=KL_nvm_backend -DSYNTHESIS <CHECKOUT>/hdl/milan/KL_nvm_backend.sv` |
| 0 | 4.115 | `yosys -q -p read_verilog <CHECKOUT>/proposal-evidence/build/area/tracked-8x8-nodsp.v; chparam -set N_STREAM_IN_P 9 KL_nvm_backend; chparam -set N_STREAM_OUT_P 9 KL_nvm_backend; chparam -set N_SPORT_IN_P 8 KL_nvm_backend; chparam -set N_SPORT_OUT_P 8 KL_nvm_backend; chparam -set N_AUDIO_UNIT_P 1 KL_nvm_backend; chparam -set N_CLK_DOM_P 1 KL_nvm_backend; chparam -set N_NAME_P 99 KL_nvm_backend; synt ...` |
| 0 | 0.316 | `sv2v --top=KL_nvm_backend -DSYNTHESIS <CHECKOUT>/proposal-evidence/prototype/KL_nvm_backend.proto.sv` |
| 0 | 8.072 | `yosys -q -p read_verilog <CHECKOUT>/proposal-evidence/build/area/proto-8x8.v; chparam -set N_STREAM_IN_P 9 KL_nvm_backend; chparam -set N_STREAM_OUT_P 9 KL_nvm_backend; chparam -set N_SPORT_IN_P 8 KL_nvm_backend; chparam -set N_SPORT_OUT_P 8 KL_nvm_backend; chparam -set N_AUDIO_UNIT_P 1 KL_nvm_backend; chparam -set N_CLK_DOM_P 1 KL_nvm_backend; chparam -set N_NAME_P 99 KL_nvm_backend; synth_xilinx ...` |
| 0 | 0.327 | `sv2v --top=KL_nvm_backend -DSYNTHESIS <CHECKOUT>/proposal-evidence/prototype/KL_nvm_backend.proto.sv` |
| 0 | 7.978 | `yosys -q -p read_verilog <CHECKOUT>/proposal-evidence/build/area/proto-8x8-nodsp.v; chparam -set N_STREAM_IN_P 9 KL_nvm_backend; chparam -set N_STREAM_OUT_P 9 KL_nvm_backend; chparam -set N_SPORT_IN_P 8 KL_nvm_backend; chparam -set N_SPORT_OUT_P 8 KL_nvm_backend; chparam -set N_AUDIO_UNIT_P 1 KL_nvm_backend; chparam -set N_CLK_DOM_P 1 KL_nvm_backend; chparam -set N_NAME_P 99 KL_nvm_backend; synth_ ...` |
| 0 | 0.256 | `sv2v --top=KL_nvm_backend -DSYNTHESIS <CHECKOUT>/hdl/milan/KL_nvm_backend.sv` |
| 0 | 4.102 | `yosys -q -p read_verilog <CHECKOUT>/proposal-evidence/build/area/tracked-1x1-page-bound-30.v; chparam -set N_STREAM_IN_P 2 KL_nvm_backend; chparam -set N_STREAM_OUT_P 2 KL_nvm_backend; chparam -set N_SPORT_IN_P 1 KL_nvm_backend; chparam -set N_SPORT_OUT_P 1 KL_nvm_backend; chparam -set N_AUDIO_UNIT_P 1 KL_nvm_backend; chparam -set N_CLK_DOM_P 1 KL_nvm_backend; chparam -set N_NAME_P 30 KL_nvm_backe ...` |
| 0 | 0.257 | `sv2v --top=KL_nvm_backend -DSYNTHESIS <CHECKOUT>/hdl/milan/KL_nvm_backend.sv` |
| 0 | 4.03 | `yosys -q -p read_verilog <CHECKOUT>/proposal-evidence/build/area/tracked-1x1-page-bound-30-nodsp.v; chparam -set N_STREAM_IN_P 2 KL_nvm_backend; chparam -set N_STREAM_OUT_P 2 KL_nvm_backend; chparam -set N_SPORT_IN_P 1 KL_nvm_backend; chparam -set N_SPORT_OUT_P 1 KL_nvm_backend; chparam -set N_AUDIO_UNIT_P 1 KL_nvm_backend; chparam -set N_CLK_DOM_P 1 KL_nvm_backend; chparam -set N_NAME_P 30 KL_nvm ...` |

The two grade-phase commands that exit 1 are the build-time refusals, which MUST fail (REFUSAL lines above).

## SHA-256 of every evidence source

| sha256 | file |
|---|---|
| a49c0d7760051161676e41f004c10526bae4df1ff028eec279dbb4cf15e2d24e | proposal-evidence/harness/cosim_api.h |
| 52b5e7839082ac1bbdc26bd724540d789ec60b69a76652bbb7da5355a5f14773 | proposal-evidence/harness/cosim_bridge.cpp |
| 81e85278b7df7f45ed56e8e70601ac95dcb4fedd58db71346f6aa080d9fed5b2 | proposal-evidence/harness/cosim_bridge.h |
| 97e4c7774fb76f36e9b891459a67f0c6d31a9d27d7bccaabfe9f65701ca8de87 | proposal-evidence/harness/cosim_cases.cpp |
| 6274198dcffd44302c8447cdf1b511a552bdf38392e09297e25cc81de5afa27c | proposal-evidence/harness/cosim_host.c |
| a1582388437e74cf2c246cdc544e7a5abed9e94b655b5ba92053bdc65d6de6cc | proposal-evidence/harness/size_stubs/command.h |
| b0986d3feb4ac224f8d660f3b2c1804a68be77431774bacee7f558c19e6de551 | proposal-evidence/harness/size_stubs/generated/csr.h |
| b987b253e7dbe9cd5d206ab046da8b642446b275cf1f41ec5066432cc04c8ef2 | proposal-evidence/harness/size_stubs/generated/mem.h |
| 77442df6ec9da01e332a4cf283c03d7a89b3db03389c86546a57aa31f9b680a1 | proposal-evidence/harness/size_stubs/hw/common.h |
| 9e32c0958ab0f57feb8bfa3e7bb79ed57916f11243fc751f673fb7e805054c79 | proposal-evidence/harness/size_stubs/init.h |
| c2aeb3b098e543ff306b443a33049f4b7cb860642b19b0262e2543b2d28b3450 | proposal-evidence/harness/size_stubs/libbase/crc.h |
| 50cfa4347bae790a1ba511881d76f72801c3ac93a7096915475991f5527b2cfa | proposal-evidence/harness/size_stubs/system.h |
| a1582388437e74cf2c246cdc544e7a5abed9e94b655b5ba92053bdc65d6de6cc | proposal-evidence/harness/stubs/command.h |
| 67d05a5b35dc82b1033675225a3bd24e446dda43535cf11cd7c538f0e3b2491a | proposal-evidence/harness/stubs/generated/csr.h |
| 7dc2ecfb649dd841484877cedd8495068d5bcc773fb11ebf9f8bc6013f9343f8 | proposal-evidence/harness/stubs/generated/mem.h |
| d56b44d934a02d0b75b0b6bd10c123abeef08d3cb3c55c1aca07527d4e787598 | proposal-evidence/harness/stubs/hw/common.h |
| 9e32c0958ab0f57feb8bfa3e7bb79ed57916f11243fc751f673fb7e805054c79 | proposal-evidence/harness/stubs/init.h |
| e8eba505669fd27493a523d28e841b210e221c2ef6d45ddf1e7f649c426fc18e | proposal-evidence/harness/stubs/libbase/crc.h |
| 559e2f037b42c1f77488ee0b4da8e9b673850b796cf59af8aba1cfb7c79d26b1 | proposal-evidence/harness/stubs/nvm_host.h |
| 50cfa4347bae790a1ba511881d76f72801c3ac93a7096915475991f5527b2cfa | proposal-evidence/harness/stubs/system.h |
| 0f604aca5619d57d1739ac27e0579838dc180012f8aa63e8045d4cb784017a8b | proposal-evidence/make_command_results.py |
| 16fce8e6b916f9ee479bceeb18d3240fb24f33f3920725e9a1484b4fe90c4fdf | proposal-evidence/prior-session/phase-grade.log |
| 19eaf43821a7660ec323a87c8457bf74823beb296c39f5e01aa8a683aa50f061 | proposal-evidence/prior-session/round3-reviewed-console/final-1-build.log |
| 19eaf43821a7660ec323a87c8457bf74823beb296c39f5e01aa8a683aa50f061 | proposal-evidence/prior-session/round3-reviewed-console/final-2-run.log |
| 1cdc7e4fd7f3b9e3554ff16c40b2ca5546ab21d9ecfd72a13e1732f29d7f6d9c | proposal-evidence/prior-session/round3-reviewed-console/final-3-grade.log |
| 19eaf43821a7660ec323a87c8457bf74823beb296c39f5e01aa8a683aa50f061 | proposal-evidence/prior-session/round3-reviewed-console/final-alt-build.log |
| 19eaf43821a7660ec323a87c8457bf74823beb296c39f5e01aa8a683aa50f061 | proposal-evidence/prior-session/round3-reviewed-console/final-alt-run.log |
| 19eaf43821a7660ec323a87c8457bf74823beb296c39f5e01aa8a683aa50f061 | proposal-evidence/prior-session/round3-reviewed-console/phase-build.log |
| 6a420bda665145b8236502ed694bea57494367e1e8a2aa4554b52376773e0927 | proposal-evidence/prior-session/round3-reviewed-console/phase-grade.log |
| 19eaf43821a7660ec323a87c8457bf74823beb296c39f5e01aa8a683aa50f061 | proposal-evidence/prior-session/round3-reviewed-console/phase-run.log |
| 595fd5b8da5d161bd49826bc7c86eb4d9b5ee3613d6999121280be24adbc1ca8 | proposal-evidence/prior-session/unused-drafts/control_section.svh |
| 4ec4c86fa48e6c1e8182b9110c72d46da5f25536bd9d956401f1e55e4f3e4deb | proposal-evidence/prior-session/unused-drafts/ownership_section.svh |
| 297f057e0b549456b0d06b7122d76bd150c7cfa8e1992275345616f03fd344fd | proposal-evidence/prototype/KL_nvm_backend.proto.sv |
| d14652e61c70b57ea52dee8ad546de970f9f3a4c9371579536ab5eec2f9572ad | proposal-evidence/prototype/milan_baremetal.proto.c |
| 28e03a3a5dff5bce0895d036a41790265915beb86146d4df8fc107d6a7cbdf09 | proposal-evidence/rtl/cosim_top.sv |
| 3396c320abec8fd73648b03f620243b1a18af24dc3f7e019b0a658fe1adf5752 | proposal-evidence/run.py |
| 5e74b15ce8b9414a1929c163ff10d3c97c13c976e57da15d3b773a864793d86d | proposal-evidence/sources/issue-418-comment-5571549944.json |
| 64d22e6744a6ac477d6d07f76fd2bb1d7ef7182b15d20b1809949545997e1718 | proposal-evidence/sources/issue-418-comment-5571549944.md |
| 131c1aa7fc303c6c5e2f58876f0fc2ce1c35936302a5f5d38fa9b8f135484d5a | proposal-evidence/sources/issue-419-body.txt |
| 6d68470f152453e439b90802f77f9ce3e020b80a05fcd61141657d27e56fbc64 | proposal-evidence/sources/issue-419-comment-5572365944.md |
| f7bf928d48448464d0dee1f975c9df6a1b50a4f7732c70ac83e081665b5859c4 | proposal-evidence/sources/issue-419-comment-5572530439.md |
| 4d35df6cef79035990fbc78d6ea5a310e8ddcadec7b718609590c217e06dbb12 | proposal-evidence/sources/issue-419-comment-5572929807.md |
| c8ca214cd5317dbf8dd893a673c109efbed814c849aa5a219a80b61189045466 | proposal-evidence/sources/issue-419-comment-5573055828.md |
| 3675ae8547bfaeda2b137961c107a7425ef97c18eb4ff77dc858305d106b047a | proposal-evidence/sources/issue-419-comment-5573056108.md |
| 57fed227bdeacc147a8a5e1d5f25d21e5a3409c923796fd63d35a43aff626519 | proposal-evidence/sources/issue-419-comment-5573056321.md |
| 925093001e550cf85f57734382d71f9d79d2493d73621be4e0026ff677f278b7 | proposal-evidence/sources/issue-419-comment-5573056555.md |
| b4f7d1bf2063241fe0bf888b8f57b1b45fea43e43bf7a2c8cb5690ef92baf182 | proposal-evidence/sources/issue-419-comment-5573056769.md |
| f084b43443f206c4a3320f165b1c3e6d0e6a5c3e7ca5884568c59b612a2e6b1f | proposal-evidence/sources/issue-419-comment-5573069707.md |
| e9b470bb85d826c3bb3b62f23e4b5d3bdb3d65fbed00195f2972a9072c8a3166 | proposal-evidence/sources/issue-419-comment-5652830557.md |
| 01bbda78d850f0ae8baa5a7a75877170feabe2b79c64b6bb11b1efe7c5d9a91e | proposal-evidence/sources/issue-419-comment-5670792796.md |
| e54af404c541edbea7c42dd2c6453e2f73acf68c3ca21b271a4beb5fced88c2d | proposal-evidence/sources/issue-419-comment-5671186014.md |
| 4f99a8ec204d7d135c8677c5ebe7ce21c36999ad3f8ef153f6866833f6c9309f | proposal-evidence/sources/issue-419-comment-5729969523.md |
| 6056fe86d0f2ae5e1db6037e9b428662a3c14fc6f6b16a942a90931c0a3666da | proposal-evidence/sources/issue-419-comment-5730427393.md |
| bcf3333a40abe83657ea7659b24fbd1f0819a2a15732e94bc668f8a86e447d6a | proposal-evidence/sources/issue-419-comment-5739523021.md |
| 09bd514edfbd1ef1142d9334f3deb44723e281fe24ab556766e314e6eac45cd6 | proposal-evidence/sources/issue-419-comment-5740180418.md |
| 0e32cb8d5ed3dc6aa17497f933d69849bdc9d0936dc54c06b4f41b42fd75f5d1 | proposal-evidence/sources/issue-419-comment-5740255143.md |
| 94f05dd8fa6c261a135c5117b68d2d1b5d5f217bc08ad6b2f692aa9b16083c22 | proposal-evidence/sources/issue-419-comment-5743971020.md |
| 8a5c4dde70728843cc46ed35fbca505c3c1e5cb41e36cb52b532d6eb43baefae | proposal-evidence/sources/issue-419-comments-recheck.json |
| 340a05a0f9131731cb4fedbde6ca346b23194339fecac967af62c62fbea12fb4 | proposal-evidence/sources/issue-419-comments-revb.json |
| a8288a7433de909703acd4c57ca98c0b76b9a1665f4cf16a3f5a20b9b5d16796 | proposal-evidence/sources/issue-419-comments.json |
| d17c04517b0d82a17a5f3bde7133d72029922128623b3d0e3fa0ae0f0794c99b | proposal-evidence/sources/issue-419-comments.txt |
| 769141a5a94ee6e94b4ffaccc636ad37ea3d8cf553d6253a227bae05e8323b95 | proposal-evidence/sources/issue-420-comment-5670583242.json |
| 139fcdb5423bb971529d2fe2efccf7ce107ac15f0384c38ad306395e2461e1a8 | proposal-evidence/sources/issue-420-comment-5670583242.md |
| 5e6530f3f7a210b5f7d5c160c906fb6176aec06e41b2eb6a02315c17b1cad8cc | proposal-evidence/sources/issue-420-comment-5670792010.json |
| ea1f4353e722585f389b28212b90eb64a796da12f7a4fc87a6525d72561a7642 | proposal-evidence/sources/issue-420-comment-5670792010.md |

## SHA-256 of the evidence outputs

| sha256 | file |
|---|---|
| 0b99e50d386cdc69ca36fceb1a4fb4fe00d13459d95caf881709d784a5145b4d | proposal-evidence/results.txt |
| 72bbdc54c26ad595d7dcba76ee1aae94f16d716e9f7ab20dffb53286b7282899 | proposal-evidence/results.json |
| 6f65c13089ba9f0cb17c9cb889bb7bed87ed6c509bac090c4b65deb4efda8d72 | proposal-evidence/console/revb-0-build-seam-failure.log |
| bd76a4ee4f6e1879ae69258d619536b8931adaa6a0abfc08ba655b7b0b3966e1 | proposal-evidence/console/revb-1-build.log |
| f69b312d5122a3df3301512a94d202df9aecfde24ab49f2831aecc3bd4506dc9 | proposal-evidence/console/revb-2-run-1.log |
| ea5976c06b3161d186c648b1807221e94efef08a817821de42d977ddc33c320b | proposal-evidence/console/revb-2-run-2.log |
| 2faeaf3a4f63f192bc92fd9a3603ac0bbb0f526be317834c361e39e4bdae7785 | proposal-evidence/console/revb-2-run-3.log |
| dc438ef65397a1cbc4b06fe18de9729b8a30e1bc761b0d282e70ef3514e959b8 | proposal-evidence/console/revb-3-grade.log |
| 529cee2c548343521dc0e1ccce807ee3ad3693216000202268715c8737e3f0d6 | proposal-evidence/logs/manifest-build-2026-09-19T190037+0000.json |
| bf5609b44d29ee1d0b411bbf32c48e6c0b2675a7dee2d0d4ae3c198f4934074b | proposal-evidence/logs/manifest-run-2026-09-19T190145+0000.json |
| 1e3d1dae6a205357f3c931e4c474dbdf523099e21a88bedeb4cc6d48e62d56ff | proposal-evidence/logs/manifest-run-2026-09-19T190710+0000.json |
| 01237ab336ead3d5718c2e912938c82d8e7b3921f4d49e704f16cb2399cf3bb4 | proposal-evidence/logs/manifest-run-2026-09-19T191108+0000.json |

## SHA-256 of every production file examined

run.py's PRODUCTION list is hashed before and after the run; unchanged: True.

| sha256 | file |
|---|---|
| 8a7287eea6b886f9a4d134aec8c03de188f3b718694fafc2eeadc3763da26738 | AGENTS.md |
| f95106643c4b8d0bc39b1ef50ff821039b63c422325c14ea3264484a44bb13ec | CONTRIBUTING.md |
| cb689c50e8da12a12f1917c5cc7506362f63d610b6c6d600f267c628e2916b0d | REQUIREMENTS.md |
| ab04f949f7be197d5d8003a39f49b1d4cd405d5983940bafaaef666d40a73f2e | configs/endstation_ax7101_1x1_tdm8.yaml |
| 5ab2b7244745c55fdecaf147d35b231584587d6f3e756f646a3d90db0cbd745e | configs/endstation_ax7101_8x8.yaml |
| 9acf2ce9d741d1533c4ef88d1eb6f94495851b5252917f02371c2f3330b05c1c | docs/design/SAVED_STATE_FASTCONNECT.md |
| 546fcc735d9d8a69c7100156bfe009a4d4a28cb806d6769b0a709a807000a2e2 | docs/reference/REGISTER_MAP.md |
| 1747eca968607cf7d12a631613c5175db206e99f8b665cbbc0bcb13b21e3c4ff | hdl/common/csr/milan_csr.sv |
| eb905bc486aa9f533e5fa53a9cb33da6c1556f60ab1fbc2d2bbdb33858d585d3 | hdl/milan/KL_nvm_backend.sv |
| e99bfb4388ebad069bc1a6612e73bdce21f672c2663217cf1540b8fa8cd3d919 | hdl/milan/KL_pp_shadow.sv |
| 8c581ac93c6e86addf35e716a136c03198342a332747d285376cd6eda1eb06ca | protocol-processor/docs/architecture/02_interfaces.md |
| d159048760dbe89a9d76570bf82b16f7ce7411608340e29543205631a1a0c351 | protocol-processor/hdl/acmp/KL_acmp_nvm_shadow.sv |
| b504951db8c81134ef54030e37879431f84ea8005e38c46479c8f66dcc4bbb85 | protocol-processor/hdl/acmp/pp_acmp_pkg.sv |
| 63bb80169ed4118b1d4e6e7ddc819a71648a9801abdd4b3984b7f75801039211 | protocol-processor/hdl/aecp/KL_aecp_desc_store.sv |
| c0916f98d71691f72b880b5332157beafbfe9b9dd5dc64bd351294d6edbee099 | protocol-processor/hdl/aecp/KL_aecp_dyn_state.sv |
| e126d210a0db3091980602da7a88ef1a979dd029dde3168467a2299c4f4cf016 | protocol-processor/hdl/aecp/KL_aecp_engine.sv |
| 980eeda20e444bd6964ccf4dc9cfc27eb7d4cb5784d6f364bacf75fc1bf94e2d | protocol-processor/hdl/aecp/ucode/gen_ucode.py |
| 194e8120bf715103645e095288cbed84e7c3f1704647c2efbe3f2585f2dd76b6 | protocol-processor/hdl/packet_engine/KL_pp_nvm_port.sv |
| 463b9ff71649ab67222c7266d5580fc46c28cc1aa2d45bd8fcfcd8b5f7e33709 | protocol-processor/hdl/top/protocol_processor_top.sv |
| 1883d2a55945e8aad0e897a21a81acbbbaeff0b5825839ff7f04573b31bbdc9d | scripts/check_nvm_record_space.py |
| 71a6e6a0b9fe861ace3d529ced9bdf1276707b2a4581f3c38ecec8cacc568c8f | scripts/nvm_contract.py |
| eaa31c5956a6808a2bb94356cbb35e90074942134196dbf446d37b65f5a1c913 | scripts/nvm_klj2.py |
| e67fc3aec5dd66ad9720d8e2a4c8ffd67aa3bb01dc4c564d00ff1b0e73b59bf4 | scripts/nvm_shape.py |
| 3c28591f76afad67eebd77ed185a021e3a2bcdff5c3f7650d7a1e0374ab77b41 | sw/firmware/milan_baremetal/milan_baremetal.c |
| efbc5d5c494ccb86127019d48fba41ede3655ff27c329b56dc6d1f30cac07450 | sw/firmware/nvm_hosttest/nvm_host.c |
| 86c3e3a159997a367414f338d0e3eb24abd2f8854ec6044f071578d098038755 | sw/firmware/nvm_hosttest/test_nvm_firmware.py |
| 52846748780c460dc9b583e10a0e8e35004489ac69a671f575eb1bd386f9e0c9 | sw/litex/milan_soc.py |
| 39a46b5dae849702fcbe699d57ab59b64e51a0b7933e0a0c473b58c06e80176f | syn/yosys/ooc.sh |
| ccd6042030d1ef982cf6b6fe076cf4b44f403830336b20bb4384c6c9a7808735 | tb/verilator/nvm_backend/Makefile |
| 5c8cf8fc5053ec628d2a353678a5491700ed36d5d9b1d58b68274d419527dcc7 | tb/verilator/nvm_backend/mutate.py |
| 4d39fc75fdd29b56a5cfd0e2e2b85c6c360e7f4c41da698bbfad4d839bf1c677 | tb/verilator/nvm_backend/sim_main.cpp |
