Reviewer receipts for R703-2 (PR #792, head cd3525c3ddcbdb5d78bf8fccdab354c468926997).
Host path substitution in published copies: the product LiteX tree is written $LITEX and the user's home
$HOME (build.json copies, environment.txt, stale_probe2.log). Every other receipt is byte-for-byte as produced.
runs/<name>/        results.json, table.md, build.json and the printed summary + rc of each harness run:
                    a1x1, a8x8 = arm A; b1x1, b8x8 = arm B (7 groups); s1x1, s8x8 = shutdown-entry arm;
                    c-slow, c-slowsd, c-asbuilt = the harness's three controls
gates/              docs, idiom, hygiene gates and git diff --check at the head; summary.txt has every rc
selftest.log        run.py --self-test at the head
compare_published.txt, build_identity.txt     my runs against the published packet (33750832)
evidence_manifest_check.txt                    the published packet's blob SHA-1 and manifest sha256 checks
recompute_A1.json, recompute_A8.json          round-1 independent recomputation (scripts/recompute.py), unmodified
population_fanout_*.txt, drain_*.txt          raw-log composed populations, records ahead, SET_NAME fan-out, per-pass releases
readme_cells_vs_results.txt                    each path's worst instance found in the README
review_mutants_unmodified.log, review_mutants2.log, mutant_regrade_escapes.txt   self-test mutants (probe 3, F3)
stale_probe2.log, regrade_probe.txt           reuse attestation and regrade refusal probes (probes 4 and 5)
fixture_regen.txt                              fixture and oracle regenerated from my 1x1 fixture run
srp_service.txt, srp_service_armB.txt, srp_tail_1x1.txt, probes/srp-tail-1x1/   SRP service under the composed load (F1)
fanout_full_*.txt, probes/fanout-full-*/                     SET_NAME fan-out at the registration capacity (F2)
clone_identity_final.txt                       the clone restored to exact head bytes, modes, index and gitlinks
environment.txt                                tool identities
