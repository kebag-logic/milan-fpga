# Round 2 packet, PR #1017 (#1009 step 1), head 079c4fa15

- full-run/: the full service-budget run at 1x1/1if and 8x8/1if from a clean checkout of the head: each point's identity (commit, tree, status, submodules, command, rc, the firmware's and the testbench's sha256), results.json, table.md, the run's verdict lines; the 8x8/1if egress ledger; each family's worst row.
- receipts/: each gate from the same clean checkout (its first line names the commit, the tree and the status), and the LUT attribution.
- board/: this morning's board run, regraded (response to durable per change kind; each power cut).

The results and tables are published unchanged: their sha256 equal those identity.txt recorded at the run (below). The
identity, verdict-line and gate files have host paths replaced by placeholders (<clone>, <build>, <out>, <scratch>,
<host-path>). MANIFEST.txt holds every published file's sha256.
  1x1-results.json: raw 9a7c045e18930661c6ca09fa38d00645e49e603d4de25ddc84661c32af5d79fd, published 9a7c045e18930661c6ca09fa38d00645e49e603d4de25ddc84661c32af5d79fd
  1x1-table.md: raw 555dff21c0b1c09fb134810c9c649e6c567091c900dff11588ef9a23168f38d4, published 555dff21c0b1c09fb134810c9c649e6c567091c900dff11588ef9a23168f38d4
  8x8-1if-results.json: raw 65deb1452dacb101f854ece451e2b76b51dcbc9cc15506199ed8225e302472ce, published 65deb1452dacb101f854ece451e2b76b51dcbc9cc15506199ed8225e302472ce
  8x8-1if-table.md: raw 46251545f15f85c787d1e21157659d70804d8a0aa5bfc20a3a7d5d60c01427ba, published 46251545f15f85c787d1e21157659d70804d8a0aa5bfc20a3a7d5d60c01427ba
