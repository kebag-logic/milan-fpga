Run from a clean clone at `48f12dc14099a3630a98eb07e9ec790695a72bfb`, with the three required public submodules initialized at their gitlinks. Use an empty packet scratch directory and the verified 5.050 simulator. No command writes tracked source or contacts a hardware target.

```sh
rtk proxy python3 <packet>/scripts/run_focused.py . <packet> <simulator> --jobs 4
rtk proxy python3 <packet>/scripts/run_seed_probe.py . <packet> <simulator>
rtk proxy python3 <packet>/scripts/verify_tree.py .
rtk proxy python3 <packet>/scripts/verify_merge.py . <packet>
```

The first command runs the clean harness and 26 mutation builds, joined before exit. The second runs the independent exhaustive compiled-state check and its zero-seed negative control. Run these two build campaigns sequentially: each is capped at 16 compiler workers. Other scripts only read/parse evidence. All generated sources, models and temporary indexes go under `<packet>/scratch/`.

The resource checker takes the published directory at archive `84add8ed571d376f8a1b39c3c6f71c4e80eed32a`. Fetch that exact archive commit if absent, and extract only `review-evidence/686-r1/author-r2/resource-receipts/` into packet scratch. It does not need another reviewer's packet.

```sh
rtk proxy python3 <packet>/scripts/verify_resources.py . <packet> <resource-receipts>
```

Expected at archive 84add8ed: all six individual regenerations exit 0 and print `record EQUAL`; all three current endpoints pass baseline F. The combined script exits 1 because four archived orchestration scripts have stale inner-manifest hashes (R549-2-F1). This failure is retained, not masked. The helper reads exact commit objects and rehashes decompressed input content, so gzip compression level is immaterial to record equality.

Read `receipts/public-inventory.json` for the public snapshot underlying the retained source-bank publication portion of R549-1-F4. Publishing those banks requires no reviewer source change.

`receipts/` contains raw run outputs and exit statuses. Build logs replace private simulator installation prefixes with `<simulator-root>`; `receipts/redactions.json` records original/published SHA-256 values. No measurement or test-output value is changed. The original logs and all builds remain in unpublished scratch. `MANIFEST.sha256` covers every publishable file other than itself; REPORT.md is included too.
