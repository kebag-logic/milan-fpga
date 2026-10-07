Run from an isolated checkout of f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152.
Keep this packet's scripts together. They locate output relative to the packet and use only scratch/ for dependencies, builds and mutations.
Use a fresh scratch directory for a complete replay; existing reversal directories are intentionally rejected.
Dependencies: Python 3, Git, a C compiler, CMake, Make, the graph renderer and its browser, and authenticated repository access for the link check.
The unit framework is built locally from release 1.7.0, with resolved commit feeb85ed48d163f6b7b0011a6d8e6043951541e4 checked explicitly.

Set PACKET to this packet directory and CHECKOUT to the exact-head checkout. All commands remain foreground commands.

```sh
cd "$CHECKOUT"
python3 "$PACKET/scripts/run_checks.py" dependency
python3 "$PACKET/scripts/run_checks.py" docs
python3 "$PACKET/scripts/run_checks.py" links
python3 "$PACKET/scripts/run_checks.py" graphs
python3 "$PACKET/scripts/run_checks.py" OFF
python3 "$PACKET/scripts/run_checks.py" ON
python3 "$PACKET/scripts/check_inventory.py"
python3 "$PACKET/scripts/focused_reversals.py" --profile OFF
python3 "$PACKET/scripts/focused_reversals.py" --profile ON
python3 "$PACKET/scripts/verify_checkout.py"
```

Independent foreground invocations may run concurrently through a foreground supervisor that waits for every child.
The profile build lock keeps the total compiler-worker ceiling at 16.
The reversal driver has no jobs option; each profile uses its unchanged two-worker build command.
The focused wrapper selects the three relevant cases in memory and otherwise runs the repository's original driver.
It changes only disposable source copies and retains every campaign command, return code, output, and restored-byte digest.

The original runs' raw outputs are in receipts/. Check the published packet from its root with:

```sh
sha256sum -c MANIFEST.sha256
```

The inventory and checkout scripts write their JSON results to standard output.
The final audit expects those results in receipts/inventory.json and receipts/checkout-final.json.
It audits actual failure records, rather than accepting a test name appearing anywhere in output.
Only files listed in MANIFEST.sha256 and REPORT.md are publication inputs. scratch/ is excluded.
