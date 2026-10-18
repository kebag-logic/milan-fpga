[A649]

# Publish thisClock and {thisClock} from reset until a peer is elected

Refs #82

## Problem

Until a first gPTP peer appeared, the engine published grandmaster 0 and an empty path. The
published GM reset to zero, only the microcode wrote it, and the path count was forced to zero
while the GM was zero. The parent's shadow copies the bank only on `pub_commit_o`, so
GET_AVB_INFO and GET_AS_PATH served the same zeros.

IEEE 802.1AS-2020 10.3.13.2.4 b) makes an instance with no port vector its own grandmaster,
and i) then sets pathTrace to {thisClock}.

## Change

The change is RTL-only. The ROM image is byte-identical and no microcode moved; the ROM has 8
free words, not enough for a boot leg.

- `hdl/top/KL_gptp_engine.sv`: while no grandmaster has been elected since reset (the raw GM
  is still at its reset value of zero), the outputs name thisClock, path count 1 and an
  all-zero tail. thisClock comes from the existing S_CID mirror, which the init leg writes and
  a warm reset keeps. The raw publish bank, and every microcode read of it, is unchanged.
- The engine raises one commit of its own after each reset, once thisClock is known and the
  microCPU is idle, so it never splits a handler's staged writes from that handler's COMMIT.
  A microcode COMMIT that comes first cancels it.
- BTCA is untouched. A better peer replaces both, and when it falls silent, the existing
  receipt-timeout mastership path publishes thisClock and {thisClock} again.
- Docs: a new "Before any peer" section in INTEGRATION; additions to the HDL and test
  guides; two moved evidence anchors.

## Interface

There are no port, parameter or width changes. Parameter and port declarations are
byte-identical to the parent's current pin. The commit is still a single-cycle pulse over
stable outputs. Parent identity and flags keep their reset values at boot. For the parent's
shadow, the boot commit is a GM edge from 0 to thisClock. So `pub_disc_o` pulses once and the
path generation advances once after each reset.

## Timing seen by the consumer

- Warm reset: the commit lands one cycle after reset release.
- Cold start: thisClock is a ROM constant installed by the first one-second timer beat. The
  commit follows that beat, measured at 1.2003 s after release. Before it, outputs stay zero,
  as before. Closing this window needs the identity at reset (a parameter or port) or ROM space
  that does not exist. That is why this PR refers to #82 rather than closing it.

## Tests

The engine suite has ten new checks: 1623 per image (was 1613), three images.

| scenario | phase | checks |
|---|---|---|
| boot, cold reset, no peer | 1d | a commit lands with the first beat; it names thisClock; its path is {thisClock} |
| boot, warm reset | 35 | a commit follows the release at once; it names thisClock; its path is {thisClock} |
| a peer wins from the boot state | 35 | its commit names the peer GM and carries its three-entry path |
| that peer falls silent | 35 | the mastership commit names thisClock with path {thisClock} |

Each check has a planted mutant that fails it, and the mutation arm now requires every #82
control to fail each check it names: boot publication restored to zero; no engine commit after
reset; thisClock hides an elected peer; an elected peer keeps the self path; becoming
grandmaster keeps the departed GM; becoming grandmaster keeps the departed path. The arm is
39/39 (was 33/33). Against the base RTL the new harness fails exactly the six boot checks.

Repository gates are rc 0 at base and head: contract, lint, docs, microCPU 768, parser 337 +
9/9, engine as above, gaskets 81 + 5/5, tsngen 288 + 4/4, bench tag.

Parent consumer gates on dev `e9cbb676`, with the gitlink set to this head in the index only:

- Elaboration of `milan_datapath`, `KL_pp_shadow` and `KL_gptp_shadow` passes (+12 cells in the
  plane).
- The ratcheted lint, port-contract and wire-accountability checks pass.
- `gptp_shadow` 309/309, `gptp_tables` 36, `gptp_txts` 85 + 6/6, `gptp_plane` 29 + 62 + 8.
- The field campaign passes 677/0.
- `milan_dp` plane-on legs: `gptp` 182/182, `gptp-lat` 182/182, `gmstep` 190.
- The gPTP docs check and the ROM-digest ledger need the usual pin-bump edits. Applied in
  scratch only, they pass, and the ledger row carries the same digest as the current pin.
- Not run at head:
  - the `gptp_shadow` and `gptp_tables` mutant arms, which refuse an uncommitted gitlink by
    design (they pass at base);
  - suites whose deadline exceeds the review window: the full `milan_dp` run, physical gPTP,
    `capture_coherence`, `milan_dp_mclk` and `milan_dp_render`.

## Known limits, unchanged by this PR

- Mastership on announce receipt timeout still requires asCapable. If asCapable falls before
  the elected peer's Announces stop, the departed peer stays published.
- From reading the code (not tested): after a warm reset the scratch best record survives, and
  an Announce worse than that record re-publishes it.
- gm_present stays 0 at boot. Whether it should follow 10.3.13.2.4 g) is a separate question.
