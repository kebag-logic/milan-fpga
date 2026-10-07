[R533] Round-9 focused reproduction

Set `SOURCE` to a clean detached checkout at `edeef61c5a0cc6c18caa61db4019a8e378baf366`, and `PACKET` to this packet's directory. Initialize the four required gitlinks. Supply the distribution's C/C++ compilers, test libraries, Python dependencies and the pinned Markdown environment. These commands do not install shared packages.

```sh
mkdir -p "$PACKET/scratch"
cd "$SOURCE"
export TMPDIR="$PACKET/scratch" PYTHONDONTWRITEBYTECODE=1
python3 -B "$PACKET/run_group.py" --repo "$SOURCE" --packet "$PACKET" srp
python3 -B "$PACKET/run_group.py" --repo "$SOURCE" --packet "$PACKET" a0
python3 -B "$PACKET/binding_required.py"
python3 -B "$PACKET/run_prior_probes.py" "$SOURCE"
python3 -B "$PACKET/check_bounds.py"
python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$PACKET/scratch/coverage"
python3 -B "$PACKET/image_checks.py" --repo "$SOURCE" --archive "$SDK_ARCHIVE" --litex-root "$LITEX_ROOT"
python3 -B "$PACKET/mailbox_check.py" --repo "$SOURCE" --verilator "$PINNED_VERILATOR"
python3 -B "$PACKET/audit_public.py" "$SOURCE"
python3 -B "$PACKET/integrity.py" "$SOURCE"
```

`SDK_ARCHIVE` is the repository-pinned `riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz`, SHA256 `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`. `LITEX_ROOT` contains the provisioned LiteX, Picolibc and compiler-runtime source checkouts. Their input hashes were compared with the public size record; the image script requires the linked ELF hashes and every section/storage measurement to match it. `PINNED_VERILATOR` must report release 5.050.

The foreground group controller runs independent jobs concurrently, at four compile jobs each and no more than 16 total. Each has its own log and return-code file. During this review, the A0 group overlapped the four-job coverage check; the later prior probes and image builds were also overlapped within that cap. The mailbox invocation uses `make -j16 VBUILD_JOBS=1`. No job is left running at handoff.

`binding_required.py` is the public R533-8 probe with the direct-binding block removed and its expected result changed to success. Production sources and the original required-behavior assertion are unchanged. `probe_mutants.py` is the unmodified R532-8 script. Its raw exit 1 means a caught plant, so `run_prior_probes.py` checks the expected exit and both named interface failures; it rejects build refusals. The unplanted control must exit 0. Intentional failing assertions in mutation receipts are successful discrimination evidence, not positive-suite failures.

`focused.py` runs 28 selected standing plants at each interface count, including the 14 new binding controls, seven access-bound controls, six four-way controls and the inherited binding debug guard. Its A0 arm compiles the actual current A0 test against pristine and planted C11 sources under gcc, clang and AddressSanitizer.

`docs-checks.log` lists the seven exact documentation/contract commands. Run those in the pinned Markdown environment. `public-audit.json` verifies 105 retained public logs underlying 107 source-validation invocations; two invocations retain only original hashes. It is an evidence-integrity check, not a rerun of those gates.

Published logs retain output text with checkout, packet, SDK and installation paths replaced by role aliases. `receipt-provenance.json` records both original and published digests. Unnormalized originals and all build products stay in `scratch/`, which is excluded from publication. `MANIFEST.sha256` lists the complete publishable packet. Only the listed files and REPORT.md should be published.
