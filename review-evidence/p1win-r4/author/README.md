# Review packet, round 4 (head `079c4fa15`, unchanged since round 2)

Receipts only: no code change and no new bench run.

- `PR-BODY.md`: the PR body at this head. It now has R941-3-RES1's wording, the corrected failing-run diagnosis
  (the 0.39 to 0.62 s are measured from the relay's power-off instant, not from the command's return) and the si0
  paragraph citing the manager's ruling and these receipts.
- `board/si0-identity.txt`: the rerun of the input-0 case at 8x8/1if. It gives the PR head, the flashed image's
  sha256 and the firmware rebuilt at the head (byte-identical to the image's), the test revision (`27734fa0`, accepted
  by the ruling), the environment, start and end times, and rc.
- `board/si0-report.txt`: that rerun's report as numbers. These are the bind, the durable reading, the cut, the
  withdraw, power-on, the DUT's first ENTITY_AVAILABLE, the Talker declaration, the probe, the Listener's Asking
  Failed and REGISTERING_FAILED, and the verdict.
- `board/fail-8x8-input0.txt`: the failing run's three attempts on input 0 at 8x8/1if. It gives the outlet's
  off and on instants, the command's return, the withdraw, the DUT's last frame, the probe each attempt took as its
  settle, and its own declaration.
- `MANIFEST.txt`: sha256 of every file.

Round 3's packet (`pub-win-r3/`) still holds the notice arms and the per-cut listings.
