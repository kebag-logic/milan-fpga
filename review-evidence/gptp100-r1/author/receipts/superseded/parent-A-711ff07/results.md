# superseded/parent-A-711ff07

- Head: `af7e7e9e9dbbfebc27560f7ab3992a3d6daeb9e7`
- Base: `604899c08ff1cd1830e1dd08b733109ef852400c`
- Finished: NOT FINISHED; runner exit -
- Environment: the pinned Verilator 5.050, `VERILATOR_JOBS=4`, `MAKEFLAGS=-j4`, one unit, MemoryMax 10G.
- Log sha256 is of the original log; the copy here has host paths replaced by placeholders.

| # | Command | rc | Seconds | Log | Log sha256 |
|---:|---|---:|---:|---|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | 2.929 | [01.log](01.log) | `8a80e135fafe8237` |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | 9.879 | [02.log](02.log) | `76feffb8c521ad49` |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | 231.822 | [03.log](03.log) | `4089873e5431143f` |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | 2.586 | [04.log](04.log) | `403a78cd6109c4d2` |
| 5 | `python3 sw/builder/test_builder.py` | 1 | 1904.63 | [05.log](05.log) | `bb92010b1a2284e0` |
