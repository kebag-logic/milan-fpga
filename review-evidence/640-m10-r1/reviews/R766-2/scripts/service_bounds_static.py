"""Show that the round 2 edit to MAILBOX_SPLIT.md touches no line the
ctrl_service_bounds reader requires. Run from the review clone:
python3 -I service_bounds_static.py <base> <head>"""
import subprocess, sys
base, head = sys.argv[1], sys.argv[2]
keys = ["| an event behind 15 others |", "| an ACMP command behind a full acmp ring |",
        "| an ENTITY_AVAILABLE behind a full adp ring |", "| a response with 7 frames owed ahead of it |",
        "With F4's SRP attached before the loop starts", "At 1 us per access, event envelopes are",
        "Neither fits T_svc = 10 ms; neither do the other rows. The 20 ms ACMP",
        "ceiling still covers both event envelopes, but none of the other rows."]
def page(rev):
    return subprocess.run(["git", "show", f"{rev}:docs/design/MAILBOX_SPLIT.md"], capture_output=True, text=True).stdout
a, b = page(base), page(head)
la = [l for l in a.splitlines() if any(k in l for k in keys)]
lb = [l for l in b.splitlines() if any(k in l for k in keys)]
print("reader-anchored lines at", base + ":", len(la), "at head:", len(lb), "identical:", la == lb)
diff = [l for l in b.splitlines() if l not in a.splitlines()]
print("head-only lines:", len(diff))
print("any reader key in head-only lines:", any(k in l for l in diff for k in keys))
