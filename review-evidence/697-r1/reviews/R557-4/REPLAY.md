Portable review replay

Use a detached checkout of 625b001173fda5f6401af1dceaef8d8ab86f5ae9 with the repository's documented native and RV32 dependencies. Set REPO to that checkout and PACKET to a fresh packet directory. All disposable output belongs beneath PACKET/scratch. These commands run in the foreground.

```sh
python3 scripts/run_checks.py --repo "$REPO" --packet "$PACKET"
python3 scripts/source_audit.py --repo "$REPO" --packet "$PACKET"
python3 scripts/compare_objects.py --repo "$REPO" --packet "$PACKET"
python3 scripts/prior-unchanged/comment_probes.py "$REPO"
python3 scripts/prior-unchanged/needle_probes.py "$REPO"
python3 scripts/prior-unchanged/regrade.py "$REPO" "$PACKET/scratch/checks/mutations"
python3 scripts/independent_comment_probes.py --repo "$REPO" --work "$PACKET/scratch/comment-probes"
python3 scripts/full_comment_bypass.py --repo "$REPO" --work "$PACKET/scratch/full-comment-bypass" --output "$PACKET/receipts/full-comment-bypass.json"
python3 -O scripts/needle_ownership_probes.py --repo "$REPO" --output "$PACKET/receipts/needle-ownership-probes.json"
python3 scripts/verify_checkout.py --repo "$REPO" --output "$PACKET/receipts/checkout-final.json"
```

The repository checks pass. The unchanged prior comment probes print gaps: 0; all default-output needle fragments are refused. The full assembly bypass script returns zero when it reproduces the defect, with bypass=true and object_bytes_equal=true. This is evidence of a gate failure, not successful refusal. The signed-zero exploratory probes do not drive the finding.

The prior needle script places its final MAAP message in an unrelated test's table entry, so that final message must also be refused. needle_ownership_probes.py supplies the correctly owned positive control.

The native/campaign supervisor bounds compiler work to 16 combined workers. It records each subprocess return code and waits for all lanes. compare_objects.py uses its generated compile databases and the base snapshot prepared by source_audit.py. The unchanged prior scripts are preserved byte for byte; their public source URLs and hashes are in receipts/prior-script-provenance.json.

For a reused optimized campaign, run the repository's scripts/mutation.py from REPO with --work "$PACKET/scratch/checks/mutations" --jobs 16, then repeat the regrade. The expected result is 311 caught plants and 329 matched killers. Render repository diagrams with scripts/render_graphs.py --output "$PACKET/scratch/graphs".

The published logs have location-only redactions. Original local receipts and disposable builds are excluded from publication. No GitHub write is needed for replay.
