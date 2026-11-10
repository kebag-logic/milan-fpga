Receipts of review R807-2 (PR #864 at 936e0a566867aa648fb48e772a26fec99e3619c9).
Paths are redacted: $CLONE is the reviewer's clean detached clone of the head, $PACKET this packet,
$LITEX the host's LiteX tree (its venv supplies migen), $TOOLS the host's pinned tool directory.
gates/       the delta's lane gates run at the head (scripts/gates.sh), one log and rc each; the
             *-hostpy-nomigen and docs-first-no-renderer files are the first runs under the host python
             without migen or the Markdown renderer, kept; each gate was re-run in the right environment.
mutants/     generator mutation probes (scripts/mutants.sh, scripts/mutants2.sh) on a copy of the head; summary.txt.
probe_wrap.log  the 32x32 ACMP transmit ring decode in both forms, evaluated in the pinned simulator
             (scripts/probe_wrap/wrap_tb.sv against the generated 32x32 KL_mbx_pkg.sv).
lint-*.log   lint of the generated 32x32 and the tracked KL_mbx with its leaves.
builder-*.log  the end-station builder at three configs (AEM_ROM_BYTES_C figures).
scripts-*.json  the backlog groups' script hashes at 1x1/1if and 8x8/2if at round 3's head and at this head.
owed32-script.txt  the head's 32x32 owed-row frames and transmit waits.
gh-pr-checks.txt, check-runs-936e0a56.tsv  hosted contexts at the head (read-only).
tree-integrity.txt  the clone after every probe: HEAD, tree, index, gitlinks, no untracked file.
