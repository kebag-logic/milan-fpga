# #464 author receipts (A167)

Lane checkout: `$CANDIDATE`, branch `464-aem-store-selftest`.
Base: `ec34fcdee0ca9ffa63564a9af8ad70a3a618de29`. Head: `1576f0893ae9781074fffb105f5384fe774ff11e`.
Interpreters: `/usr/bin/python3` = Python 3.14.7 (host default); `$WORKSPACE_HOME/.local/bin/python3.12` = Python 3.12.13 (stand-in for the hosted docs-check `python3`, which is 3.12 on ubuntu-latest).
Scratch trees live under `$AEM_SCRATCH-*`. Every scratch tree comes from `git archive`, and the lane checkout is never written.

| Receipt | What it shows | Reproduce |
|---|---|---|
| `baseline_original_arms.txt` | Every ORIGINAL map-bound vector replayed on the current model: 3 IndexError, 2 wrong-cause refusals (INPUT duplicate, CRF sink), deviations recorded at AUDIO_MAP[1] against AUDIO_MAP[0] observed | `python3 -B probe_original_arms.py <checkout>` at the base head |
| `baseline_other_sections.txt` | The two-level and Base-format sections pass for their own causes at the base | `cd avdecc && python3 -B -c "import gen_aem_store as g; g._selftest_two_level(); g._selftest_base_formats()"` at the base |
| `history_da71309c.txt` | The self-test passes at `da71309c^` (b7d0bbcd) and raises IndexError at `da71309c` | `git archive <rev> avdecc hdl/common/csr` into a scratch dir, then `python3 -B avdecc/gen_aem_store.py --self-test` |
| `interpreter_matrix.txt` | Base: IndexError (3.14) and NameError `Callable` (3.12). Head: PASS on both | `bash interpreter_matrix.sh <checkout> /usr/bin/python3.14 <python3.12> -- ec34fcde 1576f089` |
| `selftest_head_py314.txt`, `selftest_head_py312.txt` | Full head transcripts, 20 ok / 0 FAIL, identical across interpreters | `python3 -B avdecc/gen_aem_store.py --self-test` |
| `mutate_selftest.py`, `mutation_receipts_py314.txt`, `mutation_receipts_py312.txt` | 28/28 planted defects and controls met at the head SHA on both interpreters | `python3 -B mutate_selftest.py <checkout> <head> [python]` |
| `gen_outputs.sh`, `gen_base.txt`, `gen_head.txt`, `manifest_base.sha256`, `manifest_head.sha256`, `shipping_bytes_comparison.txt` | 83 generated files (5 shipping images + manifests + maps + overlays, builder CLI sets, store CLI outputs) byte-identical, base against head | `bash gen_outputs.sh <checkout> <rev> <outroot>` then `cmp` the manifests |
| `preexisting_aem_rom_json_drift.txt` | The tracked `avdecc/aem_rom.json` is already 4 bytes stale at the base (out of scope) | `python3 -B decode_aem_rom_drift.py <checkout> ec34fcde` |
| `gates_worktree_commit2.txt` | Docs/CI/idiom gate set on the commit-2 content before it was committed (identical tree) | commands listed in the file |
| `final_head_gates.sh`, `final_head_gates.txt` | Core gates at the committed head, with the lane pristine before and after | `bash final_head_gates.sh <checkout> <base> [python3.12]` |
| `gates_docs_extra.txt` | traceability, bare-metal scope, solution/submodule/gPTP docs, style/TOC/hygiene/idiom self-tests | commands listed in the file |
| `gates_builder_consumers.txt` | sweep/deploy/wire/NVM record-space gates (consumers of the builder) | commands listed in the file |
| `test_builder_head.txt` | `sw/builder/test_builder.py` at the head: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11) | `python3 -B sw/builder/test_builder.py` in the lane |
| `check_entity_shape_head.txt` | `scripts/check_entity_shape.py --self-test`: 136 checks, 0 failures | same command in the lane |
| `lint_rtl_check.txt`, `xvlog_gate_check.txt` | lint 90 <= 90; xvlog analysed, 4 == ratchet | `python3 scripts/lint_rtl.py --check`; `python3 scripts/xvlog_gate.py --check` |
| `comment_taken.md` | Text of the public [A167] TAKEN comment | posted as issuecomment-5775075742 |
| `gates_ratchets_head.txt` | fail-fast, test-evidence, TODO-ownership, shell-idiom and archive gates at the head | commands listed in the file |
| `decode_aem_rom_drift.py` | reproduces `preexisting_aem_rom_json_drift.txt` | `python3 -B decode_aem_rom_drift.py <checkout> ec34fcde` |
| `interpreter_matrix.sh` | reproduces `interpreter_matrix.txt` | `bash interpreter_matrix.sh <checkout> <py>... -- <rev>...` |
