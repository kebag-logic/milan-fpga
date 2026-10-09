[A572] STOP
Head: 5603c353137e90c1fa95429f6d00ef7a2298d9ee
Branch: 665-f5-aecp. No repository edits or commits; working tree clean.

The assignment's linked-image STOP condition is reached in a sizing preflight.
At the assigned base, the existing ADP/ACMP/MAAP/SRP composition for the largest
shape with two interfaces uses 122672 bytes. A scratch-only link retaining the
existing F1 store boot/service raises the span to 147360 bytes, before any AECP
code or descriptor image. Sections: text 56948, rodata 3458, data 0, BSS 78744,
existing stack reservation 8192. The four requested sections alone total 139150,
already 8078 bytes above 128 KiB. Static pools are included in BSS, not added twice.

Matching-runtime links for shipping/largest at one/two interfaces all returned 0
(8/8). Store-composed spans: 94688, 107344, 119856, 147360; respective deltas from
base: 14320, 14320, 24688, 24688 bytes. This is a size fixture with existing stub
state owners, not implemented F5 or evidence of an irreducible minimum.

Supplemental retained-image instruction audits pass (8/8); omitted-store and
wrong-ELF-flags controls reject. A broader all-input audit returns 1 for vsnprintf
in a discarded debug-print section, on both base and probe; no closure pass is
claimed. Initial runtime stack-protector link dependencies were resolved by
rebuilding the recorded runtime sources with the firmware no-stack-protector flag;
both matrices use that same runtime.

HANDOFF.md, PR-BODY.md, reproduction scripts, coverage/gate tables and artifact
hashes are in the requested output directory. Implementation, behavioral tests,
wire differential, latency and the full acceptance gates remain unperformed.
Processor #73 remains open; future single-command-model adoption is owed.
No default/shipping image, RTL or register map changed. Work is stopped pending
a public budget disposition or scoped memory reduction.
