#!/bin/bash
# Exhaustive table of srp_mbx.c's listener_kind over every registered_kinds (0..3) and latest_kind (0..3),
# compiled from the function text at the head (extracted verbatim), against the rule written independently.
set -euo pipefail
R=$1; W=$2
fn=$(awk '/^static uint8_t listener_kind\(const struct srp_sink \*s\)/,/^}/' "$R/sw/firmware/ctrl/srp/srp_mbx.c")
cat > "$W/tt.c" <<C
#include <stdint.h>
#include <stdio.h>
struct srp_sink { uint8_t registered_kinds, latest_kind; };
$fn
/* the rule, independently: none registered 0; one kind registered: that kind; both: the latest, or Failed (1)
   when no latest is known */
static uint8_t rule(uint8_t reg, uint8_t latest) {
    if (reg == 0u) return 0u;
    if (reg != 3u) return reg;
    return (latest == 1u || latest == 2u) ? latest : 1u;
}
int main(void) {
    int bad = 0;
    for (uint8_t reg = 0; reg < 4; ++reg)
        for (uint8_t latest = 0; latest < 4; ++latest) {
            struct srp_sink s = {reg, latest};
            uint8_t got = listener_kind(&s), want = rule(reg, latest);
            printf("registered=%u latest=%u -> %u (rule %u)%s\n", reg, latest, got, want,
                   got == want ? "" : (latest == 3u ? "  [latest 3 is unreachable]" : "  MISMATCH"));
            bad += got != want && latest != 3u;
        }
    printf("%s\n", bad ? "TABLE FAIL" : "TABLE PASS");
    return bad != 0;
}
C
gcc -std=c11 -Wall -Wextra -Werror -o "$W/tt" "$W/tt.c" && "$W/tt"
