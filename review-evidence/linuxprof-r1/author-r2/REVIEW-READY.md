# [A830] REVIEW READY: milan-fpga #983 / PR #986, round 2

Commit: `66b4def34dcbc0d371ce4eb339d3d0226875befa` (`pf-linuxprof-1`), one commit on `677d605f37c3a80654df1dd2cde053b57242845b`. Local, not pushed.
Answers: R900-1 ([PR #986 issuecomment-7099822461](https://github.com/kebag-logic/milan-fpga/pull/986#issuecomment-7099822461)), NEGATIVE at `677d605f`: F1 MINOR, F2 MINOR, R1 RESIDUE.
PR description: [PR-BODY.md](PR-BODY.md). Evidence: [receipts/INDEX.md](receipts/INDEX.md).

## Delta from 677d605f

`git diff 677d605f..66b4def3 --stat`: 3 files, +78 -13.

- `sw/builder/endstation_builder.py` `load_config`: the host dispatch reads `board.target` with `_req(brd, "target", "board")`, the call `_load_board` makes, instead of `brd.get("target")`. The TSpec comment now states the rule the code computes. No calculation changes.
- `sw/builder/test_builder.py`: gate 42 gains three rows (`board` = `[]`, `""`, `["ax7101"]` on the FPGA 1x1), 28 to 31. Gate 41 gains `_check_host_tspec`.
- `docs/ENDSTATION_BUILDER.md` section 6: the TSpec rule with its clause, and gate 42's malformed-board rows.

## Closure of each finding

**R900-1-F1 (MINOR; Conformance, Robustness, Tests): malformed board bypasses ConfigError.**
For any `board`, the dispatch now runs the same check as the base, at the same point in `load_config`, so the refusal is the same. `[]`, `""` and `["ax7101"]` each raise `ConfigError: board: missing required key 'target'` at `66b4def3`, as at `854bd723`. At `677d605f` each raised AttributeError ([host-image-result.json](receipts/host-image-result.json)). `adp_entity.py` on `board: []` exits 2 through its ConfigError path ([adp-cli-malformed.log](receipts/adp-cli-malformed.log)). Gate 42's three new rows fail under `677d605f`'s builder blob with AttributeError ([discriminate.log](receipts/discriminate.log)). The valid FPGA and host controls still load, and the five FPGA missing-owner plants stay.
Not changed, and out of this finding's scope: a `board` that cannot be iterated (`null`, an integer) raises TypeError at the base and still does. That is the base's own behaviour, not the host dispatch's. It could become a separate Issue if wanted.

**R900-1-F2 (MINOR; Docs): host TSpec documented as current-format.**
Decision: the rule is the conservative widest-format TSpec. The code is unchanged, and the docs and comment now state that rule.
- Clause: IEEE 802.1Q-2018 35.2.2.8.4 a) makes MaxFrameSize "the maximum frame size that the Talker will produce". MSRP changes no FirstValue (which carries the TSpec) of a declared StreamID short of a withdrawal and two LeaveAllTime periods (802.1Q-2018 35.2.2.8). Milan v1.2 4.3.3.2 Table 4.4 gives each format's value, and the profile takes the largest.
- Why the talker can produce the widest: the host runs the target's control firmware unchanged (`sw/firmware/ctrl/host/mbx_plat_host.c`). That firmware declares one fixed TSpec per source, from the generated table (`sw/firmware/ctrl/plat/ctrl_plat.c` `configure_sources`). SET_STREAM_FORMAT on a STREAM_OUTPUT is refused only while it is streaming (`sw/firmware/ctrl/aecp/aecp_commands.c` `running`, `SET_STREAM_FORMAT` path). So an idle output can move to any format it advertises while its declaration stands.
- FPGA difference: the FPGA's supply cap stays, because the fabric emits a fixed width. On the host, the widest advertised format is a frame the talker can actually produce. So the 2026-07-28 over-reservation lesson (a TSpec for a frame nobody sends) does not apply.
- Docs: section 6 states that the width is the widest `channels_per_frame` any talker advertises (`framer_declared_channels`), shared by every talker row at `clocking.sampling_rate_hz`, and not each talker's current format. The `load_config` comment says the same.
- Test: `_check_host_tspec` in gate 41 uses a talker whose current format is 2 channels and which advertises 2 and 8. It must reserve 217 octets (the 8-channel frame), not 73, and the unedited example must reserve 217. Under an in-memory current-format mutant it fails with 73 ([discriminate.log](receipts/discriminate.log)).
- Board image: the generated entity image for the board's `config/endstation_pb2_bridge.yaml` **does not change**, because the rule does not change the TSpec. It is 5784 bytes with sha256 `461aea466d30aaf1...` and talker MaxFrameSize 217 at both `677d605f` and `66b4def3`. The host example's image is also identical (`9a59e2741913d93e...`).

**R900-1-R1 (RESIDUE): PR body Status wording.** Replaced with the reviewer's sentence. Because round 2's head is local, one clause says so. See [PR-BODY.md](PR-BODY.md) Status.

## Validation at 66b4def3

| Check | Result |
|---|---|
| Gates 32, 41, 42 | pass: 116 == 116 keys; host TSpec 217 not 73; 31/31 refused (8 FPGA, 23 host) |
| Gate `test_bad_configs_rejected` | pass |
| New tests discriminate | gate 42 rows fail at `677d605f`'s builder; `_check_host_tspec` fails under a current-format mutant |
| FPGA identity, R900-1's `identity_probe.py`, 5 configs x own/split/all-fabric | 245/245 byte-identical vs `854bd723` and vs `677d605f`; tracked tree clean |
| Docs and quality gates (24) | 24/24 rc=0, incl. `docs_check`, `check_em_dash --base 854bd723`, bare-metal `--check` and `--selftest`, `check_py_idiom` |

Acceptance criteria (#983): still met. FPGA identity holds (245/245), the profile's image and ADP fields generate, and ENDSTATION_BUILDER section 6 now matches the code on TSpec.

Open risks and questions:

- The full builder suite was not re-run this round. Round 1's 114/115 stands at `677d605f`. Gate 1b, the firmware shards and the mutation campaigns are still owed by the manager on the final candidate.
- Pushing `66b4def3` will restart the hosted gates on the PR, which is not a draft.
- The `null` or integer `board` TypeError is pre-existing at the base (see F1).
