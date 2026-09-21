"""Check the recorded counterexample and adjacent safety controls, not product conformance."""
import json
import sys
from pathlib import Path

source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("adjacent-probes.json")
rows = json.loads(source.read_text())
by_variant = {row["variant"]: row for row in rows}


def terminal(variant):
    return by_variant[variant]["obs"]["terminal"]


def timing(variant):
    return next(event for event in by_variant[variant]["events"] if event.get("k") == "boot")


def answers(variant):
    return [event for event in by_variant[variant]["events"] if event.get("k") == "ans"]


checks = {
    "all ten scenarios completed": len(rows) == 10 and all(row["rc"] == 0 and row["done"] for row in rows),
    "ready listener control completes": terminal("control")["restore_done"] == 1
    and terminal("control")["restore_fail"] == 0 and terminal("control")["entity_en"] == 1
    and len(answers("control")) == 2,
    "held preload blocks both walks and GET with an idle port": all(
        terminal("held")[key] == 0 for key in ("mgr_done", "restore_done", "restore_fail", "d3_closed", "entity_en", "port_busy")
    ) and terminal("held")["own"] == 1 and not answers("held")
    and timing("held")["prog_waited"] == 2000068,
    "finite preload exceeds the advertised two-deadline recovery": terminal("finite")["restore_done"] == 1
    and terminal("finite")["restore_fail"] == 0 and timing("finite")["terminal"] == 107431
    and len(answers("finite")) == 2,
    "4094-cycle descriptor control completes": terminal("4094")["restore_done"] == 1
    and terminal("4094")["restore_fail"] == 0 and terminal("4094")["entity_en"] == 1,
    "4095-4097 descriptor responses cause contained rollback": all(
        terminal(v)["restore_done"] == 1 and terminal(v)["restore_fail"] == 1
        and terminal(v)["d3_rb"] == 1 and terminal(v)["d3_cause"] == 6
        and terminal(v)["entity_en"] == 1
        and len(answers(v)) == 2 and all(int(a["v"], 16) == 0 for a in answers(v))
        for v in ("4095", "4096", "4097")
    ),
    "burst debt beyond rollback deadline stays CLOSED": all(
        terminal(v)["restore_done"] == 0 and terminal(v)["restore_fail"] == 1
        and terminal(v)["d3_closed"] == 1 and terminal(v)["d3_cause"] == 6
        and terminal(v)["own"] == 1 and terminal(v)["entity_en"] == 0
        and not answers(v) for v in ("24090", "24098", "24100")
    ),
}
print(json.dumps(checks, indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
