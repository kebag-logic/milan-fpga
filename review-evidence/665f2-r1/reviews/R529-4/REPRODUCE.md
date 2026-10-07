[R529] Reproduction notes

Use an isolated checkout at `5968967e19411428b71dde5c4712d4a8fa528cfb` with the three required submodules initialized at their recorded pins. Supply the repository-pinned RV32 compiler through `MILAN_RV32_CC`, the pinned simulator through `VERILATOR`, and the locked Markdown interpreter through `MARKDOWN_PYTHON`. Set `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR` below the packet's `scratch/` directory. Host C/C++ compilers and the test libraries must already be available.

All helpers accept `--root` and `--packet`, except the link helper, which accepts `--root`, `--baseline`, `--out`, and optionally `--cc`. Run helpers in the foreground. Keep total simultaneous compile workers at or below 16. The recorded commands and return codes live in `receipts/*.json` and `receipts/*.rc`.

- `audit_catalog.py`: reconstruct and compare both parent catalogs; export complete/disjoint partitions.
- `run_gates.py --phase firmware`: four controller partitions, coverage and the inherited full NVM campaign. The recorded full NVM attempt timed out; it supplies no success verdict.
- `run_gates.py --phase finish`: rerun controller partition 1, run the five-shape NVM baseline, the full differential and the mailbox suite. First extract `git archive HEAD hdl/milan/mailbox sw/mailbox sw/firmware tb/verilator/mbx tb/common` under `scratch/mbx-tree/`.
- `run_gates.py --phase docs`: focused documentation and harness self-checks.
- `merge_probes.py`: four reviewer-defined controller fault probes, each following a positive control.
- `nvm_probe.py`: the exact-sized positive case and three erased-record boundary faults.
- `debug_rv32.py`: the complete controller/MMIO debug object arm and the MAAP assertion dependency.
- `measure_link.py`: independent generated-entity links, actual RV32 library members, symbols, sections and target object dimensions. Extract `git archive d51b373ad7e8e8381af2797be3ebb8ee45c62e3c sw/firmware/ctrl sw/firmware/gtest` under `scratch/dev/`, then use it as `--baseline`; keep `--out` under `scratch/`. The helper constructs shipping 1x1, shipped 8x8, maximum-capacity and two-interface variants. These sizing entries do not boot a board or establish the CSR adapter's functional support above eight AAF outputs.
- `verify_integrity.py --out <receipt>`: exact head/tree, tracked blob bytes, modes, index entries, clean status and required submodule pins.

`MANIFEST.sha256` lists every publishable receipt and helper. Scratch trees, ELFs, SDK data and builds are excluded. The link helper regenerates those artifacts. The original author sizing helper was not present in the public author-r4 directory examined; the independent helper is a cross-check, not a reproduction of the author's ELF hash.
