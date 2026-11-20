**Owner decision (2026-11-20 17:1x): the flip train's 1x1/1if margins.**

- **The situation:** the SRP cut (#665's ruling of 2026-11-20, item 3) brings 8x8/1if within its 0.75 load ceiling: 0.7436, with no statement exceeded. Its code-layout and cache effects move four 1x1/1if costs past their statements: the paced map edit, the held SET_STREAM_INFO, the ADP record and the centisecond tick. Restated by the usual rule, they put 1x1/1if's last queued notice at 141.53 ms (bound 140) and ACMP at 32.74 ms (bound 30).
- **Decided by the owner:** item 4 of that ruling applies at 1x1/1if here too. The two stale notice-path statements are restated from the fresh every-source measurement of the final image, by the usual rule: the AECP notice item 210 to 150 us, and the long notice 365 to 315 us. The four moved costs are restated by the rule.
  - The 1x1/1if rows are then: last queued notice 132.93 ms (bound 140), ACMP 29.01 ms (bound 30), txL 47.83 ms (bound 49).
  - No owner bound moves.
- **Records:** the exception is named in the train's record and in each restated statement's comment. Round 29's rule otherwise stands.
