# HANDOFF r5: [A834] lane lwsrppin, round 5 (the egress ledger ruling)

Status (01:05 CET 2026-11-25): **REVIEW READY at `67838b379f9e9ecb6cf6fbd0f162a5bb852ca570`**, local and not pushed. Every item
of the ruling is done, with evidence. Nothing of this lane is running. ETA: none remaining. Next is a push by the
manager, then the hosted gates and the local CI replica at the new head, then one delta reviewer.

Head: one commit on `507bce7f`, `Restate the held-egress ledger at 8x8/1if at the flip train's and the lwSRP pin
merge's measurements` (one line, no trailers). It changes three paths: `egress_ledger.py`, its README and
`SPLIT_CONTROL_MEMORY.md`. The PR's remote head is still `507bce7f`. No push, no comment, no bench, and
`dev-soft-core` (`2f2a8152`) not merged.

Outputs: `REVIEW-READY.md`, `PR-BODY.md` (full, not applied), `receipts/INDEX.md` (70 files, every one text and under
200 KB).

## Brief items

| # | Item | Outcome |
|---|---|---|
| 1 | `egress_ledger.py`: the two named measurements | `TRAIN` (`2509db68`) and `PINNED` (`507bce7f`), copied from round 4's `results/backlog-owed.json` to 10 ns (checked EQUAL). `MEASURED` is the largest of the five per row. The tool derives 64.31, 64.51, 64.71, 64.91, 65.11, 63.29 and 63.23 ms, which equal the ruling's expected figures and the rule computed separately in Decimal. **No rounding step differs** |
| 2 | Section 13 | A new bullet restates the ledger by the ruling (linked). It gives the train's share (+0.75..1.50 ms over `402834ac`, 5 of 7 over, debt per #1005) and this PR's share (+0.08568..0.09425 ms on six rows, -0.22290 on `service.aecp.last`) separately, with the figures each sets. The table gains both columns and the new figures |
| 3 | Self-test, leg, image identity | `--selftest` rc 0: 72 of 72 controls, 18 of 18 mutants caught (3 new). `--point 8x8-1if` rc 0 on round 4's merge-head results directory, on its log, and on the train's results. `plat_ledger.py --build-dir` at the new head: 28 of 28 ELF, bin and hex files byte-identical to `507bce7f`'s, the harness images `eed56acc…` and `79c5326c…` among them. No changed path is a harness build input |
| 4 | Docs gates, PR body | `docs.yml` steps 46 of 46 rc 0 at the head (em-dash gate as a push from `507bce7f`: 0 findings over 15 added lines), porcelain 0 before and after. `PR-BODY.md`: the open decision is replaced by the ruling's outcome (both shares, the figures, the ruling's conditions). A new THE SHARE section names #969's amended ruling (issuecomment-7116192252, item 2) as what owes `srp-bound`'s one pass to #977 |

## Notes for the manager

1. **One path beyond the ruling's two.** `tb/verilator/ctrl_service_budget/README.md` changed (2 lines). Its
   `MEASURED` sentence named two measurements and its mutant count said fourteen, which was already stale at
   `507bce7f` (three measurements and 15 mutants). Leaving it unchanged would have left the tool's own documentation
   wrong about the change. It is documentation of the changed tool, with no effect on any image.
2. **#1005 criterion 3** says that "from now on" a restatement needs a per-PR attribution. This restatement is the
   one the #992 ruling itself decides. A delta reviewer may ask that the ordering be stated, and `REVIEW-READY.md`
   lists it as an open question.
3. **The ruling's last condition**, one delta reviewer, is open. The other three are done.
4. **The docs gates ran as a systemd user unit** (`lwsrppin-r5-docs`, CPUs 0-7, booked by `cpu_ranges.py pick`),
   because a foreground call cannot run longer than its timeout. The first attempt was stopped by hand after 15
   steps, all rc 0. The full set was then rerun from the start, so the receipt is a single complete run of
   54 minutes.
5. **Housekeeping.** Scratch `/data-2/milan/tmp/lwsrppin-a834/r5/` is 31 MB (`ledger/b-head` rebuild, `docs2`). The
   lane checkout has porcelain 0. Round 4's harness trees in `r4/harness` are what this round's leg read; keep them
   until review closes.

REVIEW READY 67838b379f9e9ecb6cf6fbd0f162a5bb852ca570
