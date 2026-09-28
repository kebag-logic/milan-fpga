#!/usr/bin/env python3
"""Reconcile every match of the section 15.2 named search, line by line.

Runs the contract's search at the committed head of a processor tree, marks
each matching line as rewritten by this lane (blame inside the lane's range)
or carries its location-specific scope reason, and writes a Markdown table.
A match with no rule is reported as UNREVIEWED and fails the run.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

PATTERN = (
    r"NVM_MARK|persist|dirty[[:space:]/!#*]+mark|aecp_dyn_dirty_o|nvm_unflushed_o"
    r"|d3_unflushed_o|restore_(done|fail|blank)_o|T-NVM|RETRY_MAX_P"
    r"|RETRY_BACKOFF_CYC_P|DEB_TICKS_P|entity_enable"
    r"|Nothing[[:space:]/!#*]+in[[:space:]/!#*]+the[[:space:]/!#*]+processor"
    r"|groups[[:space:]/!#*]+6[[:space:]/!#*]+and[[:space:]/!#*]+7"
    r"|integrating[[:space:]/!#*]+platform|platform.s[[:space:]/!#*]+saved-state"
    r"|never[[:space:]/!#*]+delay|asynchronous[[:space:]/!#*]+to[[:space:]/!#*]+protocol")

#: (file regex, line regex or None, disposition) - first match wins. Every
#: line the lane rewrote is dispositioned by blame before these apply.
RULES = [
    (r"^docs/(README|guides/README)\.md$", None,
     "index entry pointing at 07 section 5, the updated authority"),
    (r"^docs/10_RESOURCE_AND_EFFORT\.md$", None,
     "historical estimate of the earlier front end; not a contract; D3 area is the packet's DR4"),
    (r"^docs/diagrams/(src/)?01-", None,
     "F01.1/F01.2 concept figures: one model-to-NVM 'persist' relation, still true for the two "
     "producers; draw.io cannot export headless here (diagrams README), so source and export stay paired"),
    (r"^hdl/packet_engine/KL_pp_side_port\.sv$", None,
     "the image-window lock keeps the REQUESTED enable (15.2 row 21); unchanged by design"),
    (r"^hdl/adp/KL_adp_engine\.sv$", None,
     "module-internal use of its entity_enable_i input, which the top drives with the effective "
     "enable (port comment updated)"),
    (r"^hdl/aecp/(KL_aecp_ucpu\.sv|ucpu_pkg\.sv)$", None,
     "the NVM_MARK micro-op and its completion strobe, retained (15.2: mark instructions stay valid)"),
    (r"^hdl/srp/KL_srp_listener_fsm\.sv$", None, "unrelated sense: a latched SRP record persists"),
    (r"^hdl/packet_engine/KL_pp_nvm_port\.sv$", r"asynchronous",
     "port-level fact: the device's commits stay asynchronous; 03 section 6 rule (d) now bounds the "
     "separate latch hold"),
    (r"^hdl/acmp/KL_acmp_nvm_shadow\.sv$", None,
     "raw binding-manager fact limited to this module (its RAW VERDICTS paragraph); the top combines"),
    (r"^hdl/acmp/KL_pp_acmp_lsn_admit\.sv$", None,
     "the gate's input is the binding manager's raw terminal; release paragraph updated"),
    (r"^hdl/aecp/ucode/gen_ucode\.py$", r"NVM_MARK",
     "mark instruction retained as a completion effect; its comment rewritten where it claimed persistence"),
    (r"^tb/(prng|tx_slots|acmp_talker)/", None,
     "unrelated sense of 'persist' (a flag, a byte or a kill persists)"),
    (r"^tb/(adp_engine|side_port)/", None,
     "module suite drives the module's own entity_enable_i; the top's restore gating is graded in pp_top D3R1"),
    (r"^tb/ucpu/", None, "grades the NVM_MARK completion strobe itself; retained"),
    (r"^tb/dyn_state/", None,
     "diagnostic dirty (section E) and the change qualifier (section H); section E title updated"),
    (r"^tb/pp_top/gsi_internal\.hpp$", None,
     "boot helper waiting for the combined restore_done_o before its section"),
    (r"^tb/pp_top/sim_main\.cpp$", r"nvm_mark|NVM_MARK",
     "R21, W9k and W10j grade the completion mark as a completion effect (R21 comment rewritten)"),
    (r"^tb/pp_top/sim_main\.cpp$", r"entity_enable_i",
     "harness drive of the requested enable, or a comment on software load order (updated)"),
    (r"^tb/pp_top/sim_main\.cpp$", None,
     "boot helpers and sections R, S0, S9, BW observe the combined pins or the binding walk's own "
     "tap, as the README names them"),
    (r"^tb/pp_top/(d3_phases\.hpp|pp_top_wrap\.sv|README\.md)$", None,
     "the lane's D3 grading of the combined pins and the writer (sections D3O, D3S, D3R)"),
    (r"^tb/acmp_nvm/", None,
     "raw binding-manager suite: the module's own verdicts and parameters (README says so); "
     "historical counts keep their heads"),
    (r"^docs/architecture/04_adp_engine\.md$", r"PERSISTENT",
     "unrelated capability flag (AEM_PERSISTENT_ACQUIRE_SUPPORTED)"),
    (r"^docs/architecture/06_aecp_engine\.md$", r"PERSISTENT|persistence or notification",
     "the lock's PERSISTENT flag, or waived MVU fields that store nothing"),
    (r"^docs/architecture/06_aecp_engine\.md$", r"COMMIT`, `NVM_MARK",
     "the effect micro-op list: mark retained as a completion effect"),
    (r"^docs/architecture/05_acmp_engine\.md$", r"Binding persistence via NVM|persistent binding",
     "scope/delta table rows naming binding persistence; still true"),
    (r"^docs/architecture/02_interfaces\.md$", r"entity_enable = 0|control/status: `entity_enable`",
     "quasi-static load and side-port rules keyed to the requested enable; unchanged"),
    (r"^docs/architecture/07_memory_maps\.md$", r"after `entity_enable`|control/status: entity_enable",
     "side-port access rules keyed to the requested enable; unchanged"),
    (r"^docs/architecture/07_memory_maps\.md$", r"^# 07|## 5\. Persistence|Persisted",
     "section titles and the normative persisted/volatile table header"),
    (r"^docs/architecture/01_overview\.md$", r"counters, and persistence|persistence orchestration|binding persists",
     "scope statements; still true"),
    (r"^docs/guides/integrator\.md$", r"before `entity_enable_i`|persistence seed|Level controls",
     "quasi-static inputs set before the requested enable, or MAAP's unrelated persistence seed"),
    (r"^docs/guides/operator\.md$", r"before `entity_enable`|after\s*$|`entity_enable_i` \||shutdown",
     "side-port window rules and the requested enable's shutdown semantics; unchanged"),
    (r"^docs/guides/operator\.md$", r"entity_enable", "side-port rule keyed to the requested enable"),
    (r"^docs/guides/hdl-engineer\.md$", None,
     "directory map and shutdown semantics; consistent (module table updated)"),
    (r"^docs/00_MILAN_COMPLIANCE_REVIEW\.md$", None,
     "requirement text, the original-document finding or the retained decision table; statuses "
     "updated only where a stage has executable evidence"),
    (r"^hdl/aecp/KL_aecp_dyn_state\.sv$", r"PERSISTENCE",
     "design rationale: the D3 restore writes these rows with their valid flags; still true"),
    (r"^hdl/aecp/KL_aecp_dyn_state\.sv$", r"persisted set marks",
     "the diagnostic dirty (port comment marks it so); IDENTIFY excluded"),
    (r"^hdl/aecp/KL_aecp_engine\.sv$", r"eff_nvm_mark_o",
     "the completion-mark export and its wiring; export comment rewritten"),
    (r"^hdl/top/protocol_processor_top\.sv$", r"output logic        restore_fail_o",
     "declaration under its rewritten combined-verdict comment"),
    (r"^hdl/top/protocol_processor_top\.sv$", r"persisted set|persisted field|nvm_unflushed_o,",
     "the binding manager's own pending vector, raw by design; the OR with d3_unflushed_o is stated"),
    (r"^hdl/top/protocol_processor_top\.sv$", r"Quasi-static",
     "MAAP quasi-static inputs set before the requested enable; unrelated to the restore"),
    (r"^hdl/top/protocol_processor_top\.sv$", r"OP_NVM_MARK|aecp_nvm_mark_o|eff_nvm_mark_o",
     "the completion-mark export (comment rewritten: completion only, no record selection)"),
    (r"^hdl/top/protocol_processor_top\.sv$", r"END, and restore_done_o",
     "the admission release is one term of the combined restore_done_o; true"),
    (r"^hdl/top/protocol_processor_top\.sv$", r"nvm_walk_done_w|dbg_dirty_o|dyn_dirty_o",
     "wiring of the binding manager's raw verdicts and pending, or the diagnostic dirty, to their named nets"),
    (r"^hdl/top/protocol_processor_top\.sv$", r"entity_enable_i|restore_",
     "side-port lock and status words: the requested enable beside the combined verdicts (comments added)"),
    (r"^docs/diagrams/2[0-4]-.*\.svg$", None,
     "requested-enable semantics (shutdown, Milan 5.6.1 gate) beside the added restore release"),
    (r"^docs/architecture/05_acmp_engine\.md$", r"T-NVM-RS-DEADLINE|persistence that wedges",
     "the binding walk's own read deadline and listener release; raw facts of that walk, still true"),
    (r"^docs/architecture/05_acmp_engine\.md$", r"BW4 grades",
     "suite pointer; the sentence now adds the D3 grading"),
    (r"^docs/architecture/07_memory_maps\.md$", r"system_unique_id|stored nor persisted",
     "MVU-waiver deferral; SUID/MCR spans stay deliberately erased (DR5)"),
    (r"^docs/architecture/07_memory_maps\.md$", r"P-NVM-RS-TMO-CYC",
     "the binding walk's failure table (DEVICE/UNFRAMED and per-walk atomicity preserved)"),
    (r"^docs/architecture/02_interfaces\.md$", r"master gate",
     "rule 5's first line; its continuation now names the restore release"),
]


def lane_commits(tree: Path, base: str) -> set:
    out = subprocess.run(["git", "rev-list", f"{base}..HEAD"], cwd=tree, check=True,
                         capture_output=True, text=True).stdout.split()
    return set(out)


def blame(tree: Path, rel: str) -> dict:
    out = subprocess.run(["git", "blame", "-l", "-s", "HEAD", "--", rel], cwd=tree,
                         check=True, capture_output=True, text=True).stdout
    owners = {}
    for n, line in enumerate(out.splitlines(), 1):
        owners[n] = line.split()[0].lstrip("^")
    return owners


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tree", type=Path, required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=args.tree, check=True,
                          capture_output=True, text=True).stdout.strip()
    hits = subprocess.run(["rg", "-n", "-U", "-i", PATTERN, "docs", "hdl", "tb"],
                          cwd=args.tree, check=True, capture_output=True,
                          text=True).stdout.splitlines()
    lane = lane_commits(args.tree, args.base)
    blames = {}
    rows, unreviewed, rewritten = [], 0, 0
    for hit in hits:
        rel, line, text = hit.split(":", 2)
        n = int(line)
        if rel not in blames:
            blames[rel] = blame(args.tree, rel)
        owner = blames[rel].get(n, "")
        if any(owner.startswith(c) or c.startswith(owner) for c in lane if owner):
            why = f"rewritten or added by this lane ({owner[:8]}); states the D3 contract"
            rewritten += 1
        else:
            why = None
            for frx, lrx, reason in RULES:
                if re.search(frx, rel) and (lrx is None or re.search(lrx, text)):
                    why = reason
                    break
            if why is None:
                why = "UNREVIEWED"
                unreviewed += 1
        snippet = text.strip().replace("|", "\\|")[:90]
        rows.append(f"| `{rel}:{n}` | {snippet} | {why} |")
    body = [
        "# Section 15.2 contract sweep: statement-by-statement reconciliation",
        "",
        f"Processor head `{head}`; lane range `{args.base}..HEAD`.",
        f"The contract's named search over `docs hdl tb` returned {len(hits)} matching lines "
        f"(multiline, case-insensitive). {rewritten} of them were rewritten or added by this "
        f"lane; every other one carries its location-specific scope reason. Unreviewed: "
        f"{unreviewed}.",
        "",
        "| Location | Matching text | Disposition |",
        "|---|---|---|",
        *rows,
        "",
    ]
    args.out.write_text("\n".join(body))
    print(f"{len(hits)} matches, {rewritten} rewritten, {unreviewed} unreviewed")
    return 1 if unreviewed else 0


if __name__ == "__main__":
    sys.exit(main())
