# Review packet, round 3 (head `079c4fa15`, unchanged from round 2)

- `PR-BODY.md`: the PR body as it stands at this head.
- `notice-arms/`: the CPU budget harness's notice arms, each run from a clean clone of `079c4fa15` (no status entry
  before or after): `run.py --point <pt> --variant answering-later`, `--variant answering-every-port` and
  `--variant talker-notices`, at 1x1 and 8x8-1if. Per run: `<pt>-<arm>-identity.txt` (commit, tree, status,
  submodules, command, start and end, rc, the firmware's and the testbench's sha256), `-results.json`, `-table.md`,
  `-rc.txt` and `-verdict-lines.txt` (the run's NOTICE and verdict lines). `worst.txt`: each arm's worst retried,
  queued and Talker notice against its bound, made by `notices_r3.py` from the six `results.json`.
- `cuts/`: every power cut of the two power-cycle runs (`cuts-8x8.txt`, 38; `cuts-1x1.txt`, 9), each with the last bind
  before it from the test's report, whether that bind came after the previous cut, and whether the hold reading was
  taken; then the test's attempts as its report logs them. `cuts.py` made the listings.
- `board/summary-8x8-input0.txt`: the corrected test's run of the one inconclusive case (8x8/1if, stream input 0). Its
  part (1) is empty: that run asks for one reading, in the hold.
- `MANIFEST.txt`: sha256 of every file.

Host paths are replaced by placeholders (`<clone>`, `<build>`, `<out>`, `<scratch>`, `<host-path>`).
