This packet reviews source head `8883d4998496c6d2e234143b43807731e8851b63`, tree `a169a601df764715eec1b404b16da3df73217142`. Commands below use an exact-head disposable checkout as `review_root` and the extracted packet as `review_packet`. All scripts take explicit paths. Keep temporary files under the packet's `scratch/` directory.

```sh
review_root=/path/to/exact-head-checkout
review_packet=/path/to/894b-r844-4-packet
mkdir -p "$review_packet/scratch"
export TMPDIR="$review_packet/scratch"
export PYTHONDONTWRITEBYTECODE=1
python3 -B "$review_packet/scripts/verify_checkout.py" "$review_root"
python3 -B "$review_packet/scripts/focused_checks.py" "$review_root" "$review_packet/scratch/repeated-checks"
python3 -B "$review_packet/scripts/transmit_contract_probe.py" "$review_root"
python3 -B "$review_packet/scripts/published_rows_recipe.py" "$review_root"
python3 -B "$review_packet/scripts/record_classes_mixed_probe.py" "$review_root/tb/verilator/ctrl_service_budget"
```

`focused_checks.py` runs four lightweight checks concurrently and waits for all of them. No firmware build or bank is launched. It includes the harness's `run.py --self-test`, which is considerably longer than the other checks. The recorded first attempt used the wrong spelling `--selftest` (harness.rc = 2); the script now uses the corrected spelling, whose actual run is in harness-corrected.log/rc. Do not reinterpret the first invocation error as a repository failure. Self-test output includes deliberately simulated `ESCAPED` cases; the final failure total and exit code determine the self-test result.

The transmit probe is diagnostic and prints its envelope failure; its process exit is not a gate verdict. It uses the published 8x8/1if input recipe because default rows_tiers inputs omit that point, then invokes the existing tx_statements checker with the resulting inputs. It makes no disk mutation to the source. The mixed-point probe likewise reports refusal counts rather than a process-level gate; expect two findings in its first case at this head.

For the old-module control, copy the harness into `scratch/old-module/`, replace **only** record_classes.py with the blob from af2c4d7a, then run the same mixed probe with that directory. The first mixed case has zero findings. This is a module control, not a claim to execute the entire old tree.

Public archive: repository commit `88f4b944a0be6b418cab966e9828ea2bcc3716f5`, directory `review-evidence/894b-r1`. Extract MANIFEST.json and author-r* paths only, excluding nested receipts/reviews/ paths to `scratch/public/`. The copied published_rows_recipe.py is the public author's current row recipe; mixed probe is the public prior mixed-point probe. The other probes are reviewer-written.

```sh
python3 -B "$review_packet/scripts/verify_archive.py" "$review_packet/scratch/public"
python3 -B "$review_packet/scripts/ledger_boundary_probe.py" "$review_root" "$review_packet/scratch/public/author-r10/receipts/harness/legs-46cf2a7d/M8-A3/leg.log"
```

The ledger probe reads the published measured log, verifies its baseline, and raises each of seven ledger rows in memory by 0.001 ms above its limit. All must be refused by name. Image checks compare published SHA256 receipts, not rebuilt binaries. The archive hash check authenticates content against the manifest, not a signer. Published-r7 receipts are historical evidence, explicitly named as such.

After any probe, run verify_checkout.py again. It computes literal Git blob hashes, modes and index entries, checks each initialized submodule at its required gitlink, and discloses uninitialized gitlinks. Scratch contents are disposable and excluded from publication. MANIFEST.sha256 inventories only publishable files, with paths relative to this packet.
