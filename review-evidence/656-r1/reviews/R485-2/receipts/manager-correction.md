https://github.com/kebag-logic/milan-fpga/pull/662#issuecomment-5986948467

[A10] Manager correction to the PR body, at the unchanged head `d0e29f6d`. This resolves R484-1 M1 = R485-1 F2. Only the "INTERNAL against an asynchronous talker" bullet under Known limitations changed, and it now uses the reviewers' text:

- the loopback slip is about 0.48 events/s per fed pair per 10 ppm (0.51/s at plan A's 10.64 ppm);
- the pre-A2-a TDM-junction clause is limited to this leg's old axis-paced talker; a talker on any other clock also slipped on the loopback path at INTERNAL before A2-a.

No tree change. The REVIEW READY comment on #656 keeps the old coefficient and is left unedited under the assignment rule; this comment supersedes it.

Dispositions:

- R484-1 S1 = R485-1 F1 (the 160-PDU pin): optional, not taken in this PR. The pin cannot pass falsely, and the PR discloses the exposure.
- R484-1 R2 = R485-1 RES-1 (stale 137/177 counts and the `:287` duration): residue, carried to #495 at merge.

Delta reviews R484-2 and R485-2 re-read the body at this head.

