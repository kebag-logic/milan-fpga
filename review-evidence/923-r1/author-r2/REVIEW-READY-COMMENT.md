[A789] REVIEW READY (#923 and #924)
Commit: `70c100da` (branch `923-aecp-maps`, on `16ba667d`; local, the manager pushes)

Changed:
- #923: an accepted ADD or REMOVE_AUDIO_MAPPINGS commits the mappings that change the map to the datapath's map store through interface 0's `EDIT` window before the core's map moves, all or none (Milan v1.2 5.4.2.27, 5.4.2.28). A store refusal is the command's answer. The restored maps reach the store when AECP opens: each moved port's reset set leaves first, then each restored set joins it. Files: `aecp.h`, `aecp_maps.c`, `aecp_face.c`, `mbx.c`/`mbx.h`, `aecp_mbx.c`, `ctrl_app_aecp.c`.
- #924: SET_CONFIGURATION past configurations_count answers NO_SUCH_DESCRIPTOR (IEEE 1722.1-2021 7.4.7.1). SET_STREAM_INFO takes the 48-octet 2013 body (`aecp_commands.c`).
- Ruling (A) of issuecomment-6906679024:
  - `ctrl_memory.LEDGERED` gains the 8x8/1if platform entry at 56.5 RAMB36 (S14 debt). The 8x8/2if entries go to 59.5 and 61.0.
  - The product build plans a ledgered image at its own entry by its symbols (`own_point`, `add_ctrl_memory`).
  - The ledger tests, `plat_ledger.py` and the fit page's sections 3 and 5 follow.
- Tests:
  - 14 GoogleTest cases and 30 planted defects, each caught by its named test.
  - `twin-maps` and `twin-maps-plants` on the split RTL.
  - The coverage ratchet records the six changed files at 100 %.
- Harness (`split_soc.py`): `EDIT` answered at the contract's bound. Its verdicts are a constant on the port; at two interfaces they had read 0. The 8x8 two-interface plan holds its named point over the build's.
- Stated costs by the rule (`edit_rows.PACED`): the one-row edit is 295 us at 1x1/1if and 355 at 8x8/2if. No tier input moves. Section 13 and FR_NFR carry the base-to-head figures.

Validation (clean clones of `70c100da` unless named):
- Workflow jobs of `rtl-fast.yml`, `elaborate.yml` and `docs.yml`, step by step (`verify_wf.py`): 118 steps rc 0, 130 not run with their reasons, 0 bad, among them the AECP (329 of 329), SRP (421 of 421) and control (716 of 716) campaigns, `fw_coverage.py --check` (PASS, 39 files), the publication census and `ctrl_boundary.py`.
- Native 4-shard sweep (`scripts/run_all_suites.sh --wait --shard k/4`): every shard exit 0: 65 suites PASS, 2,713,040 checks, 0 failures, none timed out.
- `twin-maps`: 20 checks PASS. `twin-maps-plants`: the no-edit plant fails its 3 checks by name.
- CPU budget harness, full arm A at 1x1/1if (93 groups) and 8x8/1if (93, reported), and the edit legs of arm B. Firmware as at `def26a61`; the harness's later change is a no-op at one interface.
  - 0 refusals and no pass over THE SHARE at 1x1/1if.
  - The only budget misses are the seven `backlog-owed` held-egress rows, the base's and already ruled.
  - `record_classes.py` over every leg at both points: RESULT PASS (long 975/975, paced 295/300, ordinary 210/235 us at 1x1/1if).
  - `rows_tiers.py` prints the base's table; `load_grade.py --check` and `flip_grade.py --check --point 1x1/1if` PASS.
- Costs, base `16ba667d` to head, same legs:
  - 1x1/1if: one-row edit 23,877 to 27,866 cycles (295 us); largest legal command 86,698 to 92,714 (975, stated 975).
  - 8x8/2if: 28,627 to 33,481 (355); 126,152 to 132,751 (1,395, stated 1,650).
- Release image: `bios.bin` byte-identical at both configs (`679b4a44`; nothing it reads changed after).
- S9 split images, six head routes and two base routes at ExtraPostPlacementOpt:
  - 8x8/1if meets WNS and WHS >= +0.030 ns on all three directives (best +0.295 / +0.036). The base misses setup at +0.011 on #927's edit-claim enable.
  - 1x1/1if misses hold on all three (+0.015 / +0.014 / +0.014) on the TDM render FIFO crossing, as its base does (+0.014). Recorded as misses at the base, owed to #927 (ruling issuecomment-6923091710).
- Device and area:
  - 1x1/1if: 82 of 135 Block RAM tiles (base 81). LUT -74, FF -8, one RAMB36: the plan's RAMB18 for the new 2 KiB rom bank is placed as a RAMB36.
  - 8x8/1if: 92.5 tiles at both. LUT +52, FF +36.

Acceptance criteria:
- #923: met.
  - The edit and the restore reach the render store on the split RTL (twin-maps).
  - GET_AUDIO_MAP agrees after every command.
  - BAD_ARGUMENTS with the mappings in place, SUCCESS for 1, 2, 4 and 6 channels once they are removed.
  - Each check has a planted defect caught by name; branch coverage of the new code is 100 %.
- #924: met. Tested and planted; the 48-octet body is answered in the 84-octet form.

Open risks/questions:
- SET_STREAM_INFO bodies past 84 octets are still taken: #926.
- The 1x1/1if hold miss is #927's.
- Round 1's STOP counted 21 twin-maps checks; it is 20.
