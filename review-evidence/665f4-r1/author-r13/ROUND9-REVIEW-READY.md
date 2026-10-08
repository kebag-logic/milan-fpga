[A560] REVIEW READY
Commit: `edeef61c5a0cc6c18caa61db4019a8e378baf366`

Round 9 changes: the explicit composition owns deferred ACMP-to-SRP binding delivery, preserving interface/sink identity and retrying refusals. Unbind and replacement supersede pending requests. Added real-input integration cases and discriminating plants, executable SRP access measurements, the owned A0 overflow-byte fixture, and the requested documentation corrections. No mailbox, RTL, register-map, default-placement or shipping-image change was needed.

Validation (all final commands exit 0):
- `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$SCRATCH/campaign-verified"`: 469 control plants, 129 SRP plants at IF=2, 28 additional IF=1 plants and two pin controls caught.
- `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4`: 435 tests across five shapes; all 109 plants caught.
- Coverage writer and independent checker: all 22 files at 100% after unchanged exclusions; delivery code 63/63 lines and 32/32 branches.
- Required binding probe passes without direct delivery. All four external SRP probes are caught at IF=1/2. A0 controls pass under GCC, AddressSanitizer and Clang; each planted run fails A0 by name without an overflow.
- Builder, absent/pinned compiler audits, both image auditors, mailbox, MAAP differential, harness controls and all 75 documentation commands pass. Explicit unavailable-calibration and compiler-absent declarations retain their stated scope.

The packet contains 107 final individual receipts, the complete Round 8 gate mapping, test/plant and coverage tables, linked sizes, source hashes and integrity proof in `HANDOFF.md`, `PR-BODY.md` and `ROUND9-*`. Four-module mailbox bounds remain 3128/3977; delivery adds no mailbox accesses. Linked spans are 78784/91488 bytes for 1x1 and 93488/120960 for 8x8 at IF=1/2.

Integrity: clean committed tree and unchanged dependency pins; generated scratch removed from the source tree; no gate jobs remain running. Resource deviation: recorded peak memory was 9053396992 bytes, 53396992 above the 9000000000-byte target. Flushing finished-product cache restored headroom; the disk floor held. The packet records this excursion explicitly.

Relates to #665. Corrected-head reviews, finding closure, the lens ledger, hosted firmware-unit/rtl-fast checks after manager publication, trusted workflow replication and candidate/merge validation remain pending. REVIEW READY is implementation evidence, not a review verdict or completion of #665.
