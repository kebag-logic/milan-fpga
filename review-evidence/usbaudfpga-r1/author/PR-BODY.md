[A860]

## Status

Desk implementation and technical validation complete; the local handoff is stopped by the disclosed cleanup-rule violation. Bench acceptance remains open. Relates to #1021.

## Description

Add optional eight-channel USB playback and capture on Arty. All 32 subslot bits pass through the AVB capture mapper and render queue. Socket-3 interval records qualify explicit feedback from the gPTP-locked media oscillator. Complete frames cross clock domains; the 20-byte status acknowledges a capture epoch before new-epoch packets are sent. No sample-rate conversion is present.

The contract is [USB audio #9 at 47e6bbc9](https://github.com/kebag-logic/usb-audio/blob/47e6bbc93093c325b00a9263fdb9ceb20869ef46/docs/AUDIO-FPGA.md). The reference watchdog expires after three milliseconds on the FPGA's own clock. Feedback remains valid until the expiry edge; a coincident reference is refused and qualification restarts from a new baseline. USB bus counts and sequence determine reference continuity.

The audio option uses the split control profile and is mutually exclusive with the network option until A2 is wired. All network-attachment files remain unchanged. Shared queue storage defaults to 24 bits, and both ALINX shipping programming payloads remain byte-identical.

## How to reproduce

Generate the eight-channel Arty audio profile and enable the audio option. Link control firmware against that selection's generated register and flash maps. Use default synthesis, Explore optimization, ExtraTimingOpt placement, and AggressiveExplore routing and physical optimization. Control is 100 MHz; media and the external bus are 50 MHz. The matched audio-disabled profile is the resource baseline. The updated route uses fresh synthesis and no incremental reference.

## How to validate

The full-window million-frame run passes 37,419,648 checks with zero failures. All 24 protocol and 46 transport defect controls reach their named failures. Watchdog controls name both 2.9 ms acceptance and 3 ms refusal, including the last pre-expiry cycle and own-clock expiry without references. The default suite passes both storage widths and build-option exclusions.

All four Arty corner reports pass: minimum setup +0.002 ns, hold +0.018 ns and pulse-width slack +1.389 ns, with zero failing endpoints. Setup was +0.005 ns in the prior route; this narrow margin applies to the exact recorded artifact. All 55 pad endpoints, 13 crossing-skew bounds and finite flag-pair hold/setup pass. All 83,063 routable nets are routed without errors. Final cost is +2,592 LUTs, +5,861 registers, +454 slices and +8 block-RAM tiles, with no additional DSPs. Both complete ALINX programming-data comparisons pass, bound to unchanged inputs. Exact hashes and recipes accompany the receipts.

## Definition of done

Technical desk validation is complete. Independent internal review verified the technical delta and evidence; its overall verdict remains negative because the execution exception is unresolved. External review, protected checks and merge validation remain required. Bench acceptance must measure interval-delivery variation under load, verify coordinated reset/arming, physical bus timing and capture-DMA fencing, establish host binding and sustain bidirectional audio. Concurrent network traffic additionally requires A2 wiring. This change does not close #1021 before those measurements are accepted.

The local evidence packet discloses an execution exception: preliminary documentation self-check temporary removals lacked advance ledger entries. Their randomized names were not retained. The repeat passed with cleanup auditing; this does not retroactively satisfy the original pre-removal instruction.
