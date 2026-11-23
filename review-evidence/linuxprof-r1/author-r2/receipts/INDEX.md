# milan-fpga #983 round 2 receipts

Head `66b4def34dcbc0d371ce4eb339d3d0226875befa`, parent `677d605f37c3a80654df1dd2cde053b57242845b` (round 1, published), source base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`. Branch `pf-linuxprof-1`, local, not pushed. Every command ran in the foreground with `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR=receipts/scratch`. The tracked tree was clean after every run.

| Receipt | What it shows | rc |
|---|---|---|
| [gates-32-41-42.log](gates-32-41-42.log) | `test_builder.py --gates test_builder_doc_key_map,test_host_profile_feeds_the_generators,test_host_profile_refusals`: gate 32 116 == 116 keys; gate 41 now also reports that a talker advertising 2 and 8 channels at current 2 reserves 217 octets, not the current 73; gate 42 31/31 refused (8 FPGA, 23 host) | 0 |
| [gate-bad-configs.log](gate-bad-configs.log) | `test_builder.py --gates test_bad_configs_rejected`, the existing load_config refusal gate | 0 |
| [discriminate.py](discriminate.py), [discriminate.log](discriminate.log) | the new tests fail for their defects. The three malformed-board rows fail with AttributeError under `677d605f`'s builder blob. `_check_host_tspec` fails under an in-memory current-format mutant of `framer_declared_channels` (73 reserved, 217 required), and passes unmutated | 0 |
| [host_image_probe.py](host_image_probe.py), [host-image-result.json](host-image-result.json), [host-image.log](host-image.log) | `board` = `[]`, `""`, `["ax7101"]` on the FPGA 1x1: ConfigError `board: missing required key 'target'` at `854bd723` and `66b4def3`, AttributeError at `677d605f`. Host example and board `endstation_pb2_bridge.yaml` images: 5784 bytes, the same sha256 at `677d605f` and `66b4def3`, talker MaxFrameSize 217 at both | 0 |
| [adp-cli-malformed.log](adp-cli-malformed.log) | `adp_entity.py` on the FPGA 1x1 with `board: []`: `adp_entity: board: missing required key 'target'`, exit 2 (its ConfigError path), no traceback | 2 (expected) |
| [board-noniterable.log](board-noniterable.log) | `board: null` and `board: 5`: TypeError at `854bd723` and at `66b4def3` alike. This is base behaviour, outside F1, and unchanged | 0 |
| [identity_probe.py](identity_probe.py) (R900-1's, unmodified), [identity-result.json](identity-result.json), `identity-{854bd723,677d605f,66b4def3}.json/.log/.rc` | 245 FPGA builder, image and generator-header artifacts, 5 configs at own, split and all-fabric placements: 0 changed vs base, 0 changed vs `677d605f` | 0, 0, 0 |
| [docs-gates.log](docs-gates.log) | 24 docs and quality gates at the head, each rc=0. Includes `docs_check`, `check_em_dash --base 854bd723` (pinned renderer in a scratch venv, see [em-dash-venv-install.log](em-dash-venv-install.log)), `check_baremetal_only --check` and `--selftest`, `check_py_idiom`, `check_doc_paths` | 0 x 24 |
| [comment-milan-fpga-983.md](comment-milan-fpga-983.md) | the posted [A830] REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/983#issuecomment-7100207805 | posted |

Board input: `milan-linux/config/endstation_pb2_bridge.yaml` of kebag-logic/ti-sitara-am65x-bsp at `cce8c9a4143548c80800b2def821431ff45e3698`, fetched read-only to `../download/`. Git blob `9b0702b770e04c33e0650ffe3d1d6c4c8d83d2a3`, 3521 bytes, sha256 `c82d220a...02cd`. R900-1's receipt lists `55270fe0...f9e`. That is the sha256 of the same bytes with one extra trailing newline, so the YAML content is the same.

Intermediate result, kept: the first commit `fb021a13` failed `check_py_idiom` (`load_config` grew from 91 to 101 lines, over the 100-line limit). The in-function comment was shortened and the rationale left in ENDSTATION_BUILDER section 6. The commit was amended to `66b4def3`, and every receipt above was re-run at `66b4def3`. `identity-fb021a13` was discarded; it also showed 245/245 unchanged.

Not run this round: the full builder suite (round 1: 114/115 at `677d605f`), gate 1b to completion, the firmware shards and mutation campaigns, act, hosted runs. `scratch/` (venv and temporary files) is disposable and not publishable.
