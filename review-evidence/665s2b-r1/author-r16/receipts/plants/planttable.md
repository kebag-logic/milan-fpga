| # | Campaign | Plant | File | Test | Failing words |
|---:|---|---|---|---|---|
| 1 | loop | `transmit-binds-twice` | `loop/ctrl_loop.c` | `LoopBring.L18TransmitBindingRefusals` | L18 a second transmit client is refused |
| 2 | loop | `transmit-binds-no-function` | `loop/ctrl_loop.c` | `LoopBring.L18TransmitBindingRefusals` | L18 a transmit client with no function is refused |
| 3 | loop | `transmit-binds-no-age` | `loop/ctrl_loop.c` | `LoopBring.L18TransmitBindingRefusals` | L18 a transmit client with no age is refused |
| 4 | loop | `transmit-beside-records` | `loop/ctrl_loop.c` | `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord` | L19 a pass that takes a record does not call the transmit |
| 5 | loop | `transmit-beside-a-backlog` | `loop/ctrl_loop.c` | `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord` | L19 nor one that takes more than CTRL_LOOP_TX_EVENTS events |
| 6 | loop | `transmit-without-an-event` | `loop/ctrl_loop.c` | `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord` | L19 a pass that takes one event and no record calls it |
| 7 | loop | `transmit-beside-a-centisecond` | `loop/ctrl_loop.c` | `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord` | L19 nor one that dispatches a centisecond, though it takes no input |
| 8 | loop | `transmit-pass-marked-after-the-polls` | `loop/ctrl_loop.c` | `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord` | L19 its polls read the pass as THE TRANSMIT's |
| 9 | loop | `transmit-before-the-polls` | `loop/ctrl_loop.c` | `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord` | L19 after its polls |
| 10 | loop | `transmit-after-the-retry` | `loop/ctrl_loop.c` | `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord` | L19 before THE RETRY and THE STEP |
| 11 | loop | `transmit-owed-lets-it-sleep` | `loop/ctrl_loop.c` | `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord` | L19 a transmit still owed asks for the next pass at once |
| 12 | loop | `transmit-pass-uncounted` | `loop/ctrl_loop.c` | `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord` | L19 the pass is counted as one that called the transmit |
| 13 | loop | `transmit-in-the-aged-steps-pass` | `loop/ctrl_loop.c` | `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord` | L19 the pass given whole to an aged step does not call it |
| 14 | loop | `transmit-age-ignored` | `loop/ctrl_loop.c` | `Loop.L20AnAgedTransmitIsAPassOfItsOwn` | L20 the next pass calls the transmit though input waits, then THE RETRY |
| 15 | loop | `transmit-aged-pass-takes-input` | `loop/ctrl_loop.c` | `Loop.L20AnAgedTransmitIsAPassOfItsOwn` | L20 and takes nothing else: no event, no record, no poll, no centisecond |
| 16 | loop | `transmit-aged-pass-sleeps` | `loop/ctrl_loop.c` | `Loop.L20AnAgedTransmitIsAPassOfItsOwn` | L20 the aged transmit's pass asks for the next pass at once |
| 17 | loop | `transmit-aged-pass-uncounted` | `loop/ctrl_loop.c` | `Loop.L20AnAgedTransmitIsAPassOfItsOwn` | L20 the pass is counted as an aged transmit's |
| 18 | loop | `transmit-aged-pass-not-a-transmit-pass` | `loop/ctrl_loop.c` | `Loop.L20AnAgedTransmitIsAPassOfItsOwn` | L20 and as one that called the transmit |
| 19 | loop | `transmit-aged-pass-without-the-retry` | `loop/ctrl_loop.c` | `Loop.L20AnAgedTransmitIsAPassOfItsOwn` | L20 the next pass calls the transmit though input waits, then THE RETRY |
| 20 | loop | `transmit-aged-back-to-back` | `loop/ctrl_loop.c` | `Loop.L20AnAgedTransmitIsAPassOfItsOwn` | L20 without reading the age after a pass given whole |
| 21 | loop | `transmit-ordinary-pass-unmarked` | `loop/ctrl_loop.c` | `Loop.L20AnAgedTransmitIsAPassOfItsOwn` | L20 the next pass calls the transmit though input waits, then THE RETRY |
| 22 | loop | `transmit-age-before-the-retry-age` | `loop/ctrl_loop.c` | `Loop.L20AnAgedTransmitIsAPassOfItsOwn` | L20 an aged retry's pass, read first, takes its round alone |
| 23 | loop | `transmit-age-before-the-step-age` | `loop/ctrl_loop.c` | `Loop.L20AnAgedTransmitIsAPassOfItsOwn` | L20 an aged step's pass, read first, takes no build |
| 24 | loop | `transmit-age-read-after-the-input` | `loop/ctrl_loop.c` | `Loop.L20AnAgedTransmitIsAPassOfItsOwn` | L20 the age is read once as the pass starts, before it takes any input |
| 25 | loop | `tick-pass-uncapped` | `loop/ctrl_loop.c` | `Loop.L21APassThatDispatchesACentisecondTakesOneRecordOfAChannel` | L21 a pass that dispatches a centisecond takes CTRL_LOOP_RX_PER_TICK_PASS records of a channel |
| 26 | loop | `tick-cap-in-every-pass` | `loop/ctrl_loop.c` | `Loop.L21APassThatDispatchesACentisecondTakesOneRecordOfAChannel` | L21 the next pass, which dispatches none, takes CTRL_LOOP_RX_PER_PASS |
| 27 | loop | `tick-cap-ignored` | `loop/ctrl_loop.c` | `Loop.L21APassThatDispatchesACentisecondTakesOneRecordOfAChannel` | L21 a pass that dispatches a centisecond takes CTRL_LOOP_RX_PER_TICK_PASS records of a channel |
| 28 | srp | `transmit-built-by-the-poll` | `srp/srp_mbx.c` | `TransmitWaitsForAPassThatTakesNoRecord` | a pass that takes a record builds no MRPDU |
| 29 | srp | `transmit-hold-unreported` | `srp/srp_mbx.c` | `TransmitWaitsForAPassThatTakesNoRecord` | a held build is reported owed |
| 30 | srp | `transmit-centisecond-holds-nothing` | `srp/srp_mbx.c` | `TransmitWaitsForAPassThatTakesNoRecord` | a centisecond holds a build |
| 31 | srp | `transmit-record-holds-nothing` | `srp/srp_mbx.c` | `TransmitWaitsForAPassThatTakesNoRecord` | a received record holds a build |
| 32 | srp | `transmit-unbinding-holds-nothing` | `srp/srp_mbx.c` | `TransmitWaitsForAPassThatTakesNoRecord` | an unbinding that withdraws a declaration holds the build that sends it |
| 33 | srp | `transmit-binding-holds-a-build` | `srp/srp_mbx.c` | `TransmitWaitsForAPassThatTakesNoRecord` | a binding holds no build itself |
| 34 | srp | `transmit-walk-holds-nothing` | `srp/srp_mbx.c` | `TransmitWaitsForAPassThatTakesNoRecord` | the walk that finds its declaration holds the build that declares it |
| 35 | srp | `transmit-reentry-unguarded` | `srp/srp_mbx.c` | `ReentryFromOutputIsRefusedAndCounted` | adapter.reentries |
| 36 | srp | `transmit-not-bound` | `srp/srp_mbx.c` | `TransmitWaitsForAPassThatTakesNoRecord` | the next pass that takes no record builds one |
| 37 | srp | `transmit-attaches-over-a-bound-client` | `srp/srp_mbx.c` | `AttachmentFailureIsAtomicAndDetachesAfterLoopReset` | a loop whose THE TRANSMIT client is bound is refused |
| 38 | srp | `transmit-kept-by-destroy` | `srp/srp_mbx.c` | `AttachmentFailureIsAtomicAndDetachesAfterLoopReset` | destroy detaches THE TRANSMIT's client |
| 39 | srp | `transmit-age-counts-unheld` | `srp/srp_mbx.c` | `AHeldBuildTakesAPassOfItsOwnPastItsAge` | the build's pass follows the one that dispatches the centisecond past its age, counted from its hold |
| 40 | srp | `transmit-aged-at-its-limit` | `srp/srp_mbx.c` | `AHeldBuildTakesAPassOfItsOwnPastItsAge` | the build's pass follows the one that dispatches the centisecond past its age, counted from its hold |
| 41 | srp | `transmit-age-kept-by-a-build` | `srp/srp_mbx.c` | `AHeldBuildTakesAPassOfItsOwnPastItsAge` | two builds' passes stand more than CTRL_LOOP_TX_AGE centiseconds apart |
| 42 | srp | `transmit-aged-beside-an-owed-frame` | `srp/srp_mbx.c` | `AnOwedFrameComesBeforeTheBuild` | no held build takes a pass of its own while a frame is owed |
| 43 | srp | `transmit-builds-beside-the-owed-frame` | `srp/srp_mbx.c` | `AnOwedFrameComesBeforeTheBuild` | the pass whose poll sends the owed frame builds no other |
| 44 | srp | `transmit-declarations-in-the-poll` | `srp/srp_mbx.c` | `OwnDeclarationsThatRewriteARegisteredValueAreCopied` | over-saturated |
| 45 | srp | `transmit-reclaim-before-the-declarations` | `srp/srp_mbx.c` | `SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding` | a refused adoption takes no room a retained receive waits for |
| 46 | srp | `transmit-reclaim-only-with-the-build` | `srp/srp_mbx.c` | `SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding` | adapter.received |
