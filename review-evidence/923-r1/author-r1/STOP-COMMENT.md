[A789] STOP (#923 and #924): the 8x8/1if platform image needs 56.5 RAMB36, past the 56 that no ledger entry lets a product build exceed

**The question.** May the target platform's 8x8/1if image, a shipping image, plan 56.5 RAMB36 as S14 debt? If yes, by what mechanism? The product SoC build plans every image to the 56-RAMB36 budget and names no ledgered point (`sw/litex/milan_soc.py` `add_ctrl_memory`, `ctrl_memory.plan`). The owner's flip criterion of 2026-11-12 holds every point except the two 8x8/2if ones at or under 56 (`docs/design/SPLIT_CONTROL_MEMORY.md` section 5: "every SoC build is still refused past 56"). The assignment says an image over a **ledger entry** is not a stop: raise the entry. This image has no entry, so raising its limit means a new product exception and a change to the product build. No issue settles that.

**The images** (linked by `ctrl_srp_image.py` and `ctrl_plat_image.py` on one runtime and flash map; rom / sram bytes and planned RAMB36):

| Image | Base `16ba667d` | Head `def26a61` | Against its limit |
|---|---|---|---|
| platform 1x1/1if | 117,480 / 56,224, 43.0 | 119,648 / 56,224, 43.5 | within 56 |
| platform 8x8/1if | 130,184 / 97,328, **56.0** (888 B of rom spare) | 132,352 / 97,328, **56.5** | **over the 56 budget; refused** |
| platform 8x8/2if | 131,744 / 114,224, 60.5 (`ctrl_plat` 20,352 B) | 133,912 / 114,288, 61.0 (`ctrl_plat` 20,416 B) | over its entry of 60.5, the cap |
| size fixture 8x8/2if | 126,608 / 113,248, 59.0 | 128,784 / 113,248, 59.5 | over its entry of 59.0 |

Every other image stays within 56. The rom growth is the change's own code, 2,168 B at every platform point. In compiled text: `aecp_maps.c` +1,720 B (the command's commit 144 B; the boot commit of the restored maps, five functions, 1,124 B) and `aecp_face.c` +1,012 B (the `EDIT` window walk). A one-loop walk measured 216 B smaller. Even with the boot commit's refusal handling dropped as well, an estimated 1,270 B would remain, over the 888 B the image had spare. The command path alone, #923's first item, is an estimated 1,100 B. No compaction inside #923's scope returns the image to 56.0.

**Recommendation (A).** Ledger the target platform's 8x8/1if image at 56.5 RAMB36: half a tile, 1,280 B of rom owed to S14 (the move of cold code to flash, decision D3). The product SoC build would plan an image at its own ledgered point by its symbols, as the measurements already do by name. The memory tests, `plat_ledger.py` and section 5 would be updated with it. Under the assignment's rule, the two 8x8/2if entries are raised to their measured 59.5 and 61.0 (`ctrl_plat` 20,416 B), each half a tile of further S14 debt; the platform's goes past its 60.5 cap. (B) The alternative, the image held at 56.0, needs code moved out of the image, which is S14's work.

**State of the lane at `def26a61` (local; nothing pushed):**
- #923: an accepted ADD or REMOVE_AUDIO_MAPPINGS commits its changing mappings to the datapath's map store through the `EDIT` window before the core's map moves. It runs the release processor's transaction, and a store refusal is the command's answer. The restored maps reach the store when AECP opens. #924: SET_CONFIGURATION past configurations_count answers NO_SUCH_DESCRIPTOR, and SET_STREAM_INFO takes the 48-octet body. No RTL, mailbox contract or row bound changes.
- 14 new firmware unit tests and 29 planted defects, each caught by its named test on its words. The AECP app arm passes at one and two interfaces: 161 tests.
- Split co-simulation (`make -C tb/verilator/milan_dp twin-maps`, the platform firmware on the split datapath RTL): 21 checks pass. They cover an edited map reaching the render store, BAD_ARGUMENTS with the mappings in place, SUCCESS for 1, 2, 4 and 6 channels once they are removed, and a saved map restored at the next boot reaching the store. Its plant, the edit port cut (#923's defect), fails the store, format and edit checks by name.
- CPU budget harness, the edit groups: the largest legal command's record at 1x1/1if is 92,489 CPU cycles, 975 us by the rule, its stated 975 us unchanged. The one-row edit is 26,177 cycles, 275 us, under the paced class's 300 us, so no row moves. 0 budget misses and 0 passes over the share in those groups at 1x1/1if and 8x8/1if. The full runs at both points, the answering-ports arm and the firmware campaigns are still running.
- The release image is byte-identical: `bios.bin` at both configs, base and head.
- The 1x1/1if split image is queued for its route. The 8x8/1if image cannot be built until this is decided: the product build refuses 56.5.
