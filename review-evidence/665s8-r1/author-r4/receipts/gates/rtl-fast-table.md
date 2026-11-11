| Job | Step | Name | rc | Log |
|---|---|---|---:|---|
| changes | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__changes__ci_step_1.log` |
| changes | scope | Classify the change conservatively | 0 | `rtl-fast__changes__scope.log` |
| changes | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| verilator-lint | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__verilator-lint__ci_step_1.log` |
| verilator-lint | ci_step_2 | Fetch RTL dependencies | 0 | `rtl-fast__verilator-lint__ci_step_2.log` |
| verilator-lint | ci_packages_3 | Resolve exact package downloads 3 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| verilator-lint | ci_step_6 | Build Verilator from source on cache miss | NOT RUN | builds Verilator v5.050 from source on a cache miss; the pinned v5.050 build is on PATH here |
| verilator-lint | ci_step_7 | Run the ratcheted whole-tree lint gate | 0 | `rtl-fast__verilator-lint__ci_step_7.log` |
| verilator-lint | ci_step_8 | Prove protocol-processor source lists are derived | 0 | `rtl-fast__verilator-lint__ci_step_8.log` |
| verilator-lint | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| bdd-conformance | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__bdd-conformance__ci_step_1.log` |
| bdd-conformance | ci_step_3 | Fetch the processor model inputs | 0 | `rtl-fast__bdd-conformance__ci_step_3.log` |
| bdd-conformance | ci_step_4 | Install behave | NOT RUN | pip-installs behave into the runner's interpreter; the Markdown venv on PATH carries behave |
| bdd-conformance | ci_step_5 | Run the specification-facing suite | 0 | `rtl-fast__bdd-conformance__ci_step_5.log` |
| bdd-conformance | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| yosys-tool | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__yosys-tool__ci_step_1.log` |
| yosys-tool | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| yosys-tool | ci_step_5 | Build Yosys from source on cache miss | NOT RUN | builds Yosys v0.66 from source on a cache miss; the host's Yosys is v0.66 at the pinned sha 86f2ddebc |
| yosys-tool | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| yosys-elaboration | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__yosys-elaboration__ci_step_1.log` |
| yosys-elaboration | ci_step_2 | Fetch RTL dependencies | 0 | `rtl-fast__yosys-elaboration__ci_step_2.log` |
| yosys-elaboration | ci_step_4 | Install the pinned Yosys and prove the version | NOT RUN | links /opt/yosys with sudo; the host's Yosys is v0.66 at the pinned sha 86f2ddebc (yosys -V in the gate logs) |
| yosys-elaboration | ci_step_6 | Install the pinned sv2v release | NOT RUN | installs sv2v into /usr/local/bin with sudo; sv2v v0.0.12 is already installed there |
| yosys-elaboration | ci_step_7 | Elaborate the integration-heavy tops | 0 | `rtl-fast__yosys-elaboration__ci_step_7.log` |
| yosys-elaboration | ci_step_8 | Prove the OOC read sets come from run.sh and refuse a bad one | 0 | `rtl-fast__yosys-elaboration__ci_step_8.log` |
| yosys-elaboration | ci_step_9 | Prove ooc.sh generates the ROMs and fails on a failed top | 0 | `rtl-fast__yosys-elaboration__ci_step_9.log` |
| yosys-elaboration | ci_step_10 | Prove both synthesis flows refuse active elaboration guards | 0 | `rtl-fast__yosys-elaboration__ci_step_10.log` |
| yosys-elaboration | ci_step_11 | Prove the result cache refuses a planted entry | 0 | `rtl-fast__yosys-elaboration__ci_step_11.log` |
| yosys-elaboration | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| publication-census | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__publication-census__ci_step_1.log` |
| publication-census | ci_step_2 | Set memory-derived census workers | 0 | `rtl-fast__publication-census__ci_step_2.log` |
| publication-census | ci_step_4 | Fetch RTL dependencies | 0 | `rtl-fast__publication-census__ci_step_4.log` |
| publication-census | ci_packages_3 | Resolve exact package downloads 3 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| publication-census | ci_step_8 | Build Yosys from source on cache miss | NOT RUN | builds Yosys v0.66 from source on a cache miss; the host's Yosys is v0.66 at the pinned sha 86f2ddebc |
| publication-census | ci_step_9 | Install the pinned Yosys and prove the version | NOT RUN | links /opt/yosys with sudo; the host's Yosys is v0.66 at the pinned sha 86f2ddebc (yosys -V in the gate logs) |
| publication-census | ci_step_11 | Install the pinned sv2v release | NOT RUN | installs sv2v into /usr/local/bin with sudo; sv2v v0.0.12 is already installed there |
| publication-census | ci_step_12 | Run the publication census in every shape the builder builds | 0 | `rtl-fast__publication-census__ci_step_12.log` |
| publication-census | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| split-cdc | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__split-cdc__ci_step_1.log` |
| split-cdc | ci_step_2 | Fetch RTL dependencies | 0 | `rtl-fast__split-cdc__ci_step_2.log` |
| split-cdc | ci_packages_3 | Resolve exact package downloads 3 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| split-cdc | ci_step_6 | Build Yosys from source on cache miss | NOT RUN | builds Yosys v0.66 from source on a cache miss; the host's Yosys is v0.66 at the pinned sha 86f2ddebc |
| split-cdc | ci_step_7 | Install the pinned Yosys and prove the version | NOT RUN | links /opt/yosys with sudo; the host's Yosys is v0.66 at the pinned sha 86f2ddebc (yosys -V in the gate logs) |
| split-cdc | ci_step_9 | Install the pinned sv2v release | NOT RUN | installs sv2v into /usr/local/bin with sudo; sv2v v0.0.12 is already installed there |
| split-cdc | ci_step_10 | Prove every split crossing goes through an approved primitive | 0 | `rtl-fast__split-cdc__ci_step_10.log` |
| split-cdc | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-unit | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-unit__ci_step_1.log` |
| firmware-unit | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-unit__ci_step_3.log` |
| firmware-unit | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| firmware-unit | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | installs libgtest-dev and libgmock-dev with sudo apt-get; this host has GoogleTest and GoogleMock 1.18.0 (the distribution packages) and no apt |
| firmware-unit | ci_step_7 | Prove the tally reads a failing and a crashing test as failures | 0 | `rtl-fast__firmware-unit__ci_step_7.log` |
| firmware-unit | ci_step_9 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast__firmware-unit__ci_step_9.log` |
| firmware-unit | ci_step_10 | Run the control-plane firmware suites and RV32 builds | 0 | `rtl-fast__firmware-unit__ci_step_10.log` |
| firmware-unit | ci_step_11 | Run the saved-state store suites and its RV32 build | 0 | `rtl-fast__firmware-unit__ci_step_11.log` |
| firmware-unit | ci_step_12 | Hold the firmware coverage ratchet | 0 | `rtl-fast__firmware-unit__ci_step_12.log` |
| firmware-unit | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-control-mutants | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-control-mutants__ci_step_1.log` |
| firmware-control-mutants | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-control-mutants__ci_step_3.log` |
| firmware-control-mutants | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| firmware-control-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | installs libgtest-dev and libgmock-dev with sudo apt-get; this host has GoogleTest and GoogleMock 1.18.0 (the distribution packages) and no apt |
| firmware-control-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast__firmware-control-mutants__ci_step_8.log` |
| firmware-control-mutants | ci_step_9 | Run the control mutation campaign | 0 | `rtl-fast__firmware-control-mutants__ci_step_9.log` |
| firmware-control-mutants | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-aecp-mutants | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-aecp-mutants__ci_step_1.log` |
| firmware-aecp-mutants | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-aecp-mutants__ci_step_3.log` |
| firmware-aecp-mutants | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| firmware-aecp-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | installs libgtest-dev and libgmock-dev with sudo apt-get; this host has GoogleTest and GoogleMock 1.18.0 (the distribution packages) and no apt |
| firmware-aecp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast__firmware-aecp-mutants__ci_step_8.log` |
| firmware-aecp-mutants | ci_step_9 | Run the AECP mutation campaign | 0 | `rtl-fast__firmware-aecp-mutants__ci_step_9.log` |
| firmware-aecp-mutants | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-srp-mutants | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-srp-mutants__ci_step_1.log` |
| firmware-srp-mutants | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-srp-mutants__ci_step_3.log` |
| firmware-srp-mutants | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| firmware-srp-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | installs libgtest-dev and libgmock-dev with sudo apt-get; this host has GoogleTest and GoogleMock 1.18.0 (the distribution packages) and no apt |
| firmware-srp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast__firmware-srp-mutants__ci_step_8.log` |
| firmware-srp-mutants | ci_step_9 | Run both SRP mutation campaigns and pin controls | 0 | `rtl-fast__firmware-srp-mutants__ci_step_9.log` |
| firmware-srp-mutants | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-boundary | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-boundary__ci_step_1.log` |
| firmware-boundary | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-boundary__ci_step_3.log` |
| firmware-boundary | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| firmware-boundary | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | installs libgtest-dev and libgmock-dev with sudo apt-get, and the LiteX pins with pip; this host has GoogleTest and GoogleMock 1.18.0 (the distribution packages), no apt, and the LiteX venv at the pins first on PATH |
| firmware-boundary | ci_step_8 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast__firmware-boundary__ci_step_8.log` |
| firmware-boundary | ci_step_9 | Hold the TSN stack boundary over the firmware builders' compiles | 0 | `rtl-fast__firmware-boundary__ci_step_9.log` |
| firmware-boundary | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| firmware-verilator | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__firmware-verilator__ci_step_1.log` |
| firmware-verilator | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__firmware-verilator__ci_step_3.log` |
| firmware-verilator | ci_packages_2 | Resolve exact package downloads 2 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| firmware-verilator | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | NOT RUN | installs libgtest-dev and libgmock-dev with sudo apt-get; this host has GoogleTest and GoogleMock 1.18.0 (the distribution packages) and no apt |
| firmware-verilator | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| firmware-verilator | ci_step_10 | Build Verilator from source on cache miss | NOT RUN | builds Verilator v5.050 from source on a cache miss; the pinned v5.050 build is on PATH here |
| firmware-verilator | ci_step_11 | Put Verilator on PATH and prove the version | NOT RUN | puts /opt/verilator on PATH and runs it from there; the pinned v5.050 build is on PATH here (verilator --version in the gate logs) |
| firmware-verilator | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast__firmware-verilator__ci_step_13.log` |
| firmware-verilator | ci_step_14 | Hold the TSN stack boundary over the Verilator builders' compiles | 0 | `rtl-fast__firmware-verilator__ci_step_14.log` |
| firmware-verilator | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| wire-timing | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__wire-timing__ci_step_1.log` |
| wire-timing | ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast__wire-timing__ci_step_3.log` |
| wire-timing | ci_step_5 | Put a job-private Python environment on PATH | NOT RUN | creates a job-private venv for the pip install that follows; the LiteX venv at the pinned revisions with the patch series applied is first on PATH here |
| wire-timing | ci_step_7 | Install LiteX at the pinned revisions | NOT RUN | pip-installs the LiteX pins into the runner's fresh venv; the LiteX venv at the pins is first on PATH here |
| wire-timing | ci_step_10 | Install sbt | NOT RUN | downloads sbt 1.10.7 into /opt with sudo; the host's offline sbt and its coursier cache generate the CPU here |
| wire-timing | ci_step_11 | Place the VexiiRiscv source at the revision LiteX pins | NOT RUN | places the VexiiRiscv source at the revision LiteX pins in the runner's fresh venv; the LiteX venv here carries it |
| wire-timing | ci_step_12 | Apply the toolchain patch series | NOT RUN | applies the toolchain patch series to the runner's fresh LiteX; the LiteX venv here carries the series applied |
| wire-timing | ci_step_13 | Install the image's runtime sources and the simulation's tapcfg data at the bench's revisions | NOT RUN | pip-installs picolibc's and compiler-rt's pythondata packages, at 6a13ccce and 6eb76609, and tapcfg's, at a12c3f59, into the runner's fresh venv; the LiteX venv first on PATH here carries all three at those revisions (git rev-parse of its checkouts), and installing into it would replace its editable installs. The step's own command ran into a fresh venv in the job's replica (receipts/replica) |
| wire-timing | ci_packages_13 | Resolve exact package downloads 13 | NOT RUN | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| wire-timing | ci_step_17 | Build Verilator from source on cache miss | NOT RUN | builds Verilator v5.050 from source on a cache miss; the pinned v5.050 build is on PATH here |
| wire-timing | ci_step_18 | Put Verilator on PATH and prove the version | NOT RUN | puts /opt/verilator on PATH and runs it from there; the pinned v5.050 build is on PATH here (verilator --version in the gate logs) |
| wire-timing | ci_step_20 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast__wire-timing__ci_step_20.log` |
| wire-timing | ci_step_21 | Time the split placement at the wire, without and with the composed load | 0 | `rtl-fast__wire-timing__ci_step_21.log` |
| wire-timing | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| rtl-fast | ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast__rtl-fast__ci_step_1.log` |
| rtl-fast | ci_step_2 | Require every applicable fast gate to pass | NOT RUN | the fast verdict converts the hosted jobs' results; every job's own steps ran above |
| rtl-fast | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration: collects a hosted run's runtime evidence |
| ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration: collects a hosted run's runtime evidence |
| ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration: collects a hosted run's runtime evidence |
| ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | CI orchestration: collects a hosted run's runtime evidence |
| ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration: watches and cancels a hosted run |
| ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | CI orchestration: watches and cancels a hosted run |
| ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | CI orchestration: watches and cancels a hosted run |
| ci-fail-fast | ci_record | Record actual job execution | NOT RUN | CI orchestration: watches and cancels a hosted run |
| ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration: cancels a hosted run |
| ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | CI orchestration: cancels a hosted run |

56 steps ran, 65 not run with a reason, 0 bad
