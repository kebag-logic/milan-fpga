# Evidence, [A434] round 4 of PR #618 (issue #617)

Head: `35f58b9cca1de9215f787872734e6a9040f82c19` (local, not pushed). Verilator 5.050, Yosys 0.66, sv2v v0.0.13, host GNU make 4.4.1 and GNU make 4.3 (built from the GNU tarball). Home prefix redacted to `$HOME` in copied logs. Work directory: `$VALIDATION_STORAGE/617-a434-work`.

| File | What |
|---|---|
| `gate-summary-35f58b9c.txt` | every gate at the head: rc, name, exact command, seconds (87 entries, all rc 0) |
| `gate-summary-035dbede.txt` | the full pre-run at `035dbede` before the ROM-image commit (86 entries, all rc 0) |
| `gates-list.tsv` | the gate list: stream, name, command (the round-3 set plus `makeflags_repro`) |
| `gate-logs/<gate>.log` | the gate logs at the head under 200 KB |
| `large-logs-sha256.txt` | sha256 and size of every log over 200 KB (three gate logs and the six timing-run suite logs), not copied |
| `suite-tally-35f58b9c.txt` | `scripts/suite_tally.py` over the 13 suite logs: 52,288 checks, 0 failures |
| `mf-repro-before.txt` | the `MAKEFLAGS` reproduction at `ddb07747`: make 4.4.1 with and without `w`, the make 4.3 chain, the 4.4.1 chain |
| `mf-repro-layers.txt` | each fix alone on `ddb07747`: round-4 `mutants.py` with the old Makefile, round-4 Makefile with the old `mutants.py` |
| `makeflags-check-can-fail.txt` | the committed `MAKEFLAGS=w` check against the `ddb07747` Makefile and with each `--no-print-directory` removed (FAIL), and the round-4 Makefile (PASS) |
| `makeflags-cause-tail.txt` | the tail the round-4 arm prints for the original hosted failure (Makefile fix removed) |
| `planted-break-demo.txt` | a planted syntax error graded as a dp mutant by the `ddb07747` arm and by the round-4 arm |
| `arm-profile-ddb0774-4cpu.tsv` | the `ddb07747` arm item by item on 4 CPUs: build seconds, largest build process, run seconds, verdict |
| `before-B1-4cpu.time`, `before-B2-4cpu.time`/`.phases`, `before-B3-4cpu.time`/`.phases` | `ddb07747` suite runs under make 4.3 on 4 CPUs |
| `after-A1-4cpu.time`/`.phases`, `after-A2-2cpu.time`/`.phases`, `after-A3-4cpu.time`/`.phases` | round-4 suite runs under make 4.3: `035dbede` on 4 and 2 CPUs, the head on 4 CPUs (the timing gate) |
| `arm-after-A3-4cpu.txt`, `arm-before-B3-4cpu.txt`, `arm-gate-suite_capture_coherence.txt` | the leg verdicts and the whole arm output of those runs and of the suite gate |
| `settle-150k-{m,p}{80,100,150}.log`, `settle-150k-sha256.txt` | the recorded converged-lock runs: the committed CRF-settle placements at 150,000 columns |

Scripts in `../scripts/`: `export.sh` (tree exports), `timed_suite.sh` and `monitor.sh` (timing), `mf_repro.py`, `mfdrv.Makefile` and `mf_gate.sh` (the `MAKEFLAGS` reproduction), `arm_profile.py`, `planted_demo.py`, `mfcause_demo.py`, `smoke.py`, `mfcheck.py`, `romtest.py`, `rom_patch.py`, `settle_probe_make.py`, `run_gates.sh`.
