**Ruling: CPU margin before the flip train's final measurement.** Decided for the owner under the delegation of 2026-11-11. No owner bound or date moves.

1. **The trigger.** Several AECP records sit at their statements, and code placement alone moves them across: the 1x1/1if paced map edit measures 310 us on one image and 320 us on another, against 310. A restatement by the rule (measured + 5 %, up to 5 us) would push 1x1/1if's last-queued-notice row past its 140 ms bound, which never moves.
2. **A projection now, with no build.** Take each thin record at its worse measured value plus the rule: the map edit at 340 us, 8x8/1if's largest legal command at 1,850 us, and the held SET_STREAM_INFO past 245 us. Run the row rules and list every held row or owner bound that breaks. Only those are cut; the rest restate by the rule.
3. **A margin-recovery logic cut starts now.**
   - It targets 1x1/1if's last-queued-notice row, sized so the row holds 140 ms with the map edit at 340 us.
   - A structural saving (per-notice cycles, or the edit split across passes) is preferred to shaving the edit back to its statement.
   - It is based on the train head with #943's current round, and joins the train as step 15 with ordinary reviews, before the final measurement.
4. **Pinning link order or alignment is rejected for the train.** It hides a zero-margin statement and breaks on the next change. It may be raised after the flip.
5. **The final head's image rules.** No statement is taken from a luckier image.
6. **Owner trigger:** if the cut cannot give the 140 ms row real margin by the weekend, the choice between the bound and the date is the owner's.
