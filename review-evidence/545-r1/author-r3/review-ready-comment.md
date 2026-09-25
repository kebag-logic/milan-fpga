[A308] REVIEW READY

Commit: `92ad1687d84ff077f872719b4f1df601f82064d2` (local, unpushed).

Changed: U15 arms one guard trip; both counting variants now fail its named check and join the explicit campaign. The hosted budget basis and connected-campaign triggers are current. No RTL logic or processor pin changed.

Validation: all assigned local gate commands returned 0. Clean two-CPU default: 936.448 s versus round 2's 952.797 s; 100/8/113/90 checks pass. The servo campaign passes 10/10. The unchanged reviewer script reports CLEAN-PASS and four KILLED verdicts. The connected leg passes 58/58; its full campaign passes 16/16. All 33 default datapath commands return 0. Area reproduces the prior figures, with no round-3 delta.

Acceptance: assignment items 1-3 addressed. Builder gate 11 calibration is NOT RUN because its required board report is absent; all executed arms pass. The conservative release-tail observation remains outside this round under #495.

`HANDOFF.md` and the complete updated `PR-BODY.md` are prepared in the assigned packet. Independent re-review and new hosted evidence remain pending publication. No push, PR edit, dev merge or hardware operation was performed.
