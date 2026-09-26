[A336] REVIEW READY

Head: `83c84b19e09d397ed2eb6f5ace337686ce0ef86b`

Round 3 addresses R334-F1 and R335-F1 only: the harness effect-port contract bundle is contiguous again (162 undocumented, matching base), and both harness builds are warning-free. Production RTL, scenario stimulus and assertions are unchanged.

Validation: all repository gates return 0; 1,014,722 suite checks, 7,751 combined processor checks, 85 focused name-write checks, and the 46-build historical figure gate pass. All 12 prescribed parent consumer commands return 0 with the supplied patch and this processor pin; the integration suite passes three builds of 402 checks each. The private parent copy was deleted.

The builder utilization-calibration arm remains not run because its external implementation report is absent. Full updated PR body and receipts are prepared for review. No push or PR edit was performed.
