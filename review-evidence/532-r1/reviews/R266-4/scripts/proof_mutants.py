#!/usr/bin/env python3
"""R266-3 (re-run in R266-4) mutants of scripts/act_slot_proof.sh: one per protective check, plus a no-op control.

Usage: proof_mutants.py SOURCE OUTDIR [ID...]
Writes OUTDIR/<ID>/act_slot_proof.sh for each mutant (every edit must apply exactly
once to SOURCE, or the script refuses) and OUTDIR/<ID>/mutant.txt describing it.
"""
import pathlib
import sys

# (id, the check it removes or weakens, old text, new text)
MUTANTS = [
    ("X00", "control: a comment-only edit", "# In order, it proves:", "# In order, it proves (control):"),
    # parse_arguments
    ("A01", "numeric-slot check removed", 'case "$number" in \'\'|*[!0-9]*) echo "slots are numbers: $number" >&2; exit 2 ;; esac',
     ': "$number"'),
    ("A02", "numeric check skips the serial slot", 'for number in "$slot_a" "$slot_b" "$serial_slot"; do',
     'for number in "$slot_a" "$slot_b"; do'),
    ("A03", "numeric check skips slot B", 'for number in "$slot_a" "$slot_b" "$serial_slot"; do',
     'for number in "$slot_a" "$serial_slot"; do'),
    ("A04", "slot A == slot B accepted", 'if [ "$slot_a" -eq "$slot_b" ] || [ "$slot_a" -eq 0 ]',
     'if [ "$slot_a" -eq 0 ]'),
    ("A05", "slot A == 0 accepted", '|| [ "$slot_a" -eq 0 ] || [ "$slot_b" -eq 0 ]; then',
     '|| [ "$slot_b" -eq 0 ]; then'),
    ("A06", "slot B == 0 accepted", '|| [ "$slot_a" -eq 0 ] || [ "$slot_b" -eq 0 ]; then',
     '|| [ "$slot_a" -eq 0 ]; then'),
    # verify_runner
    ("B01", "digest comparison removed", 'if [ "$actual" != "$sha" ] || [ -n', 'if [ -n'),
    ("B02", "write-bit test removed", '[ -n "$(find "$runner" -maxdepth 0 -perm /0222)" ] \\\n    || {',
     'false \\\n    || {'),
    ("B03", "non-root writability test removed (documented: no case)",
     '|| { [ "$(id -u)" -ne 0 ] && [ -w "$runner" ]; }; then', '; then'),
    ("B04", "non-empty log directory accepted", 'if [ -n "$(ls -A "$logs")" ]; then', 'if false; then'),
    ("B05", "verify_runner never called", "prove() {\n  verify_runner\n", "prove() {\n  mkdir -p \"$logs\"\n"),
    # complete / reference / compare
    ("C01", "complete always true", 'local actual expected="" name\n', 'local actual expected="" name\n  return 0\n'),
    ("C02", "completion ignores exit status on success", '[ "$actual" = "exit 0$expected" ]',
     '[ "${actual#exit ?}" = "$expected" ]'),
    ("C03", "completion ignores exit status on failure",
     'if [ "$actual" = "exit 1$expected"$\'\\n\'"$name FAILED" ]; then return 0; fi',
     'if [ "${actual#exit ?}" = "$expected"$\'\\n\'"$name FAILED" ]; then return 0; fi'),
    ("C04", "exit 0 with any PASS prefix completes",
     'if [ "$actual" = "exit 1$expected"$\'\\n\'"$name FAILED" ]; then return 0; fi',
     'if [ "$actual" = "exit 1$expected"$\'\\n\'"$name FAILED" ]; then return 0; fi\n    if [ -n "$expected" ] && [ "$actual" = "exit 0$expected" ]; then return 0; fi'),
    ("C05", "reference records PASS without completion", 'reference() {\n  if complete "$1"; then',
     'reference() {\n  if true; then'),
    ("C06", "compare skips completion", 'if ! complete "$1"; then', 'if false; then'),
    ("C07", "compare skips the verdict comparison", 'elif same_verdict "$1" "$2"; then', 'elif true; then'),
    ("C08", "verdict file keeps PASS lines only", 's/^act-ci: ([a-z-]+): (PASS|FAILED).*/\\1 \\2/p',
     's/^act-ci: ([a-z-]+): (PASS).*/\\1 \\2/p'),
    # replay / await / ended / overlap
    ("D01", "replay never passes the slot", 'slot_args=(--slot "$slot" --slot-root "$(slot_root "$slot")")',
     'slot_args=()'),
    ("D02", "isolated-slot holder marker is the slot-0 marker",
     'if [ "$slot" -ne 0 ]; then marker="act-ci: slot $slot: own daemon"; fi', ':'),
    ("D03", "ended ignores refusals", "grep -q -E '^act-ci: ([a-z-]+: (PASS|FAILED)|REFUSED)'",
     "grep -q -E '^act-ci: ([a-z-]+: (PASS|FAILED))'"),
    ("D04", "ended ignores verdicts", "grep -q -E '^act-ci: ([a-z-]+: (PASS|FAILED)|REFUSED)'",
     "grep -q -E '^act-ci: (REFUSED)'"),
    ("D05", "overlap does not wait for slot A's holder",
     'if await_holder parallel-a "$slot_a" && await_holder parallel-b "$slot_b" \\',
     'if await_holder parallel-b "$slot_b" \\'),
    ("D06", "overlap does not wait for slot B's holder",
     'if await_holder parallel-a "$slot_a" && await_holder parallel-b "$slot_b" \\',
     'if await_holder parallel-a "$slot_a" \\'),
    ("D07", "overlap ignores run A's verdict", '&& ! ended parallel-a && ! ended parallel-b; then',
     '&& ! ended parallel-b; then'),
    ("D08", "overlap ignores run B's verdict", '&& ! ended parallel-a && ! ended parallel-b; then',
     '&& ! ended parallel-a; then'),
    # interrupt gate
    ("E01", "interrupt gate ignores the runner's exit status",
     '--sudo --slot "$slot_a" --slot-root "$slot_root_a") >"$log" 2>&1 \\',
     '--sudo --slot "$slot_a" --slot-root "$slot_root_a") >"$log" 2>&1; true \\'),
    ("E02", "interrupt gate ignores the PASS line", "&& grep -q '^interrupt-selftest: PASS ' \"$log\" \\\n", ""),
    ("E03", "interrupt gate ignores the slot teardown line",
     '    && grep -q "^interrupt-selftest: slot $slot_a: " "$log"; then', '    ; then'),
    ("E04", "interrupt gate accepts any slot's teardown line",
     '"^interrupt-selftest: slot $slot_a: "', '"^interrupt-selftest: slot [0-9]*: "'),
    # isolation target
    ("F01", "listener start failure ignored",
     '--entrypoint python3 "$probe_image" -c "$LISTENER" >/dev/null || return 1',
     '--entrypoint python3 "$probe_image" -c "$LISTENER" >/dev/null || true'),
    ("F02", "target start failure not recorded",
     'record FAIL "isolation target: it could not be started on the default daemon (see isolation.log)"',
     ':'),
    ("F03", "container presence after removal not checked", 'if [ -n "$containers$networks" ]; then',
     'if [ -n "$networks" ]; then'),
    ("F04", "network presence after removal not checked", 'if [ -n "$containers$networks" ]; then',
     'if [ -n "$containers" ]; then'),
    ("F05", "failed container query read as absent", '|| containers=unknown', '|| containers='),
    ("F06", "failed network query read as absent", '|| networks=unknown', '|| networks='),
    ("F07", "target not removed before the collisions", '  parallel\n  remove_target\n', '  parallel\n'),
    # isolation probes
    ("G01", "slot may reach the container",
     'if [ "$inside" = "container=refused published=refused internet=reached " ]',
     'if [ "${inside#container=* }" = "published=refused internet=reached " ]'),
    ("G02", "slot may reach the published port",
     'if [ "$inside" = "container=refused published=refused internet=reached " ]',
     'if [ "${inside/published=reached/published=refused}" = "container=refused published=refused internet=reached " ]'),
    ("G03", "slot need not reach the probe name",
     'if [ "$inside" = "container=refused published=refused internet=reached " ]',
     'if [ "${inside/internet=refused/internet=reached}" = "container=refused published=refused internet=reached " ]'),
    ("G04", "host reach not required", '&& [ "$outside" = "container=reached published=reached " ]; then',
     '; then'),
    ("G05", "host need not reach the container", '&& [ "$outside" = "container=reached published=reached " ]; then',
     '&& [ "${outside#container=* }" = "published=reached " ]; then'),
    ("G06", "host need not reach the published port",
     '&& [ "$outside" = "container=reached published=reached " ]; then',
     '&& [ "${outside% published=* }" = "container=reached" ]; then'),
    ("G07", "every slot's control probes slot A's namespace",
     '"--net=/run/netns/milan-act-slot-$slot"', '"--net=/run/netns/milan-act-slot-$slot_a"'),
    ("G08", "slot B's control is recorded from slot A's probe",
     '      if [ -n "$target" ]; then isolation "$slot"; else',
     '      if [ -n "$target" ]; then isolation "$slot_a"; else'),
    # collisions
    ("H01", "rival need not be refused before the holder's verdict",
     'if [ "$rival_early" -eq 1 ] && [ "$rival_status" = 2 ] \\', 'if [ "$rival_status" = 2 ] \\'),
    ("H02", "rival exit status not checked", 'if [ "$rival_early" -eq 1 ] && [ "$rival_status" = 2 ] \\',
     'if [ "$rival_early" -eq 1 ] \\'),
    ("H03", "rival refusal reason not checked", '    && grep -q -E "$refusal" "$logs/collide-$slot-rival.log" \\\n', ''),
    ("H04", "collision holder completion not checked",
     '&& complete "collide-$slot-holder" && same_verdict "collide-$slot-holder" serial-a; then',
     '&& same_verdict "collide-$slot-holder" serial-a; then'),
    ("H05", "collision holder verdict not compared",
     '&& complete "collide-$slot-holder" && same_verdict "collide-$slot-holder" serial-a; then',
     '&& complete "collide-$slot-holder"; then'),
    ("H06", "slot-A collision accepts any refusal", 'collide "$slot_a" "is in use by another runner invocation"',
     'collide "$slot_a" "REFUSED"'),
    ("H07", "slot-0 collision accepts any refusal", 'collide 0 "act-toolcache|already exist"', 'collide 0 "REFUSED"'),
    ("H08", "rival lateness judged from the rival", 'if ended "collide-$slot-holder"; then rival_early=0; fi',
     'if false; then rival_early=0; fi'),
    # verdict
    ("I01", "any FAIL line ignored when ten PASS", 'if grep -q \'^FAIL\' "$logs/SUMMARY" || [ "$(grep -c',
     'if false || [ "$(grep -c'),
    ("I02", "ten-PASS backstop removed (documented: no case)", ' || [ "$(grep -c \'^PASS\' "$logs/SUMMARY")" -ne 10 ]; then',
     '; then'),
]


def main() -> int:
    source = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    outdir = pathlib.Path(sys.argv[2])
    wanted = set(sys.argv[3:])
    for ident, described, old, new in MUTANTS:
        if wanted and ident not in wanted:
            continue
        count = source.count(old)
        if count != 1:
            print(f"{ident}: edit applies {count} times, refusing", file=sys.stderr)
            return 2
        mutant = source.replace(old, new, 1)
        if mutant == source:
            print(f"{ident}: edit changes nothing, refusing", file=sys.stderr)
            return 2
        target = outdir / ident
        target.mkdir(parents=True, exist_ok=True)
        (target / "act_slot_proof.sh").write_text(mutant, encoding="utf-8")
        (target / "mutant.txt").write_text(f"{ident}: {described}\n", encoding="utf-8")
        print(f"{ident}\t{described}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
