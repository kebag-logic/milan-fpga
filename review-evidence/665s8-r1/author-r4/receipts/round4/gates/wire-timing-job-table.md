| Step | Name | rc | Log |
|---|---|---:|---|
| ci_step_1 | Set CPU-derived job budgets | 0 | `rtl-fast/logs/rtl-fast__wire-timing__ci_step_1.log` |
| ci_step_3 | Fetch RTL dependencies | 0 | `rtl-fast/logs/rtl-fast__wire-timing__ci_step_3.log` |
| ci_step_5 | Put a job-private Python environment on PATH | not run | creates a job-private venv for the pip install that follows; the LiteX venv at the pinned revisions with the patch series applied is first on PATH here |
| ci_step_7 | Install LiteX at the pinned revisions | not run | pip-installs the LiteX pins into the runner's fresh venv; the LiteX venv at the pins is first on PATH here |
| ci_step_10 | Install sbt | not run | downloads sbt 1.10.7 into /opt with sudo; the host's offline sbt and its coursier cache generate the CPU here |
| ci_step_11 | Place the VexiiRiscv source at the revision LiteX pins | not run | places the VexiiRiscv source at the revision LiteX pins in the runner's fresh venv; the LiteX venv here carries it |
| ci_step_12 | Apply the toolchain patch series | not run | applies the toolchain patch series to the runner's fresh LiteX; the LiteX venv here carries the series applied |
| ci_step_13 | Install the image's runtime sources and the simulation's tapcfg data at the bench's revisions | not run | pip-installs picolibc's and compiler-rt's pythondata packages, at 6a13ccce and 6eb76609, and tapcfg's, at a12c3f59, into the runner's fresh venv; the LiteX venv first on PATH here carries all three at those revisions (git rev-parse of its checkouts), and installing into it would replace its editable installs. The step's own command ran into a fresh venv in the job's replica (receipts/replica) |
| ci_packages_13 | Resolve exact package downloads 13 | not run | resolves the Ubuntu runner's apt package downloads (ci_install_cache.py); this host has no apt, and the packages that job installs are present |
| ci_step_17 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source on a cache miss; the pinned v5.050 build is on PATH here |
| ci_step_18 | Put Verilator on PATH and prove the version | not run | puts /opt/verilator on PATH and runs it from there; the pinned v5.050 build is on PATH here (verilator --version in the gate logs) |
| ci_step_20 | Install and verify the pinned RV32 SDK | 0 | `rtl-fast/logs/rtl-fast__wire-timing__ci_step_20.log` |
| ci_step_21 | Time the split placement at the wire, without and with the composed load | 0 | `rtl-fast/logs/rtl-fast__wire-timing__ci_step_21.log` |
| ci_record | Record actual job execution | not run | records GitHub's own step results; needs the hosted step context |

wire-timing at dbe54e46f09802ab8b9bd3f3223d36bf4891394b: 4 steps ran, 10 not run with a reason, 0 bad
