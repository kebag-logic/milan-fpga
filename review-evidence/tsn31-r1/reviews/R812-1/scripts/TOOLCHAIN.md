# Reviewer toolchain for the tsn-c-stack CI steps

The workflow (`.github/workflows/quality.yml`) runs on ubuntu-24.04 with Clang 18, GCC 13 and GoogleTest/GMock 1.14.0.
This review used:

| Item | Source |
|---|---|
| Clang 18.1.3 | the pinned toolchain root (`$TOOLS/clang-18`), wrapped by `clang18-wrapper.template.sh` |
| compiler-rt 18.1.3 (sanitizer runtimes; not in the pinned root) | `libclang-rt-18-dev_18.1.3-1ubuntu1_amd64.deb`, sha256 `82d5d27d12c0abdf4cefbafa6044e7544a4cbbbec9c04784f5ce326979842b2b`, merged into `scratch/res18` with the pinned root's `lib/clang/18` |
| libstdc++ headers for Clang 18 (the CI image's GCC 13) | `libstdc++-13-dev_13.2.0-23ubuntu4_amd64.deb` sha256 `0e34b7a6ad0d9db6c718301a0c30a077590decbb31099d0fd6ac957222d77a94` and `libgcc-13-dev_13.2.0-23ubuntu4_amd64.deb` sha256 `d36c9acb969dd37fdc0496120715d8bba67a5cc43a0c2569717314e6ad80020c`, extracted to `scratch/gcc13/x`, used through `--gcc-toolchain` |
| clang-tidy 18.1.3 | `$TOOLS/clang-tidy-18` |
| GoogleTest/GMock 1.14.0 | `$TOOLS/gtest-1.14.0` (pkg-config and CMake prefix) |
| GCC, RISC-V GCC, QEMU, CMake, cppcheck, Mermaid CLI | host: GCC 16.2.1, riscv64-elf-gcc 16.2.0, QEMU 11.1.3, CMake 4.4.5, Cppcheck 2.22.0, Mermaid CLI 11.16.0 |

The first validate run (`receipts/run1-envfail`) used the wrappers before the GCC 13 headers were added.
Its `clang-sanitizers-build` gate failed with 95 errors inside the host's GCC 16 libstdc++ headers (`__builtin_popcountg`
undeclared and similar errors in every test binary, not only `acmp_wide`). That was an environment fault and is not evidence
about the PR. Run 2 (`receipts/run2`) is the run that counts. It used a fresh clean clone of the head and the full toolchain above.

Scripts take the packet directory and tree paths as arguments, and `env.sh` needs `TOOLS` set to the pinned toolchain root.
