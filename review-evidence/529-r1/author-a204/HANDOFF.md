# #529 handoff ([A204])

## State

- Lane `$LANES/529-crf-input-counters`, branch `529-crf-input-counters`, head
  `f815577559d4922c945dcf1436d4394ff2c10567`. It has four commits on base `ede8d48e`, is clean,
  and is **not pushed** (no push, PR edit or merge by this role).
- Public: `[A204] TAKEN` https://github.com/kebag-logic/milan-fpga/issues/529#issuecomment-5796592626
  and `[A204] REVIEW READY` https://github.com/kebag-logic/milan-fpga/issues/529#issuecomment-5797833943
- `PR-BODY.md` is ready for a draft PR against `dev`: it starts `[A204]` and carries `Closes #529`.
- Evidence: `RECEIPTS.md`, `mutation_receipt.txt`, `logs/`, the Yosys `yosys/{base,head}` records.

## What changed (closure criteria 1-4)

1. `milan_datapath.sv` connects all ten `KL_crf_rx` Table 5.16 outputs. `ctr_crf_w` /
   `ctr_crf_block` serve them on the solicited GET_COUNTERS face for STREAM_INPUT
   `CRF_SNK_IDX_C` (= `N_STREAMS`) only when the shape declares the CRF sink.
2. They are served full 32-bit at the Table 7-157 quadlets under `counters_valid = 0xF3F`.
   The AAF rows are unchanged (`0xFFF`), and undeclared indices still answer
   NO_SUCH_DESCRIPTOR with the empty body (the processor is the existence authority).
3. `crf_dirty_p_w` reaches the Table 5.22 descriptor arbiter as {STREAM_INPUT, `N_STREAMS`}.
   The STREAM_INPUT pending vector is now `PP_CTR_SIN_N_C` wide, and the processor's
   `KL_aecp_notify` already accepts index < `N_STREAM_IN_P` (= `ACMP_SINKS_C`).
4. `sim_nxn.cpp` `[CTRS-CRF]` (every broad leg) and `[NOTIFY-CRF]` (timed `obj_notify`),
   each shown red under eight wiring mutants (table in `RECEIPTS.md`).

## Next steps for the coordinator

1. Push the branch, then open the PR as a draft with `PR-BODY.md`.
2. Run the trusted-dev `act_ci.py --pr <n>` replica and post local self-test evidence as a PR
   comment (the numbers are in `RECEIPTS.md`).
3. Assign an internal cleared-context reviewer and an external reviewer. Every AGENTS.md lens
   is still open.
4. After merge: bench confirmation that a Milan controller rates the entity Milan-compatible
   (#117 acceptance 4).

## Decisions and assumptions to review

- **Mask and layout.** The prompt and REGISTER_MAP said "compact valid mask". This lane
  serves the IEEE Table 7-157 offsets with `0xF3F`, not a compacted quadlet 0..9 layout.
  Milan's Stream Input table keeps the IEEE offsets, and only the Stream Output table
  (5.17) compacts. That is also the repository's counters contract, and it is what a
  controller decodes by bit position. If a reviewer reads Table 5.16 differently, the
  change is one case table and one constant.
- **No VERSION step**: following the existing unreleased CHANGELOG entry, the release step
  owns the bump. Flag it if the maintainer wants this lane to reserve a minor.
- **Port budget regeneration** also dropped three `chan_tdm_render.*` rows that were already
  stale at base (tool-generated file; hand-editing it is not allowed).
- The `KL_crf_rx.sv` and datapath banner comments dropped a pointer to audit B3 as "the
  remaining CRF gap", because B3's CRF half was closed by #74.

## Not run here

`milan_dp_gptp` (physical-rate selection, longer than the foreground command limit),
`scripts/run_all_suites.sh`, the full Yosys bank, the `tdm8render-mutants` gateware campaign,
`act`/Docker, hosted CI, and the HDL reference build (pinned parser wheel not installed).
