#!/bin/bash
# Plant one fault per probe in a disposable export of HEAD and record each checker's rc.
# Expected: every planted fault makes its checker return nonzero; the clean export returns 0
# (links checked with --local-only; the 8 licence-file links are expected failures in all runs).
# Usage: checker_mutation_probes.sh <clone> <workdir> <mmdc-out>
set -u
CLONE=$1; W=$2; OUT=$3
fresh() { rm -rf "$W"; mkdir -p "$W"; git -C "$CLONE" archive HEAD | tar -x -C "$W"; }
run() { ( cd "$W" && python3 "doc/tools/$1" "${@:2}" ) > "$OUT/$PROBE.log" 2>&1; echo "$PROBE rc=$? :: $1 ${*:2} :: $(grep -E '^(FAIL|Graphs|Sentences|Unlinked|Local)' "$OUT/$PROBE.log" | grep -v 'LICENSE\|NOTICE' | head -2 | tr '\n' ' ')"; }
mkdir -p "$OUT"
PROBE=clean-sentences; fresh; run check_sentences.py
PROBE=clean-references; fresh; run check_references.py
PROBE=clean-links-local; fresh; run check_links.py --local-only
PROBE=long-sentence; fresh; echo "This planted sentence contains exactly twenty six words so that the sentence length checker must reject it without any exception at all today ok." >> "$W/doc/tester.md"; run check_sentences.py
PROBE=long-wrapped; fresh; printf '\nOne two three four five six seven eight nine ten eleven twelve thirteen\nfourteen fifteen sixteen seventeen eighteen nineteen twenty twentyone twentytwo twentythree twentyfour twentyfive twentysix.\n' >> "$W/doc/manager.md"; run check_sentences.py
PROBE=long-table-cell; fresh; printf '\n| a | b |\n| --- | --- |\n| x | One two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty 21 22 23 24 25 26 |\n' >> "$W/README.md"; run check_sentences.py
PROBE=plain-file; fresh; echo "Edit src/core/mrp_mad.c first." >> "$W/doc/developer.md"; run check_references.py
PROBE=plain-clause; fresh; echo "See clause 10.7.7 for details." >> "$W/doc/developer.md"; run check_references.py
PROBE=plain-issue; fresh; echo "Tracked in #4 today." >> "$W/doc/tester.md"; run check_references.py
PROBE=plain-function; fresh; echo "Call mrp_rx with the payload." >> "$W/doc/integrator.md"; run check_references.py
PROBE=inline-code-file; fresh; echo 'Edit `build.sh` first.' >> "$W/doc/integrator.md"; run check_references.py
PROBE=plain-kconfig-file; fresh; echo "Edit Kconfig.zephyr first." >> "$W/doc/integrator.md"; run check_references.py
PROBE=plain-table; fresh; echo "Read Table 10-3 now." >> "$W/doc/developer.md"; run check_references.py
PROBE=missing-file; fresh; echo "See the [gone](missing.md)." >> "$W/doc/tester.md"; run check_links.py --local-only
PROBE=missing-heading; fresh; echo "See the [gone](manager.md#no-such-heading)." >> "$W/doc/tester.md"; run check_links.py --local-only
PROBE=line-range-past-eof; fresh; echo "See the [rows](../src/core/mrp_mad.c#L970-L990)." >> "$W/doc/tester.md"; run check_links.py --local-only
PROBE=outside-repo; fresh; echo "See the [x](../../../etc/hostname)." >> "$W/doc/tester.md"; run check_links.py --local-only
PROBE=dead-external; fresh; echo "See the [x](https://example.invalid/nothing)." >> "$W/doc/tester.md"; run check_links.py
PROBE=graph-16-nodes; fresh; { echo; echo '~~~mermaid'; echo 'flowchart TD'; for i in $(seq 1 16); do echo "    N$i[n$i] --> N$((i+1))[n$((i+1))]"; done | head -16; echo '~~~'; } >> "$W/doc/tester.md"; run render_mermaid.py --output "$OUT/g-$PROBE"
PROBE=graph-syntax-error; fresh; printf '\n~~~mermaid\nflowchart TD\n    A[a] --> B[b\n~~~\n' >> "$W/doc/tester.md"; run render_mermaid.py --output "$OUT/g-$PROBE"
PROBE=graph-output-inside; fresh; run render_mermaid.py --output "$W/doc/out"
PROBE=unclosed-fence; fresh; printf '\n~~~sh\necho hi\n' >> "$W/doc/tester.md"; run check_sentences.py
