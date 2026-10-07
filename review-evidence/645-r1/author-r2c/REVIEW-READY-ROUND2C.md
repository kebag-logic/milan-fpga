[A531] REVIEW READY
Commit: 886e16201654ba0fd0c60c41c228ea4c75b2f6d3 (branch `645-ring-slip`, local, not pushed). Live dev `09f1841b` is merged with `--no-ff` at this head.

Changed: round 2 of PR #672 under rulings 6009543884, 6009767440, 6010634115 and 6009790232.
- **Symmetric settle action.** From the empty side it holds up to five pops. From the full side it drops exactly the excess above the target. All pairs act in lockstep and the slip counters do not move. Each output's repeats or drops are consecutive events within at most two consecutive output PDUs, with nothing outside that span.
- **Excursion arm.** It fires past the two-axis-cycle quiet band: 320, 80, 40 and 20 ns at 6.25, 25, 50 and 100 MHz.
- **Recovery qualification.** After an action, the arm re-arms only after 2,048 consecutive quiet ticks.
- **Declared residual.** A second INTERNAL pull that starts inside that recovery window is not guaranteed a recentre. The worst observed isolated window is 0.551148640 s; continuing disturbances can extend it without bound. `MEDIA_CLOCK_FOLLOWING.md` states this.
- **Traceability.** The module-matrix generator credits compiled sources only.
- **Docs.** The disengaged 2,048-tick text, the measured quiet distribution, and the 56 us pull-in slip count (4 phases, not 3).
- **Dev merges.** Seven `--no-ff` merges: `30e3c018`, `bd884631`, `6714181d`, `6a05347d`, `79b086d4`, `910f338d` and `09f1841b`. After `132d79e7` no merge needed a manual resolution.

Validation (every command unpiped and rc 0; receipts are in the handoff packet):
- **Arrival campaigns: 128/128 runs.** The grid is 2 offset signs x 4 arrival envelopes (none, 0 to 5 us, 2 us plus the 24 us tail, 0 to 60 us) x 16 phases.
  - All 320,462,699 quiet samples lie within +/-1 axis cycle, so the band of 2 is twice the peak.
  - No quiet window has a settle pulse, an excursion arm or a pending settle.
  - Each transient gets one recentre and no slip after it.
  - Minimum margins are 2.17 ticks on the empty side and 2.24 ticks on the full side.
  - The preserved four-band baseline gives identical histograms.
- **Focused legs.** Fine pulls 10/10, including the paired pulls inside and outside recovery. The controller passes at four clock rates. All ten planted controls are caught, including NO-RECOVERY, HIGH-ARM and QUIET-ARM. INTERNAL pull-in 32/32.
- **At `f6bd415f`**, the last merge that changed shipping HDL:
  - default sweep: 61/61 suites, 2,184,055 checks, 0 failures;
  - physical gPTP: 197 checks, 0 failures. Two recentres reach the wire at the exact -5 step inside the span, and the recentre controls pass 14/0;
  - render pull-in 18/18; LAW boundary 81/81;
  - builder rc 0. Its Arty calibration arm is NOT RUN because that build tree is absent;
  - source-list and wire selftests rc 0.
- **At this head:**
  - 28/28 source and docs gates;
  - `mbx` suite, the only suite that reads the merged mailbox change: 316, 361 and 316 checks, 0 failures; mutants 5/5;
  - portability: 58 modules PASS;
  - vendor parser: PASS at the ratchet, 0 findings in `hdl/`;
  - dev's firmware-unit job 7/7.
- **Timing** (BUILDING.md section 5, the best of three directives). It was measured at the head's gateware: `f6bd415f` content, with nothing under shipping `hdl/`, `constraints/`, `syn/`, `configs/` or `sw/litex/` changed since. WNS / WHS in ns:

  | Directive | Slow | Fast | Result |
  |---|---|---|---|
  | ExtraPostPlacementOpt | +0.368 / +0.062 | +1.633 / +0.034 | selected, 0 critical warnings |
  | AltSpreadLogic_high | +0.039 / +0.102 | +1.434 / +0.019 | meets the margin |
  | ExtraTimingOpt | +0.017 / +0.102 | +1.536 / +0.036 | recorded, below the margin |

  TNS and THS are 0 everywhere. All three runs produced bitstreams and manifests, with no rejected constraint. The gate passes.
- **Own area.** OOC +119 LUT / +82 FF, within the 120 / 120 limit. The own sources are byte-identical since that measurement.

Acceptance criteria: round-2 items 1 to 6, as amended, are met with the evidence above. The PR body says Closes #645 and Closes #647, except their physical bench items, which stay with the manager.

Open risks/questions:
- The declared second-pull residual stands, as ruled.
- #657's four render-mutation failures are out of scope, and the full mutation campaign is not claimed.
- R474-1's and R475-1's findings await independent re-review at this head. No verdict or lens ledger is claimed.
- HANDOFF.md and PR-BODY.md are in the assigned evidence directory. Nothing was pushed and no PR was edited.
