# Assigned gate results

Head: `d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1`.

All assigned gates returned zero. The datapath default ran in one invocation.
Commands ran in the foreground with separate logs and recorded exit codes.
The behavior command ran from `tests/`; other commands used the candidate root.

| Gate | Command | Exit | Seconds | Receipt |
|---|---|---:|---:|---|
| crf-rx-default | `env VERILATOR=$TOOLS/verilator-v5.050/bin/verilator PYTHONUNBUFFERED=1 stdbuf -oL -eL make -C tb/verilator/crf_rx` | 0 | 784.52 | [crf-rx-default.log](crf-rx-default.log) |
| mmcm-servo | `env VERILATOR=$TOOLS/verilator-v5.050/bin/verilator make -C tb/verilator/mmcm_servo` | 0 | 750.25 | [mmcm-servo.log](mmcm-servo.log) |
| milan-dp | `make -C tb/verilator/milan_dp run VERILATOR_JOBS=4` | 0 | 1810.05 | [milan-dp.log](milan-dp.log) |
| docs-git-final | `python3 scripts/docs_check.py` | 0 | 8.18 | [docs-git-final.log](docs-git-final.log) |
| docs-no-git-final | `env GIT_DIR=$MISSING_GIT_DIR python3 scripts/docs_check.py` | 0 | 8.18 | [docs-no-git-final.log](docs-no-git-final.log) |
| em-dash | `$TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d` | 0 | 4.64 | [em-dash.log](em-dash.log) |
| doc-style | `python3 scripts/check_doc_style.py` | 0 | 0.07 | [doc-style.log](doc-style.log) |
| toc-pinned | `$TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/gen_toc.py --check` | 0 | 2.37 | [toc-pinned.log](toc-pinned.log) |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | 0.12 | [doc-paths.log](doc-paths.log) |
| module-matrix | `python3 scripts/../docs/traceability/gen_module_matrix.py --check` | 0 | 0.97 | [module-matrix.log](module-matrix.log) |
| xvlog | `python3 scripts/xvlog_gate.py --check` | 0 | 186.46 | [xvlog.log](xvlog.log) |
| source-lists | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.32 | [source-lists.log](source-lists.log) |
| cpp-idiom | `python3 scripts/check_cpp_idiom.py` | 0 | 1.17 | [cpp-idiom.log](cpp-idiom.log) |
| py-idiom-final | `python3 scripts/check_py_idiom.py` | 0 | 9.29 | [py-idiom-final.log](py-idiom-final.log) |
| behave | `behave --no-capture -f plain` | 0 | 1.27 | [behave.log](behave.log) |
| diff-check | `git diff --check 39a0171c8c39e68065b14b9178b30d708a9f7645 HEAD` | 0 | 0.02 | [diff-check.log](diff-check.log) |

The no-git mode sets `GIT_DIR` to a nonexistent path; the receipt confirms
the filesystem-walk inventory used by CI without Git metadata.
The TOC and em-dash gates use the existing pinned Markdown environment.
Front-end analysis ran, rather than skipping: four pinned-processor findings
match the existing ratchet, with zero local RTL findings.

The final connected harness gate and review campaigns used the installed 5.050 simulator.
The datapath invocation used the system 5.052 simulator; no source changes
were made for either version. Full commands and setup attempts also appear
in `gates.jsonl`. The initial TOC dependency refusal and probe-wrapper setup
error were corrected and rerun; neither is presented as validation.
