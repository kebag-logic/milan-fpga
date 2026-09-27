[A375] Measurement notes

Cycle 1 used the controller-cycle01.py watcher. Its carrier reads share the query loop, so query timeouts delayed the observed down edge. Cycles 2-10 use controller.py, with a separate 100 ms carrier sampler. Both perform the same read-only query round. Neither changes any binding or clock selection during a cycle.

The final analyze.py was rerun over every cycle. It uses unwrapped tap timestamps, a median host anchor, and measured host offsets. Early progress estimates for cycles 1-2 used acquisition timestamps directly; final tables use the uniform final calculation. Raw captures are unchanged.

The CRF validator checks the exact bound stream ID, subtype, version, audio timestamp type, 48 kHz base frequency, eight timestamp-data bytes, interval 96, VLAN 2 and priority 3. Ethernet padding is permitted. Captures omit the FCS, so this is a PDU-shape check rather than a physical CRC measurement.

MEDIA_RESET counts intervals and resets at STREAM_START. Full trajectories are retained. No hidden toggle count is inferred across a wire gap. No later restart rule is applied.

The first capture preflight failed because the approved tap lacked a matching driver after the host kernel changed. No power command ran. The temporary driver repair and its cleanup are recorded separately.
