## STOP boundary

Assignment item 5 says: “STOP before any port, parameter or register-map change, or any change outside `hdl/acmp` and its tests.”

The first unexercised item fails. Milan v1.2 5.3.8.9 requires the settled SRP parameters to retain the values received in the last successful PROBE_TX_RESPONSE. Table 5.38 returns those parameters in GET_RX_STATE. Section 5.4.2.10 also requires the received values in settled-input GET_STREAM_INFO.

The listener accepts a 16-bit field but truncates it both in storage and at its settlement output:

| Location at unchanged head | Finding |
| --- | --- |
| `hdl/acmp/KL_pp_acmp_listener.sv:355` | `vlan_f_r` receives all 16 bits. |
| `hdl/acmp/KL_pp_acmp_listener.sv:1271` | A15 stores only bits 11:0. |
| `hdl/acmp/pp_acmp_pkg.sv:152` | The fixed F07.6 record reserves bits 319:316. |
| `hdl/acmp/pp_acmp_pkg.sv:153` | The settled VLAN field occupies only bits 315:304. |
| `hdl/acmp/KL_pp_acmp_listener.sv:691` | GET_RX_STATE zero-extends the stored 12 bits. |
| `hdl/acmp/KL_pp_acmp_listener.sv:187` | `act_settle_vlan_o` is a 12-bit port. |
| `hdl/acmp/KL_pp_acmp_listener.sv:782` | That port is driven with `vlan_f_r[11:0]`. |
| `hdl/top/protocol_processor_top.sv:1898` | Settlement consumer wire is 12 bits. |
| `hdl/top/protocol_processor_top.sv:1918` | The top latches that truncated value. |
| `hdl/top/protocol_processor_top.sv:1021` | Each `bound_vlan_r` element is 12 bits. |
| `hdl/top/protocol_processor_top.sv:692` | The published bound VLAN port is 12 bits per sink. |
| `docs/architecture/07_memory_maps.md:495` | The documented F07.6 field is 12 bits followed by four reserved bits. |

Completing preservation through this existing settlement path would require widening a port and changing top-level logic outside the assigned scope. Reassigning the four reserved record bits would also alter the documented field layout. A private side store could preserve ACMP readback locally, but would not make the existing settlement output retain the same full value. No such partial remedy was implemented or declared conformant. No parameter, port, record layout or out-of-scope processor file was changed.

## Two unexercised items: outcomes

1. **VLAN retention: reproduced nonconformant.** An accepted successful probe response with `stream_vlan_id = 0xA123` settles with action value `0x0123`, stores `0x0123`, and returns `0x0123` in GET_RX_STATE. The diagnostic explicitly checks the full wire field under Milan 5.3.8.9, not only an ordinary 12-bit VID. There is no conformant disposition or completed correction under the present scope.
2. **Probe controller guard: reproduced nonconformant.** Bind using controller C1, observe the emitted probe, then bind the same talker/source using controller C2 while the probe is pending. The binding updates and remains in PRB_W_RESP, as specified by Milan 5.5.3.5.17 step 2. A reply matching the actual C1 probe is then ignored; an otherwise identical C2 reply is accepted. The guard must instead use the sent probe's fields (5.5.3.5.18 step 1). The retry also changes the controller, violating the duplicate requirement in 5.5.3.5.16 step 1.

The controller path is `hdl/acmp/KL_pp_acmp_listener.sv:526` (guard reads `bind_ctlr_eid`), `:1205` (A6 overwrites it), `:697` (probe/retry serializer reads it), and `:1250` (A13 reuses that serializer). The current suite's guard check at `tb/acmp_listener/sim_main.cpp:383` makes the same current-binding assumption. The new diagnostic derives the expected controller and sequence from the actually emitted probe, never from that reference model. No controller fix was attempted after the VLAN STOP was established.

## Assigned corrections, unchanged

| Item | Existing implementation | Clause and required result | Outcome |
| --- | --- | --- | --- |
| LD1 | `hdl/acmp/KL_pp_acmp_listener.sv:672` | Milan v1.2 Table 5.36: successful UNBIND_RX_RESPONSE talker entity and unique ID both zero. | Unchanged; acceptance not met. |
| LD2 | `hdl/acmp/KL_pp_acmp_listener.sv:1242` | Milan v1.2 5.5.3.5.30 step 2: the discovered-talker retry-delay transition preserves ACMP status. | Unchanged; acceptance not met. |
| LD3 | `hdl/acmp/pp_acmp_pkg.sv:123` | IEEE 1722.1-2021 8.2.1.5 / Table 8-3: CONTROLLER_NOT_AUTHORIZED is 16, while 13 is TALKER_MISBEHAVING. | Unchanged; acceptance not met. |
| TD1 | `hdl/acmp/KL_acmp_talker.sv:1301` | Milan v1.2 5.5.4.2 step 1 / Table 5.44: an invalid source returns TALKER_UNKNOWN_ID. The assignment's ruling gives this procedure precedence over 5.5.2.7. | Unchanged; acceptance not met. |

## Test expectations and failing witnesses

**Existing expectation changes: none.** The listener still uses the old UNBIND talker values (`tb/acmp_listener/sim_main.cpp:337`), clears status for A12 (`:473`), defines unauthorized as 13 (`:57`), masks VLAN (`:484`, `:487`), and uses current-binding probe identity. The talker's valid-source DISCONNECT test (`tb/acmp_talker/sim_main.cpp:607`) remains unchanged. If work resumes, each altered expectation needs its own clause reason and planted mutant. None of the four required new suite checks or their planted mutants has been delivered.

The external diagnostic adds five clause assertions. All five fail against the unchanged base, following successful compilation and setup. These are **observed existing-defect witnesses**, not planted-mutant receipts, and do not discharge the assignment's mutation requirement. Setup completion and frame-existence assertions pass.

| Diagnostic assertion | Location | Observed failing witness | Authority |
| --- | --- | --- | --- |
| Full VLAN at settlement | `stop-diagnostic.cpp:58` | 0xA123 -> 0x0123 | Milan v1.2 5.3.8.9 |
| Full VLAN in GET_RX_STATE | `stop-diagnostic.cpp:67` | 0xA123 -> 0x0123 | Milan v1.2 5.3.8.9 and Table 5.38 |
| Accept the sent probe controller | `stop-diagnostic.cpp:81` | Original controller response ignored; remains PRB_W_RESP | Milan v1.2 5.5.3.5.17 step 2; 5.5.3.5.18 step 1 |
| Reject a controller absent from the sent probe | `stop-diagnostic.cpp:93` | Replacement controller response accepted; reaches SETTLED_NO_RSV | Milan v1.2 5.5.3.5.18 step 1 |
| Retry the original probe | `stop-diagnostic.cpp:107` | Retry differs from the first probe after same-talker rebind | Milan v1.2 5.5.3.5.16 step 1 |

`stop-diagnostic.log` contains all five failures. The diagnostic exits 1 deliberately; it is not an rc-0 acceptance gate. No permanent suite check, mutation table or source file was added to the processor tree.

## Processor suite gates

The listener baseline and the diagnostic share the same compiled unchanged RTL. Baseline mode calls the committed suite's original entry point; diagnostic mode uses its transport harness with direct clause assertions. The independent talker baseline runs the committed suite through its Makefile. Both builds ran concurrently, outside the repository, with the pinned 5.050 compiler exported as `VERILATOR` and 16 build jobs. Every command completed; no build remains running.

| Gate | Base | Head | Evidence / disposition |
| --- | --- | --- | --- |
| `tb/acmp_listener` | rc 0; 3111 PASS, 0 FAIL | Same unchanged head; not rerun | `listener-baseline.log`, `.rc` |
| `tb/acmp_talker` | rc 0; 1342 PASS, 0 FAIL | Same unchanged head; not rerun | `talker-baseline.log`, `.rc` |
| Focused clause diagnostic | rc 1; five failures | Same unchanged head | `stop-diagnostic.log`, `.rc` |
| ROM generation | rc 0 | Same unchanged head | `listener-rom.log`, `.rc` |
| Diagnostic build | rc 0 | Same unchanged head | `listener-diagnostic-build.log`, `.rc` |
| `scripts/run_suites.sh` | Not run — STOP | Not run — STOP | The two module runs above are not the complete suite bank. |
| `scripts/lint_hdl.sh` | Not run — STOP | Not run — STOP | No lint acceptance claim. |
| `make check` | Not run — STOP | Not run — STOP | No documentation-gate acceptance claim. |
| `scripts/gen_matrix.py --check` | Not run — STOP | Not run — STOP | No matrix acceptance claim. |
| `syn/yosys/run.sh` | Not run — STOP | Not run — STOP | No synthesis acceptance claim. |

Reproduction uses the unchanged base checkout plus `run-diagnostics.py` and `stop-diagnostic.cpp` from this directory:

```sh
python3 "$evidence/run-diagnostics.py" --repo "$processor" --scratch "$scratch" --output "$evidence" --compiler "$pinned_compiler"
```

Set `processor` to the requested processor checkout, `scratch` to its assigned temporary root, `evidence` to this output directory, and `pinned_compiler` to the assigned 5.050 executable. The driver writes a separate log and rc file per command, waits for both builds, and returns 0 only when both baselines pass and the diagnostic returns 1. The retained diagnostic log must additionally show the five named failures; a nonzero build is not counted as a defect witness.

## Campaign table

No changed processor file exists, so there is no completed base/head campaign comparison. Every campaign is unrun after STOP. The following lists known campaign entry points for resumption, not a passing-results table; re-inventory dependencies against the actual future diff. These campaigns containing a `pp_top` build compile both ACMP engines even when their planted defect targets a different engine.

| Campaign | Base | Head |
| --- | --- | --- |
| `tb/acmp_talker/retry_mutants.py` | Not run | Not run |
| `tb/pp_top/acmp_mutants.py` | Not run | Not run |
| `tb/pp_top/gsi_mutants.py` | Not run | Not run |
| `tb/pp_top/d3_mutants.py` | Not run | Not run |
| `tb/pp_top/aecp_dispatch_mutants.py` | Not run | Not run |
| `tb/pp_top/aecp_mutants.py` | Not run | Not run |
| `tb/pp_top/ctr_mutants.py` | Not run | Not run |
| `tb/pp_top/notify_mutants.py` | Not run | Not run |
| `tb/pp_top/name_wr_mutant.py` | Not run | Not run |
| `tb/adp_engine/mutants.py` | Not run | Not run |
| `tb/maap/mutants.py` | Not run | Not run |
| `tb/srp_top/mutants.py` | Not run | Not run |
| `tb/srp_admission/mutants.py` | Not run | Not run |

The standalone suite READMEs and mutation tables were inspected for the existing VLAN and controller assumptions. No mutation arm was edited, removed or replanted. No record-equivalence claim is made for unrun campaigns.

## Scratch parent and consumer table

The authorized parent clone is under the assigned temporary root, directory `parent`. It was cloned from the requested parent remote, detached at dev `28f9666feab2b2ba287643c63ed3a16b1e0bb863`, and both supplied patches were applied with `git apply`, after a successful apply check. The processor index entry is mode 160000 at the unchanged processor head. The parent has no new commit and was not pushed. Submodules remain uninitialized because the consumer execution was stopped; no Git command was run inside a submodule directory.

| Parent item | Result | Evidence |
| --- | --- | --- |
| Exact parent base | Verified | `checkout-receipts.json` |
| Adoption patch 148 | Apply check rc 0; apply rc 0 | `parent-adoption-148-6c22d3ca.patch`; parent diff |
| Adoption patch 22 | Apply check rc 0; apply rc 0 | `parent-adoption-22-28f9666f.patch`; parent diff |
| Processor index gitlink | `ed340b9b85258194247334b85e62cf9c23d4d051` | `checkout-receipts.json` |
| Parent diff whitespace | rc 0 | `checkout-receipts.json` |
| Required consumer set of 17, as assigned on issue 163 | Base: not run; head: not run | 0 of 17 executed, no gate verdicts or tally equality claimed. |

## OOC 1x1 before / after

| Metric | Base | Head | Delta / acceptance |
| --- | --- | --- | --- |
| LUT | Not measured — STOP | Not measured — STOP | Unknown; +40 limit not validated. |
| FF | Not measured — STOP | Not measured — STOP | Unknown; +40 limit not validated. |

No Vivado instance was launched. The prior issue's OOC measurements are not substituted for fresh measurements in this lane.

## Artifacts and delivery

`PR-BODY.md` is a STOP description beginning with the required role label and using `Relates to #168`. It is not a request to create a PR for an empty diff.

The output directory contains only small documents, scripts, supplied patches, logs, rc files and manifests. Compiled objects and executables remain in the temporary root. Executable and PDF sizes and hashes are recorded in `external-artifacts.json`. `SHA256SUMS` authenticates the retained small artifacts. No toolchain, virtual environment, package installation, tree export or file over 200 KB is stored here.

Public status: TAKEN was posted when work began; final delivery is STOP at the unchanged head. Resumption requires resolving the VLAN interface/scope boundary before implementation. The four assigned fixes, permanent suite checks, planted mutants, full suite/campaign/parent gates and fresh OOC comparison remain outstanding.
