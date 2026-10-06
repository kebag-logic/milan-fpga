Portable reproduction commands, from any checkout containing the reviewed history:

```sh
rtk proxy python3 /PATH/TO/PACKET/scripts/run_focus.py /PATH/TO/CLONE /PATH/TO/NEW-PACKET /PATH/TO/PINNED-5.050
rtk proxy python3 /PATH/TO/PACKET/scripts/check_delta.py /PATH/TO/CLONE /PATH/TO/NEW-PACKET /PATH/TO/PINNED-5.050
rtk proxy python3 /PATH/TO/PACKET/scripts/run_docs.py /PATH/TO/CLONE /PATH/TO/NEW-PACKET
rtk proxy python3 /PATH/TO/PACKET/scripts/check_results.py /PATH/TO/CLONE /PATH/TO/NEW-PACKET
rtk proxy python3 /PATH/TO/PACKET/scripts/verify_tree.py /PATH/TO/CLONE /PATH/TO/NEW-PACKET
```

Use a fresh packet path. `run_focus.py` verifies the prescribed head and the simulator's 5.050 identity, extracts the exact commit under scratch, runs the complete 86-arm notification campaign with four workers, and concurrently runs ADP and interface guards. It waits for every child and writes separate logs, exit codes and elapsed times. The campaign's make calls inherit `-j16`; native compiler fanout is clamped to three per campaign worker, two for the concurrent ADP build and one for the guard task. All temporary trees use packet/scratch. There is no detached shell job.

The other scripts are short foreground checks. Run the documentation script without GIT_DIR or GIT_WORK_TREE overrides, because its selftests create repositories of their own. It reads the checkout and places fixtures under scratch. No source patch, installation, full bank, physical build or hardware access is needed. The delta script needs the two parent commits and merge history; it compares imported control records, checks unchanged paths, and reads the elaborated declaration graph for four storage shapes. The result checker requires successful builds, completed simulations, real nonzero failing runs, and every named assertion. It also reconciles the 30 DN/interface controls with the README's numerical failure counts.

Raw campaign logs include expected FAIL lines in negative-control runs. Their authoritative outcome is receipts/notify/results.json, checked by check_results.py. Scratch is disposable and excluded from publication. MANIFEST.sha256 lists the publishable packet files and is verified with `sha256sum -c MANIFEST.sha256` from the packet root.
