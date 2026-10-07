Use a fresh packet directory with these scripts and the pinned dependency
interpreter, CPU packages and generator sources described in PR #694.
The source clone must be detached at the reviewed head, with its three
required submodules initialized. No shared installation is modified.

```sh
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
python3 "$PACKET/scripts/verify_tree.py" "$SOURCE_ROOT" d6b6ca899ae4c248a1342867bb89060e24febcd5
python3 "$PACKET/scripts/fetch_public.py" "$PACKET/scratch/public"
python3 "$PACKET/scripts/prepare_scratch.py" --root "$SOURCE_ROOT" --packet "$PACKET" --python "$LITEX_PYTHON"
python3 "$PACKET/scripts/run_campaigns.py" --root "$SOURCE_ROOT" --packet "$PACKET" --python "$LITEX_PYTHON" --jobs 4
python3 "$PACKET/scripts/summarize_effects.py" "$PACKET"
python3 "$PACKET/scripts/summarize_ax.py" "$PACKET"
export TMPDIR="$PACKET/scratch/tmp"
"$LITEX_PYTHON" "$PACKET/scripts/additional_probes.py" "$SOURCE_ROOT"
"$LITEX_PYTHON" "$PACKET/scripts/byte_count_underflow.py" "$SOURCE_ROOT"
```

The final command is the regression: expected rc 1 at the reviewed head,
rc 0 after a correct fix. All preceding commands should return 0.
The campaign supervisor stays in the foreground and awaits every child.
CPU and AX campaigns run concurrently, with at most two active exports.
Each has its own log and return-code receipt. Generator processes use four
active processors and a 2 GiB heap limit; make receives `-j16` if invoked.

Selective builder checks were run from the source root with the pinned
dependency interpreter and `MILAN_LITEX_PYTHON` selecting that interpreter:

```sh
"$LITEX_PYTHON" -c 'import runpy; b=runpy.run_path("sw/builder/test_builder.py"); b["test_soc_option_refusals"](); assert not b["SKIPPED"]'
"$LITEX_PYTHON" -c 'import runpy; b=runpy.run_path("sw/builder/test_builder.py"); b["test_toolchain_patches_are_applied"](); assert not b["SKIPPED"]'
python3 scripts/check_doc_style.py
python3 scripts/check_solution_docs.py
python3 scripts/check_py_idiom.py
```

Raw export logs are retained in scratch. Publishable copies replace only
local source/dependency/home locations with role placeholders.
`receipts/log-provenance.json` binds original and published hashes.
These substitutions never alter the generated-artifact comparison or hashes.
