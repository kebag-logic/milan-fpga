# Focused reproduction

Run from this packet directory. Set REVIEW_ROOT to a detached checkout of
8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb. Initialize the five submodules
listed in checkout-before.log at their gitlinks. All disposable data stays in scratch/.

```sh
rtk proxy python3 -B verify_checkout.py "$REVIEW_ROOT"
rtk proxy python3 -B check_figures.py "$REVIEW_ROOT" "$PWD/scratch/figures"
```

The figure probe calls the repository's actual pin_controls and figure checker.
Expected: 192 pin controls, zero misbehavior; populations 103/8/5/192;
the current page passes; the old 185 value fails; all four one-more controls fail by name.
It uses poisoned disposable stack clones and a simulator substitute, not an RTL build.
No full compiler-boundary/builder bank is invoked.

The recorded supplemental pin-control run used timeout 600 and ended rc=124
after 185 successful controls. Its final counter prerequisite control and six
lifecycle controls did not finish. A complete local pass is not claimed.
The independent completed figure-only check is reproducible with:

```sh
rtk proxy python3 -B check_figure_contract.py "$REVIEW_ROOT" 192
```

Here 192 is supplied from the published executed count and seven-target derivation;
this entry point does not pretend to execute the pin controls.

Run these from REVIEW_ROOT, using a scratch virtual environment with
tools/markdown/requirements.txt installed via --require-hashes:

```sh
rtk proxy python3 -B scripts/docs_inventory.py --check
rtk proxy python3 -B scripts/docs_check.py
rtk proxy python3 -B scripts/check_em_dash.py --base 15168e14
rtk proxy python3 -B scripts/gen_toc.py --check
rtk git diff --check 15168e14 HEAD
```

The system interpreter initially lacked html5lib; the em-dash and contents
checks refused with rc=2. Their setup logs are retained. The final runs used
scratch/venv/bin/python with the repository's hash-locked dependencies and passed.
No shared package installation was performed.

For published evidence, fetch eea845dba7b561499de5cf537a5b665d72e278b1 into
the clone, and run check_packet.py and spotcheck_receipts.py with that clone as
the working directory. They read Git blobs directly. They execute no packet code.
The first verifies manifest hashes; the second prints bounded raw receipt sections.

```sh
rtk git merge-tree --write-tree aa30d77f75cd97b3a29878ca0ed68010a7629266 8aeb2f0bb9bfad9c486a0abf9dbeaf134d3de2fb
```

Expected merge tree: 0e5c07bdf20743cfa16be75379315462b53ba26d.
Comparing all Makefiles and sw/firmware/ctrl/test/ctrl_*.py with the source head
produces no differences. This is a count-dependency check, not validation of
the final current-dev merge candidate.

After probes rerun verify_checkout.py. No tracked source byte or index entry
should change. MANIFEST.sha256 lists publication files; scratch/ is excluded.
