# Receipts, [A209] #408 + #409

Head `a13b6e2e461695cdb8d978444ae499a5a6745429`, base dev `759da623072358afdb0e9d570a7b4b6a788492c9`.
SDK: `$VALIDATION_STORAGE/504-manager-r1/sdk-install` (verified, 10-sdk-verify.log). Verilator 5.050 from the scoped pinned-tool-bin on PATH.

| File | What |
|---|---|
| 00-base-head.txt | the base commit |
| 01/02-base-gate1b-{sdk,absent}.log | gate 1b at the base, `test_firmware_compiler.py`, SDK mapped / absent (217/217, 182/182) |
| 10-sdk-verify.log | `ci_rv32_sdk.py --verify-only` |
| 11/12-head-gate1b-{sdk,absent}.log | gate 1b at the head (228/228 and 167/167, 27/27 + 4/4, exit 0) |
| 20-static-gates.log | docs, style, idiom, hygiene and ratchet gates plus `git diff --check`, each rc=0 |
| 30/31-head-builder-{sdk,absent}.log | whole `test_builder.py` main via `tools/run_builder.py` (exit 0 both) |
| 40-accepted-at-base/ | every accepted case graded by the BASE gate (all RED, each on its retired rule), plus the asm-fence case at head and base |
| 41-disconnect/ | patches, label sets, raw outcomes and `summary.txt` for each replacement disconnected, plus the unpatched control |
| 42-probes/ | exploratory probes of the new controls and the spliced-define shapes (head and base), before they entered the gate |

`*.audit.jsonl` files log every compiler-candidate call: requested and actual argv and the return code.
