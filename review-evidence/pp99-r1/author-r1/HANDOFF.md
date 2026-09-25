[A244] Author handoff for issue #99

Repository: `Mister-M-alt/protocol-processor-control-plane-avb-milan`  
Worktree: `$LANES/pp99-integrator-params`  
Branch: `99-integrator-params`  
Base: `008edbbf486598ae237414273d75e385cf0e1a56`  
Head: `383a89a5d125c6e1fe59f68338494160c07516ce`  
Commit subject: `[A244] Complete the integration parameter inventory`

Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/99#issuecomment-5810655949

Section 2 and diagram 21 contain all 24 overridable top parameters. The former guide had 18: it omitted the five names in the assignment and `NVM_RS_TMO_CYC_P`. Each parameter now has its own row with an owner reference. F01.5 continues to own architectural parameter values, F08.1 protocol timing values, and the top declarations implementation defaults. No RTL or default changed; `hdl/`, `tb/`, and `syn/` have no tracked difference from the base.

`N_CONTROL_P` sizes IDENTIFY CONTROL descriptor state, distinct from the registered-controller count. The timeout rows identify core-clock versus millisecond units and verification overrides. `DESC_MEM_TMO_CYC_P` also budgets response-memory, AECP gather, and listener stream-command waits.

Parameter table (locations, not copied values): the default-location column identifies each exact implementation expression. The documented-owner column identifies the normative home when one exists, or the top declaration and its implementation contract when there is no master-table entry. F01.5 leaves the stream counts to the product; the top supplies its own implementation defaults.

| Parameter | Default location | Documented owner |
|---|---|---|
| `N_STREAM_IN_P` | [Top declaration, line 75]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:75) | [F01.5]($LANES/pp99-integrator-params/docs/architecture/01_overview.md#fig-01-params), `P-N-STREAM-IN` |
| `N_STREAM_OUT_P` | [Top declaration, line 77]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:77) | [F01.5]($LANES/pp99-integrator-params/docs/architecture/01_overview.md#fig-01-params), `P-N-STREAM-OUT` |
| `N_AUDIO_UNIT_P` | [Top declaration, line 81]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:81) | [F01.5]($LANES/pp99-integrator-params/docs/architecture/01_overview.md#fig-01-params), `P-N-AUDIO-UNITS` |
| `N_CLK_DOMAIN_P` | [Top declaration, line 82]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:82) | [F01.5]($LANES/pp99-integrator-params/docs/architecture/01_overview.md#fig-01-params), `P-N-CLOCK-DOMAINS` |
| `N_CONTROL_P` | [Top declaration, line 83]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:83) | [Top declaration and banner]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv); [AECP dynamic-state store]($LANES/pp99-integrator-params/hdl/aecp/KL_aecp_dyn_state.sv) |
| `RX_SLOTS_P` | [Top declaration, line 85]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:85) | [F01.5]($LANES/pp99-integrator-params/docs/architecture/01_overview.md#fig-01-params), `P-RX-SLOTS` |
| `RX_SLOT_BYTES_P` | [Top declaration, line 86]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:86) | [F01.5]($LANES/pp99-integrator-params/docs/architecture/01_overview.md#fig-01-params), `P-RX-SLOT-BYTES` |
| `TX_STD_SLOTS_P` | [Top declaration, line 88]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:88) | [F01.5]($LANES/pp99-integrator-params/docs/architecture/01_overview.md#fig-01-params), `P-TX-STD-SLOTS` |
| `TX_OVERSIZE_BYTES_P` | [Top declaration, line 89]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:89) | [F01.5]($LANES/pp99-integrator-params/docs/architecture/01_overview.md#fig-01-params), `P-TX-OVERSIZE-BYTES` |
| `CLK_HZ_P` | [Top declaration, line 91]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:91) | [F01.5]($LANES/pp99-integrator-params/docs/architecture/01_overview.md#fig-01-params), `P-CLK-HZ` |
| `TIM_DIV_US_P` | [Top declaration, line 93]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:93) | [Top declaration and banner]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv); [F08.2 timebase]($LANES/pp99-integrator-params/docs/architecture/08_timing.md#fig-08-timerhw) |
| `TIM_DIV_MS_P` | [Top declaration, line 94]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:94) | [Top declaration and banner]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv); [F08.2 timebase]($LANES/pp99-integrator-params/docs/architecture/08_timing.md#fig-08-timerhw) |
| `TROM_HEX_P` | [Top declaration, line 96]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:96) | [Top declaration and banner]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv); [listener ROM generator]($LANES/pp99-integrator-params/hdl/acmp/rom/gen_ltn_rom.py) |
| `UCODE_HEX_P` | [Top declaration, line 101]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:101) | [Top declaration and banner]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv); [AECP µcode generator]($LANES/pp99-integrator-params/hdl/aecp/ucode/gen_ucode.py) |
| `DESC_BASE_P` | [Top declaration, line 115]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:115) | [Top declaration and banner]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv); [07 §3.3.1 memory contract]($LANES/pp99-integrator-params/docs/architecture/07_memory_maps.md#331-realization-the-image-lives-in-main-memory-not-on-chip) |
| `DESC_LINE_BYTES_P` | [Top declaration, line 117]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:117) | [Top declaration and banner]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv); [07 §3.3.1 descriptor store]($LANES/pp99-integrator-params/docs/architecture/07_memory_maps.md#331-realization-the-image-lives-in-main-memory-not-on-chip) |
| `DESC_IDX_ENTRIES_P` | [Top declaration, line 119]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:119) | [Top declaration and banner]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv); [07 §3.3.1 descriptor store]($LANES/pp99-integrator-params/docs/architecture/07_memory_maps.md#331-realization-the-image-lives-in-main-memory-not-on-chip) |
| `DESC_NAME_ENTRIES_P` | [Top declaration, line 121]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:121) | [Top declaration and banner]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv); [07 §3.3.1 descriptor store]($LANES/pp99-integrator-params/docs/architecture/07_memory_maps.md#331-realization-the-image-lives-in-main-memory-not-on-chip) |
| `DESC_MEM_TMO_CYC_P` | [Top declaration, line 123]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:123) | [Top declaration and bindings]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv); [AECP engine]($LANES/pp99-integrator-params/hdl/aecp/KL_aecp_engine.sv) |
| `NVM_RS_TMO_CYC_P` | [Top declaration, line 129]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:129) | [F01.5]($LANES/pp99-integrator-params/docs/architecture/01_overview.md#fig-01-params), `P-NVM-RS-TMO-CYC`; [F08.1]($LANES/pp99-integrator-params/docs/architecture/08_timing.md#fig-08-constants), `T-NVM-RS-DEADLINE` |
| `REG_TL_TIMEOUT_MS_P` | [Top declaration, line 134]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:134) | [F08.1]($LANES/pp99-integrator-params/docs/architecture/08_timing.md#fig-08-constants), `T-NOTIF-TIMELIMITED`; [top declaration]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv) |
| `LOCK_TIMEOUT_MS_P` | [Top declaration, line 135]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:135) | [F08.1]($LANES/pp99-integrator-params/docs/architecture/08_timing.md#fig-08-constants), `T-LOCK-UNLOCK`; [top declaration]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv) |
| `RESP_BASE_P` | [Top declaration, line 145]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:145) | [Top declaration and banner]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv); [07 §3.3.2 response-buffer contract]($LANES/pp99-integrator-params/docs/architecture/07_memory_maps.md#332-the-other-main-memory-region-the-aecp-response-buffer) |
| `SRP_DOM_DEF_VID_P` | [Top declaration, line 153]($LANES/pp99-integrator-params/hdl/top/protocol_processor_top.sv:153) | [F01.5]($LANES/pp99-integrator-params/docs/architecture/01_overview.md#fig-01-params), `P-SRP-DOM-DEF-VID`; [F10.2 Domain FSM]($LANES/pp99-integrator-params/docs/architecture/10_srp_engine.md#fig-10-domsm) |


Diagram 21 uses `docs/diagrams/21-integration-faces.svg` as its hand-authored master, per `docs/diagrams/README.md`; it has no draw.io master. The PNG is generated. Regeneration command, run from the repository root:

```sh
rtk proxy timeout 180 rsvg-convert -w 1905 -o docs/diagrams/21-integration-faces.png docs/diagrams/21-integration-faces.svg
```

The PNG was regenerated and visually inspected: the complete list fits in the central panel without clipping or overlaps. A second independent export matched the committed PNG byte for byte; see [diagram-regeneration.log]($MANAGEMENT/2026-09-23/pp99-a244/diagram-regeneration.log). The SVG links its inventory to the guide's explicit anchor.

The new `scripts/check-integrator-params.py` parses the top parameter header, omits derived localparams, compares the guide table's first column and diagram 21's `integration-parameters` text, and rejects missing, extra, duplicate, empty, or unparseable inventories. It is wired into `.github/workflows/hdl.yml`'s docs job and the `params` prerequisite of `make check`. Eleven probes cover missing rows despite prose mentions, extra/duplicate guide and diagram entries, added/removed top parameters, empty/malformed inputs, and comments/strings/grouped declarations/localparams.

All documentation/static gate commands in `.github/workflows/hdl.yml` were run locally, plus the static µPC gate at the start of the suite driver, `make check`, and the new-check probes. Commands ran in the foreground with generous timeouts, with direct output redirection to logs and no pipelines around their verdicts. The table shows the underlying command; the local wrapper added `rtk proxy timeout 3600` and recorded the actual return code in [gates.jsonl]($MANAGEMENT/2026-09-23/pp99-a244/gates.jsonl).

| Gate command | RC | Evidence |
|---|---|---|
| `python3 scripts/check-links.py` | 0 | [links.log]($MANAGEMENT/2026-09-23/pp99-a244/links.log) |
| `python3 scripts/check-matrix.py` | 0 | [compliance-matrix.log]($MANAGEMENT/2026-09-23/pp99-a244/compliance-matrix.log) |
| `python3 scripts/check-integrator-params.py` | 0 | [params.log]($MANAGEMENT/2026-09-23/pp99-a244/params.log) |
| `python3 scripts/render-wavedrom.py --check` | 0 | [wavedrom.log]($MANAGEMENT/2026-09-23/pp99-a244/wavedrom.log) |
| `make stale` | 0 | [stale.log]($MANAGEMENT/2026-09-23/pp99-a244/stale.log) |
| `./scripts/lint_hdl.sh` | 0 | [hdl-lint.log]($MANAGEMENT/2026-09-23/pp99-a244/hdl-lint.log) |
| `python3 scripts/check_upc_map.py` | 0 | [upc-map.log]($MANAGEMENT/2026-09-23/pp99-a244/upc-map.log) |
| `python3 scripts/gen_matrix.py --check` | 0 | [module-matrix.log]($MANAGEMENT/2026-09-23/pp99-a244/module-matrix.log) |
| `make -C tb/nvm_port figures` | 0 | [nvm-readme-figures.log]($MANAGEMENT/2026-09-23/pp99-a244/nvm-readme-figures.log) |
| `./syn/yosys/run.sh` | 0 | [portability.log]($MANAGEMENT/2026-09-23/pp99-a244/portability.log) |
| `make check` | 0 | [make-check.log]($MANAGEMENT/2026-09-23/pp99-a244/make-check.log) |
| `python3 $MANAGEMENT/2026-09-23/pp99-a244/probe_params.py` | 0 | [parameter-probes.log]($MANAGEMENT/2026-09-23/pp99-a244/parameter-probes.log) |

`make check` reports 41 Mermaid and 18 WaveDrom blocks, 879 links, 115 requirement rows, 17 findings, 90 module rows with zero untested, and `top 24, guide 24, diagram 24, OK`. The NVM README gate completed 46 builds and confirmed all measured figures. Portability passed every listed top and the memory-mapping assertions; its existing diagnostic warnings are retained in the log.

For the lint and NVM figure checks, the CI-pinned version `v5.050` was used from a cached package extracted inside this output directory (the system installation is a different version):

```sh
export VERILATOR_ROOT=$MANAGEMENT/2026-09-23/pp99-a244/verilator-5.050/usr/share/verilator
export PATH=$MANAGEMENT/2026-09-23/pp99-a244/verilator-5.050/usr/bin:$PATH
```

The CI prerequisite `git fetch --no-tags origin refs/pull/13/head` supplied the historical source used by the NVM figure check. The full dynamic suite sweep was not part of this documentation/static assignment and was not run. No physical hardware was used.

Required negative demonstration:

```sh
rtk proxy timeout 180 python3 scripts/check-integrator-params.py --guide $MANAGEMENT/2026-09-23/pp99-a244/integrator-before.md
```

`integrator-before.md` was read directly from base `008edbbf486598ae237414273d75e385cf0e1a56` using `git show`. This check returns **1 as expected** with exactly six guide omissions: `LOCK_TIMEOUT_MS_P`, `NVM_RS_TMO_CYC_P`, `N_AUDIO_UNIT_P`, `N_CLK_DOMAIN_P`, `N_CONTROL_P`, and `REG_TL_TIMEOUT_MS_P`. The updated diagram remains at 24, so this failure isolates the pre-change guide. See [params-before.log]($MANAGEMENT/2026-09-23/pp99-a244/params-before.log). The normal invocation returns **0**, with all three inventories equal.

The repository was clean after the single commit. The commit has one subject line and no body or trailers. [PR-BODY.md]($MANAGEMENT/2026-09-23/pp99-a244/PR-BODY.md) starts with `[A244]` and contains `Closes #99`. No push, PR creation/edit, merge, other checkout, or delegation was performed. The issue review-ready comment uses the exact body in [REVIEW-READY.txt]($MANAGEMENT/2026-09-23/pp99-a244/REVIEW-READY.txt).

The issue-comment posting response is recorded in [review-ready-post.log]($MANAGEMENT/2026-09-23/pp99-a244/review-ready-post.log).
