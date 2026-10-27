# milan-fpga companion: checks new at the snapshot and the mutants that fail them

64 new check names; 64 of 64 fail under at least one companion mutant.

## Renamed, assertion unchanged

- [milan_dp gptp] kept to explicit GM emits one AS_PATH push (was: absent to explicit GM emits one AS_PATH push)
- [milan_dp gptp] {thisClock} to maximum path advances generation once (was: empty to maximum path advances generation once)

## New checks

- [gptp_shadow] published path head is the received head <- the shadow drops entry 0 (the old seven-slot canonicaliser)
- [gptp_shadow] TLV-less selected PathTrace keeps its count <- the empty sequence published without a TLV
- [gptp_shadow] TLV-less selected path keeps its head <- the empty sequence published without a TLV; the shadow drops entry 0 (the old seven-slot canonicaliser)
- [gptp_shadow] TLV-less selected path keeps tail 1 <- the empty sequence published without a TLV
- [gptp_shadow] TLV-less selected path keeps tail 2 <- the empty sequence published without a TLV
- [gptp_shadow] TLV-less selected path spends no path generation <- the empty sequence published without a TLV
- [gptp_shadow] better TLV-less Announce keeps the previous count <- the empty sequence published without a TLV
- [gptp_shadow] better TLV-less Announce keeps the previous head <- the empty sequence published without a TLV; the shadow drops entry 0 (the old seven-slot canonicaliser)
- [gptp_shadow] TLV-less GM A-to-B is path-generation silent <- the empty sequence published without a TLV
- [gptp_shadow] explicit one-entry PathTrace head is the GM <- the shadow drops entry 0 (the old seven-slot canonicaliser)
- [gptp_shadow] kept to explicit GM spends one path generation <- the empty sequence published without a TLV
- [gptp_shadow] TLV-less refresh keeps the explicit path <- the empty sequence published without a TLV
- [gptp_shadow] TLV-less refresh spends no path generation <- the empty sequence published without a TLV
- [gptp_shadow] empty PathTrace publishes count one <- a TLV-less Announce is refused by the parser; the empty-path refusal restored; the path-count refusal restored
- [gptp_shadow] empty PathTrace publishes thisClock at entry 0 <- a TLV-less Announce is refused by the parser; the empty-path refusal restored; the path-count refusal restored; the shadow drops entry 0 (the old seven-slot canonicaliser)
- [gptp_shadow] explicit to empty path spends one path generation <- a TLV-less Announce is refused by the parser; the empty sequence published without a TLV; the empty-path refusal restored; the path-count refusal restored
- [gptp_shadow] path headed elsewhere publishes count three <- the path-count refusal restored; the path-head refusal restored
- [gptp_shadow] path headed elsewhere publishes the received head <- the path-count refusal restored; the path-head refusal restored; the received head replaced by the grandmaster; the shadow drops entry 0 (the old seven-slot canonicaliser)
- [gptp_shadow] path headed elsewhere keeps the GM scalar <- the shadow publishes entry 0 as the grandmaster
- [gptp_shadow] path headed elsewhere ends with thisClock <- the path-count refusal restored; the path-head refusal restored
- [gptp_shadow] path headed elsewhere spends one path generation <- a TLV-less Announce is refused by the parser; the empty sequence published without a TLV; the empty-path refusal restored; the path-count refusal restored; the path-head refusal restored
- [gptp_shadow] restored path spends one generation <- a TLV-less Announce is refused by the parser; the empty sequence published without a TLV; the empty-path refusal restored; the path-count refusal restored; the path-head refusal restored
- [milan_dp gptp] TLV-less refresh is neither tapped off nor parser-dropped <- a TLV-less Announce is refused by the parser
- [milan_dp gptp] TLV-less refresh is not event-dropped <- a TLV-less Announce is dropped at the event queue
- [milan_dp gptp] TLV-less fabric publication keeps the path count <- the empty sequence published without a TLV
- [milan_dp gptp] TLV-less refresh keeps fabric path generation <- the empty sequence published without a TLV
- [milan_dp gptp] TLV-less refresh emits no GET_AS_PATH push <- the empty sequence published without a TLV
- [milan_dp gptp] TLV-less GET_AS_PATH serves the kept path B <- the empty sequence published without a TLV
- [milan_dp gptp] TLV-less GM switch keeps the path count <- the empty sequence published without a TLV
- [milan_dp gptp] TLV-less GM switch spends no path generation <- the empty sequence published without a TLV
- [milan_dp gptp] TLV-less GM switch emits no false GET_AS_PATH push <- GET_AS_PATH entry 0 served from the grandmaster (the old datapath)
- [milan_dp gptp] TLV-less GM switch still emits one GET_AVB_INFO push <- a TLV-less Announce is dropped at the event queue; a TLV-less Announce is refused by the parser; the shadow publishes entry 0 as the grandmaster
- [milan_dp gptp] TLV-less GM switch still increments GPTP_GM_CHANGED <- a TLV-less Announce is dropped at the event queue; a TLV-less Announce is refused by the parser; the shadow publishes entry 0 as the grandmaster
- [milan_dp gptp] #87 TLV-less GM switch: GET_AS_PATH keeps count five <- the empty sequence published without a TLV
- [milan_dp gptp] #87 TLV-less GM switch: GET_AS_PATH entry 0 is still GMID <- GET_AS_PATH entry 0 served from the grandmaster (the old datapath); the empty sequence published without a TLV; the shadow drops entry 0 (the old seven-slot canonicaliser)
- [milan_dp gptp] #87 TLV-less GM switch: GET_AS_PATH still ends with thisClock <- the empty sequence published without a TLV
- [milan_dp gptp] kept to explicit GM advances generation once <- the empty sequence published without a TLV
- [milan_dp gptp] empty path commits before captured old response leaves wire <- a TLV-less Announce is refused by the parser; the empty-path refusal restored; the path-count refusal restored
- [milan_dp gptp] empty PathTrace serves count one <- a TLV-less Announce is refused by the parser; the empty-path refusal restored; the path-count refusal restored
- [milan_dp gptp] explicit GM to empty path advances generation once <- a TLV-less Announce is refused by the parser; the empty-path refusal restored; the path-count refusal restored
- [milan_dp gptp] explicit GM to empty path emits one AS_PATH push <- a TLV-less Announce is refused by the parser; the empty-path refusal restored; the path-count refusal restored
- [milan_dp gptp] post-cut response is wholly new count one <- a TLV-less Announce is refused by the parser; the empty-path refusal restored; the path-count refusal restored
- [milan_dp gptp] #88 post-cut response is {thisClock} <- GET_AS_PATH entry 0 served from the grandmaster (the old datapath); a TLV-less Announce is refused by the parser; the empty-path refusal restored; the path-count refusal restored; the shadow drops entry 0 (the old seven-slot canonicaliser)
- [milan_dp gptp] empty-path push body equals post-cut solicited response <- a TLV-less Announce is refused by the parser; the empty-path refusal restored; the path-count refusal restored
- [milan_dp gptp] #88 path headed elsewhere serves count three <- the path-head refusal restored
- [milan_dp gptp] #88 path headed elsewhere advances generation once <- the path-head refusal restored
- [milan_dp gptp] #88 path headed elsewhere keeps the scalar GM <- the path-head refusal restored; the shadow publishes entry 0 as the grandmaster
- [milan_dp gptp] #88 GET_AS_PATH count three <- the path-head refusal restored
- [milan_dp gptp] #88 GET_AS_PATH entry 0 is the received head <- GET_AS_PATH entry 0 served from the grandmaster (the old datapath); the path-head refusal restored; the received head replaced by the grandmaster; the shadow drops entry 0 (the old seven-slot canonicaliser)
- [milan_dp gptp] #88 GET_AS_PATH entry 1 is the parent <- the path-head refusal restored
- [milan_dp gptp] #88 GET_AS_PATH ends with thisClock <- the path-head refusal restored
- [tsn_fuzz ptp] better vector, one path-trace hop against stepsRemoved 1 (10.3.10.2.1): adopted <- the path-count refusal restored
- [tsn_fuzz ptp] better vector, one path-trace hop against stepsRemoved 1 (10.3.10.2.1): no longer grandmaster <- the path-count refusal restored
- [tsn_fuzz ptp] better vector, one path-trace hop against stepsRemoved 1 (10.3.10.2.1): parent follows its source <- the path-count refusal restored
- [tsn_fuzz ptp] better vector, one path-trace hop against stepsRemoved 1 (10.3.10.2.1): parser drop counter unmoved <- the path-count refusal restored
- [tsn_fuzz ptp] better vector, path-trace head is not the announced grandmaster (10.3.10.2.1): adopted <- the path-head refusal restored; the shadow publishes entry 0 as the grandmaster
- [tsn_fuzz ptp] better vector, path-trace head is not the announced grandmaster (10.3.10.2.1): no longer grandmaster <- the path-head refusal restored
- [tsn_fuzz ptp] better vector, path-trace head is not the announced grandmaster (10.3.10.2.1): parent follows its source <- the path-head refusal restored
- [tsn_fuzz ptp] better vector, path-trace head is not the announced grandmaster (10.3.10.2.1): parser drop counter unmoved <- the path-head refusal restored
- [tsn_fuzz ptp] better vector, stepsRemoved 255 on a one-hop path trace (10.3.10.2.1b): GM unmoved <- (b) the stepsRemoved refusal removed
- [tsn_fuzz ptp] better vector, stepsRemoved 255 on a one-hop path trace (10.3.10.2.1b): flags stable <- (b) the stepsRemoved refusal removed
- [tsn_fuzz ptp] better vector, stepsRemoved 255 on a one-hop path trace (10.3.10.2.1b): parent unmoved <- (b) the stepsRemoved refusal removed
- [tsn_fuzz ptp] better vector, stepsRemoved 255 on a one-hop path trace (10.3.10.2.1b): parser drop counter unmoved <- the path-count refusal restored
- [tsn_fuzz ptp] better vector, stepsRemoved 255 on a one-hop path trace (10.3.10.2.1b): rejected, plane stays GM <- (b) the stepsRemoved refusal removed
