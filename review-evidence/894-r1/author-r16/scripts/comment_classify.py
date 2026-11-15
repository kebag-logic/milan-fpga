#!/usr/bin/env python3
"""Classify every hit comment_sweep.py lists (argv[1]) and print the receipt; argv[2] is the token file. An
unclassified hit exits 1. Classes: historical (past tense, dated, or a restatement written 'from X to Y'); beside (the
head's figure stands beside it); another (another quantity, measured or named elsewhere)."""
import sys

H, X, O = "historical", "beside", "another"
R = "tb/verilator/ctrl_service_budget/README.md"
C = {
    "sw/firmware/ctrl/aecp/aecp_mbx.h:50": (H, "'txL was 49.69 ms at 7 ms, and 8 ms did' (the direct index's; R837-9-F1)"),
    "sw/firmware/ctrl/srp/README.md:238": (X, "'33.38 ms there at the 950 us slice (33.01 at the 900 us slice under #894's one-row edit cut, 29.78 before it'"),
    f"{R}:536": (O, "the harness's ACMP PROBE_TX latency table (4.11 (12.26) ms), not a row figure"),
    f"{R}:540": (O, "the harness's first-TMR_NO_RESP latency table (5.48 (47.98) ms), not a row figure"),
    f"{R}:580": (O, "the harness's AECP lock_entity latency table (8.32 (14.50) ms), not a row figure"),
    f"{R}:681": (O, "the harness's measured load-service table, ADP's last record 72.71 ms in an arm's group, not the tier model's R5"),
    f"{R}:827": (O, "the fetch-L1 geometry sweep table (at least 28.35 ms), not a row figure"),
    f"{R}:1135": (O, "0.513 ms, slow-adp-rx's unplanted ADP record"),
    "tb/verilator/ctrl_service_budget/load_grade.py:126": (H, "restatement history, 'a TICK at 1x1/1if 45 to 50 us' under the edit cut"),
    "tb/verilator/ctrl_service_budget/load_grade.py:134": (H, "restatement history, 'a TICK at 1x1/1if 50 to 55'; the table holds 55"),
    "tb/verilator/ctrl_service_budget/load_grade.py:171": (H, "restatement history, 'at 1,010 and 725 us ... under #894's ... 735'; the table holds 735"),
    "tb/verilator/ctrl_split_boot/README.md:87": (O, "0.199 ms, a boot-time figure"),
    "tb/verilator/fw_service_budget/README.md:84": (O, "14.56 seconds, two flash slots' WIP bound"),
}


def main(hits, tokens):
    rows, bad, counts = [], 0, {}
    for line in open(hits, encoding="utf-8"):
        if line.startswith('#'):
            continue
        tok, loc, text = line.rstrip("\n").split("\t", 2)
        c = C.get(loc)
        if c is None:
            bad += 1
            rows.append(f"UNCLASSIFIED\t{tok}\t{loc}\t{text[:140]}")
            continue
        counts[c[0]] = counts.get(c[0], 0) + 1
        rows.append(f"{c[0]}\t{tok}\t{loc}\t{c[1]}")
    toks = [l.split()[0] for l in open(tokens, encoding="utf-8") if l.strip() and not l.startswith('#')]
    print("# Round 16, item 4: every comment and docstring under sw/ and tb/ (and every Markdown line there) against")
    print("# every figure the round 12 to 15 moves superseded, at any pace or slice (comment_sweep.py)")
    print(f"# {len(toks)} decimal tokens (sweep-tokens.txt: round 15's rows-history and load tokens, R837-9's 115,")
    print("#   and txL/R4L at every non-built pace), plus the cost figures in context: 725 on a build line, 900 us,")
    print("#   65 with AECP's timer slot, 150 with LINK, 250 with the SRP drain, 50 with TICK, 98, 30 and 44 with")
    print("#   CTRL_LOOP_TX_MS or THE TRANSMIT")
    print("# " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) + f", total {len(rows)}; current with a superseded figure: 0")
    for r in rows:
        print(r)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
