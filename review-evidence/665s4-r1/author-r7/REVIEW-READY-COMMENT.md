[A698h] REVIEW READY

Commit: `37e0393094e62d395edc2798a6a6da2f34badbec`, local branch `s4-f1-target` (`665-s4-f1-target`, PR #812). Local only: nothing pushed. It is `7643aef613` plus four commits, no rebase, no force. Merge base `a68536fa`, still the tip of `dev-soft-core`.

Changed, against [A10]'s four items (issuecomment-6689759393):
1. **No silent placeholder image.** `ctrl_plat_image.py` refuses a link with no `--flash-map` by name, exit 2, before it compiles, whenever a runtime archive exists. The boundary gate's compile is left alone: its archives do not exist, so it stops at its link with no ELF, and `ctrl_runs.py` is unchanged. `sw/firmware/ctrl/plat/README.md:88-102` carries the map in its command and says where it comes from: `gen_flash_port.py`, from a product split export.
2. **R738-4 F2.** `nvm_split_target/README.md:158` and `ctrl_nvm/README.md:338` give 13.861 ms. PR body lines 53, 98 and 99 are restated.
3. **R738-4 F3.** `ctrl_split_boot/run.py --placement-controls` is the committed negative test, and it runs last in `--self-test`. `boot_soc.build` must refuse a moved register in its own words, and `map_deviations` must accept the true map and name each edit. Two planted defects of the refusal are in the tree and print `PLANT guard-removed: caught` and `PLANT deviations-empty: caught`.
4. **PR body line 213** states what is now true.

Beyond the items, each because the items required it:
- `docs/design/SPLIT_CONTROL_MEMORY.md:319` was a second documented no-map link, listed by neither review. It would have been refused as written, so it carries the map.
- `sw/firmware/ctrl/README.md:711` quoted the self-test's count, now 37, which moved the head once. Every gate here ran at the final head.
- R737-3-R1, R737-3-R2 and R738-4-RES2 are applied, because those lines had to change.

Validation, all rc 0 at this head on clean clones, tree clean after each:
- **The reviewer's `nomap_probe.sh`, unedited:** `no-map link rc=2`, the named refusal, no ELF.
- **Each page's command, taken from the page's own fence and run unedited:** exit 0, with no `lui 0xf0004` and no `lui 0x20000` in `ls_*`. 39.0 tiles at 1x1, 59.0 ledgered at 8x8 with two interfaces. The same scan on a no-map image from `7643aef613` finds 4 and 1, in the functions the reviews name, so it can fail.
- **`firmware_boundary`, both modes:** `ctrl_boundary: PASS`. In each, `ctrl_image_selftest.py: exit 0`, and every `ctrl_plat_image.py` run printed `stopped at its link`.
- **S3's split boot:** `ctrl_split_boot: PASS (0 finding(s))` at both shapes, ready at 84.372 and 184.622 ms, 4,218,617 and 9,231,088 CPU cycles, 18 of 18 writes: equal to round 6's. Self-test: `6 of 6 native controls as required; 2 of 2 plants caught; 0 placement controls wrong`.
- **`--placement-controls`, both shapes:** `8 of 8 as required`. **`ctrl_image_selftest.py`:** `37 checks PASS`.
- **Nine literal mutants in a scratch clone:** `9 planted, 0 escaped`, including R738-4's two: the guard's call removed gives `PLACEMENT export-refuses: WRONG (export TAKEN)`, and `map_deviations` returning empty gives `PLACEMENT register-moved: WRONG (deviations [])`.
- **The reviewers' own scripts:** `refusal_probe.py` `misses: 0`; `portable_checks.sh` every line rc 0.
- **Docs:** `docs.yml`, every job on a fresh clone with an empty `HOME` and a new virtual environment: 71 steps ran, each rc 0; 24 not run, each with its reason. All three SDK steps downloaded the archive, verified the pinned `d42680e9...` and printed `SDK fresh installation: verified`.
- **`check_nvm_capture.py`** rc 0. `rg '13\.863'` finds it only in `SAVED_STATE_SNAPSHOT_OWNERSHIP.md`'s history.
- **`git diff --check a68536fa`** rc 0, one merge base, **privacy check at 0**.

Acceptance criteria: the four items are met, with the evidence above. R737-3-F1, R738-4-F1, F2 and F3 are answered at this head and await re-review.

Open risks and questions:
- **For the manager: does "any split image" reach the size fixture?** `ctrl_srp_image.py --layout split --with-aecp` still links on the stand-ins with no map, and the design page documents it. I left it: it is a separate builder and not a booted image, and `build.flash_map` needs it to make the first export the map is read from. Refusing it would break the map's own generation.
- **One gate attempt failed, cause not found.** `firmware_boundary`'s first attempt, at the ancestor `c2befb12`, was refused because `test_ctrl_firmware.py` exited -15, a SIGTERM, 212 s in. Peak memory was 1.4 GB, the journal shows no kill, and the docs step beside it has no signal call. The passing run overlapped that same step, so the overlap does not reproduce it. Both modes pass at this head on fresh clones. The log is kept.
- The placement controls need the product LiteX tree, so no hosted job runs them (R738-4-S2 stands). The refusal's control does run hosted, inside the firmware boundary job.
- Not re-run: the 97 short gates, the other long gates, S2 and S4 at either point, and the D5 plant. The assignment's gates are those this delta touches, and `split_soc.py`, the firmware C and the RTL did not change.
- Left for the checklist: R738-4-RES1, R738-4-RES3 and the retained residue.
- Still open from round 6: the gate environment's SDK is not the pinned build, and this round's figures used it; S2's 8x8 page needs an owner.
