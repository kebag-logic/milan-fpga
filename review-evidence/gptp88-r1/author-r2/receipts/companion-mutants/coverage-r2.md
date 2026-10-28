# Round-2 parent checks and the companion mutants that fail them

13 check names new since the round-1 companion; 13 of 13 fail under at least one planted mutant (9 mutants).

- [gptp_shadow] entry-0-only change keeps count three <- the received path is published without thisClock
- [gptp_shadow] entry-0-only change publishes the new head <- the received head replaced by the grandmaster; the shadow drops entry 0 (the old seven-slot canonicaliser)
- [gptp_shadow] entry-0-only change keeps tail 1 <- the shadow drops entry 1
- [gptp_shadow] entry-0-only change keeps tail 2 <- the appended entry is the announcing source; the received path is published without thisClock; thisClock lands one slot early
- [gptp_shadow] entry-0-only change spends one path generation <- C2 the shadow path generation compares entries 1..7 only; the received head replaced by the grandmaster; the shadow drops entry 0 (the old seven-slot canonicaliser)
- [milan_dp gptp] entry-0-only change keeps count three <- the received path is published without thisClock
- [milan_dp gptp] entry-0-only change advances generation once <- C2 the shadow path generation compares entries 1..7 only; the received head replaced by the grandmaster; the shadow drops entry 0 (the old seven-slot canonicaliser)
- [milan_dp gptp] entry-0-only change emits one GET_AS_PATH push <- C3 the AS_PATH comparator drops its entry-0 term; GET_AS_PATH entry 0 served from the grandmaster (the old datapath); the received head replaced by the grandmaster; the shadow drops entry 0 (the old seven-slot canonicaliser)
- [milan_dp gptp] entry-0-only change: GET_AS_PATH count three <- the received path is published without thisClock
- [milan_dp gptp] entry-0-only change: GET_AS_PATH serves the new entry 0 <- GET_AS_PATH entry 0 served from the grandmaster (the old datapath); the received head replaced by the grandmaster; the shadow drops entry 0 (the old seven-slot canonicaliser)
- [milan_dp gptp] entry-0-only change: GET_AS_PATH keeps entry 1 <- the shadow drops entry 1
- [milan_dp gptp] entry-0-only change: GET_AS_PATH keeps thisClock last <- the appended entry is the announcing source; the received path is published without thisClock; thisClock lands one slot early
- [milan_dp gptp] entry-0-only push body equals solicited path <- C3 the AS_PATH comparator drops its entry-0 term; GET_AS_PATH entry 0 served from the grandmaster (the old datapath); the received head replaced by the grandmaster; the shadow drops entry 0 (the old seven-slot canonicaliser)
