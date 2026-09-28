#!/usr/bin/env python3
"""Tree-wide search for statements the #602 ruling falsifies, at one commit.

Usage: stale_scan.py CLONE [COMMIT]
Prints every hit outside docs/history/** of (1) phrasings that assert a
PHC step/re-base toggles mr or counts MEDIA_RESET, or that this waits for
#602, and (2) the broader co-mention inventory (PHC/step/re-base/settime/
adjtime on the same line as mr/MEDIA_RESET) for manual classification.
The known stale line is flagged so a reader can confirm it is still present.
"""
import subprocess
import sys

STRICT = (r"still toggles|until #602|#602'?s? (RTL|change) lands|602 lands|toggles once|"
          r"counts that one toggle|step's MEDIA_RESET|one .?mr.? toggle and (one )?MEDIA_RESET|"
          r"MEDIA_RESET record|counted media event|re-?base pulses|pulses .?mr|"
          r"mcr_restart_p_w.{0,80}media_rebase|media_rebase_p_w.{0,40}mcr_restart")
BROAD = (r"(PHC|step|re-?base|settime|adjtime).*(`mr`|\bmr\b|MEDIA_RESET)|"
         r"(`mr`|\bmr\b|MEDIA_RESET).*(PHC|step|re-?base|settime|adjtime)")
EXCLUDE = [":!docs/history/**", ":!*.svg", ":!*.png", ":!*.drawio", ":!third_party/**"]
KNOWN = "docs/findings/394_387_E1_SWITCH_CYCLES.md:173:"


def grep(clone: str, commit: str, pattern: str, ignore_case: bool) -> list[str]:
    cmd = ["git", "-C", clone, "grep", "-n", "-I", "-E"] + (["-i"] if ignore_case else [])
    cmd += [pattern, commit, "--"] + EXCLUDE
    out = subprocess.run(cmd, capture_output=True, text=True)
    return [line[len(commit) + 1:] for line in out.stdout.splitlines()]


def main() -> int:
    clone = sys.argv[1]
    commit = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    strict = grep(clone, commit, STRICT, True)
    broad = grep(clone, commit, BROAD, False)
    print(f"== strict phrasings at {commit}: {len(strict)} hit(s)")
    for line in strict:
        print(("  [KNOWN-STALE] " if line.startswith(KNOWN) else "  ") + line[:300])
    print(f"== broad co-mention inventory: {len(broad)} hit(s)")
    for line in broad:
        print(("  [KNOWN-STALE] " if line.startswith(KNOWN) else "  ") + line[:300])
    return 0


if __name__ == "__main__":
    sys.exit(main())
