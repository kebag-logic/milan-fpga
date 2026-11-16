# CPU service budget harness, round 2

Clone at c805f699; the harness's inputs are those of afa3ea19, and its images are the base's
(`image-identity-base-70f4056f-head.txt`). Each point was built once (`build.log`, with the group adp-link). Its groups
then ran as parts with `--reuse-build --groups ... --out <build>/results`, each on a booked 8-CPU range or beside
another part on one. The 1x1 parts C2 and C3 ran on the session pool. Then one `--regrade` graded every group
(`regrade.log`, `table.md`; `results.json` recorded by sha256 in `large-files.sha256`).

- **The parts.** The host was restarted three times on 2026-11-16 (15:40 power cycle, 18:46 crash, 19:39
  maintenance). Each time every part without an rc was treated as cut: its groups' files were removed and the groups
  re-run (round-2 handoff). The parts whose logs are here are the ones that completed with an rc: 1x1 part0 and
  C0-C3; 8x8/1if part0, B1 and C0-C6.
- **1x1/1if, regrade rc 0.**
  - 96 groups graded, 0 refusals, 0 of 130,341 work passes over the 2.000 ms share.
  - 7 budget misses (7 of 950 probe instances, 4 of 92 paths). All seven are the `backlog-owed` held-egress rows, the
    base's already-ruled rows.
- **8x8/1if, regrade rc 1.**
  - 95 groups graded, 0 refusals, 0 of 270,769 work passes over the share.
  - 7 budget misses (7 of 947, 4 of 85 paths), the same seven `backlog-owed` rows.
  - Eleven stated-cost lines (`STATED`): the polls base in four save groups, and the ACMP item and declined offer
    in `backlog-owed`. They are the base's. The image and testbench are byte-identical to the base's and the
    simulation is cycle-exact. The base keys the statements on the interface count, so 8x8/1if is held to 1x1/1if's;
    #920 records the same exit at this base (issuecomment-6908928237).
