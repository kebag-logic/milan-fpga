# parser: checks new at head and the mutants that fail them

Base 337 check executions, head 378; 45 new check names; 4 base names no longer run; 45 of 45 new names fail under at least one planted mutant.

## New checks

- TLV-less ann: absent, zero count and loop <- word 12 marks a TLV-less Announce present (#87)
- out-of-message path: absent, zero count and loop <- word 12 marks a TLV-less Announce present (#87)
- #88 one entry, stepsRemoved 3: event <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 one entry, stepsRemoved 3: presence, count and loop <- the path-count refusal restored (#88); the refusal outlives its frame; word 12 drops the presence bit (#87)
- #88 one entry, stepsRemoved 3: identity 0 <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 one entry, stepsRemoved 3: no drop <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 two entries, stepsRemoved 2: event <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 two entries, stepsRemoved 2: presence, count and loop <- the path-count refusal restored (#88); the refusal outlives its frame; word 12 drops the presence bit (#87)
- #88 two entries, stepsRemoved 2: identity 0 <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 two entries, stepsRemoved 2: identity 1 <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 two entries, stepsRemoved 2: no drop <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 three entries, stepsRemoved 0: event <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 three entries, stepsRemoved 0: presence, count and loop <- the path-count refusal restored (#88); the refusal outlives its frame; word 12 drops the presence bit (#87)
- #88 three entries, stepsRemoved 0: identity 0 <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 three entries, stepsRemoved 0: identity 1 <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 three entries, stepsRemoved 0: identity 2 <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 three entries, stepsRemoved 0: no drop <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 short loop, stepsRemoved 5: event <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 short loop, stepsRemoved 5: presence, count and loop <- the path-count refusal restored (#88); the refusal outlives its frame; word 12 drops the presence bit (#87)
- #88 short loop, stepsRemoved 5: identity 0 <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 short loop, stepsRemoved 5: identity 1 <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 short loop, stepsRemoved 5: no drop <- the path-count refusal restored (#88); the refusal outlives its frame
- #88 head not the grandmaster, two entries: event <- the path-head refusal restored (#88); the refusal outlives its frame
- #88 head not the grandmaster, two entries: presence, count and loop <- the path-head refusal restored (#88); the refusal outlives its frame; word 12 drops the presence bit (#87)
- #88 head not the grandmaster, two entries: identity 0 <- the head is replaced by grandmasterIdentity (#88); the refusal outlives its frame
- #88 head not the grandmaster, two entries: identity 1 <- the path-head refusal restored (#88); the refusal outlives its frame
- #88 head not the grandmaster, two entries: no drop <- the path-head refusal restored (#88); the refusal outlives its frame
- #88 head not the grandmaster, one entry: event <- the path-count refusal restored (#88); the path-head refusal restored (#88); the refusal outlives its frame
- #88 head not the grandmaster, one entry: presence, count and loop <- the path-count refusal restored (#88); the path-head refusal restored (#88); the refusal outlives its frame; word 12 drops the presence bit (#87)
- #88 head not the grandmaster, one entry: identity 0 <- the head is replaced by grandmasterIdentity (#88); the path-count refusal restored (#88); the refusal outlives its frame
- #88 head not the grandmaster, one entry: no drop <- the path-count refusal restored (#88); the path-head refusal restored (#88); the refusal outlives its frame
- #88 head is thisClock: event <- the path-head refusal restored (#88); the refusal outlives its frame
- #88 head is thisClock: presence, count and loop <- the path-head refusal restored (#88); the refusal outlives its frame; word 12 drops the presence bit (#87)
- #88 head is thisClock: identity 0 <- the head is replaced by grandmasterIdentity (#88); the refusal outlives its frame
- #88 head is thisClock: identity 1 <- the path-head refusal restored (#88); the refusal outlives its frame
- #88 head is thisClock: no drop <- the path-head refusal restored (#88); the refusal outlives its frame
- #88 empty path: event <- the empty-path refusal restored (#88); the path-count refusal restored (#88); the refusal outlives its frame
- #88 empty path: present, count zero <- an empty path is not marked present (#87); the empty-path refusal restored (#88); the path-count refusal restored (#88); the refusal outlives its frame; word 12 drops the presence bit (#87)
- #88 empty path: no drop <- the empty-path refusal restored (#88); the path-count refusal restored (#88); the refusal outlives its frame
- #88 empty path between unknowns: event <- the empty-path refusal restored (#88); the path-count refusal restored (#88); the refusal outlives its frame
- #88 empty path between unknowns: present, count zero <- an empty path is not marked present (#87); the empty-path refusal restored (#88); the path-count refusal restored (#88); the refusal outlives its frame; word 12 drops the presence bit (#87)
- #88 empty path between unknowns: no drop <- the empty-path refusal restored (#88); the path-count refusal restored (#88); the refusal outlives its frame
- #88 path after an empty path: no event <- an empty path is not marked present (#87)
- #88 path after an empty path: no w12 <- an empty path is not marked present (#87)
- #88 path after an empty path: one drop <- an empty path is not marked present (#87)

## Base checks no longer run

- TLV-less ann: zero count and loop
- out-of-message path: zero count and loop
- path-count mismatch: no event
- path-count mismatch: one drop
