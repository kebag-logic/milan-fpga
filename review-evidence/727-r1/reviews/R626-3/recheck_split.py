#!/usr/bin/env python3
"""Independent check of the #727 split. Does not import the selector.

Usage: recheck_split.py SELECTOR.py RTL_YML LISTDIR
Reads the tables with ast, timeout-minutes and the matrix from rtl.yml with a
plain regex, re-implements "pins and the dedicated suite first, then longest
first to the least-loaded balanced worker (ties: lexical suite, lower worker)",
and compares with LISTDIR/shard{I}.txt and LISTDIR/inventory.txt.
"""
import ast
import re
import sys


def tables(path):
    out = {}
    for node in ast.parse(open(path, encoding="utf-8").read()).body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            target = node.targets[0] if isinstance(node, ast.Assign) else node.target
            if isinstance(target, ast.Name):
                try:
                    out[target.id] = ast.literal_eval(node.value)
                except ValueError:
                    pass
    return out


def main():
    selector, workflow, listdir = sys.argv[1:4]
    t = tables(selector)
    seconds, overhead = t["SUITE_SECONDS"], t["WORKER_OVERHEAD_SECONDS"]
    text = open(workflow, encoding="utf-8").read()
    job = text[text.index("\n  verilator-shards:\n"):]
    job = job[:re.search(r"\n  [a-z][a-z0-9-]*:\n", job[1:]).start() + 1]
    timeout = int(re.search(r"\n    timeout-minutes: (\d+)\n", job).group(1))
    total = int(re.search(r"\n        total: \[(\d+)\]\n", job).group(1))
    shards = re.search(r"\n        shard: \[([0-9, ]+)\]\n", job).group(1)
    inventory = open(f"{listdir}/inventory.txt").read().split()
    lists = [open(f"{listdir}/shard{i}.txt").read().split() for i in range(total)]
    print(f"rtl.yml verilator-shards: timeout-minutes {timeout}, total [{total}], "
          f"shard [{shards}]")
    bound = timeout * 36  # 60 % of timeout-minutes in seconds
    print(f"60% bound: {bound} s ({bound / 60:.1f} min)")
    print(f"inventory {len(inventory)} suites; table {len(seconds)}; "
          f"inventory==table keys: {sorted(inventory) == sorted(seconds)}")
    # independent re-implementation
    pins = {"tsn_fuzz": 1, "chmap_capture": 3, "milan_dp": total - 1}
    load = list(overhead)
    owner = {}
    for s, w in pins.items():
        owner[s] = w
        load[w] += seconds[s]
    for s in sorted((s for s in inventory if s not in pins),
                    key=lambda s: (-seconds[s], s)):
        w = min(range(total - 1), key=lambda w: (load[w], w))
        owner[s] = w
        load[w] += seconds[s]
    mine = [[s for s in inventory if owner[s] == i] for i in range(total)]
    ok = True
    for i in range(total):
        pred = overhead[i] + sum(seconds[s] for s in lists[i])
        same = mine[i] == lists[i]
        ok &= same and pred <= bound
        print(f"worker {i}/{total}: {len(lists[i])} suites, predicted {pred} s "
              f"({pred / 60:.1f} min, {100 * pred / (timeout * 60):.1f}% of timeout), "
              f"independent split equal={same}")
    flat = [s for lst in lists for s in lst]
    union = sorted(flat) == sorted(inventory)
    dup = len(flat) != len(set(flat))
    ded = lists[total - 1] == ["milan_dp"]
    pin = "tsn_fuzz" in lists[1] and "chmap_capture" in lists[3]
    print(f"union==inventory {union}; duplicates {dup}; worker {total - 1} is "
          f"milan_dp alone {ded}; tsn_fuzz on 1 and chmap_capture on 3 {pin}")
    ok &= union and not dup and ded and pin
    # old rule, for the issue's context
    import hashlib
    old = [overhead[i] for i in range(total)]
    for s in inventory:
        if s == "milan_dp":
            w = total - 1
        else:
            w = int.from_bytes(hashlib.sha256(s.encode()).digest()[:8], "big") % (total - 1)
        old[w] += seconds[s]
    print("old SHA-256 rule with the same table (incl. #696 maap): "
          + ", ".join(f"{v} s ({v / 60:.1f} min)" for v in old))
    print("RESULT", "OK" if ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
