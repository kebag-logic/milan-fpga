R244-1 independent-pass draft, written before reading any prior public finding
or other reviewer report on PR #519. Exact head 4671e582cfa4bba4809b9e3a354ce5b6eb967f99.

A (MAJOR; Conformance, RTL, Robustness, Tests, Docs): a filesystem codec that
does not round-trip (Big5, Big5-HKSCS) moves a Git filename to other bytes;
T reads the resulting empty ls-tree as absence in all three commits and
reports contained/0 for a tip that reverted the source change. Base 52711029
reports STRANDED/1 for the same history; head under UTF-8 reports UNKNOWN/1.
Receipt: receipts/probe-big5.txt, probes/probe_big5.py.

B (MINOR; Tests, Robustness): default self-test crashes (exit 1,
UnicodeDecodeError) under an ASCII-encoded parent because
merge_containment_selftest_mutations.py reads/writes the checker source with the
locale encoding; base self-test passes 145/145 in the same environment.
Receipts: mut/control-ascii-parent, receipts/selftest-base-ascii-parent.out.

C (MINOR; Tests): documented T guards survive mutation of the full self-test
(455/455): --no-renames in the retention diff, --ignore-submodules=none under
diff.ignoreSubmodules=all, exactly-one merge base (fault injection masks it);
two of these produce false contained/0 on real histories. Receipts:
receipts/mutations.json, receipts/probe-guards.txt.

Out of scope (pre-existing, unchanged arm): running the checker from a
subdirectory reports contained/0 for stranded linear work at base and head.
Receipts: receipts/probe-subdir-{base,head}.txt.
