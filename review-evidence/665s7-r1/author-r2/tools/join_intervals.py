"""join_intervals.py GRADER_DIR CAPTURE: each timer-driven Join interval measure_time computes, per application."""
import json, sys
sys.path.insert(0, sys.argv[1])
import srptx_grade as g
cap = g.load(__import__("pathlib").Path(sys.argv[2]))
doc = cap.doc
print("timer keys:", sorted(doc["timers"][0]), doc["timers"][:3])
print("mac keys:", sorted(doc["mac"][0]))
print(json.dumps(g.measure_time(cap), indent=1)[:1500])
