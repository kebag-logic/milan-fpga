Source: https://github.com/kebag-logic/milan-fpga/blob/d50e88ad616414b573238b52bdbd23a3e3de07bf/review-evidence/640-m7-r1/author-r4/HANDOFF.md

## Round 4 continuation

Ruling: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6162175442

Starting parent `354f781828d8b4d73037129f297b072320a10f9c`, staged merge source
`fa8209889411e8ca95757174c981f720dbcd95a2`; starting donor
`6b5a4282586a3851117674891d1955253e3de452`, clean. Origin and original
`e8454e27` ancestry verified. Preserve the existing parent merge.

Authorized steps: split the donor clock self-test and document its nested
fixture evaluator; split four C++ declarations; correct the ROM budget and
FUTO location. Compare the 30 clock controls and 337 parser checks before
and after. Pass the parent Python/C++ gates without exceptions or budget
changes. Commit the donor correction and update the parent pin and generated
records, then commit the parent merge. Run the 26 table controls and all
parent gates recorded for Round 4.

No new physical measurement is required by this ruling. Every area/timing
number in sections 1, 5 and 6 belongs to its recorded historical revision.
The daily issue #640 measurement records the integrated effect the day after
the merge. No new physical acceptance is claimed.

Changes so far: `gptp-processor/syn/ooc/check_ooc_clock.py:269` separates
fixture definitions (`selftest_arms`, 95 lines) from execution (`selftest`,
30 lines at :366); `:376` documents `findings`. All 29 defect fixtures,
required findings and four clean fixtures compare equal, and production
function syntax trees match. The 30-control outputs also match.

`gptp-processor/tb/verilator/parser/sim_main.cpp:275`, `:1344`, `:1424`,
`:1496` split the four declarations with unchanged initializers. Its 337-check
output matches byte-for-byte (2,049 bytes, SHA-256
`f521be7f25439184b14991a9667aabeb05d84a3b98f27df2b6dbe2ea2e8e556c`).
`gptp-processor/docs/MANAGER.md:103`, `:105`, `:111`, `:113` now report
1,016/1,024 words (99.2%), eight free, SERVO in the prefix, FUTO@249 outside it.
The generator confirms those values and the unchanged default image digest.

Parent Python/C++ gates and their 54/75 self-tests pass without any budget
change. Donor contract/lint/docs pass. A first donor documentation invocation
caught one overlong sentence; the revised two sentences pass. The first
isolated workflow self-test could not find sudo in its container image; the
prepared CPython 3.12.3 image passes. Both attempts remain in scratch receipts.
CI scope and event-contract checks pass. All 35 parent static checks pass on
resolved tree `3a0b668761728b2e9fcc328f71f67f885ef3d11e`. The 36-check table
census and 29-check plane run pass. The original staged merge tree
`3112cc103cfa17756ee0b5ede78aa0bdc9a46627` is preserved except for the new
donor gitlink and its eight documentation pointers, generated diagrams and
ROM digest row (17 paths total).

Donor correction commit: `e4869fd0c42889b2ac806587cc5c78afb1c33461`.
Parent merge commit: `412e3f6c8c402bce63e94c291d2782b5579aaa1d`, parents
`354f781828d8b4d73037129f297b072320a10f9c` and
`fa8209889411e8ca95757174c981f720dbcd95a2`, tree
`3a0b668761728b2e9fcc328f71f67f885ef3d11e`.
Both repositories are clean. Neither was pushed. Existing commits were
preserved, with no rebase or amend.

The donor aggregate was deliberately interrupted after 415.9 seconds because
the full engine campaign would exceed the foreground command window. It has
no passing aggregate verdict. Its microCPU (768), parser (337 plus eight
mutants) and three engine simulation seeds (1,613 each) completed. All 33
engine mutation entries are being rerun in five disjoint batches of seven,
seven, seven, seven and five, each retaining the original positive control.
The driver source and verdict logic are unchanged. Remaining donor targets
will run separately. The PHC-step campaign passes all eight arms (62 clean checks); the shadow
run passes 309 checks. The 26 table controls all pass at the committed parent
in ranges 7/7/7/5, with no failed named checks. Remaining donor batches and
small constituent targets are still running.

Final heads, complete results and receipt hashes appear below. Progress notes in this section describe the sequence; the final results supersede their pending states.

### Continuation campaign scheduling

The per-command foreground window is shorter than the complete donor engine
campaign. The first aggregate was interrupted with no aggregate PASS claim.
The unmodified donor engine driver runs disjoint original index ranges
[0,7), [7,14), [14,21), [21,28), [28,33), each with its own original clean
control. Batch 0 passes eight checks (seven defects plus the clean control).
Driver SHA-256: `078d176b829cd21ed7f31339624a6b3d52db9fd113b68b7994a990217527e3d1`.

The table driver's committed-pin verification now accepts parent `412e3f6c8`.
It runs ranges [0,7), [7,14), [14,21), [21,26) under the same window. Its
input copier, simulator commands and named-failure verdict are unchanged.
Driver SHA-256: `c2e7cab57e000a73805190aa960d5277ef745c282ae9924220e91198a0c6594d`.
The native interpreter provides the pidfd support this driver requires.
Each batch uses no more than two compiler workers; no more than two simulation
builds run concurrently. All scratch and receipts stay on disk outside the tree.

The em-dash gate passes at the committed parent against dev `fa820988`,
including 339 planted controls. An attempted ROM check flag was refused as an
unknown top; the supported ROM-record command then passed and left the ledger
byte-identical to the committed record. This is not resource re-recording.

### Continuation parent static gate table

All rows below returned zero on tree `3a0b668761728b2e9fcc328f71f67f885ef3d11e`,
which is the committed parent merge tree. Logs and status files use the receipt
names below in `r4-resume/` under the existing scratch root.

| Command | rc | Receipt |
|---|---:|---|
| `python3 scripts/docs_check.py` | 0 | `docs.log` |
| `env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 | `docs-nogit.log` |
| `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | `gptp-docs.log` |
| `python3 scripts/check_gptp_docs.py --selftest` | 0 | `gptp-docs-self.log` |
| `python3 scripts/check_submodule_docs.py` | 0 | `submodule-docs.log` |
| `python3 scripts/check_submodule_docs.py --selftest` | 0 | `submodule-docs-self.log` |
| `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | `submodule-diagram.log` |
| `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | `submodule-diagram-self.log` |
| `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | `timesync-diagram.log` |
| `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | `timesync-diagram-self.log` |
| `python3 scripts/check_diagram_pngs.py` | 0 | `pngs.log` |
| `python3 scripts/check_diagram_pngs.py --selftest` | 0 | `pngs-self.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `module-matrix.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `doc-paths.log` |
| `python3 scripts/gen_toc.py --check` | 0 | `toc.log` |
| `python3 scripts/gen_toc.py --selftest` | 0 | `toc-self.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | `toc-anchors.log` |
| `python3 scripts/check_feature_status.py` | 0 | `feature-status.log` |
| `python3 scripts/check_py_idiom.py` | 0 | `py-idiom.log` |
| `python3 scripts/check_cpp_idiom.py` | 0 | `cpp-idiom.log` |
| `python3 scripts/check_sv_idiom.py` | 0 | `sv-idiom.log` |
| `python3 scripts/check_sh_idiom.py` | 0 | `sh-idiom.log` |
| `python3 scripts/check_hygiene.py --check` | 0 | `hygiene.log` |
| `python3 scripts/measure_naming.py --check` | 0 | `naming.log` |
| `python3 scripts/measure_fail_fast.py --check` | 0 | `fail-fast.log` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `evidence.log` |
| `python3 scripts/check_port_contracts.py` | 0 | `ports.log` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | `source-lists.log` |
| `python3 scripts/lint_rtl.py --check` | 0 | `lint.log` |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | `resource-baseline.log` |
| `python3 scripts/check_doc_style.py` | 0 | `doc-style.log` |
| `python3 scripts/gen_one_valued_table.py --check` | 0 | `one-valued.log` |
| `make -C tb/verilator/gptp_tables print-inputs` | 0 | `make43-inputs.log` |
| `make -C tb/verilator/gptp_tables limits` | 0 | `make43-limits.log` |
| `python3 syn/ooc/pp_resource_gate.py --selftest` | 0 | `resource-self.log` |

### Table campaign completion

At parent `412e3f6c8c402bce63e94c291d2782b5579aaa1d` and donor
`e4869fd0c42889b2ac806587cc5c78afb1c33461`, all four table batches returned zero:
7 controls in 122.7 s, 7 in 130.1 s, 7 in 122.7 s and 5 in 72.1 s.
Together they run every original index 0 through 25 exactly once. Every defect
failed the table's own named check. This is current-head evidence, replacing
the prior uncommitted-pin refusal, with no change to any test or declaration.
The clean run remains 36/36, including the eleven consumer-column censuses.

### Reproducing the bounded batches

Use the pinned build environment and disk-backed `TMPDIR`, with `MAKEFLAGS=w`
and `VERILATOR_JOBS=2`. These are runtime selections of the existing mutation
lists, not repository edits. From the parent root, the following command runs
one table batch; run it separately for `BATCH=0`, `1`, `2`, `3`. Use the native
interpreter with pidfd support. Each invocation returns the original driver's
exit status and verifies committed input bytes before creating private copies.

```sh
BATCH=0 python3 - <<'PYRUN'
import importlib.util
import os
from pathlib import Path
import sys

source = Path("tb/verilator/gptp_tables/mutants.py").resolve()
spec = importlib.util.spec_from_file_location("table_controls", source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert len(module.MUTATIONS) == 26
batch = int(os.environ["BATCH"])
assert 0 <= batch < 4
module.MUTATIONS = module.MUTATIONS[batch * 7:(batch + 1) * 7]
sys.exit(module.main())
PYRUN
```

For the donor's original 33 entries, run the same command separately with
`source = Path("gptp-processor/tb/verilator/engine/mutants.py").resolve()`,
expected length 33 and `0 <= batch < 5`, for batches 0 through 4. That driver
also runs its original positive control in each batch. The scratch launchers
add only source digests and index-range reporting. They are retained as
`r4-resume/table_chunk.py` and `r4-resume/donor_engine_chunk.py`; the final
audit checks every batch's digest, indices, entry names, verdict and exit code.
No mutation, assertion, acceptance criterion or source anchor was changed.

### Final continuation results

REVIEW READY at parent `412e3f6c8c402bce63e94c291d2782b5579aaa1d` and donor
`e4869fd0c42889b2ac806587cc5c78afb1c33461`. The parent is the authorized merge
of dev `fa820988` into `354f7818`. Its tree equals the gated resolved tree.
The donor correction is on top of the preserved `6b5a4282` merge. No existing
commit was rewritten. Both repositories are clean, with no push or PR edit.

The 35-row static gate table above is all rc 0. The following simulation and
contract results complete the continuation; all completed constituent targets
pass. The interrupted `make tb` aggregate is not represented as rc 0.

| Check | Result | Defect sensitivity / limitation |
|---|---|---|
| Clock checker before/after | 30/30 each; identical output, fixtures and required findings | Missing, wrong or late clock; wrong port/period; absent synthesis evidence; unclocked registers; critical warnings. Production function syntax trees unchanged. |
| Parser before/after | 337/337 each; identical complete simulator output | Error flags on first, interior and final bytes, writes after rejection and stale words in the next accepted frame. All eight original parser mutants caught. |
| Python/C++ idiom gates and controls | rc 0; 54/54 and 75/75 self-tests | Detect the imported long/undocumented function and four multi-declarator declarations. Long-function debt returns to 9; undocumented and multi-declarator findings return to zero. No budget or exception changed. |
| Table clean run | 36/36 | Five storage locksteps, explicit decode and all eleven column censuses. Result queue reaches depth two and 111 writes behind a waiting result. |
| Table mutation batches | 26/26, all batch rc 0 | Wrong depths/latencies/indices, wrong result write index, odd-count decode, undeclared stuck columns and incorrect declaration lists. Each fails its own named check. |
| Plane run | 29/29 | Publication, PHC and wire flags; positive regression, not a new planted campaign. |
| PHC-step campaign | 62 clean checks; 8/8 arms, rc 0 | Two passing controls and six defect arms (five distinct defects): stale rate window, crossed exchange, absent rearm/liveness and unearned credit. |
| Shadow run | 309/309, rc 0 | Integrated shadow regression; its separate mutation campaign was not repeated. |
| Donor microCPU | 768/768, completed constituent | Instruction and state-port regression; no new planted campaign in this target. |
| Donor engine simulations | 1,613/1,613 at each of three seeds | Protocol and servo behavior, high request/Sync counters. Completed before the aggregate interruption. |
| Donor engine mutation batches | 33/33 defects plus five clean controls; all rc 0 | Pair/result retention, ready/credit, loss handling, reset, step/slew thresholds and trim/integrator limits. The original driver requires named runtime failures for its slew arms and its original failed-harness verdict for the other arms. |
| Donor gasket suite | 81/81; 4/4 mutants, rc 0 | Truncated FIFO level, frozen RX/TX SFD toggles and missing end-of-frame. |
| Donor traffic-generator suite | 288/288; 3/3 mutants, rc 0 | Zeroed sequence ID, discarded grandmaster identity and early TX end-of-frame. |
| Simulated board-wrapper target | rc 0 | Two done toggles retain their tags; simulation only. |
| CI scope / events / isolated workflow self-test | rc 0 each; events 2,174 items | Scope/history classification, replay boundary and workflow event drift. Offline workflow test uses read-only source, no network/credentials/socket and CPython 3.12.3. |
| Pins, diagrams, ROM records and resource policy | rc 0 | Six exact gitlinks, eight gPTP pages, generated source-bound rasters and unchanged default ROM digest. Resource policy checks three endpoints; no new physical measurement. |
| Final batch audit | rc 0 | Exact original source digests, every index/name once, expected verdicts and rc 0 in every batch; no omission or duplicate. |

Final parent pin changes are at `docs/design/GPTP_PLANE.md:32`,
`docs/design/TIME_SYNC.md:115`, `docs/reference/SUBMODULES.md:24`,
`docs/traceability/ieee8021as.md:53`, and `docs/guides/gptp/`
`MANAGER.md:23`, `HDL_DEVELOPER.md:33`, `SYSTEM_INTEGRATOR.md:61`,
`TEST_DEVELOPER.md:30`. The generated diagrams and PNG manifest carry
`e4869fd0`; `syn/yosys/rom_digests.tsv:61` records its unchanged image digest.
The gitlink plus these documentation/generated paths are the only 17 changes
from the preserved staged merge. No resumed parent RTL or test source changed.

The historical primitive and M0s resource/route tables in sections 5 and 6
remain tied to their listed revisions in the `e8454e27` lineage. No new area
credit, route verdict or resource acceptance re-record is claimed. The ruling
assigns the merged-effect measurement to the daily #640 work after merging.
Independent reviews must cover these new heads; old positives do not transfer.
The full hosted/candidate-merge bar and post-merge containment remain later work.

The pinned compiler and make were unchanged. CPython 3.12.3 ran the usual
checks; native CPython 3.14.7 ran the table driver for pidfd support. Every
foreground gate invocation stayed under ten minutes. At most two simulation
builds ran concurrently, each capped at two compiler workers. The service's
reported peak was 8,463,949,824 bytes, below 9 GB. No vendor run or
physical access occurred.

### Additional exact commands

Commands below use the same environment as the static table. The workflow
self-test runs only inside the disposable container. `$SCRATCH` denotes the
external disk-backed evidence directory. No gate output was piped.

| Command | rc | Receipt |
|---|---:|---|
| `python3 gptp-processor/syn/ooc/check_ooc_clock.py --selftest` | 0 | `donor-before-clock.log` |
| `python3 gptp-processor/syn/ooc/check_ooc_clock.py --selftest` | 0 | `donor-after-clock.log` |
| `python3 gptp-processor/syn/ooc/check_ooc_clock.py` | 0 | `donor-clock.log` |
| `make -j8 -C gptp-processor/tb/verilator/parser run` | 0 | `donor-before-parser.log` |
| `make -j8 -C gptp-processor/tb/verilator/parser run` | 0 | `donor-after-parser.log` |
| `make -C gptp-processor contract lint docs` | 0 | `donor-static-fixed.log` |
| `python3 gptp-processor/hdl/ucode/gen_gptp_ucode.py -o "$SCRATCH/gptp-default.hex"` | 0 | `donor-rom.log` |
| `python3 scripts/check_py_idiom.py --selftest` | 0 | `py-idiom-self.log` |
| `python3 scripts/check_cpp_idiom.py --selftest` | 0 | `cpp-idiom-self.log` |
| `python3 scripts/ci_scope.py --selftest` | 0 | `ci-scope.log` |
| `python3 scripts/ci_events.py --check` | 0 | `ci-events.log` |
| `python3 -I scripts/act_ci.py --selftest` | 0 | `act-self-prepared.log` |
| `make -j8 -C tb/verilator/gptp_tables run limits` | 0 | `gptp-tables-run.log` |
| `make -j8 -C tb/verilator/gptp_plane run` | 0 | `gptp-plane-run.log` |
| `make -j8 -C tb/verilator/gptp_plane phc-step` | 0 | `gptp-phc-step.log` |
| `make -j8 -C tb/verilator/gptp_shadow run` | 0 | `gptp-shadow-run.log` |
| `bash syn/yosys/ooc.sh --record-rom-digests` | 0 | `rom-digests-record.log` |
| `python3 scripts/check_em_dash.py --base fa8209889411e8ca95757174c981f720dbcd95a2` | 0 | `em-dash.log` |
| `make -j8 -C gptp-processor/tb/verilator/gaskets` | 0 | `donor-gaskets.log` |
| `make -j8 -C gptp-processor/tb/tsngen` | 0 | `donor-tsngen.log` |
| `make -j8 -C gptp-processor/bench/arty test` | 0 | `donor-arty.log` |

Batch commands are reproduced above. Original failed attempts are preserved:
`donor-static` returned 2 for one sentence-length violation, then
`donor-static-fixed` passed; `act-self` returned 1 for a missing executable
in the first isolated image, then `act-self-prepared` passed; `rom-digests`
returned 2 for an unsupported option, then the supported generator command
passed without a ledger delta; `donor-tb` was interrupted after 415.9 seconds
and returned -2. All its completed constituents and every remaining target
now have passing evidence. None of those attempts is hidden or called a PASS.

### Continuation receipts

Scratch root: `$VALIDATION_STORAGE/640m7-a587/r4-resume/`. No receipt below was copied
to the output directory. Files over 200 KB remain outside it.

| Receipt | Bytes | SHA-256 |
|---|---:|---|
| `act-self-prepared.log` | 59168 | `6a28c53acbded43c63ca0ec57eb4fb5f58c1f0826a0a6d8a8bd539d364f6debe` |
| `act-self.log` | 18538 | `16d1d5c9beda06145bf44bc82e40e2bf33b0b673c1679199c9205ed7921206d5` |
| `additional-commands.json` | 1547 | `f3cd5b4446b032545980907e7cc3689e477dbddcfd66090deea91b7523be818f` |
| `before-after.log` | 170 | `9acfffc22ea54354ac9dc3d5d0250e60285457464a7df44d78b9ea5175d6e7df` |
| `campaign-audit.log` | 185 | `4f19513f696ec26fdcac668935f8e492c74254f3375d062d595892f7b20ef435` |
| `campaign_audit.py` | 2007 | `ab206920d63ca19efc7fe8819abce43d3f5da87c6d85cb345ade03af86db9734` |
| `ci-events.log` | 167 | `cbf7f2bb4fa19ca31b60e6e86d022a8f00176c252a015526d8ef299bd1933eb1` |
| `ci-scope.log` | 15329 | `be3ebff4df64fbd38d8a614ddb3be3ff889801c4531ac3a81747f7ae1185c010` |
| `clock-equivalence.log` | 114 | `71a824133bc57f6d55071644653d80066c79d8bc7b237d1d5de9b96ae94264b3` |
| `cpp-idiom-self.log` | 3593 | `7fd74c4ebf8b2f0a9812a20518981f63c8350a34c535bcde2c7fa6c58fbec2b9` |
| `cpp-idiom.log` | 316 | `7c773521653f1e4211a0bb3d719c5d2939de5ef85a8e22d4e83d3280de97c09c` |
| `doc-paths.log` | 85 | `7033b54b2784b7b8d9f1fc7da5b907a49ef6b6572f7579790e4ec9d6f48572ed` |
| `doc-style.log` | 47 | `1491d3f6bec03b920cf58f5fb28e6abff4a9d433a758bc0fe5d2db77bf4f53cd` |
| `docs-nogit.log` | 196 | `08a0ebc92d5f7c34c1af5243f7bc58aa869502fbc0eaf6e6e873add0ac7c820d` |
| `docs.log` | 128 | `afd69244ae6e7091eb4b64694f7d41e43df44ce57725a896bb48a551fdfd2584` |
| `donor-after-clock.log` | 41 | `99a0559caf79c40591b86d49bde93bcdd98a53230af48cbaa02cf09ee27ece09` |
| `donor-after-parser.log` | 4164 | `8b30ccc07db74c520df1ccd99031a01f7c778b719af8a3a716096e31e55cc15c` |
| `donor-arty.log` | 1064 | `4a79ec13b0b9ead7757c44d36f5030f864c1927b693f31fb164e77ad9b410745` |
| `donor-before-clock.log` | 41 | `99a0559caf79c40591b86d49bde93bcdd98a53230af48cbaa02cf09ee27ece09` |
| `donor-before-parser.log` | 3215 | `bdaca5979478959da8a1cce3e0bda3e5d9274404d90e762ea10b35ce519d24ae` |
| `donor-clock.log` | 68 | `95d7509d88fb0432367164d91a04052eea11195787c8cd4b986997967557c02f` |
| `donor-engine-0.log` | 1620 | `2604981321c078d91405adc884f58e2db7065336258f472355bb26bc394a9ae1` |
| `donor-engine-1.log` | 1195 | `3b698a40c76e15e54b7ff4215a3549374b222988c0d8849f6d1f7cb35a5f9f06` |
| `donor-engine-2.log` | 1171 | `f576ea6fd2f61cda020c44a831df6b79b68e824eb6898f3924d87433d6dec6e5` |
| `donor-engine-3.log` | 1063 | `b43b70fca6652082cd049776d69a8ed25708e6465b3dde3a12c061c8d9d9e6ef` |
| `donor-engine-4.log` | 841 | `e2e5420ae19ead00148e8989263746eb33ac52958bd9c70948a1baee2c281b4e` |
| `donor-gaskets.log` | 1876 | `4c9caf476954f74a3c807650a6e95ab98fd46a12c6e62ed7c394f02e5e0d333a` |
| `donor-rom.log` | 303 | `1dee52966fa53d4e5447bc1fe5a2d49a0db5c1d7e1640d1e5a01f612aa0b939f` |
| `donor-static-fixed.log` | 4270 | `ca3432bc23ce6e86ce8fd366aff86e1e55c866362dd73df62ab040e138f6f6eb` |
| `donor-static.log` | 2127 | `823d49fd17e888119f61f8aeff72de372f21dc3ff2356800252d35ea995cee3f` |
| `donor-tb.log` | 10362 | `483a5ad3ded85cdb8c2eb50b0ee5c8a24e819aa96dc11fa24099e4633f45a1ba` |
| `donor-tsngen.log` | 1877 | `c31c0e191ea69dbf2ed9ad1e66af577ff8b8ce0e094923226eababc15585bc7f` |
| `donor_engine_chunk.py` | 794 | `e5d25b85fb57204a3a48e43e54ce69d7b61cd7ad2896821460dbb9420566bd06` |
| `em-dash.log` | 141 | `a8a3f603a691dc4590c987b99d2a057236e3337b0fd283fba10241f8777a6829` |
| `evidence.log` | 18788 | `99be30210e18d0af8473388a5625b5174bbb7dc01f0809a9618917c2a8ac89b7` |
| `fail-fast.log` | 5967 | `88736e013ea360ab7771ca768e0227032b26f748c1f24c20f1a260b788a67d8b` |
| `feature-status.log` | 29 | `802f5eeb2f0aa147169f3ddb9c64d4369ca92ab380455195403f2e8ae02490d0` |
| `final-state.log` | 784 | `56022346517b5933678ecc1ce695b6434c3c0b088e162c5de2e43fb5992e15a9` |
| `gptp-default.hex` | 13312 | `a435fba6167238268fa9074dd4645dd03380e56ff1eeea273fd3fc2fcecab9fd` |
| `gptp-docs-self.log` | 46 | `200332e4eddfd8a6338d8a4dbe27d2f513de92f951a1aa1f6b25882182bc290e` |
| `gptp-docs.log` | 66 | `7ca87a8501c54854805f1cf90d49b2a8ff6353a1049fd21cf0631569f5024e41` |
| `gptp-phc-step.log` | 1907 | `7cb6fb858cf4868ee1db86d9dadef61fcba88dc3027d22ffdb202c278aae0942` |
| `gptp-plane-run.log` | 1668 | `0fbc2f1205b9e6fad8d0919c86918bd1aae080a72ac2495af2de8bd4524c5416` |
| `gptp-shadow-run.log` | 2330 | `cf57f1f963452630137af4a1abdfbd395f9fee549415b9d8294936ebaed3b8c9` |
| `gptp-tables-mutants-0.log` | 577 | `4c73a0626cc20e26d1ce9b4ed0a30b700816c2b02a0322e95c3de46e519ac1ed` |
| `gptp-tables-mutants-1.log` | 569 | `d91c9a5050bef623d3b23451b4aa88d4730a646a0efc4b791ce978d7cc20ca09` |
| `gptp-tables-mutants-2.log` | 567 | `e4b478436759a883133e3404a7a10361e4488a2acf2796b98cd91c02e888c5b3` |
| `gptp-tables-mutants-3.log` | 501 | `4315fa567286e3f823d97bde81bd59af951bf68f2c77f5b0999c5265762d4aef` |
| `gptp-tables-run.log` | 3430 | `8692b7580909a3ecdeecd66c4594b649d57cb95a13bcdafc52a44acc727b6448` |
| `hygiene.log` | 2000 | `16c9e549e4e17018801eaa9d34610a7939b4f6c87fcc7fc51e8a6fc838afe660` |
| `lint.log` | 14186 | `f7765c8f0fb403026f5eba51c6e99b88abd23c1fba7a10b0b9ebd3fa9feec214` |
| `make43-inputs.log` | 1113 | `6e5bab65938768f013ed4195a68b2f8af5fd7a83dcfd7c03df85237a2abfe63b` |
| `make43-limits.log` | 253 | `895e6a6cc7671084b922d6b570d791d64857fd3c37e640e4aa5694f312ff1cdd` |
| `module-matrix.log` | 118 | `4e782e68ed5c09299d5d990702b634a2358aa1d5cbc2fd822374561e249c2687` |
| `naming.log` | 36490 | `8db123cd4a9ebdcc6a488529e53b67d91b48a7c2b4e8d577d9ea17ec0b724965` |
| `one-valued.log` | 43 | `b1818889beca5d5a8dea520e8fd1c0b9b2cb350cf97740418713fd9e2a3a12a8` |
| `passing-inputs.json` | 944 | `12ae6d135790c1d2a37cdeca73bbb00b5ebefb49598e87f72df57fd1b341fd30` |
| `pngs-self.log` | 59 | `918e8cc85a2a2b0d45eeb3f0c7b006824c81e2ed404a535eded095b09d875dc5` |
| `pngs.log` | 66 | `05e0fcfa26a97494e8983dcfca3ad89cdaf91e390acbfb9dbdfb6f614cba4e51` |
| `ports.log` | 421 | `cd9f24fbfd71df64a01d448c13e8aee85846692cbc781f4f45e8eecc7f950bf6` |
| `py-idiom-self.log` | 2531 | `d7413b83955948950d15e364a901be97cf05148dad38e97be07b2d63eb46406d` |
| `py-idiom.log` | 461 | `4a29b174d272f40260506cf2d18a92fe21b4b97e645f30dab78616a6568be035` |
| `repin.log` | 404 | `d65416942e69b6e953c42aa708c0a0c27a060a7c8475f32bb9823f784366552d` |
| `resource-baseline.log` | 27 | `2114d909e60add091220b415987d4409a611d70c9e84f1bb9e0ae12d6a2f14a0` |
| `resource-self.log` | 36595 | `768e343f39de02e68d68aa0a6da0d45bda263cfdea9c5bbb13cb4e037eb80ec7` |
| `rom-digests-record.log` | 198 | `baddd8a42481b7ac6ce7a5c1dc7a31807055e408b20d73cea1003ee70eb34579` |
| `rom-digests.log` | 82 | `855a4eb4d24e91c8643416e11b80671aff75e021a7adf6124e614ffd8724a8dd` |
| `sh-idiom.log` | 235 | `7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9` |
| `source-lists.log` | 153 | `ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95` |
| `state-proof.log` | 415 | `f3352082dfe3adb12482954dafc7c3ce1fad7f5d301333b8237f80bc2594b94f` |
| `static-gates.json` | 3001 | `098892238d99c4ad93561b910b08c9051bc00aa782bdff64bbeaa70f4016eeea` |
| `submodule-diagram-self.log` | 60 | `51bca8fb66fd6f0acc480e3364f74fd7a4874946b191468bfbe20ad159cca889` |
| `submodule-diagram.log` | 54 | `4f2d621c17d265a6e2851eaa978fe81af61cf6bbf152cce8ab90ba77b4f91e18` |
| `submodule-docs-self.log` | 66 | `54dbecff3ad17dc651e86c7b313ef57fa96baf89fb40f0fb90af4bbb8ddc802b` |
| `submodule-docs.log` | 47 | `c4bbf250ee33a3cc538cbbf1028e693c8acc058adc782d1f1feef249cd2faa0b` |
| `sv-idiom.log` | 218 | `aed2873a1909e4a41b3e6dee6dc5aaab993bbf1ef41f556062a5b377a6a8b167` |
| `table_chunk.py` | 746 | `15b416c1dc628e9699d6ecc85267f2ee2d5c0e1cb6adc7063b51d61f334e356b` |
| `timesync-diagram-self.log` | 61 | `7c7ad79fa685d29607abf71e3a99d98855fd7ffa1ba5fbf7de23bfb41a33c8fa` |
| `timesync-diagram.log` | 60 | `51058c96a481bf763246394b619601227bdec11b6b11ddcaa1d6f57593d2f1f4` |
| `toc-anchors.log` | 64 | `9d9e538fb10cc7787bf9f74abf5a385ad07c4336858a66a6b03ad7311245e459` |
| `toc-self.log` | 38 | `d7fd5f6ebcdd25e6cf93b623b0fba00cfa32d19c812ce34eb6b8d8b352ac9b32` |
| `toc.log` | 94 | `69f1c8a46304a5e42bd93366b34a8efb1e6aea995f10a25f83cedbdab720a5cf` |

Generated raster receipts (retained in the repository):

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `docs/diagrams/submodule_boundaries.png` | 438329 | `cec6255edea7b7d3d2dc7377f6d7217e6b6c1c6814dfbc4db26dd7cb30d32734` |
| `docs/diagrams/timesync_chain.png` | 314514 | `63bbccf71eaa015227b0976935db9d5b486e7e049ffbfb69a892f7c6c399e577` |

Public REVIEW READY receipt: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6162686301
