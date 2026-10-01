[A477] STOP

**Condition.** The lane rules make one precondition a STOP. The bench host's hand-set address on the SoC board's USB network link must be present. At 12:57 CEST it was missing.

**Evidence (read-only, on the bench host only):**
- The link's interface is up with carrier, but it holds no IPv4 address.
- The SoC board's USB audio function and the external audio capture are both present on the bench host.
- The host restarted at 12:02:44 CEST. The host's own log shows the interface appearing at 12:03:18 CEST. An automatically created address configuration was activated on it. That configuration fails and retries every 45 s: 28 attempts by 12:54 CEST, every one failed.
- The static configuration that carries the address exists, but it is not the one active on the link.
- So the hand-set address is gone. Each automatic re-activation would also clear it again.

**State.**
- No bench action was taken: the lock was never held, and no console, SoC board, controller-host, DUT, reference-peer, capture or power-strip access occurred.
- Nothing changed anywhere, so nothing needs restoring.
- No commit: `b6-bench-1001` stays at `ea3fb388`. No findings page was written and no PR exists.

**Not done.** Everything from the identity gate onward: the tool controls, Direction A (A0, A1, A2), Direction B and the restore.

**Owner item.** Put the bench host's address back on the SoC board's USB network link, in a way the automatic configuration does not replace. Then resume this lane from the identity gate.
