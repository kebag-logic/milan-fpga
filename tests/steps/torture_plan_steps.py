# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Steps for torture_campaign_plan.feature.
#
# These steps audit tb/tools/torture_campaign.py - the plan the on-bench runner
# executes - and nothing else. They never touch a socket, a board or a capture:
# the whole point is that the campaign's COVERAGE and its ASSERTION CONTRACT are
# reviewable in three seconds at a desk, because the alternative is auditing
# them by spending bench time, and bench time is the resource the campaign is
# trying to spend well.
#
# The plan is DATA (torture_campaign.Step), so every assertion here is a
# property of that data. When a new area or condition is added to the plan, the
# scenarios that describe the contract - clause present, severity valid, unique
# ids, full assertion set on a bind - apply to it automatically.

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from behave import given, then, when

if TYPE_CHECKING:
    # Signatures only, and deliberately not a runtime import: behave is what
    # loads this module, so `behave.runner` is already in sys.modules by the
    # time a step runs, and nothing here is worth an import that could move
    # under an unpinned `pip install behave` in CI.
    from behave.runner import Context

ROOT = Path(__file__).resolve().parents[2]
# `sys.path` holds strings; the Path stops at this boundary.
sys.path.insert(0, str(ROOT / "tb" / "tools"))

import torture_campaign as tp  # noqa: E402


@given("the campaign plan is importable")
def step_tp_import(context: Context) -> None:
    """Prove `build_plan` is still the entry point before any scenario leans on it, and start from an empty plan."""
    assert hasattr(tp, "build_plan"), "torture_campaign.build_plan missing"
    context.tp_plan = []
    context.tp_cov = {}


def _plan(context: Context, areas: list[str] | None = None,
          dut: tp.Device | None = None,
          peer: tp.Device | None = None) -> list[tp.Step]:
    """Build the plan for `areas` over the given devices and hang it, with its coverage audit, on the scenario
    context for the `then` steps to read."""
    d = dut or tp.ARTY
    p = peer or tp.PEER
    context.tp_dut, context.tp_peer = d, p
    context.tp_plan = tp.build_plan(areas, d, p)
    context.tp_cov = tp.plan_covers_every_index(context.tp_plan, d, p)
    return context.tp_plan


@when("the matrix area is planned")
def step_tp_matrix(context: Context) -> None:
    """Plan the full bind matrix - every DUT talker into every peer listener, the return direction, and the
    intra-DUT loopback that keeps the campaign meaningful with the reference device out of the rack."""
    _plan(context, ["matrix"])


@when("the matrix area is planned for a device with {t:d} talker and {l:d} "
      "listener")
def step_tp_matrix_solo(context: Context, t: int, l: int) -> None:
    """Plan the matrix over a synthetic device with `t` talkers and `l` listeners - the narrow shape the coverage
    audit must still be able to tell apart from the real one."""
    solo = tp.Device("solo", "aa" * 8, "bb" * 6, talkers=t, listeners=l)
    _plan(context, ["matrix"], solo, solo)


@when("the churn area is planned")
def step_tp_churn(context: Context) -> None:
    """Plan the churn area alone: the implicit rebind, the unbind/re-bind pair and the rebind storm."""
    _plan(context, ["churn"])


@when("the torture area is planned")
def step_tp_torture(context: Context) -> None:
    """Plan the adverse-conditions area alone: the traffic storms, the malformed frames and the physical-layer
    entries a human performs."""
    _plan(context, ["torture"])


@when("the matrix and churn areas are planned")
def step_tp_matrix_churn(context: Context) -> None:
    """Plan matrix and churn together, so a per-area audit has two areas of one plan to tell apart."""
    _plan(context, ["matrix", "churn"])


@when("the whole campaign is planned")
def step_tp_all(context: Context) -> None:
    """Plan the whole campaign over the real DUT and peer, in the execution order `build_plan` emits."""
    _plan(context)


# ------------------------------------------------------------------ coverage --
@then("the plan covers every DUT talker index")
def step_tp_cov_dut_t(context: Context) -> None:
    """Every DUT talker index is bound somewhere in the plan. Index 0 is a hard alias of the flat registers, so an
    index-0-only campaign exercises the alias path and reports full coverage of it."""
    want = context.tp_dut.talker_indices()
    assert context.tp_cov["dut_talker"] == want, \
        f"{context.tp_cov['dut_talker']} != {want}"


@then("the plan covers every DUT listener index")
def step_tp_cov_dut_l(context: Context) -> None:
    """Every DUT listener index is bound somewhere in the plan - the side where GET_COUNTERS once answered index 0
    for every index and left sinks >= 2 with an empty mask."""
    want = context.tp_dut.listener_indices()
    assert context.tp_cov["dut_listener"] == want, \
        f"{context.tp_cov['dut_listener']} != {want}"


@then("the plan covers every peer talker index")
def step_tp_cov_peer_t(context: Context) -> None:
    """Every peer talker index is bound too: without the return direction the DUT is only ever a source."""
    want = context.tp_peer.talker_indices()
    assert context.tp_cov["peer_talker"] == want, \
        f"{context.tp_cov['peer_talker']} != {want}"


@then("the plan covers every peer listener index")
def step_tp_cov_peer_l(context: Context) -> None:
    """Every peer listener index is bound too, so what the DUT reports has a second end to be corroborated against."""
    want = context.tp_peer.listener_indices()
    assert context.tp_cov["peer_listener"] == want, \
        f"{context.tp_cov['peer_listener']} != {want}"


@then("the plan contains outbound, return and loopback pair sets")
def step_tp_pair_sets(context: Context) -> None:
    """All three pair sets are present - `out.` DUT-to-peer, `ret.` peer-to-DUT and `loop.` intra-DUT - because each
    covers indices the other two cannot reach."""
    pre = {s.sid.split(".")[0] for s in context.tp_plan}
    for want in ("out", "ret", "loop"):
        assert want in pre, f"no {want}.* pair set in the plan ({sorted(pre)})"


@then("the plan covers only index {n:d}")
def step_tp_cov_only(context: Context, n: int) -> None:
    """The synthetic one-stream device covers index `n` and nothing else, in both directions."""
    assert context.tp_cov["dut_talker"] == [n], context.tp_cov
    assert context.tp_cov["dut_listener"] == [n], context.tp_cov


@then("that is fewer indices than the real DUT shape")
def step_tp_cov_fewer(context: Context) -> None:
    """The one-stream coverage is strictly smaller than the real DUT's, which is what proves the audit can still say
    no rather than reporting whatever it was handed."""
    assert len(context.tp_cov["dut_talker"]) < len(tp.ARTY.talker_indices()), (
        "the one-stream audit is not distinguishable from the real DUT shape - "
        "the coverage check has stopped being able to say no")


@then("the CRF talker index is in the plan")
def step_tp_crf_t(context: Context) -> None:
    """The CRF media-clock talker index is inside the covered set, not left out with the audio streams."""
    assert tp.ARTY.crf_out in context.tp_cov["dut_talker"], context.tp_cov


@then("the CRF listener index is in the plan")
def step_tp_crf_l(context: Context) -> None:
    """The CRF media-clock listener index is inside the covered set."""
    assert tp.ARTY.crf_in in context.tp_cov["dut_listener"], context.tp_cov


@then("the CRF pair steps are marked as the media clock pair")
def step_tp_crf_note(context: Context) -> None:
    """The CRF pair is marked in its note, so a runner can aim the Milan 7.3.2 format expectation at the right pair
    instead of applying it to every stream."""
    hits = [s for s in context.tp_plan if "CRF media-clock pair" in s.note]
    assert hits, ("no step is marked as the CRF media-clock pair - a runner "
                  "cannot then apply the Milan 7.3.2 format expectation to the "
                  "right pair")


# ------------------------------------------------------------ the contract --
@then("every connect step carries the full bound-streaming assertion set")
def step_tp_full_set(context: Context) -> None:
    """Every connect step owes the whole bound-streaming assertion set - rebinds included, since a rebind re-enters
    the bound state and so re-triggers the counter reset it would otherwise be excused from."""
    # EVERY connect step, INCLUDING the rebinds.  The `"rebind" in s.sid`
    # exclusion that used to be here silently dropped 8 of the 105 connect steps
    # from a scenario titled "every bind step owes the whole set" - and the
    # rebind is the step that most needs the set, because Milan 5.5.3.5.43's
    # implicit rebind re-enters the bound state and so re-triggers the 5.3.8.10
    # counter reset.
    need = {a.name for a in tp.BOUND_STREAMING_ASSERTS}
    bad, seen = [], 0
    for s in context.tp_plan:
        if s.op != "connect":
            continue
        seen += 1
        got = {a.name for a in s.asserts}
        if not need <= got:
            bad.append((s.sid, sorted(need - got)))
    assert seen, "no connect steps in the plan"
    assert not bad, f"{len(bad)} of {seen} connect steps miss assertions: " \
                    f"{bad[:5]}"
    context.tp_connects = seen


@then("that includes the rebind steps")
def step_tp_full_set_rebinds(context: Context) -> None:
    """The plan really contains rebind connect steps carrying that set, so the scenario is exercising the exclusion
    it exists to keep removed rather than passing over an empty list."""
    reb = [s for s in context.tp_plan
           if s.op == "connect" and s.sid.endswith(".rebind")]
    assert reb, ("no rebind connect steps in this plan, so the scenario is not "
                 "exercising the exclusion it exists to remove")
    need = {a.name for a in tp.BOUND_STREAMING_ASSERTS}
    for s in reb:
        got = {a.name for a in s.asserts}
        assert need <= got, (s.sid, sorted(need - got))


@then("every bind is followed by a measure-before-start step")
def step_tp_start_if_needed(context: Context) -> None:
    """Each bind is followed by its own measure-before-start step, which is the step that owns the SRP licence
    question; a bind with no such successor has nowhere to ask it."""
    plan = context.tp_plan
    binds = [i for i, s in enumerate(plan) if s.op == "connect"]
    assert binds, "no bind steps"
    for i in binds:
        nxt = plan[i + 1] if i + 1 < len(plan) else None
        assert nxt is not None and nxt.op == "start_stream_if_needed", (
            f"{plan[i].sid} is not followed by a measure-before-start step "
            f"(next is {nxt.sid + ' / ' + nxt.op if nxt else 'nothing'}); the "
            f"licence question belongs to its own step, so a bind with no such "
            f"successor has nowhere to ask it")
    context.tp_sin = plan[binds[0] + 1]


@then("that step asserts the stream starts on the bind alone")
def step_tp_start_assert(context: Context) -> None:
    """That step is where 'the stream starts on the bind alone' is graded, against Milan v1.2 5.3.7.3."""
    names = {a.name for a in context.tp_sin.asserts}
    assert tp.A_STREAM_ON_BIND_ALONE.name in names, names
    assert "5.3.7.3" in tp.A_STREAM_ON_BIND_ALONE.clause


@then("that step measures before it sends anything")
def step_tp_start_measure_first(context: Context) -> None:
    """That step carries a measurement window and says so in its note, so a runner cannot send START_STREAMING
    first and then never learn whether it was needed."""
    assert context.tp_sin.args.get("measure_first_s", 0) > 0, (
        "the step does not carry a measurement window, so a runner could send "
        "START_STREAMING first and never learn whether it was needed")
    assert "measure BEFORE" in context.tp_sin.note, context.tp_sin.note


@then("that step asks the SRP licence before it grades any silence")
def step_tp_licence_first(context: Context) -> None:
    """The licence reading is asked before any silence is graded: a bound-but-ungated talker is CORRECTLY silent
    under 5.3.7.3, and grading it without the reading turns conformance into a violation."""
    names = {a.name for a in context.tp_sin.asserts}
    assert tp.A_SRP_LICENCE.name in names, (
        f"the measure-before-start step does not carry "
        f"{tp.A_SRP_LICENCE.name}, so a bound-but-ungated talker - which Milan "
        f"v1.2 5.3.7.3 makes CORRECTLY silent - would be graded as a violation")
    assert "5.3.7.3" in tp.A_SRP_LICENCE.clause
    assert "0x694" in tp.A_SRP_LICENCE.clause, tp.A_SRP_LICENCE.clause


@then("no bind step grades whether frames are advancing")
def step_tp_bind_has_no_tick(context: Context) -> None:
    """No bind step grades whether frames are advancing - the D1 fix held as a property of the plan, because the
    licence bit is not readable from a bind step."""
    # THE D1 FIX AS A PLAN PROPERTY.  A_TX_TICKING / A_RX_TICKING used to sit in
    # BOUND_STREAMING_ASSERTS, so every connect step in the plan owed a
    # frames-advance verdict that it had no licence reading to condition on.
    ticks = {tp.A_TX_TICKING.name, tp.A_RX_TICKING.name}
    assert not (ticks & {a.name for a in tp.BOUND_STREAMING_ASSERTS}), (
        "the bound-streaming set still contains a frames-advance assertion; the "
        "licence (LWSRP_STATUS bit 8) is not readable from a bind step, so "
        "grading silence there turns every conformant bound-but-ungated pair "
        "into a SHALL failure")
    bad = [s.sid for s in context.tp_plan
           if s.op == "connect" and (ticks & {a.name for a in s.asserts})]
    assert not bad, bad[:5]


@then("the licence-owning step carries the cross-participant invariants")
def step_tp_licence_xside(context: Context) -> None:
    """The licence-owning step carries the cross-participant invariants and names BOTH ends, because a one-sided
    measurement can report agreement with nothing."""
    names = {a.name for a in context.tp_sin.asserts}
    for a in (tp.A_XSIDE_CORROBORATED, tp.A_XSIDE_UNLICENSED_SILENT,
              tp.A_XSIDE_NOT_MORE, tp.A_XSIDE_PRUNED,
              tp.A_XSIDE_INTERVAL_AGREE, tp.A_INSTRUMENT_LOSSLESS):
        assert a.name in names, (a.name, sorted(names))
    # and it names BOTH ends, because a one-sided measurement cannot corroborate
    for k in ("talker", "talker_index", "listener", "listener_index"):
        assert k in context.tp_sin.args, (k, context.tp_sin.args)


@then("every unbind verifies the stop took effect")
def step_tp_unbind_stops(context: Context) -> None:
    """Every disconnect verifies the stop took effect, with a MAC to address it to. Without that, the first
    START_STREAMING latches the talker and every later pair measures an already-streaming one."""
    unbinds = [s for s in context.tp_plan if s.op == "disconnect"]
    assert unbinds, "no disconnect steps"
    for s in unbinds:
        names = {a.name for a in s.asserts}
        assert tp.A_STOP_TAKES_EFFECT.name in names, (
            f"{s.sid} does not verify the stop.  Without it the first "
            f"START_STREAMING latches the talker and every later pair measures "
            f"an ALREADY-STREAMING talker, so stream.starts-on-bind-alone "
            f"reports a false PASS for every pair after the first")
        assert s.args.get("stop_streaming") is True, s.args
        assert s.args.get("stop_window_s", 0) > 0, s.args
        assert s.args.get("talker_mac"), (
            f"{s.sid} has no talker MAC, so STOP_STREAMING cannot be addressed")


@then("the whole campaign has no assertion that can only be INFO at SHALL "
      "severity")
def step_tp_no_shall_only_info(context: Context) -> None:
    """No SHALL assertion is one the runner could only ever emit as INFO: the growth checks are shown to produce
    both a FAIL and a PASS, so they contribute to the exit code rather than reading as coverage."""
    # An assertion whose severity is SHALL but which the runner can only ever
    # emit as INFO contributes nothing to the exit code while reading as
    # coverage.  The three growth assertions were exactly that.
    for a in (tp.A_NO_LATE_EARLY, tp.A_NO_SEQ_MISMATCH, tp.A_NO_UNSUPPORTED):
        assert a.severity == "SHALL", a
    v, _ = tp.check_no_growth({"LATE_TIMESTAMP": 0}, {"LATE_TIMESTAMP": 1},
                              ("LATE_TIMESTAMP",))
    assert v == "FAIL", ("check_no_growth cannot produce a FAIL, so the growth "
                         "assertions are decoration at SHALL severity")
    v, _ = tp.check_no_growth({"LATE_TIMESTAMP": 4}, {"LATE_TIMESTAMP": 4},
                              ("LATE_TIMESTAMP",))
    assert v == "PASS", "check_no_growth cannot produce a PASS either"


@then("coverage is audited per area")
def step_tp_cov_per_area(context: Context) -> None:
    """Coverage is audited per area and every area walks every index on its own - the only form of the audit that
    the matrix area's completeness cannot mask."""
    by = tp.plan_coverage_by_area(context.tp_plan, context.tp_dut,
                                 context.tp_peer)
    assert set(by) == {s.area for s in context.tp_plan}, sorted(by)
    for area in by:
        ok, d = tp.area_covers_every_index(context.tp_plan, area,
                                          context.tp_dut, context.tp_peer)
        assert ok, (area, d["missing"])
    context.tp_by_area = by


@then("the per-area audit can say no about one area while another is complete")
def step_tp_cov_per_area_bites(context: Context) -> None:
    """The per-area audit rejects an index-0-only audio area over a plan the whole-plan audit still passes, which is
    the masking that made the per-area form necessary."""
    lonely = [s for s in context.tp_plan if s.area != "audio"
              or s.sid.endswith(".t0") or s.sid == "audio.thdn"]
    ok, d = tp.area_covers_every_index(lonely, "audio", context.tp_dut,
                                      context.tp_peer)
    assert not ok, "an index-0-only audio area passed the per-area audit"
    assert tp.area_covers_every_index(lonely, "matrix", context.tp_dut,
                                     context.tp_peer)[0]
    # the WHOLE-plan audit is still green over the same plan: that is the
    # masking, and it is why the per-area form had to exist
    whole = tp.plan_covers_every_index(lonely, context.tp_dut, context.tp_peer)
    assert whole["dut_talker"] == context.tp_dut.talker_indices(), whole


@then("the topology is configuration and a typo is refused")
def step_tp_topology(context: Context) -> None:
    """The device shape is configuration: a parsed spec widens the coverage, and a misspelled field raises instead
    of running the whole campaign against the wrong shape and reporting full coverage of it."""
    d = tp.parse_device_spec("talkers=8,listeners=8,crf_out=8,crf_in=8",
                             tp.ARTY)
    plan = tp.build_plan(["matrix"], d, tp.PEER)
    cov = tp.plan_covers_every_index(plan, d, tp.PEER)
    assert cov["dut_talker"] == list(range(9)), cov
    try:
        tp.parse_device_spec("listners=10", tp.ARTY)
    except ValueError:
        pass
    else:
        raise AssertionError("a misspelled device field was silently ignored, "
                             "so the whole campaign would run against the "
                             "wrong shape and report full coverage of it")


@then("every assertion carries a non-empty clause")
def step_tp_clauses(context: Context) -> None:
    """No assertion is left without a clause, so every verdict a runner emits can name what it is grading against."""
    bad = [(s.sid, a.name) for s in context.tp_plan for a in s.asserts
           if not a.clause.strip()]
    assert not bad, f"assertions with no clause: {bad[:5]}"


@then("every assertion severity is SHALL or RECOMMENDED or INFO")
def step_tp_severity(context: Context) -> None:
    """Every severity is one of the three the exit code knows how to weigh; a fourth spelling would be silently
    counted as neither."""
    bad = [(s.sid, a.name, a.severity) for s in context.tp_plan
           for a in s.asserts
           if a.severity not in ("SHALL", "RECOMMENDED", "INFO")]
    assert not bad, bad[:5]


@then("no two steps share an id")
def step_tp_unique(context: Context) -> None:
    """No two steps share an id, so a verdict record identifies exactly one step of one run."""
    ids = [s.sid for s in context.tp_plan]
    dups = sorted({i for i in ids if ids.count(i) > 1})
    assert not dups, f"duplicate step ids: {dups[:5]}"


@then("every step serialises to JSON with its clauses attached")
def step_tp_json(context: Context) -> None:
    """Every step serialises to JSON carrying a clause AND a severity for each assertion it names, so the record a
    runner emits is readable without the plan beside it."""
    for s in context.tp_plan:
        d = s.as_dict()
        json.dumps(d)
        assert set(d["assert_clauses"]) == set(d["asserts"]), s.sid
        assert set(d["assert_severity"]) == set(d["asserts"]), s.sid


# ----------------------------------------------------------------- the churn --
def _rebinds(context: Context) -> list[tp.Step]:
    return [s for s in context.tp_plan if s.sid.endswith(".rebind")]


@then("there is a rebind step that does not unbind first")
def step_tp_rebind(context: Context) -> None:
    """The churn area contains a rebind that does not unbind first - Milan v1.2 5.5.3.5.43's implicit rebind, the
    transition a bind/unbind loop never reaches."""
    reb = _rebinds(context)
    assert reb, "no implicit-rebind step in the churn area"
    for s in reb:
        assert s.args.get("no_unbind_first"), s.sid
        assert "5.5.3.5.43" in s.clause, s.clause


@then("each rebind moves to a DIFFERENT talker index than its first bind")
def step_tp_rebind_diff(context: Context) -> None:
    """Each rebind moves to a DIFFERENT talker index than its first bind, so the step can distinguish 'handled the
    transition' from 'ignored the command'."""
    first = {s.sid: s.args["talker_index"] for s in context.tp_plan
             if s.op == "connect" and not s.sid.endswith(".rebind")
             and s.sid.startswith("churn.implicit-rebind")}
    for s in _rebinds(context):
        base = s.sid.rsplit(".", 1)[0]
        assert base in first, f"{s.sid} has no matching first bind"
        assert s.args["talker_index"] != first[base], (
            f"{s.sid} rebinds to the SAME talker index - that cannot "
            f"distinguish 'handled the transition' from 'ignored the command'")


@then("the rebind step asserts the counter reset on not-bound to bound")
def step_tp_rebind_reset(context: Context) -> None:
    """The rebind owes the not-bound-to-bound counter reset, which is the observable the implicit rebind is worth
    testing for."""
    for s in _rebinds(context):
        names = {a.name for a in s.asserts}
        assert tp.A_COUNTER_RESET_ON_BIND.name in names, s.sid


@then("there is a bind-while-streaming step")
def step_tp_bws(context: Context) -> None:
    """The plan binds a pair that is already streaming, not only idle ones."""
    assert any("bind-while-streaming" in s.sid for s in context.tp_plan)


@then("there is a rebind storm step with at least {n:d} iterations")
def step_tp_storm(context: Context, n: int) -> None:
    """A rebind storm of at least `n` iterations is planned, and becomes the step the following checks read."""
    hits = [s for s in context.tp_plan if s.op == "rebind_storm"]
    assert hits, "no rebind-storm step"
    assert hits[0].args["iterations"] >= n, hits[0].args
    context.tp_storm = hits[0]


@then("the rebind storm asserts the lock invariant and ADP liveness")
def step_tp_storm_asserts(context: Context) -> None:
    """The storm owes the media-clock lock invariant and ADP liveness: churn may cost neither the entity's clock
    nor its advertisement."""
    names = {a.name for a in context.tp_storm.asserts}
    assert tp.A_LOCK_INVARIANT.name in names, names
    assert tp.A_ADP_ALIVE.name in names, names


# -------------------------------------------------------- adverse honesty --
def _storms(context: Context) -> list[tp.Step]:
    return [s for s in context.tp_plan if ".storm." in s.sid]


@then("every storm step marks stream continuity as RECOMMENDED")
def step_tp_storm_rec(context: Context) -> None:
    """Stream continuity under a traffic storm is RECOMMENDED, never SHALL - the source is a recommended practice,
    and grading it as a requirement would fail a conformant device for its network."""
    ss = _storms(context)
    assert ss, "no storm steps"
    for s in ss:
        sev = {a.name: a.severity for a in s.asserts}
        assert sev.get(tp.A_STREAM_CONTINUITY.name) == "RECOMMENDED", \
            (s.sid, sev)


@then("every storm step marks control responsiveness as INFO")
def step_tp_storm_info(context: Context) -> None:
    """Control responsiveness under a storm is INFO: AVDECC is non-priority traffic, so a slow answer is recorded
    and never graded."""
    for s in _storms(context):
        sev = {a.name: a.severity for a in s.asserts}
        assert sev.get(tp.A_CONTROL_RESPONSIVE.name) == "INFO", (s.sid, sev)


@then("the storm steps cover non-priority broadcast, unicast to our own MAC, "
      "AVDECC and AVB management")
def step_tp_storm_classes(context: Context) -> None:
    """All four traffic classes are planned, and the unicast one is addressed to the DUT's own MAC - the case the
    recommended practice draws attention to by name."""
    have = {s.args["traffic"] for s in _storms(context)}
    for want in ("non-priority-broadcast", "non-priority-unicast-to-us",
                 "avdecc-flood", "avb-management"):
        assert want in have, f"{want} missing from the storm classes ({have})"
    # and the unicast case is addressed to the DUT's own MAC, which is the case
    # the recommendation draws attention to by name
    uni = [s for s in _storms(context)
           if s.args["traffic"] == "non-priority-unicast-to-us"][0]
    assert uni.args["dst"] == context.tp_dut.mac, uni.args


def _malformed(context: Context) -> list[tp.Step]:
    return [s for s in context.tp_plan if s.op == "malformed_frame"]


@then("no malformed-frame step cites the adverse-conditions recommendation")
def step_tp_malformed_source(context: Context) -> None:
    """No malformed-frame step cites the adverse-conditions recommended practice: that document covers sustained
    high rate traffic only, and a citation it does not support is a verdict nothing backs."""
    def cites(txt: str) -> bool:
        """Whether `txt` reads as a citation of the adverse-network-conditions recommended practice."""
        t = txt.lower()
        return "adverse" in t and "network" in t
    bad = [s.sid for s in _malformed(context)
           if cites(s.clause)
           or any(cites(a.clause) for a in s.asserts
                  if a is not tp.A_STREAM_CONTINUITY)]
    assert not bad, (f"{bad} cite the adverse-conditions recommended practice "
                     f"for malformed frames, and that document covers only "
                     f"sustained high rate traffic")


@then("no clause in the campaign carries a draft version number")
def step_tp_no_draft_version(context: Context) -> None:
    """No clause carries a draft version number or a quoted revision history - detail visible only to a document
    holder, and needed by no technical claim the campaign makes."""
    # PRIVACY / SOURCING RULE: cite the adverse-conditions recommended practice
    # generically.  A draft version number - and worse, a quotation of its
    # revision history - is a detail visible only to a document holder, and it
    # is not needed for any technical claim the campaign makes.
    import re
    bad = []
    for s in context.tp_plan:
        for txt in [s.clause, s.note] + [a.clause for a in s.asserts]:
            t = (txt or "")
            if re.search(r"v?0\.1\.\d", t) or "Remove[d]" in t:
                bad.append((s.sid, t[:90]))
    assert not bad, bad[:5]


@then("every malformed-frame step cites IEEE 1722.1 or IEEE 1722")
def step_tp_malformed_clause(context: Context) -> None:
    """Every malformed-frame step cites a standard - IEEE 1722.1, IEEE 1722 or Milan Table 5.6 - so the failure it
    reports is a requirement and not a preference."""
    ms = _malformed(context)
    assert ms, "no malformed-frame steps"
    for s in ms:
        assert ("1722.1" in s.clause or "1722-2016" in s.clause
                or "Milan v1.2 Table 5.6" in s.clause), (s.sid, s.clause)


@then("every malformed-frame step asserts the entity does not wedge")
def step_tp_malformed_wedge(context: Context) -> None:
    """Every malformed-frame step grades the one thing the standards do require of it: the entity does not wedge."""
    for s in _malformed(context):
        names = {a.name for a in s.asserts}
        assert "entity.no-wedge-after-malformed" in names, (s.sid, names)


@then("the malformed matrix includes an overstated control_data_length")
def step_tp_mal_over(context: Context) -> None:
    """The malformed matrix includes a control_data_length larger than the payload - the over-read."""
    assert any(s.args["mutation"] == "cdl-overstated"
               for s in _malformed(context))


@then("the malformed matrix includes an understated control_data_length")
def step_tp_mal_under(context: Context) -> None:
    """The malformed matrix includes a control_data_length smaller than the payload - the trailing-garbage case."""
    assert any(s.args["mutation"] == "cdl-understated"
               for s in _malformed(context))


@then("the malformed matrix includes a truncated AECP payload")
def step_tp_mal_trunc(context: Context) -> None:
    """The malformed matrix includes an AECP payload cut off mid-field."""
    assert any(s.args["mutation"] == "truncated-mid-payload"
               for s in _malformed(context))


@then("the malformed matrix includes an AAF stream_data_length that overstates "
      "the payload")
def step_tp_mal_sdl(context: Context) -> None:
    """The malformed matrix includes an AAF stream_data_length that overstates the payload - the streaming-side
    counterpart of the AECP over-read."""
    assert any(s.args["mutation"] == "aaf-sdl-overstated"
               for s in _malformed(context))


@then("the MAAP conflict step asserts a withdraw and reallocate")
def step_tp_maap(context: Context) -> None:
    """The MAAP conflict step grades a withdraw AND a reallocate, and becomes the step the next check reads."""
    hits = [s for s in context.tp_plan if s.op == "maap_conflict"]
    assert hits, "no MAAP conflict step"
    names = {a.name for a in hits[0].asserts}
    assert "maap.withdraws-and-reallocates" in names, names
    context.tp_maap = hits[0]


@then("the MAAP conflict clause mentions the LeaveAll wait")
def step_tp_maap_leaveall(context: Context) -> None:
    """The MAAP entry names the two-LeaveAll wait Milan Table 5.3 requires; an immediate re-claim is a different
    behaviour and would pass a step that only looked for a new address."""
    txt = context.tp_maap.clause + " " + context.tp_maap.note + " " + \
        " ".join(a.clause for a in context.tp_maap.asserts)
    assert "LeaveAll" in txt, (
        "the MAAP conflict entry does not mention the 2 LeaveAll wait Milan "
        "Table 5.3 requires - an immediate re-claim is a different behaviour")


@then("there is a wrong-SR-VID step")
def step_tp_vlan_wrong(context: Context) -> None:
    """A step streams on an SR VID that is neither the configured one nor zero."""
    hits = [s for s in context.tp_plan if s.sid.endswith("wrong-sr-vid")]
    assert hits and hits[0].args["set_vid"] not in (0, 2), hits


@then("there is a VID-zero step")
def step_tp_vlan_zero(context: Context) -> None:
    """A step streams with VID 0 - the priority-tagged case - and becomes the step the next check reads."""
    hits = [s for s in context.tp_plan if s.sid.endswith("vid-zero")]
    assert hits and hits[0].args["set_vid"] == 0, hits
    context.tp_vid0 = hits[0]


@then("the VID-zero step asserts no untagged stream frames")
def step_tp_vlan_zero_assert(context: Context) -> None:
    """The VID-zero step grades that no stream frame leaves the DUT untagged."""
    names = {a.name for a in context.tp_vid0.asserts}
    assert "wire.no-untagged-stream-frames" in names, names


@then("the source-starvation step asserts the talker keeps framing")
def step_tp_starve(context: Context) -> None:
    """Starving the source still owes a ticking talker: the required behaviour is zero fill, not absence, and only
    a frames-advance assertion tells the two apart."""
    hits = [s for s in context.tp_plan if s.op == "starve_source"]
    assert hits, "no source-starvation step"
    names = {a.name for a in hits[0].asserts}
    assert tp.A_TX_TICKING.name in names, names
    assert "wire.zero-fill-not-absence" in names, names


@then("the stream-stop step asserts STREAM_INTERRUPTED advances")
def step_tp_stop(context: Context) -> None:
    """Stopping the talker owes a STREAM_INTERRUPTED advance on the listener, so silence is observed and not merely
    assumed."""
    hits = [s for s in context.tp_plan if s.op == "stop_talker"]
    assert hits, "no stream-stop step"
    names = {a.name for a in hits[0].asserts}
    assert "counters.stream_input.stream-interrupted-advances" in names, names


# ------------------------------------------------------------ human entries --
@then("at least {n:d} steps need a human")
def step_tp_human_count(context: Context, n: int) -> None:
    """At least `n` steps need a human, and they become the set the checklist checks are read against."""
    hs = tp.human_steps(context.tp_plan)
    assert len(hs) >= n, f"{len(hs)} human steps, expected at least {n}"
    context.tp_human = hs


@then("the checklist names every human step with its action and its clause")
def step_tp_checklist(context: Context) -> None:
    """The checklist names every human step with its action, its clause and each assertion it owes, so the operator
    at the bench needs nothing else open."""
    txt = tp.checklist_text(context.tp_plan)
    for s in context.tp_human:
        assert s.sid in txt, s.sid
        assert s.human_action[:24] in txt, s.sid
        assert s.clause[:24] in txt, s.sid
        for a in s.asserts:
            assert a.name in txt, (s.sid, a.name)


@then("an empty plan produces a checklist that says so")
def step_tp_checklist_empty(context: Context) -> None:
    """An empty plan yields a checklist that says so, rather than a blank page that reads as 'nothing to do'."""
    assert "No human-action entries" in tp.checklist_text([])


@then("the human entries include a cable pull")
def step_tp_human_cable(context: Context) -> None:
    """A per-port cable pull is one of the human entries - a powerstrip cannot pull one cable."""
    assert any("cable-pull" in s.sid for s in tp.human_steps(context.tp_plan))


@then("the human entries include a grandmaster change")
def step_tp_human_gmchg(context: Context) -> None:
    """A grandmaster change is planned: the switch cycle re-elects a GM, and the step owes the GM_CHANGED counter
    advance that makes the re-election observable."""
    # the switch cycle IS the grandmaster change: the re-join re-elects one GM
    # (priority1 untouched), and the step owes the GM_CHANGED counter advance
    assert any("counters.avb_interface.gptp-gm-changed-advances"
               in {a.name for a in s.asserts}
               for s in tp.human_steps(context.tp_plan))


@then("the human entries include a grandmaster loss")
def step_tp_human_gmloss(context: Context) -> None:
    """A grandmaster loss is planned: the partition makes each island elect its own GM, recorded retroactively
    because the controller host is inside the partition."""
    # the partition IS the grandmaster loss: each island elects its own GM,
    # verified retroactively - the step owes the partition-is-the-test record
    assert any("physical.partition-is-the-test"
               in {a.name for a in s.asserts}
               for s in tp.human_steps(context.tp_plan))


@then("the human entries include a power cycle")
def step_tp_human_power(context: Context) -> None:
    """A power cycle is one of the human entries, and becomes the step the next check reads."""
    hits = [s for s in tp.human_steps(context.tp_plan)
            if "power-cycle" in s.sid]
    assert hits, "no power-cycle entry"
    context.tp_power = hits[0]


@then("the power-cycle step asserts the non-volatile state is restored")
def step_tp_power_nv(context: Context) -> None:
    """The power cycle grades both halves of the non-volatile contract: configuration restored, counters zeroed."""
    names = {a.name for a in context.tp_power.asserts}
    assert "state.restored-after-power-cycle" in names, names
    assert "counters.zeroed-after-power-cycle" in names, names


# ------------------------------------------------- the physical family --
def _phys_cycles(context: Context) -> list[tp.Step]:
    return [s for s in context.tp_plan
            if s.op in ("switch_power_cycle", "dut_power_cycle")]


@then("the physical area is the last thing the campaign runs")
def step_tp_phys_last(context: Context) -> None:
    """The physical area is the campaign's tail and nothing interleaves with it: a switch partition or a DUT power
    cycle mid-plan would pollute every verdict that followed."""
    order = []
    for s in context.tp_plan:
        if s.area not in order:
            order.append(s.area)
    assert order[-1] == "physical", order
    # and once it starts, nothing else interleaves
    tail = [s.area for s in context.tp_plan
            if s.area == "physical" or order.index(s.area) > order.index(
                "physical")]
    assert set(tail) == {"physical"}, tail


@then("every physical cycle step is still a human entry in the plan")
def step_tp_phys_human(context: Context) -> None:
    """Both cycle steps are still human entries carrying an action, so an outlet the runner cannot reach never
    silently becomes an automated pass."""
    cycles = _phys_cycles(context)
    assert len(cycles) == 2, [s.sid for s in cycles]
    for s in cycles:
        assert s.needs_human and s.human_action, s.sid


@then("the physical cycle steps name the outlet role they need")
def step_tp_phys_outlet(context: Context) -> None:
    """Each cycle names the outlet role it needs, so the switch cycle cannot be performed on the DUT's outlet."""
    roles = {s.op: s.args.get("outlet_role") for s in _phys_cycles(context)}
    assert roles == {"switch_power_cycle": "switch",
                     "dut_power_cycle": "dut"}, roles


@then("the physical recovery budgets respect the bench floors")
def step_tp_phys_budgets(context: Context) -> None:
    """The recovery budgets clear the bench floors they were measured against - the announce-receipt timeout, the
    switch's own link restore, and the worst-case cold boot."""
    by = {s.op: s.args for s in _phys_cycles(context)}
    sw, du = by["switch_power_cycle"], by["dut_power_cycle"]
    # hold >> the 802.1AS announce-receipt timeout (3 announce intervals)
    assert sw["hold_s"] >= 15, sw
    # the DN-1 must restore its links before gPTP recovery can be measured
    assert sw["link_budget_s"] >= 180, sw
    assert sw["gptp_budget_s"] >= 120, sw
    # a real drain, and the measured ~5.5 min worst-case cold boot
    assert du["off_s"] >= 5, du
    assert du["net_budget_s"] >= 120, du


@then("the partition window is asserted as the condition, not a failure")
def step_tp_phys_partition(context: Context) -> None:
    """The switch off-window is asserted at INFO: the controller host is inside the partition, so unreachability
    there is the condition of the test and can never grade the device."""
    sw = [s for s in _phys_cycles(context)
          if s.op == "switch_power_cycle"][0]
    spec = {a.name: a for a in sw.asserts}["physical.partition-is-the-test"]
    # INFO severity: unreachability during the off-window can never grade the
    # device - the controller host is INSIDE the partition
    assert spec.severity == "INFO", spec


@then("each physical family ends with a full proof pair at a non-zero index")
def step_tp_phys_proof(context: Context) -> None:
    """Each physical family ends with a full bound-streaming proof pair at a NON-ZERO index, so recovery is proved
    on the indexed path and not on index 0's alias."""
    need = {a.name for a in tp.BOUND_STREAMING_ASSERTS}
    for fam in ("switch-cycle", "dut-cycle"):
        conn = [s for s in context.tp_plan
                if s.sid.startswith(f"phys.{fam}.proof")
                and s.op == "connect"]
        assert conn, fam
        assert conn[0].args["talker_index"] > 0, conn[0].args
        got = {a.name for a in conn[0].asserts}
        assert need <= got, (fam, need - got)


# ------------------------------------------------------ runner integration --
@then("selecting the audio area yields only audio steps")
def step_tp_sel_audio(context: Context) -> None:
    """Selecting one area yields that area's steps and no others, so a bench session can spend its time where it
    means to."""
    assert {s.area for s in tp.build_plan(["audio"])} == {"audio"}


@then("selecting an unknown area raises")
def step_tp_sel_bad(context: Context) -> None:
    """An unknown area name raises, rather than planning nothing and reporting full coverage of it."""
    try:
        tp.build_plan(["not-an-area"])
    except ValueError:
        return
    raise AssertionError("an unknown area was accepted")


@then("selecting nothing yields all five areas")
def step_tp_sel_all(context: Context) -> None:
    """Selecting nothing plans every declared area: the default is the whole campaign, never a subset that drifted."""
    assert {s.area for s in tp.build_plan()} == set(tp.AREAS), \
        sorted({s.area for s in tp.build_plan()})


@then("a verdict record carries schema, step, assertion, verdict, severity and "
      "clause")
def step_tp_record(context: Context) -> None:
    """A verdict record carries schema, step, assertion, verdict, severity, clause, area, run and the free-form
    detail - and is JSON, because the runner emits one line per assertion."""
    r = tp.verdict_record("s.1", "a.b", "PASS", clause="X 1.2", area="matrix",
                          run="run-1", extra=7)
    for k in ("schema", "step", "assertion", "verdict", "severity", "clause",
              "area", "run", "detail"):
        assert k in r, k
    assert r["detail"]["extra"] == 7
    json.dumps(r)


@then("a SHALL failure exits {n:d}")
def step_tp_exit_shall(context: Context, n: int) -> None:
    """A SHALL failure exits `n`: the only verdict class that fails the run outright."""
    assert tp.exit_code([tp.verdict_record("a", "x", "FAIL")]) == n


@then("a RECOMMENDED failure exits {n:d}")
def step_tp_exit_rec(context: Context, n: int) -> None:
    """A RECOMMENDED failure exits `n`, distinct from a SHALL failure so a report can separate what the device owes
    from what the network cost it."""
    assert tp.exit_code([tp.verdict_record("a", "x", "FAIL",
                                           severity="RECOMMENDED")]) == n


@then("an outstanding human entry exits {n:d}")
def step_tp_exit_human(context: Context, n: int) -> None:
    """An outstanding human entry exits `n`: a cable pull nobody performed is not a pass."""
    assert tp.exit_code([tp.verdict_record("a", "x", "NEEDS-HUMAN")]) == n


@then("a SKIP alone exits {n:d}")
def step_tp_exit_skip(context: Context, n: int) -> None:
    """A SKIP alone exits `n` - nothing was proved, and nothing was violated."""
    assert tp.exit_code([tp.verdict_record("a", "x", "SKIP")]) == n


@then("the summary counts every verdict kind")
def step_tp_summary(context: Context) -> None:
    """The summary counts every verdict kind and carries the exit code, so one dict is the whole run's report."""
    recs = [tp.verdict_record("a", "x", v) for v in tp.VERDICTS]
    s = tp.summarise(recs)
    for v in tp.VERDICTS:
        assert s[v] == 1, (v, s)
    assert s["total"] == len(tp.VERDICTS)
    assert "exit_code" in s
