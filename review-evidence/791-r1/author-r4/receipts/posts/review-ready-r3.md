[A765c] REVIEW READY
Commit: `c7e4badb4caf61dcf47e122dc79de7b709125ec9` (branch `791-split-region-decode`, PR #888 -> `dev-soft-core`): one commit on `596e2ae3`, per the round-3 ruling on R826-2. No merge, rebase, force or amend.
Changed (F5 only, nothing else):
- `sw/litex/milan_soc.py` `exact_cpu_decode`: the naming step keeps a copy of the list it hands to LiteX's naming (`named.append(list(VexiiRiscv.memory_regions))`). The after-finalize comparison is therefore against the list that was hashed, not the live class list. A change in place after naming now gets the stray refusal, which names the cached netlist for removal. The docstrings say so.
- `sw/litex/ctrl_memory_decode.py`: two in-place shapes join SHAPES, the class list cleared and refilled with the whole rows, and an aligned row appended. Every SHAPES refusal must now carry the cache-removal words. The new mutant `the named list not copied` is caught by name. The anchor texts that quote the changed line (`_HANDED`, `pieces handed after the name`) follow it.
- Not changed, as ruled: R826-2's R5, S3 and S4.
Validation (clean clones of this head, all rc 0):
- `test_ctrl_memory.py`: 185 ok, 0 FAIL, `RESULT: PASS`. Both in-place shapes are refused with `remove it from the generator's cache`. 59 of 59 mutants are caught, including `the named list not copied`. Under that mutant the cleared-and-refilled shape is refused only as unaligned, and the appended row is not refused at all.
- R826-2's own `guard_probe2.py`: shape 1 `built exact`; shape 2 `never-named`; shapes 3 to 7 `refused; reason names-cache`.
- `ctrl_region_decode/run.py --self-test`: `none 0/0, single-mask 4/4, cover 6/6, PASS`, unchanged.
- Docs gates, every docs.yml job on its own clean clone: 9 of 9 jobs success; `102 steps ran, 0 failed; 6 not run, each with its reason` (APT resolution, hosted-only API steps). That covers `docs_check`, the doc path gate, the anchor and TOC gates, the em-dash and style gates, the Python idiom gate, and the `test_builder.py --require-rv32` legs.
- `git diff --check` against `1d6bf555`: no output.
STOP condition (a generated netlist or an all-fabric export byte moves): not met.
- Region test `88c5cdf9`, `18be4f88` and `57948043`, and product split `f8b27436`, have the same names and sha256 as at `03447eaa` and `596e2ae3`.
- No netlist was generated.
- The split export decode check gives `DECODE PASS` at 1x1 and 8x8.
- The all-fabric compare against `1d6bf555` is identical for every shipped config, apart from comment-only timestamp lines at AX7101, as before.
Not re-run at this head (outside round 3's gate list; the commit touches only the two Python files above): the full sweep, the elaborate, rtl-fast and rtl jobs, the split boots and S2's harness. Their passing results at `596e2ae3` stand in issuecomment-6802190574.
Acceptance criteria: #791 Required 1 to 3 met; the round-2 items and F5 are done.
Open risks/questions: none new. `dev-soft-core` has moved on; the candidate merge validation is the manager's.
