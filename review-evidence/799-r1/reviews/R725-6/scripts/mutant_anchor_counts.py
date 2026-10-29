"""Compare each release mutant anchor's occurrence count in two planner copies.
Usage: python3 -I mutant_anchor_counts.py <tools_dir> <planner_a> <planner_b>"""
import sys
sys.path.insert(0, sys.argv[1])
import torture_release_mutants as m
a = open(sys.argv[2]).read(); b = open(sys.argv[3]).read()
anchors = [x[1] for x in m.MUTANTS]
try:
    import torture_release_audio_mutants as am
    for x in am.AUDIO_GRADER_MUTANTS:
        anchors.append(x[1] if isinstance(x, tuple) else x)
except Exception as e:
    print("audio anchors not read:", e)
diff = [(s[:60], a.count(s), b.count(s)) for s in anchors if isinstance(s, str) and a.count(s) != b.count(s)]
print(len(anchors), "anchors;", len(diff), "differ")
for d in diff: print(d)
