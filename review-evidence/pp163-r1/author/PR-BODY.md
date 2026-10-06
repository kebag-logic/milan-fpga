[A553]

Relates to #163

The transmit arbiter's slot and state registers were fed by cones of up to 51 logic
levels at the 50 MHz clock (OOC 1x1, #638 recipe: WNS -3.562 ns, all 16 failing endpoints
in the arbiter). Two structures made them deep, and this PR cuts both:

1. **The originator's withdraw mask is registered at the top** (`org_withdraw_mask_r`). The
   mask is combinational from the originator's response, cancel and expiry choice. It fed
   the originator lane's request, the lane-queue compaction and the arbiter's
   `start_abort_i`, so the registry's identity index (`wr_ix_r`, `rows_r`), the receive
   validator's header (`hdr_src_mac_r` and the other header fields) and the response CAM
   all reached the arbiter. All three readers now take the registered copy together.
2. **The arbiter ranks its requesters in parallel.** The best-so-far scan chained its
   compares through all eight lanes (17 levels ahead of `slot_r`). The winner is now the
   eligible requester no other eligible one outranks, with ties to the lowest index. It is
   the same function: a sequential equivalence proof of the old and the new module closes
   every point, and `tb/tx_arbiter` and its five recorded mutants are unchanged.

No port, register map or parameter changes.

## Measurement, OOC 1x1 at 50 MHz

| | Before | After |
|---|---:|---:|
| Deepest path into the arbiter (logic levels) | 51 | 16 |
| Paths into the arbiter above 20 levels (worst per start/end pair) | 146,535 | 0 |
| Startpoints in the arbiter's input cone | 1,631 | 328 |
| WNS (ns) | -3.562 | +3.337 |
| TNS (ns), failing endpoints | -37.519, 16 | 0.000, 0 |
| WHS (ns) | +0.159 | +0.159 |

Before, the deepest sources were the notification `wr_ix_r` (51 levels, -2.981 ns), the
receive validator's `hdr_src_mac_r` (50, -1.795 ns), the registry `rows_r` (up to 50) and
the notification `pend_r` (47, -3.562 ns). After, the worst five paths into the arbiter
start at the registered releases (CA builder `cancel_release_slot_o`, 14 to 16 levels,
+11.912 ns). The cut cone now ends at the new register (`wr_ix_r` to
`org_withdraw_mask_r`, 28 levels, +7.229 ns), and the originator lane queue moved from 37
levels (+0.424 ns) to 14 (+12.303 ns). The design's worst path is now elsewhere
(`u_aecp/u_ucpu` to `u_aecp/u_d3`, +3.337 ns).

Area, OOC 1x1: processor -39 LUT and +10 FF; the top's own logic -159 LUT and +6 FF; the
arbiter +49 LUT and +0 FF. The resource gate passes at both revisions.

## The added cycle

A cancellation now reaches the originator lane and the arbiter's pre-start abort one clock
after the originator takes it. That is the same clock its registered release reaches the
slot pool. The race between a cancellation and the serializer's acceptance moves by one
clock:

- A probe whose cancellation lands on its acceptance clock is now sent. Its exchange is
  gone (no timer, retry or deregistration), the originator drops the acceptance, and the
  pool frees the slot after the frame's last byte.
- A cancellation on the selection clock still withdraws the probe, one clock later and
  before the pool starts it.

Graded with planted mutants:

- **`tb/pp_top` section WD** (`make withdraw`, and in the default run). It holds a
  solicited answer on its last byte until a CONTROLLER_AVAILABLE probe waits in the
  originator lane. Then it puts a superseding command's cancellation on the arbiter's
  acceptance clock (WD1) and on its selection clock (WD2, WD3).
  - `withdraw_unregistered` (the old combinational path) fails WD1 and WD2.
  - `withdraw_abort_ignored` fails WD2 and WD3.
- **`tb/aecp_notify` section CX.** The registry monitor's cancellation arrives in the
  command's own clock and in no later one, so the top's stage is the only added clock.
  - `cancel_one_clock_late` fails CX1 (and the existing IX3).

The three arms are in `notify_mutants.py`.

## Validation

At head `cd9825c947cf67b735d26cc1c42541ccd9d7f637` against base `86a7b0c5`:

- Before the RTL edit, every changed line was searched with `git grep -F` across
  `tb/**/*.patch`, every exact-text mutation table and the bench READMEs: no hits. All 283
  bench patches apply at base and head.
- `scripts/run_suites.sh`: rc 0 at both. Base has 1,028,235 checks and head 1,028,239,
  with 0 failing at both. Every suite is identical except `aecp_notify` (45 to 46) and
  `pp_top` (10,444 to 10,447).
- `scripts/lint_hdl.sh`, `make check`, `scripts/gen_matrix.py --check` and
  `syn/yosys/run.sh` all return rc 0 at both, with identical records. Yosys differs only in
  the lowered-netlist line numbers its warnings cite.
- Every campaign returns rc 0 at both, with identical records except the three new notify
  arms:
  - `d3_mutants` 110 of 110, `notify_mutants` 56 of 56 at base and 59 of 59 at head,
    `acmp_mutants` 33 of 33, `aecp_dispatch_mutants` 40 of 40 and `gsi_mutants` 20.
  - `aecp_mutants`, `ctr_mutants`, `name_wr_mutant`, and the `adp_engine`, `maap`,
    `srp_top`, `srp_admission` and `acmp_talker` retry campaigns all pass, with
    byte-identical driver logs.
  - `ix_new_identity_unset` now also fails the new CX1.
- Parent consumer set of 17 at dev `28f9666f`, with the 148 adoption patch and then the 22
  budget patch, run with the processor gitlink at base and at head: all 17 pass at both.
  - Every simulation tally is identical at both, and so are the source-list, port, naming,
    evidence, docs, lint, shell and xvlog verdicts (0 xvlog findings).
  - Two counts move with the new bench files: the Python idiom gate counts 31 more
    first-party lines, and the port-contract gate 6 more test-only hierarchical
    observations.
  - The builder reports, at both, the one calibration arm recorded before as not run (it
    needs a reference build tree).

The parent three-directive sweep on the merged pin (acceptance item 3's second half) belongs
to the pin adoption and was not run here, so this PR relates to #163 rather than closing
it.
