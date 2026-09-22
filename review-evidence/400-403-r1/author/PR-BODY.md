# Make SRP and stream declarations match generated reset and boot policy

DRAFT PREPARATION ONLY: unresolved acceptance and donor-policy blockers are linked below. No PR has been opened.

The builder previously accepted SRP values with no live consumer, published an ambiguous RX policy, and duplicated stream defaults across RTL and firmware. This change validates the supported fixed profile, connects the generated default VID through the authorized processor pin, emits a 2 ms factory row for each AAF/CRF output, names and programs the existing promiscuous posture, and makes active AAF/MAAP policy firmware-owned with an exact declared-output count.

Focused tests measure actual reset outputs/readback, host-compiled firmware writes, Domain default/adoption, post-filter destination handling, MAAP source boundaries, and per-output GET_STREAM_INFO and transmitted timestamps. Full 4x4/8x8 scenarios and CRF-off/on/VID 73 fixtures pass; planted binding, adoption, offset and reset defects fail their intended observations. Full manager-owned gates and independent reviews are pending.

Actual PTOF restore is unimplemented at the authorized pin: https://github.com/kebag-logic/milan-fpga/issues/403#issuecomment-5781186411 . The donor's supplementary CFLAGS group fails the parent's per-group warning-policy check: https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5781426819 . Neither is cleared by this draft. Donor PR13/6 continuity UNKNOWN and PR13/9 negative-merge history remain disclosed.

Closes #400
Closes #403
