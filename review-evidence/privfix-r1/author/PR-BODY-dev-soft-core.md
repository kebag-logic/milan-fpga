[A869]

Closes #1028 (on `dev-soft-core`).

## Summary

Remove bench-specific names from documentation and tools.

Some pages, tool help texts, comments and test fixtures named lab equipment and lab machines by product or host name, or used lab-style addresses. They now use neutral wording that keeps the meaning:

- the capture equipment is "the inline capture tap" (or "capture-tap" in identifiers and fixture labels);
- the lab machines are "the controller bench host" and "a second bench host";
- the switch is "the AVB switch";
- two test-fixture addresses are documentation addresses (RFC 5737, `192.0.2.x`).

No behaviour changes. The capture-format support is unchanged: the 28-octet record header, the kept FCS and the `--tap` option work exactly as before. Only prose, help text, docstrings, comments, one behave scenario title and fixture labels change.

21 files, 33 lines: 8 documentation pages, 2 CI scripts (`scripts/act_ci.py`, `scripts/check_baremetal_only.py`, self-test fixtures only), 5 tools under `tb/tools/` and 6 behave files under `tests/`. On the Markdown lines this change touches, the em dash becomes `--`, as CONTRIBUTING.md asks. In `docs/reference/REGISTER_MAP_CLASSES.md` that means the whole three-entry Contents block, because `gen_toc.py` keeps one separator per block.

Not changed:
- Nothing under `hdl/`, `sw/`, `syn/`, `configs/`, `avdecc/`, `ci/` or any submodule.
- The act slots' real Docker address pool and the two self-tests that pin it. That is a host configuration value, and changing it would change how the CI launcher configures its slots.
- `ci/image/tool-inventory.json`, `command-table.json` and `exec-audit-receipt.json` still record the previous digest of `scripts/check_baremetal_only.py`. These are CI-image snapshots that no pull-request workflow reads, and many of their recorded inputs are already older than the base, so they are left to the next image refresh.

## Testing

Each gate was run at the base (`c1c42843`) and at the head, with the five public submodules initialised and the pinned Markdown renderer. All pass at both:

- documentation: `docs_check.py`, `check_doc_style.py` (and `--selftest`), `check_em_dash.py --base c1c42843` (0 findings over the 15 added lines on 8 pages; `--selftest`), `check_doc_paths.py`, `gen_toc.py --check` and `--verify-anchors`, `docs_inventory.py --check`, `check_gptp_docs.py`, `check_solution_docs.py`, `check_submodule_docs.py`, `check_feature_status.py`, `docs/DOC_MAP.gen.py --check`, `gen_register_reference.py --check`, `ci_gate_workflows.py --check`, `generate_ci_evidence_pins.py --check`
- code quality: `check_hygiene.py --check`, `check_py_idiom.py`, `check_sh_idiom.py`, `check_todo_ownership.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `measure_fail_fast.py --check`, `bash -n tb/tools/check_tu_on_wire.sh`
- tool self-tests: `tb/tools/avtp_wire_truth.py --self-test`, `tb/tools/torture_campaign.py --self-test`, `scripts/act_ci.py --selftest`, `scripts/check_baremetal_only.py --check` and `--selftest` (867 arms)
- behave: the three touched features (231 scenarios) and the whole suite from `tests/` (511 scenarios)

Firmware is byte-identical. `sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-only` was run at the base and at the head into the same build directory, and every output file was hashed: 149 RV32 ELFs, 1,489 host ELFs and 5,664 other build outputs, all identical.
