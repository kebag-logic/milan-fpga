Run from the reviewed source checkout. Set `PACKET` to this packet and `MILAN_RV32_CC` to the pinned, verified compiler under `PACKET/scratch/sdk/bin/riscv32-linux-gcc`. Set `TMPDIR` to `PACKET/scratch`, `PYTHONDONTWRITEBYTECODE=1` and `MAKEFLAGS=-j16`. Use a fresh output packet for a complete replay.

The SDK installer command, archive digest and identity are in `receipts/sdk-install.json` and `receipts/sdk-install.log`. It installs only under scratch. The local dependency install is in `receipts/litex-env-install.json`. The focused simulation uses Python 3.12.3 and the repository's pinned packages; it does not require the complete SoC export setup.

`scripts/copy_runtime_inputs.py PACKET DEPENDENCY_ROOT` copies and verifies the 57 runtime source/header files. DEPENDENCY_ROOT contains the public `litex`, `pythondata-software-picolibc` and `pythondata-software-compiler_rt` repositories. Their revisions are respectively `a1e1c3652ec2f1346ebaea7663d2867f393ae2c4`, `6a13ccce7c575b32c102dd9dc52178505b81fe39` and `6eb76609c9627bf26635e57c63fb22cda7115887`. The exact file digests are in `receipts/runtime-inputs.json`; verification refuses differing files.

Run these commands in the foreground:

```sh
python3 "$PACKET/scripts/runtime_probe.py" \
  --picolibc "$PACKET/scratch/dependencies/pythondata-software-picolibc/pythondata_software_picolibc/data" \
  --compiler-rt "$PACKET/scratch/dependencies/pythondata-software-compiler_rt/pythondata_software_compiler_rt/data" \
  --litex-software "$PACKET/scratch/dependencies/litex/litex/soc/software" \
  --output "$PACKET/scratch/runtime"
python3 "$PACKET/scripts/run_fit.py" "$PACKET" python3
```

Create a separate detached worktree under `PACKET/scratch/previous` at `ce10328c3d89d81509e47836fa4a48b22ecdbc20`, with its own initialized submodules at their gitlinks. From that directory run:

```sh
python3 "$PACKET/scripts/run_fit.py" "$PACKET" python3 previous-
```

Back in the reviewed checkout:

```sh
python3 "$PACKET/scripts/compare_fit.py" "$PACKET"
python3 "$PACKET/scripts/audit_fit.py" "$PACKET"
"$PACKET/scratch/litex-env/bin/python3" "$PACKET/scripts/focused_memory.py" "$PACKET"
```

Each fit driver runs four independent links concurrently and waits for every result. `run_fit.py`, `compare_fit.py` and `runtime_probe.py` are byte-for-byte public copies from R607-4. The comparison's phrase "not the documented 6144" describes that earlier review's document, not the corrected round-5 page.

`receipts/ooc-emit.json` records the independent eight-top emission command. Its plan and synthesis recipe match the published author files. The author synthesis receipt is under `receipts/public/author-r5/evidence-r5/map`; synthesis itself was not rerun in this review.

`scripts/run_command.py` can wrap any foreground command with its log, return code, UTC start time and elapsed seconds. Published local receipts replace checkout/output roots with `$SOURCE` and `$PACKET`; input installations use `$TOOLS_ROOT`. Source and generated ELF hashes are unchanged by path normalization. Scratch holds builds and private-to-execution paths and is excluded from publication.
