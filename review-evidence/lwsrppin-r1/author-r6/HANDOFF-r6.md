# HANDOFF r6: [A834] lane lwsrppin, round 6 (sync onto dev-soft-core e608f8d8)

Status (03:24 CET 2026-11-25): **REVIEW READY at `2b98e219a5e2b0681f76be90083fc05e47a8f6c0`**, local and not
pushed. Nothing of this lane is running. ETA: none remaining. Next is a push by the manager, then the hosted gates and
the local CI replica at the new head, then the delta reviewer that round 5 left open.

Head: `2b98e219`, a merge commit. First parent is `67838b37` (round 5's head) and second is `dev-soft-core`
`e608f8d8`. Subject: `Merge dev-soft-core e608f8d8 (PRs #1001 and #995, the FPGA-gPTP 1213ac5b pin) into the lwSRP
d1bb4f4e pin`, one line with no trailers. The PR's remote head is still `507bce7f`. No push, no comment, no bench.

Outputs: `REVIEW-READY.md`, `PR-BODY.md` (full, not applied), `receipts/INDEX.md` (every file text and under 200 KB).

## Brief items

| # | Item | Outcome |
|---|---|---|
| 1 | Merge `e608f8d8`, diagrams by regeneration | Conflicts as expected: `submodule_boundaries.drawio`, `.png`, `PNG_MANIFEST.json`. **`scripts/generate_diagrams.py` does not exist.** The repository's generator for this diagram is `docs/diagrams/submodule_boundaries.gen.py` (`docs/diagrams/README.md`, "Regeneration"), and that is what ran. dev-soft-core's three files were staged as a parseable start (`checkout --theirs`), then the generator rewrote drawio, SVG, PNG and its manifest entry from the index's gitlinks. It shows gptp-processor `1213ac5b` and lwSRP `d1bb4f4e` (drawio, SVG, PNG inspected). Against each parent, the drawio and SVG differ by one word each: the other side's pin |
| 2 | Nothing else changed | `git diff e608f8d8 HEAD --stat`: this PR's 21 paths exactly (its own 17 plus the 4 diagram files), the same set as `2509db68..67838b37`. Every other path equals `e608f8d8`'s. `67838b37..HEAD` is dev-soft-core's 37 paths. Path by path, each change equals dev-soft-core's, except the diagram files and `SUBMODULES.md` (both sides changed it). `SUBMODULES.md` is git's clean three-way merge, and against `e608f8d8` it differs by this PR's lwSRP row only |
| 3 | Gates and image identity | Docs gates 12 of 12 rc 0. `egress_ledger.py --selftest` rc 0 (72/72, 18/18, output identical to round 5). `run.py --self-test`: rc 0, 1,015 checks, 295 of 295 mutants caught. `plat_ledger.py --build-dir` PASS. **The 8x8/1if mapped ctrl ELF is `eed56acc…`, identical to round 4's.** Every ELF, bin and AEM image is identical (20 of 28). The 8 others are `gptp_ucode.hex`, #995's gPTP pin. No STOP |
| 4 | PR body | Round 5's body with a "Synced onto dev-soft-core `e608f8d8`" note in place of the stale "`2f2a8152`, not merged" paragraph, the head line, one commit-table row, and this round's evidence rows (`receipts/tools/body.py` makes it from round 5's). The head paragraph was then rewritten by hand: round 5's said every image was identical to `507bce7f`'s (28 of 28), and at this head that holds for the control firmware, not `gptp_ucode.hex` |

## Notes for the manager

1. **Generator name.** The brief named `scripts/generate_diagrams.py --selftest`. No such file exists. The gates ran
   the README's generator checks instead: `submodule_boundaries`, `timesync_chain` and `DOC_MAP`, each `--check`
   and `--selftest`, plus `check_diagram_pngs.py` and its `--selftest`.
2. **CPU booking.** `cpu_ranges.py pick` returned nothing all round (`busy 96 cpus; free16 [] free12 [] half8 []`). So
   every gate and build ran in this session, pinned with `taskset -c 64-95`, the author/review session pool that
   `cpu_ranges.py` names as shared. No unit was started.
3. **The harness self-test ran twice.** It takes longer than a foreground call allows: round 4's took 2 h 20 min under
   load, and this round's took 25.6 min (02:56:37 to 03:22:14). The first run was stopped by hand at about half way
   (143 of 295 mutants, no failure up to there), before the call's time limit would have stopped it. It was then run
   again from the start as a background call of this session with a 1 h limit. The receipt is that second run only,
   which is complete.
4. **`gptp-processor` checkout.** After the merge commit, `git submodule update -- gptp-processor` moved the lane's
   checkout from `1616fc8f` to `1213ac5b`, so that the porcelain is 0 and the builds see the pinned donor.
5. **Routed image.** The PR body's routed 8x8/1if figures are `507bce7f`'s and do not include #995's fabric change.
   The control firmware is unchanged. Whether a route at this head is owed before merge is the manager's call.
6. **Housekeeping.** Scratch is `/data-2/milan/tmp/lwsrppin-a834/r6/` (`ledger/b-head` rebuild, the killed run's
   partial log). Round 4's `r4/harness` trees are still the harness evidence. Keep them until review closes.

REVIEW READY 2b98e219a5e2b0681f76be90083fc05e47a8f6c0
