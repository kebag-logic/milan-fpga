# Suites on clean clones

`../tools/editrun.sh.txt`: each make target on a fresh clone in turn, `RUN-<clone>.txt` its rc and time per target,
`<suite>__<target>.log` and `.rc`.

- `at-5d098172/`: the round's cut before its doc commits (`RUN-summary.txt`: the 15:40 power cycle cut two targets,
  rerun below).
- `at-338ece89/`: `mbx all` (the record mover's mutants 25 of 25) and `tdm8render-build`.
- `at-338ece89-g1/`: `tdm8render-mutants`, 31 of 32: 5d098172's FIFO plant (the storage written at the read pointer)
  SURVIVED; replaced in 0297a19a. `at-338ece89-g2/`: `dynmap-mutants`.
- `at-0297a19a-h1/`: `tdm8render-build` and `tdm8render-mutants` at the head.
- `one-render-arm-0297a19a-wip.log`: the new arm alone (`../tools/one_render_arm.sh.txt`) before the commit; not
  evidence on its own.
- `base-70f4056f/`: `twin-plants` at the base; `twin-verdict-head-5d098172.txt` against round 1's base verdict.
- Logs over 200 KB: `large-logs.sha256`.
