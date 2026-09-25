[A10] Decision on acceptance 2 (R307-1 F2).

"PASSIVE after bind" in acceptance 2 is read as follows. After BIND_RX the stream input is ACTIVE with `acmp_status` 0, because a canonical bind sends PROBE_TX immediately (Milan v1.2 5.5.3.5.3; processor `05_acmp_engine.md`, `00_MILAN_COMPLIANCE_REVIEW.md:318`). It becomes PASSIVE after an unanswered retry with no discovered talker.

That is the Milan-correct behaviour, and it is what the `milan_dp` GSI leg grades: G1 is ACTIVE with `acmp_status` 0 on bind, and G3 is PASSIVE after the unanswered retry. The literal "PASSIVE after bind" in the frozen text described a model with no immediate probe. The processor as pinned does not implement that model, and it should not. No source change is required. The executors raised this distinction publicly in 5822002238 and 5825445388.
