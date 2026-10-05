Source: https://github.com/kebag-logic/milan-fpga/issues/661

Adopt protocol-processor main ead80360 (second pin adoption: wave 2, P1/P2, C10, #85, the three area lanes, #81/#84)

The parent's second processor pin adoption, unblocked on 2026-10-05: the area work (#229) is in processor `main`, as the owner ruled on 2026-10-03.

## Scope

Move the `protocol-processor` gitlink from `631eeb34` (adopted by #635) to processor `main` `ead80360`. That brings in:
- C7 and C8 (wave 2);
- P2 and P1 (saved state);
- #143;
- C10;
- #85 (processor PR #152);
- the three area lanes: #232 (PR #153), #230 (PR #154) and #639 (PR #155);
- #81 / #84 (PR #157).

## Parent adaptations owed

Each was validated in its lane's consumer set:
- `parent-adoption-c8-bbf704ec.patch`;
- `parent-adoption-p2-p1-1269cdaf.patch`, together with the saved-state contract amendment P2 requires;
- `parent-adoption-c10-1269cdaf.patch`, including the `check_rtl_source_lists` self-test amendment;
- `parent-adoption-232-241f9184.patch`, the xvlog budget;
- the parent clean-ups the first adoption left: drop the duplicate L10/L6 checks;
- the REGISTER_MAP `0x644` `available_index` note (it resets after departing; PR #152);
- every pin-derived record re-recorded through its generator: ROM digests, the submodule pin page, the boundary diagram, and the port-contract and naming records.

## Acceptance

1. The gitlink is at `ead80360`, with the adaptations above and no other processor change.
2. #638's resource gate is re-baselined at the adopted image, as the re-baseline rule requires. The re-baseline closes #639, whose last item is "the gate's baseline re-recorded", and #234's criterion 2.
3. The saved-state capture is re-measured if the firmware digest moves (`check_nvm_capture.py`; the 8x8 maximum stays at or under 24.5 ms).
4. Every parent gate and suite passes, including the image build and route with WNS ≥ 0 at 50 MHz.
5. After the merge, the manager flashes the image and runs the soak on the bench.

Relates to #629, #229, #234, #639.
