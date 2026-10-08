[A560] REVIEW READY

Round 11 head: `b98eb2d5a21522bab3bc6bb943332cf8edf11893`. Relates to #665; PR #690.

Changed: per-sink/per-interface feedback retains the first withdrawal and its preceding registration kind through composition delivery. Continuous kind changes use the authorized settled-view ACMP entry. Pending replacement, supersession and transient-refusal behavior have integration cases and discriminating plants.

Validation: all 113 final gate receipts return 0, including every Round 10 gate. The complete `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` campaign catches 471 control plants, 160 SRP plants, two pin controls and 59 IF=1 repeats. All four named round-10 plants are caught at IF=1/2. The nine applicable original reviewer probes pass at each interface count. Coverage writer/checker retain 100% in all 22 files with no added exclusions. GCC/Clang plain and AddressSanitizer controls, saved-state tests, mailbox, differentials, images, compiler audits, documentation and full builder verification pass.

The builder receipt covers `803e8c3c9e7506c4f004d562437ae4f374fbad8e`; the only subsequent change is the mutation-oracle entry number, outside builder inputs. The complete firmware campaign and final documentation checks use the head above.

The six-access-per-sink feedback allowance gives four-module bounds of 3224 / 4073 accesses. Linked spans are 79904 / 92576 bytes for 1x1 and 94736 / 122240 for 8x8 at IF=1/2. Timing remains an uncalibrated conditional host envelope; stack is a reservation. Builder evidence retains its documented unavailable calibration-report NOT RUN.

Acceptance evidence and reproducible commands are recorded in the Round 11 handoff and PR-body packet. No mailbox, register-map, RTL, default-build or shipping-image change was needed. Independent corrected-head review, finding closure and the remaining integration/merge bar remain pending.
