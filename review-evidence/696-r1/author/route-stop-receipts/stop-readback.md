[A570] STOP — exact head `39571196045ddcc881f9ad0957742537175441d6` (clean, local, not pushed)

Ruling 6080332335 is applied. Both consumer pages are corrected in `963ad3b8e`. The shared-buffer M6 and M3 fit the `g_maap.maap_engine` ceiling and are committed: 441 LUT / 340 FF in the 1x1 recipe OOC, +2 LUT / +60 FF against `6aa25dec`. M3 adds a 32-bit generator with period 2^32 - 1, seeded at first enable from MAC plus the existing PHC. Focused evidence at the committed RTL: 171 unit checks, three real-datapath checks, 49/49 planted defects caught plus two controls, 215/215 coverage lines, and a differential with 12/12 cases and 17/17 defects.

**The shipping route misses its WNS floor, so the endpoints cannot be re-recorded and the resource gate cannot pass at this head.** The recipe ran at the head under the exclusive lock, with `--single-thread-synthesis` and `--integrated-clock` (flow identity F):

| Endpoint | Measured at the head | Gate vs the #686 record |
|---|---|---|
| `route-1x1` | LUT 50,302 (-89), FF 54,329 (+66), slice 15,769 (-19); RAMB36 74, RAMB18 27 and DSP 14, all unchanged; WNS **+0.029 ns** (record +0.241), WHS +0.015 ns; 101,206/101,206 nets routed | **exit 1**: WNS below the 0.03 ns floor; every resource within tolerance |
| `ooc-1x1` | every figure equal to the record | exit 0 |
| `ooc-8x8` | every figure equal to the record | exit 0 |

- **Worst setup path:** `milansoc_crg_clkout0` (10 ns), slack +0.029 ns, 19 logic levels, 75 % routing delay. It runs entirely inside the soft CPU's DMA bridge, from `dma_bridge_write_bridge/aligner/downW_header_reg[3]` to `onPerId_bridge/pendings_valids_reg[0]`. No cell on it belongs to `KL_maap` or `milan_datapath`.
- **MAAP in the route:** `KL_maap` is 425 LUT / 339 FF (the #686 record: 429 / 279). The route's gated sub-block movements all lie inside the processor wrapper. By definition every MAAP path has at least the design WNS. A MAAP-only timing query was cancelled before it took the contended lock.
- **Input checks:** all repository inputs (122 for 1x1, 119 for 8x8) were byte-identical to the head, every image matched its manifest, and the input hashes were equal before and after the run. Zero `Synth 8-4445` diagnostics.
- **Nothing is recorded.** `syn/ooc/pp_resource_baseline.json` is unchanged and no `record --write` ran. Recording a route below the floor would be a policy change, and the failing logic is outside this lane's RTL scope.

Also relevant: remote dev is now `7c1b52be`. It re-recorded the gate in `4640d995` and changes `milan_datapath.sv`, so the candidate merge's image differs from this head in any case (AREA_BUDGET.md: each PR measures the three endpoints on its merge result). Merging or rebasing is outside this lane's authority.

**Decision needed** on the route floor. Options:
- (a) accept this measurement as placement variation and record it with a floor exception;
- (b) leave the records alone here and re-measure on the candidate merge with dev;
- (c) something else.

I recommend (b). The failing path is in unchanged CPU logic, every resource is within tolerance, and the merge result is the image that must carry the record. The three measurement directories are retained, so (a) needs no re-measurement.

**Not run at this head, and not claimed:** the parent suite bank and the parser. The previous session's attempt at `a872917ca` ended with that session; historical parent results at `963ad3b8e` were 60/60. Portability, lint and behavior passed at `a872917ca`; `395711960` changes only a comment.

`HANDOFF.md`, `PR-BODY.md` (`Relates to #696`) and the route receipts are in the assigned output directory. The tree is clean with eleven local commits. No push. No job remains running.

