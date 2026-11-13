# The third STOP: firmware-stated costs under the composed tree's measurement

Head `525375d649132fe82eb6e18ccdaad7cdb2c8982a`. The legs and controls ran at `da1869a311ba8819157404f7123d3fe6435ebf7a`: the same firmware and build inputs, with the harness's flash device held to the flash map's journal. The two commits after it change the save grader, the self-test and docs only, so no build is stale.

## legs/

Each finished leg's verdict lines (`HEAD`, `STATED`, `REFUSED`, `SAVE`, the graded line):
- GN8, GN1: the `answering-every-port` arm, every group;
- GB8, GB1: arm B's `aecp` group;
- the four cost controls at 8x8/2if, all caught.

GA8 and GA1 (arm A, every group) were still running. `GA8-finished-groups-regrade.txt` and `GA1-finished-groups-regrade.txt` re-grade their finished groups from each leg's own clone (8 of 93 at 8x8, 12 of 94 at 1x1).

No finished leg has a save group yet. The 1x1 verification run of `save-second` at `da1869a3` was refused: "the save programmed 3444 bytes, its image is 3446" (`../rtl-fix/journal-bound/`). That is the grader's KLJ2 record header, fixed at `3e67f9ca`; the re-grade at the final head reads the logs again.

## Over a firmware-stated cost (ctrl_loop.h, aecp_mbx.h: each the heaviest measured plus 5 %, rounded up to 5 us)

| Cost | Point | Stated | Most measured | Where |
|---|---|---|---|---|
| `CTRL_LOOP_BUILD_ONE_PASS_US` | 1x1/1if | 405 us (40,500 cycles) | 40,700 cycles | GB1 `aecp`. Every arm A group at 1x1 so far: 40,504. GN1: 40,585 |
| `AECP_ROUND_COLD_US` (with `AECP_ATTEMPT_US` 34) | 8x8/2if | 165 us | a round of no notice and 2 refused attempts at 24,816 cycles, against 23,300; implied cold cost 180.16 us | GN8 `notice-every-4`: 14 rounds over in all, 8 with k=2 and 6 with k=4 |

The rule's figures are 40,700 x 1.05 rounded up to 5 us, which is 430 us, and 180.16 x 1.05 rounded up, which is 190 us.

## Over a grader table (poll_grade.py; the standing rule restates these)

| Cost | Point | Stated | Most measured | Rule's figure |
|---|---|---|---|---|
| a pass's polls base | 1x1/1if | 155 us | 17,111 cycles (`acmp-notk`, arm A) | 180 us |
| a pass's polls base | 8x8/2if | 280 us | 30,659 cycles (GN8 `notice-burst-4`) | 325 us |
| an SRP record's apply | 1x1/1if | 260 us | 26,067 cycles (GN1 `notice-every-7`) | 275 us |

## retry-search/

`ctrl_retry_search.py` on a copy of `sw/firmware/ctrl` at this head. `at-525375d6-as-committed.txt` is the committed constants; the firmware tree is the same at `3e67f9ca`. Each `what-if-*` file changes one constant in the copy:

| Copy | Result |
|---|---|
| as committed | PASS |
| `CTRL_LOOP_BUILD_ONE_PASS_US` 1x1 at 430 | PASS |
| `AECP_ROUND_COLD_US` 2if at 170, 175, 180, 185 | PASS |
| `AECP_ROUND_COLD_US` 2if at 190 | FAIL: "the first notice at 2 interface(s): 28 ms over AECP_QUEUED_FIRST_MS" (stated 22 ms) |
| both at 430 and 190 | FAIL: the same words |
