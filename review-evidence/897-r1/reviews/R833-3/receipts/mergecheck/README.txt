Merge-side check at f098f893 (merge base cec88385; #898 side 3bebf03a; #902 side 7398ec0a).
own_side_per_file.txt: for each of #898's 17 files, sha256 (first 12) of the +/- lines of git diff cec88385..3bebf03a vs git diff 7398ec0a..f098f893.
other_side_per_file.txt: for each of #902's 85 files, git diff cec88385..7398ec0a vs git diff 3bebf03a..f098f893.
SAME = that side's change is carried exactly. DIFF rows were inspected by hand (REPORT.md, merge section):
 - ctrl_split_boot/README.md: both sides made the identical one-line change; the merge equals both.
 - plat/README.md: #902's 59.5->60.0 lines equal #898's; #898's lines kept (superset).
 - SPLIT_CONTROL_MEMORY.md: #898's round-2 table replaced by 25ea917f's composed table (R833-2 F1); every other hunk of both sides kept.
 - aecp/README.md, aecp_mutants.py: f098f893's module split; coverage.ratchet: 417f44af's measured ctrl_plat.c row.
