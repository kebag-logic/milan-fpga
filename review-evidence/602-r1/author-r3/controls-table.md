| Control | Required failure | Observed failures |
|---|---|---|
| the policy level is tied low at the servo | slew path: the actual servo receives the level | 2: slew path: the actual servo receives the level; slew path: every staged sample covers the PHC tail |
| the policy level omits the applied-rate tail | slew path: every staged sample covers the PHC tail | 1: slew path: every staged sample covers the PHC tail |
| the policy level misses an extra addend stage | slew path: every staged sample covers the PHC tail | 1: slew path: every staged sample covers the PHC tail |
| the PHC re-base restart term is restored | restart: a PHC-only step leaves outgoing mr unchanged | 2: restart: a PHC-only step leaves outgoing mr unchanged; restart: a PHC-only step adds no MEDIA_RESET |
| the source-change term is removed | source control: a real source change toggles mr once | 1: source control: a real source change toggles mr once |
| selected CRF mr propagation is removed | CRF control: selected CRF mr propagates exactly once | 2: CRF control: selected CRF mr propagates exactly once; coincident: a PHC step does not suppress the CRF restart |
| the grandmaster identity re-bases the render stage as well as the step | render: the GM change is one counted re-base event | 2: render: the GM change is one counted re-base event; render: every counted re-base lands at a PDU end right after the step |
| the step does not re-centre the render stage | render: the GM change is one counted re-base event | 1: render: the GM change is one counted re-base event |
| the render re-base is keyed to the identity, not the step | render: every counted re-base lands at a PDU end right after the step | 1: render: every counted re-base lands at a PDU end right after the step |
| tu reaches the talkers four cycles late | tu: set in the first cycle the bank names GM B | 1: tu: set in the first cycle the bank names GM B |
| the plane's step does not re-arm the holdover | tu: held at least the 0.25 s holdover after the step | 1: tu: held at least the 0.25 s holdover after the step |
| tu stops the talker | licence: the talker never pauses beyond four of its intervals | 6: tu: talker PDUs graded inside the hold; licence: the talker never pauses beyond four of its intervals; licence: the talker keeps its baseline rate within 1%; restart: a PHC-only step adds no MEDIA_RESET; coincident: PDUs bracket every trial and complete the hold; coincident: a PHC step does not suppress the CRF restart |
| the grandmaster change stops the talker for good | licence: the talker never pauses beyond four of its intervals | 8: tu: talker PDUs graded inside the hold; tu: talker PDUs graded after tu clears; licence: the talker never pauses beyond four of its intervals; licence: the talker keeps its baseline rate within 1%; CRF control: outgoing PDUs bracket the received toggle; CRF control: selected CRF mr propagates exactly once; coincident: PDUs bracket every trial and complete the hold; coincident: a PHC step does not suppress the CRF restart |
| the step's re-centre snaps one event off the setpoint | render: every PDU push leaves the target fill across the event | 1: render: every PDU push leaves the target fill across the event |
| software settime is restored as an mr cause | CLKV: the settime leaves mr unchanged (#602) | 2: CLKV: the settime leaves mr unchanged (#602); CLKV: settime adds no MEDIA_RESET (#602) |
| PHC adjtime is restored as an mr cause | CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) | 1: CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) |
| both PHC restart causes are restored | CLKV: the settime leaves mr unchanged (#602) | 3: CLKV: PHC-only steps leave INTERNAL mr unchanged (#602); CLKV: the settime leaves mr unchanged (#602); CLKV: settime adds no MEDIA_RESET (#602) |
| PHC adjtime becomes an mr cause 16 cycles later | CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) | 1: CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) |
| PHC adjtime becomes an mr cause 256 cycles later | CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) | 1: CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) |
| a PHC step suppresses a coincident CRF restart | coincident: a PHC step does not suppress the CRF restart | 1: coincident: a PHC step does not suppress the CRF restart |
