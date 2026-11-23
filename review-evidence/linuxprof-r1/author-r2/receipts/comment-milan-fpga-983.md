[A830] REVIEW READY

Commit: `66b4def34dcbc0d371ce4eb339d3d0226875befa`, `pf-linuxprof-1` -> `dev-soft-core`, one commit on `677d605f37c3a80654df1dd2cde053b57242845b`. Committed locally, not yet pushed. It answers R900-1 (NEGATIVE at `677d605f`, https://github.com/kebag-logic/milan-fpga/pull/986#issuecomment-7099822461).

Changed (3 files, +78 -13):
- R900-1-F1 (MINOR): `load_config` reads `board.target` with `_req`, the call `_load_board` makes. A `board` of `[]`, `""` or `["ax7101"]` again raises `ConfigError: board: missing required key 'target'`, as at the base; at `677d605f` each raised AttributeError. Gate 42 gains these three rows (28 -> 31, 8 on the FPGA 1x1). Under `677d605f`'s builder each new row fails with AttributeError. `adp_entity.py` on `board: []` exits 2 through its ConfigError path.
- R900-1-F2 (MINOR): the rule is the conservative widest-format TSpec. The code is unchanged; ENDSTATION_BUILDER section 6 and the `load_config` comment now state it.
  - Clause: IEEE 802.1Q-2018 35.2.2.8.4 a) (MaxFrameSize is the maximum frame the Talker will produce) and 35.2.2.8 (no FirstValue change for a declared StreamID short of a withdrawal and two LeaveAllTime periods). Milan v1.2 4.3.3.2 Table 4.4 gives each format's value; the profile takes the largest.
  - Basis: the control firmware declares one fixed TSpec per source (`ctrl_plat.c` `configure_sources`). SET_STREAM_FORMAT moves a non-streaming STREAM_OUTPUT to any format it advertises (`aecp_commands.c`), and the declaration stays in place.
  - Width: the widest `channels_per_frame` any talker advertises (`framer_declared_channels`), shared by every talker row at `clocking.sampling_rate_hz`; not each talker's current format.
  - Test: gate 41's new check uses a talker with a 2-channel current format that also advertises 8. It must reserve 217 octets, not 73, and it fails under a current-format mutant.
  - The board's `config/endstation_pb2_bridge.yaml` image does **not** change: 5784 bytes, the same sha256, MaxFrameSize 217 at `677d605f` and `66b4def3`.
- R900-1-R1 (RESIDUE): the PR body's Status sentence is replaced with the reviewer's wording, plus one clause that round 2's head is local until pushed.

Validation at `66b4def3`:
- Gates 32, 41, 42 and `test_bad_configs_rejected` pass: 116 == 116 keys; TSpec 217 not 73; 31/31 refused.
- FPGA identity (R900-1's `identity_probe.py`, 5 configs x own/split/all-fabric): 245/245 byte-identical vs `854bd723` and vs `677d605f`; tracked tree clean.
- Docs and quality gates: 24/24 rc=0, including `docs_check`, `check_em_dash --base 854bd723`, `check_baremetal_only --check`/`--selftest` and `check_py_idiom`.

Acceptance criteria: still met (generation, identity, docs).

Open risks and questions:
- The full builder suite was not re-run at `66b4def3`; round 1's 114/115 at `677d605f` stands. Gate 1b, the firmware shards and the mutation campaigns are still owed on the final candidate.
- A `board` of `null` or an integer raises TypeError at the base and still does. That is outside F1 and unchanged; it could become a separate Issue.
- Pushing will restart the hosted gates; the PR is not a draft.
