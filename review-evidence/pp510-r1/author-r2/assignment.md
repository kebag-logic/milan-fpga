[A10] Round 2 assignment for PR #118. R318-1 F1 and R319-1 F1 are the same MINOR: the waiver's mutation section quotes check counts measured before the manager's merge of main `990f9652`. The merge added #115's tests, so the counts are no longer current. Executor [A293].

1. Re-measure at the merged head, and state every quoted suite, check and mutant count as measured there. Name the head in the text, or phrase the counts so that no future merge silently makes them stale.
2. Take the cheap suggestions:
   - R318-1 S1 = R319-1 S1: quote the whole Milan recommendation note and give a revision trigger;
   - R319-1 S2: remove the last phantom P-ID in 06 section 11;
   - R318-1 S2 = R319-1 S3: pin the documented "no lock check" behaviour with a response-level check, if it is cheap. If not, soften the claim.
3. No RTL change. Gates as in round 1, including the parent consumer on the 508 branch.

Review: delta reviews by [R318] and [R319].

