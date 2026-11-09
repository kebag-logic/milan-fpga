Measured before the commits, on the working tree (hdl/ and tb/ as committed in b655100 and b5f9e53), to write the
README arm counts the new rows move:
- camp-new-1: the 14 new and re-expressed arms through tb/srp_top/mutants.py --only, 25 checks, every arm KILLED.
- camp-counts-1: every arm graded on tb/srp_encoder and on the srp_top groups applicant, link and onevec
  (counts-arms.txt; 107 trials and 7 controls), 114 checks, 114 PASS, every arm KILLED.
- cmp-counts-1.txt: tools/cmp_counts.py over camp-counts-1 against the READMEs before the count edits (14 rows
  differed, every one because a new row also fails under the older arm); after the edits, 0 rows differ.
- armlogs-1: those arms (and the new ones) again with their whole logs, for the per-row breakdown each table records.
The authority is the full campaign at the head (head-84f6d6a/camp-srp), compared again with the READMEs there.
