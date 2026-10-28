[A692] STOP
Head: f67a4ca1b32f2b247b772007e9731f26d2a82440 (branch `799-adopt-processor-f65c8ff7`, 14 commits on dev `97aab1d0`, not pushed)

**Reason: a required fast-gate job fails, and fixing it needs a register-map change beyond the `src_stream_id_o` routing, the assignment's STOP condition.**

`rtl-fast`'s `publication-census` job (`python3 sw/mailbox/publication_census.py --check --selftest`) fails at this head. Per #665 (ruling 6088423771, decision 2 (a)), the census requires every class-D output of `KL_pp_shadow` to be listed and every read of it in `milan_datapath` to be named. A read that reaches the wire must be carried by a field of the mailbox publication block (`sw/mailbox/mailbox.yaml`), which the split placement's firmware writes in place of the processor.

The #202 wiring adds `src_stream_id_o` and three reads of it:
- `aaf_tx_sid_w`: the AAF stamp, reaches the wire, every shape;
- `crft_tx_sid_w`: the CRF Media Clock Output's stamp, reaches the wire, only in shapes with a CRF source;
- `gsi_osid_w`: GET_STREAM_INFO selector 2, reaches the processor's answer face.

The census gives 5 findings at this head. Two edits need no decision: list `src_stream_id_o` in `CLASS_D_PORTS`, and map the selector-2 read as a `processor` row, as `acmp_bound_sid_o`'s is. With both applied in a scratch clone, 3 findings remain, all on the two stamps:
- two unmapped wire reads;
- the CRF read differing between shapes.

The publication block has no per-source Stream ID field; its talker registers are DA_GATE, LICENCE, IDLE_SLOPE, SR_DOMAIN and TALKER_DECL. The processor consumer banks for #204, #207 and #208 did not run this job.

**Options:**
- **(A)** Add a per-source current-Stream-ID publication register to the mailbox contract, with its `KL_mbx` port, and map the two stamps to it. The CRF stamp's read also has to be made shape-independent. This is a register-map change.
- **(B)** An owner ruling that the split placement stamps the configured ID (its firmware does not move Stream IDs), plus a census mechanism for that exclusion.

**Recommendation: (A).** Whichever plane owns the Stream ID must publish the ID it declares. Otherwise the frames and the PROBE_TX answer disagree after any move, which is #202's own defect.

**Also for decision: the resource gate refuses all three endpoints** against the eleventh record (Vivado 2026.1, recipe flows, at `05b26476`, the final RTL):

| Endpoint | LUT | FF | Tolerance (LUT / FF) |
|---|---:|---:|---|
| route-1x1 | +753 (+1.47 %) | +499 | 500 / 600 |
| ooc-1x1 | +518 | +404 | 250 / 250 |
| ooc-8x8 | +1,689 | +1,562 | 316 / 339 |

- route-1x1 is below the assignment's 2 % STOP. Slices -55; RAMB and DSP unchanged.
- The route is complete with 0 routing errors. WNS +0.440 ns / WHS +0.036 ns (slow corners: WHS +0.074 ns).
- +712 of the route's LUTs are inside the processor (the #202 owed-Leave copy, move and quarantine).
- The record is not re-baselined; that is an owner decision.

**Done at this head (all in clean clones; each rc is the command's own):**

- Full sweep, four shard units at `3ee2d969`: 64 / 64 suites, **2,191,637 checks, 0 in-suite failures**, 0 timed out, tally rc 0. milan_dp: 18 legs, 13,723 checks (notify 499 with G11; sidmove 50; sidmove8 52). pp_shadow: base 651, vid73 651, crf 691, pending 317, 0 failures.
- milan_dp_gptp (physical, `--physical-gptp`): PASS, 1 / 1 suite, 209 checks, 0 failures, not timed out (the physical leg 155, the two accounting verifiers 14 and 14; 5,412 s).
- `make gsi-mutants`: rc 0, clean 499 / 499, 14 / 14 arms caught by name.
- Firmware gate set (8 commands): rc 0. `ctrl_boundary` needed `sw/firmware/ctrl/README.md` to give 171 pin controls, the four new sidmove targets (`1f7420d1`).
- rtl-fast replica: 11 / 12 jobs success; `publication-census` fails (above). behave: 14 features, 406 scenarios, 1,979 steps.
- Yosys `syn/yosys/run.sh`: 60 / 60 tops; tied-input and tap-purity PASS.
- Static gates, all rc 0:
  - lint (89 <= 89); xvlog (0 findings);
  - both idiom gates and self-tests; RTL source lists; `pp_srcs --check --selftest`;
  - port contracts; naming and test-evidence measures; integrator params;
  - ROM digests re-recorded with no diff; both diagram checks; submodule and gPTP docs; `test_builder.py`.
- Docs gates (GNU Make 4.3) at `f67a4ca1`: 42 steps rc 0 (2 skipped by rule); LiteX builder leg, markdown on CPython 3.12.3 and the no-git step rc 0.

**Evidence for #790 and #202:**
- `make gsi-mutants` returns 0: the clean leg passes 499 / 499, and all 14 arms are caught by name.
- The three new #790 arms each fail `[GSI] G11 sink 0 back in PROBING_PASSIVE after TMR_NO_TK, the stale ID: …` (stream_id, the three flags, stream_dest_mac).
- pp_shadow with the pass-through planted in a scratch clone fails 3 of 651: flags `0x52`, stream_id `0x0200000000020790` and DA `0x91E0F0002A90` while passive, which is #790's bench capture.
- Recovery legs: conflict to new declaration in 1,735 ms (1x1) and 1,816 ms (8x8). After the move, the wire, PROBE_TX, GET_STREAM_INFO and the Talker Advertise name one ID.

**Found outside scope, for a new issue:** on the 8x8 and 4x4 shapes the datapath's maap-face source index (`PP_SRC_IDX_W_C`, `$clog2(N_STREAMS)`) is one bit narrower than the processor's (`$clog2(N_STREAM_OUT_P)`). As a result, the CRF output's ALLOC_DA and conflict arrive as source 0's. The shipping 1x1 shape is unaffected.
