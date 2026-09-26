[A340]

Closes #502

## Status

Implementation and merge-dev validation are complete.
Independent review and hosted checks remain outstanding.

## Description

A changed name or audio map previously became live before its later command mark raised saved-state pending. During that interval, persistence status could claim durability over an unsaved value.

The parent now raises pending on each accepted name write and map phase-5 commit beat. The accepting pulse feeds the backend alongside sticky history, so status changes on the accepting edge. Both paths share the backend clock and reset. Later command marks retain their completion meaning.

The processor pin advances to `870ff88ad35bbd532244e4c7e6d7661b9f6e1366`, which exports the accepted name-write event. The consumer connects that event and retains the test-reader disposition. Pin documentation, the generated boundary diagram, ROM ledger, changelog and saved-state contracts follow the implementation.

K10/K12 execute real name and mapping commands through the shipping datapath. They check status from live acceptance through command completion and snapshot acknowledgement. Controls cover unchanged and repeated commands, refused output edits, both map directions, reset and the initial durable baseline. Reinstating the late-mark trigger must fail both durability checks.

Name and map record writers remain outside this issue. Their pending source clears only on reset; this change adds no flash-persistence claim. Firmware and the CSR layout are unchanged.

## Merge-dev

Merged `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf` into implementation head `87e263fd1d71b1a7a04a2e9c9339220f35e4348f`.
The resulting head is `104c8a54b183cd9215ed1e3a2e1be1634f48d33d`.

- Retained processor `870ff88a`, which contains `0922e434`.
- Kept both unreleased changelog entries.
- Preserved the earlier pin adoption history while identifying the current pin.
- Retained the recorded ROM rows for both adopted pins.
- Regenerated the boundary diagram and raster manifest from the resolved index.
- Preserved incoming CI and datapath documentation changes.

This merge introduces no further RTL, firmware or test-source change.

## How to reproduce

Start from a clean, loaded backend that reports durable status. Send a changed SET_NAME or ADD/REMOVE_AUDIO_MAPPINGS command. Observe both persistence status faces on every accepting edge until the later command mark and acknowledgement. Neither status may report durable while the changed live value remains unsaved.

## How to validate

Run the pending-status integration suite and its late-mark mutation control, the saved-state cosimulation and backend suites, and every default RTL sweep chunk. Run the complete builder in compiler-present and compiler-absent modes, firmware and capture checks, the area recipe and the repository documentation, source, lint, interface, evidence and behavior gates.

All requested local checks pass on the merge head. The default sweep passed 55 suites and 2,125,050 checks, including 11,206 in the full datapath target. Both complete builder modes passed. The area result matches the preceding implementation measurement.

The unavailable physical utilization report, deliberately absent compiler census and optional field campaigns remain explicitly outside the corresponding results. Detailed command exits and measurements accompany the review-ready evidence.

## Definition of done

- [x] Accepted live writes revoke the durability claim immediately.
- [x] Later marks retain their completion meaning.
- [x] Real-command coverage and negative controls are included.
- [x] Pin, ROM and saved-state documentation are current.
- [x] The required dev integration is committed.
- [x] Merge-head validation is complete.
- [ ] Independent review and required hosted checks are complete.
