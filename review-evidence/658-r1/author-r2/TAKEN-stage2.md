[A539] TAKEN (stage 2)
Branch: `658-dynmap-default`, on top of `c36bfb03` (not pushed)
Authoritative references: #658 stage-2 ruling 5988843004; stage-1 STOP 5988813022; Milan v1.2 5.4.2.7 (SET_STREAM_FORMAT refusal kept), 5.4.2.26 and 5.4.2.27; IEEE 1722.1-2021 7.4.44 to 7.4.46; `docs/design/SAVED_STATE_MATERIALIZATION.md` sections 1, 5.2 and 8.4
Interpreted scope:
- The parent's input store and output owner/cluster registers reset to the identity image (stream channel c to cluster c, for c below the smaller of the channel count and the port's cluster count), computed from the existing `ADP_DMAP_*` constants.
- Until the restore releases AECP (`restore_done`), the parent holds that identity clipped to the live formats, both directions. A restored narrower format therefore leaves no orphaned mapping, nothing is notified, and the persisted format survives. No processor file.
- The capture and render RAMs follow through a post-reset writer on their existing AECP write legs, with one final sweep after the release. During that sweep the edit face holds (`wait` on phases 0/1/3/4, inside the processor's bounded timeout) and the CSR map window is refused. I chose this over leaf reset images because the clip needs the writer anyway; it needs no leaf, port, register or parameter change.
- Milan 5.4.2.7 refusal unchanged; docs per ruling item 4; tests per item 5 (`dynmap` green and in `run`, re-based empty-start sections, end to end both directions, the saved 4 ch restore case, the two planted controls).
Validation plan: full `milan_dp` suite, `milan_dp_render`, `lint_rtl.py --check`, `xvlog_gate.py --check`, `check_rtl_source_lists`, `pp_srcs.py --check`, Yosys gate and builder bank as the source lists require, docs gates; area by the OOC 1x1 recipe.
Blockers: none
