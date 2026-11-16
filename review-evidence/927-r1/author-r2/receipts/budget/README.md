# CPU service-budget harness on the cut's RTL

`tb/verilator/ctrl_service_budget/run.py` at each point, built once at 5d098172 (`build-*.log`, `*/build.json`; no
later commit changes a recorded input), its groups run as parallel parts with `--reuse-build --groups ... --out ...`
(`units/part*-*.log`), reruns of the groups the 15:40, 18:46 and 19:39 host stops cut (`partq-*`), then every group's
finished log linked into `combined/` (`<point>/combined-sources.json` names each group's directory) and graded once with
`--regrade` (`units/regrade-*.log`).

- 1x1/1if: 96 groups, rc 0. 8x8/1if: 95 groups, rc 1 on STATED lines only.
- `base-1x1`, `base-8x8-1if`: the base 70f4056f's build at each point, a sample of groups (`backlog`, `aecp-fanout`,
  `acmp-notk`, `save-second`, and `backlog-owed`, the group every probe miss is in): `units/base-*.log`.
- `units/base-1x1.log` and `units/base-8x8-1if.log` are the first base runs, cut at 18:46; their finished groups were
  graded with `--regrade` (`units/base-*-grade.log`), the rest rerun (`units/base-*-r.log`, `units/base-1x1-owed.log`).
- Each point's `results.json` (over 200 KB) is recorded by sha256 in `large-logs.sha256`; `<point>/combined-table.md` is its table.
