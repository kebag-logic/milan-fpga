[A837] REPORT

PR #966 is locally review-ready at `44c566399002db32bf8a6ad3ce719488d418bcb0` (five local commits, tests/test plumbing/records/docs only; product C and RTL unchanged). Coverage check rc 0: aecp_face 229/229 lines and 204/204 branches; mbx 384/384 and 202/202; ctrl_plat 224/224 and 110/110 with the stale gate exclusion removed; gptp.h 2/2; gptp.c 665/704 and 346/437. No recorded figure lowered. All four firmware shards with `--require-rv32 --self-test` pass, including 828/828 control and 387/387 AECP mutants. The cancelled docs, elaborate and rtl-fast jobs’ substantive local steps have passing evidence after focused corrections/replays. The two previously uncovered builder arms remain explicitly uncovered. Final-head documentation checks pass; the last commit changes prose only and preserves the measured coverage inputs. No hosted verdict on the unpushed head is claimed.

The scale composition is `fe009fa2c7741b8612bdbc74fe70909d57931503`, based on that repair with int4, the scale ports, the interface-specific probe fix and the 16-value cap. All nine Arm A groups completed at 32x32/2if in each cache configuration. Both harts run at 100 MHz; hart 1 has 16 KiB I$.

| Hart 1 D$ | H0 worst pass | H1 worst pass | SHARE misses | Original / strict matrix rc |
|---|---:|---:|---:|---:|
| None | 0.83224 ms | 0.91832 ms | 0 | 1 / 1 |
| 8 KiB | 0.83225 ms | 0.78905 ms | 0 | 1 / 1 |

Each matrix has seven owed-backlog probes over the nominal 20 ms bound (61.947–65.563 ms without D$, 61.656–64.549 ms with 8 KiB). Record-mode backlog rc 0 retains those findings; strict rc is 1. MAAP has two periodic-opportunity findings in each configuration; their expiries predate interface-1 link-up and the grader drops LINK values, which is diagnostic context, not a waiver. The cached MAAP run additionally has join intervals 180.928 and 180.929 ms below 181.0 ms. No refusals or SHARE misses were observed.

Per-hart demand estimates, with both gPTP ports charged together at 0.0042 to each hart in turn:

| Hart 1 D$ | gPTP on H0: H0 / H1 | gPTP on H1: H0 / H1 |
|---|---|---|
| None | 0.599170 / 0.397682 | 0.594970 / 0.401882 |
| 8 KiB | 0.596170 / 0.390626 | 0.591970 / 0.394826 |

These are estimates using sampled costs and inherited rates, not CPU occupancy or a closed worst-case proof. Unmeasured cost transfers, in microseconds: TICK 45, GM 30, retained retry 865, owed MRPDU 7485, build-both 10810, AECP notice 350, registration probe 65, saved-state step 1030, declined ACMP 0. Historical centisecond 960 is replaced in the final tick terms by measured H0/H1 dispatch 180/5 or 150/5 plus the 45 overhead; events-none 20 and base 570 are not long-window source terms. Other transferred/unmeasured terms are each cross-hart send/take at 6.4 us, PHY at 155 us per 125 ms, the gPTP charge, notice-header costs and full-declaring/cap-dependent rates. Queue-full retries, unstaged bus/cache combinations, empty-loop background, unfinished calls and overlap with separately charged record work remain unclosed. The generated 32x32 shape has 33 slots; the calculation conservatively uses 17 sinks/interface and 68 counter descriptors.

Largest demand terms on H0 are SRP 0.2465, owed MRPDU 0.1576 and builds 0.1138; the latter two are transfers. On H1, AECP owed work is 0.0783 and ACMP owed work 0.0752/0.0682. Observed inclusive call shares are about 27.9% for H0’s SRP poll and 36.47%/31.33% for H1’s MAAP poll. Nested spans overlap. MAAP refresh scans sources; ACMP bitmap cost is not separately attributed, and the declaring bitmap loop has no demand bits in this fixture. No Zbb benefit is established; it remains off.

The one-hart 32x32 ELF is byte-identical across the new observer/cache-selection changes at the composed scale baseline: 196024 bytes, SHA-256 `2b05feba4c2c7ff44f0eda69dadf9dc882124b553ada835e7e93db9a0add1cc7`. This does not claim identity across the earlier fold/scale ports. Dedicated scale controls pass 21/21, including second-core removal from both scale build identities; second-hart unit checks pass 26/26. Actual 32x32 traces pass clean and are refused after deleting hart-1 observations. The full harness self-test remains rc 1 on six imported shape-model conflicts in one baseline check (1935-us slices versus the old 1600-us cap, 10810-us build-both versus two 1935-us builds, and missing scale entries in the built/poll tables); its mutation campaign was not run on that failing baseline. The unchanged style ratchet also remains red.

32x32 firmware memory is 179804 bytes ROM, 169104 H0 SRAM and 153760 H1 RAM, with H1 allocated at 262144 bytes as ruled. Firmware plus cross-hart RAM is 150.5 memory-tile equivalents, excluding cores, caches and other memories; no routed fit is claimed.

**STOP:** the 64x64/2if two-hart firmware build fails: `.hart1.bss` does not fit `hram`, which overflows by **92064 bytes** against 262144 bytes. Image-builder rc 2, foreground wrapper rc 1. No 64x64 execution/load or #884 placement decision is claimed. The explicit build-failure stop applies; REBOOT was not changed. No push, PR edit, route or hardware access occurred.
