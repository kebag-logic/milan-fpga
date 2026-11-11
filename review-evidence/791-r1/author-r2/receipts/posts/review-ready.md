[A765c] REVIEW READY
Commit: `596e2ae3708c4693e0929b530fea37020dc8db25` (branch `791-split-region-decode`, PR #888 -> `dev-soft-core`): five commits on `03447eaa`, no merge, rebase, force or amend.
Changed:
- Ruling 1 (R826-1 F1): `SPLIT_CONTROL_MEMORY.md` (the region-decode section and the `rom`-only line in section 7) and the `ctrl_memory.decode_pieces` docstring now state the generator as it behaves. It splits each region into aligned power-of-two terms (`AddressMapping.terms`), except a region based at 0, which it takes whole, so the 224 KiB `rom` became `(address & 0xfffc8000) == 0`, while `sram` at `0x1000_0000` was already exact. Aligned pieces make every region exact without depending on that decomposition. Checked against R826-1's `generator_terms.txt`; that as-built netlist (`18be4f88`, sha256 `d425a0e7`) is this round's single-mask control.
- Ruling 2 (F2): after LiteX's finalize, `milan_soc.exact_cpu_decode` also refuses unless every region list the CPU or any class of it holds (`cpu_region_lists`) is the naming step's list, and that list is aligned powers of two. The stray refusal names the netlist for removal from the generator's cache. `test_ctrl_memory.py`'s decode arm refuses three stand-in shapes: re-collected after naming; kept on the instance as `memory_regions`; kept on the instance as `generator_regions`. It also refuses an unaligned naming list. Five new mutants are each caught by a named check, and round 1's `naming guard off` is now caught by name. R826-1's own `guard_probe.py` now prints `refused` for both silent shapes. `sw/litex/patches/README.md` names `test_ctrl_memory.py` and `tb/verilator/ctrl_region_decode` in the re-pin procedure. The PR says "a LiteX that stops calling the naming step is refused".
- `split_soc.CpuPatches` `as-built` (the single-mask control) now builds the SoC without the hookup, because the new aligned refusal refused it. It hands the generator the same rows as before.
- Ruling 3: F3 and F4 with R826-1's exact texts.
Validation (clean clones of this head, all rc 0):
- `test_ctrl_memory.py`: 182 ok, 0 FAIL, `RESULT: PASS`.
- `ctrl_region_decode/run.py --self-test`: `none 0/0, single-mask 4/4, cover 6/6, PASS`.
- The split export's decode check at 1x1 and 8x8: `DECODE PASS`, netlist `f8b27436`.
- Split boot: 1x1 84.425 ms, 8x8 184.695 ms, PASS.
- S2 self-test: 0 failures. S2 1x1/1if: 18 groups, 0 refusals, 34 misses. S2 8x8/2if: 17 groups, 0 refusals, 63 misses. Both as round 1.
- `git diff --check` against `1d6bf555`: no output.
- Full sweep as four shards, with capture_coherence's shard on 4 CPUs: 65 of 65 suites, 2,192,899 checks, 0 failures.
- Every `run:` step of docs, elaborate, rtl-fast and rtl: `497 steps ran, 0 failed or missing; 110 not run, each with its reason`. That covers `test_builder.py --require-rv32`, behave, `test_ctrl_firmware.py --require-rv32 --self-test` with every firmware mutant driver, `fw_coverage.py --check`, firmware-boundary in the LiteX venv, and firmware-verilator. In elaborate-gates-1's first attempt, `test_soc_timing_cuts` hit its 900 s wall-clock limit on a loaded host (UNKNOWN, exit 92). That simulation does not reach the split path. The job was re-run once and passed 8 of 8; both results are recorded.
STOP condition (a generated CPU netlist or an all-fabric export byte changed): not met.
- Every CPU has the same name, so the same generator input, at this head as at `03447eaa`, in one environment: region test `88c5cdf9`, `18be4f88`, `57948043`; product split `f8b27436`; boot `99bc789b`.
- No run generated a netlist.
- The all-fabric export compare against `1d6bf555` is identical for every shipped config: CPU netlists `f5f08b17` and `7c73187a`, every builder output identical, and comment-only timestamp lines at AX7101, as at round 1.
Acceptance criteria: #791 Required 1 to 3 met (round 1's evidence holds and is re-run above); every ruling item done.
Open risks/questions:
- The guard reads only the lists held on the CPU and its classes. A re-pin that hands the generator a list held nowhere on the CPU is found by the split export check and the region simulation at the re-pin, which the re-pin procedure now names.
- `dev-soft-core` moved to `764482b4` during the round. It touches no file of this branch, and `git merge-tree` is clean. The candidate merge validation is the manager's.
