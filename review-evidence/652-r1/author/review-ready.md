[A533] REVIEW READY
Commit: `2f0f59291080aeab934e0d72e124fb448c105e12` (branch `652-builder-names`, five commits on dev `6c22d3ca`, not pushed; round 1b adds four on `d33bdc3d`, no rebase or amend)

Changed:
- Ruling item 1 (`0da678f0`): `sw/builder/test_builder.py` gate 24a (d) runs at 8 routed capture channels (123 names, same subject). Gate 24a (e) asserts the over-wide pool (712 clusters, 747 names) is refused by `build()` before any write, naming both figures. It also tests the 16-bit ROM ceiling directly on that shape's overlay, and keeps the ceiling and `--write-rtl` path with the NAME capacity planted at 747. Each has planted controls. `docs/ENDSTATION_BUILDER.md` D8 restated: the NAME block refuses first, the ROM ceiling is the second limit.
- Ruling item 2 (`bcc31bcd`, `68e4d89a`): `syn/resmap/yosys_sweep.py shapes` records every builder outcome in `shapes/outcomes.json`. A refusal (exit 1, exactly one `CONFIG ERROR:` line, no traceback) is a refused point recorded with its line. Any outcome the plan does not expect fails the step: a crash, an unexpected refusal, or an expected refusal that builds. `rm_ax7101_8x8_tdm8` and `rm_ax7101_8x8_tdm8_2ch` are `"expect": "refused"`. `run` does not price them, and `summary` records them (it refuses a priced receipt for one). `resmap_models.py` counts them as refused, with no marginal. The refusals table gains a Refused by column. The #649 page's `guard-refusals` and `datapath-marginals` tables were regenerated through `resmap_tables.py --write`, and the page's prose was restated to match.
- Ruling item 3 (`2f0f5929`): `docs/design/SAVED_STATE_FASTCONNECT.md` 4.2 now reads names 39/107, records 54/164 and highest ids `0xA6`/`0xEA` (were 38/99, 53/156, `0xA5`/`0xE2`). `scripts/check_nvm_record_space.py` check 14 compares every figure in that table with the inventory it derives for the two shapes the columns name. `--mutate=stale_allocation_table` is its negative control.

Validation (head, tree clean, pinned Verilator 5.050; each unpiped with its own log):
- `python3 sw/builder/test_builder.py --require-rv32`: rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11: no Arty `mf48` build tree on this host). Gate 24a (d) 2/2 and (e) 2/2 planted controls red; gate 38 9/9.
- `check_nvm_record_space.py`: rc 0, check 14 clean. Against the page as it was: rc 1, exactly the six stale figures. `--self-test`: rc 0, 19/19 controls red.
- `check_nvm_capture.py`, `test_nvm_firmware.py --self-test`, `check_entity_shape.py`/`check_sweep_shape.py`/`check_deploy_shape.py`/`check_wire_accountability.py --self-test`, `gen_aem_store.py --self-test`: rc 0 each.
- `yosys_sweep.py`, `resmap_models.py`, `resmap_tables.py`, `resmap_map.py`, `soc_sweep.py --selftest`: rc 0 each. Ten planted defects in the new resmap code each turned a self-test red.
- `yosys_sweep.py shapes`: rc 0, 7 built and 2 refused as expected. A plan without the marks gives rc 1; a plan expecting the 2x2 to be refused gives rc 1.
- #649 page, from that lane's published inputs: the base `summary` reproduces the published `summary.json` byte for byte (`8f8060f5...`). This head's `summary` refuses #649's priced receipts for the two refused points. Over the other 57 it gives identical entries. Every fit is unchanged. `--page ... --write`, then the check: "every table equals a fresh generation", rc 0.
- `make -C tb/verilator/{nvm_backend,nvm_cosim,fw_service_budget}`: rc 0, 751, 465 and 52 checks.
- Docs and ratchets: `docs_check`, `check_em_dash --base 6c22d3ca`, `check_doc_style`, `gen_toc` (self-test, anchors, check), `check_doc_paths`, `check_archive`, `check_feature_status`, `gen_module_matrix`, `DOC_MAP.gen`, `check_solution_docs`, `check_baremetal_only`, `check_py_idiom`, `check_sv_idiom`, `check_hygiene`, `measure_fail_fast`, `check_port_contracts`, `measure_naming`, `check_todo_ownership`, `measure_test_evidence`, `lint_rtl --check`, `check_soc_sources`, `check_rtl_source_lists`: 33/33 rc 0.
- Byte identity: every artifact of the five tracked configurations was regenerated at the head and is identical to the base (120 files, `cmp` and `diff -r` rc 0). `git status` stays clean.
- Not re-run, with reasons in HANDOFF section 5: the full Verilator sweep (59/59) and Yosys (55/55) ran at `d33bdc3d`, and no RTL, testbench, builder or configuration file changed after it. `nvm_capture_cpu` is a LiteX CPU measurement (its hosted gate `check_nvm_capture` is rc 0). Hosted CI and `act` were not run (no push).

Acceptance criteria:
1. Refused at generation, capacity read from `KL_nvm_backend.sv:247` (`N_NAME_MAX_C`), never mirrored, both figures named: met (gate 38; D8 and gate 24a now agree with it).
2. Boundary 128 accepted, 129 and 235 refused, each check with a planted control that fails it: met.
3. Tracked configurations build unchanged: met (byte identity above).
Ruling items 1 to 4: met, as listed above.

Open risks/questions:
- `scripts/nvm_contract.py` `ALLOC["NAME"] = (0x80, 128)` restates the NAME block for the record-space gate's check 3. It predates #652 and is unchanged; this is a possible follow-up.
- The regenerated #649 tables reuse #649's Yosys records for the 57 priced points. Their shape headers are byte-identical at this head, and nothing was re-priced. The two refused points' #649 run receipts stay on the page as history.
