Reproduce from an isolated checkout at 7ddbbdc9be73728b239718c8976261c7e0ad0563 with the three required submodules initialized at their gitlinks. Python, a host C compiler, Git and the repository's normal Python dependencies must be available.

Set `review_root` to that checkout and `packet_root` to this packet. Create scratch under the packet. Install the hash-locked `tools/markdown/requirements.txt` into a scratch virtual environment; the original run used a virtual environment with system site packages for the existing YAML dependency. Install the pinned compiler only into scratch:

```sh
python3 "$review_root/scripts/ci_rv32_sdk.py" --destination "$packet_root/scratch/sdk"
python3 "$packet_root/scripts/audit_tree.py" "$review_root"
python3 "$packet_root/scripts/composition.py" "$review_root" "$packet_root/scratch"
```

Use `scripts/run_gate.py --root "$review_root" --packet "$packet_root" --name NAME -- COMMAND...` to preserve the command, complete output, exit and elapsed time. It routes temporary files to scratch and suppresses Python bytecode writes. All commands run in the foreground.

Run `scripts/focused_boot.py "$review_root" "$packet_root/scratch" --compiler "$packet_root/scratch/sdk/bin/riscv32-linux-gcc"` through that wrapper for compiled mode. Omit `--compiler` for compiler-free mode; this retains the host compiler for explicit target stand-down. Preserve the SDK executable's symlink spelling, since its wrapper uses its invoked basename. The harness never changes a tracked source file. It bypasses the complete corpus bank and does not claim its counts.

Candidate gates, using the scratch virtual environment's interpreter:

```text
scripts/docs_check.py
scripts/gen_toc.py --check
scripts/gen_toc.py --verify-anchors
scripts/check_em_dash.py --base 59e7f5fd76786faa673b4522018f4e9590d294d0
scripts/ci_events.py --check
scripts/ci_events.py --selftest
scripts/check_nvm_record_space.py
scripts/check_nvm_record_space.py --self-test
scripts/check_feature_status.py --self-test
scripts/suite_tally.py --selftest
docs/traceability/gen_module_matrix.py --check
scripts/check_doc_paths.py
scripts/check_doc_style.py
scripts/check_py_idiom.py
scripts/check_baremetal_only.py --check
scripts/pp_srcs.py --check
```

Repeat docs_check with `GIT_DIR` naming a nonexistent directory inside scratch for the filesystem inventory mode. Run `git diff --check 59e7f5fd76786faa673b4522018f4e9590d294d0 HEAD`. `scripts/public_evidence.py ROOT SCRATCH` retrieves only the public source-run receipts and verifies their input hashes. Finish by rerunning `scripts/audit_tree.py ROOT`.

The two initial `focused-boot-*.log` receipts are harness setup failures; the corrected `focused-boot-*-final.log` receipts are the candidate outcomes. No full bank, hardware operation, workflow replica or hosted acceptance is part of these reproduction instructions. Limit parallel commands to eight.
