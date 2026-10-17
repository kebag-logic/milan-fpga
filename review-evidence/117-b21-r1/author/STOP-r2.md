[A625] STOP

Bench lane B21, round 2, #117 acceptance box 4, the audio continuity row, under the [B21 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6208207821). This round resumes after the [round 1 STOP](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6208887896). Refs #117.

Commit: `acba86cf02f04e8ee95f0bf5a5d8b9ec47f56d3d` (branch `117-b21-bench`, on round 1's `d64336ba`; local, not pushed, no PR). It adds the dated section "2026-10-16: bench lane B21 round 2 on dev 9ef71772" to `docs/findings/117_AUDIO_CONTINUITY.md`, with its Contents entry. No other file.

Image: dev `9ef71772`, as installed. Not flashed, reset or power-cycled.

**STOP at the identity gate: the controller host cannot be reached.** The gate's ATDECC and ADP checks go through it, and every SSH connection failed with no route to the host. 54 polls from the bench host, 19 to 32 s apart from 14:05 to 14:24 UTC, got no answer, and it was still down at 14:26. The other bench hosts answered throughout. The binding rule's format reads and the peer's counters need the same host, so neither direction could run even past the gate.

| Identity check (14:04:33 to 14:04:43 UTC, under the bench lock) | Result |
|---|---|
| Console `milan_status` | PASS, `ID=4d494c4e VERSION=00020060` |
| AEM CRC32 over 7,512 bytes in QSPI | PASS, `5ba355eb` |
| UART grader | PASS, 10/10 (SYNC=1, ASCAPABLE=1, TU=0) |
| ENTITY 0 over AECP (entity, name, firmware, serial), live ENTITY and CONFIGURATION against QSPI, clock sources, ADP model | Not read: 8 checks, controller host unreachable |
| Gate | FAIL, incomplete. The 3 console checks match; no check mismatched |

| Step | Result |
|---|---|
| Step 1, McASP capture-path self-test | NOT RUN (STOP) |
| Step 2, Direction A | NOT RUN (STOP); no run, so no per-run table |
| Step 3, Direction B | NOT RUN (STOP); no run, so no per-run table |
| #117 audio continuity row | Not graded on this image; not passed |

**Touched:** two DUT console reads and the UART grader, nothing written. The SoC board, its player and its audio bridge, the taps, the outlets and the external capture were not accessed. Nothing was staged on the controller host. The bench lock is free, so no restore is needed.

**Note:** the bench host had restarted at about 12:07 UTC, before this round. Round 1's raw files lived in its temporary directory and are gone. Their sizes and SHA-256 stay in the packet's raw-artifact index and on the page, and the packet keeps the derived read records.

**Validation**, all rc 0 at `acba86cf`, unpiped, from the physical lane path, with the Markdown gates in the pinned environment: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9`, `check_doc_paths.py`, `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check`, `scripts/check_feature_status.py --self-test`, `git diff --check` and `git diff --check 4a9b5a2a HEAD`.

**Needed to continue (owner):** the controller host back on the bench network. The round then restarts at the identity gate, then step 1 (the McASP self-test), then Directions A and B.
