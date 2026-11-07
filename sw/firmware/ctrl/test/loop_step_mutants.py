# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the loop's step (#665, THE STEP in ctrl_loop.h): its binding, its place last in the pass with
the deadline read as the pass starts, its pass that takes no input, and its age limit; of THE RETRY: its binding, its
call only in a pass that took no input and dispatched no centisecond or in a pass given whole, and what it is told of
the pass; of THE TRANSMIT: its binding and its pass given whole; of the row those passes stand in, and of THE DRAIN.
ctrl_mutants.py plants them with the rest of the control table; each must fail its named test on its own words.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

STEP_POLLS = ("\tfor (unsigned i = 0; i < l->n_polls; ++i) {\n"
              "\t\towed = l->polls[i].fn(l->polls[i].ctx) || owed;\n\t}\n")
STEP_CALL = ("\t// THE STEP, only in a pass that took no input: no input's service waits on it\n"
             "\tif (l->step != NULL && work == 0u) {\n\t\tbool waits = l->step(l->step_ctx, deadline);\n"
             "\t\tl->step_age = waits ? l->step_age : 0u;\n\t\towed = waits || owed;\n\t}\n")
#: THE RETRY's call in a pass that takes nothing, between the polls and THE STEP (ctrl_loop.c).
RETRY_CALL = ("\t// THE RETRY, only in a pass that took no input and dispatched no centisecond, before THE STEP, "
              "whose\n\t// deadline counts its time\n"
              "\tif (l->retry != NULL && work == 0u && l->stats.ticks == ticks) {\n"
              "\t\towed = round_of(l, deadline) || owed;\n\t}\n")
#: The pass given whole: a build first, then an aged step, then THE RETRY's round, which the other two carry.
BUILD = ("\t\tif (l->transmit != NULL && l->transmit_aged(l->transmit_ctx)) {\n"
         "\t\t\tl->transmit(l->transmit_ctx);\n\t\t\tl->stats.transmit_passes++;\n")
STEP_AGED = ("stepping) {\n\t\t\tl->step_age = 0u;\n\t\t\t(void)l->step(l->step_ctx, deadline);\n"
             "\t\t\tl->stats.aged_passes++;\n")
COUNTED = "\tl->stats.retry_passes++;\n"
GIVEN = "\t\t\tl->whole++;\n\t\t\treturn 1u;\n"
#: When a pass given whole may follow another (ctrl_loop.c, whole_runs).
ROW = ("\treturn l->whole < CTRL_LOOP_WHOLE_RUN && (!l->backlog || l->retry_firm) && !l->events_left &&\n"
       "\t       (l->drain_ch == 0u || !mbx_rx_waiting(l->drain_ch - 1u, mbx_rx_mark(l->drain_ch - 1u)));\n")


def mutants(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the step, of THE RETRY and of THE TRANSMIT, built with ctrl_mutant.Mutant."""
    return (*step_mutants(kind), *retry_mutants(kind), *transmit_mutants(kind), *tick_mutants(kind),
            *row_mutants(kind))


def step_mutants(kind: Callable[..., T]) -> tuple[T, ...]:
    """The step's defects."""
    return (
        # THE STEP (#665): bound once, last in the pass, with the deadline read as the pass starts
        kind("step-binds-twice", "loop/ctrl_loop.c", "if (l->step != NULL || fn == NULL", "if (fn == NULL",
             "port", "LoopBring.L10StepBindingRefusals", "L10 a second step is refused"),
        kind("step-binds-no-function", "loop/ctrl_loop.c", "|| fn == NULL || clock == NULL) {", "|| clock == NULL) {",
             "port", "LoopBring.L10StepBindingRefusals", "L10 a step with no function is refused"),
        kind("step-binds-no-clock", "loop/ctrl_loop.c", "|| fn == NULL || clock == NULL) {", "|| fn == NULL) {",
             "port", "LoopBring.L10StepBindingRefusals", "L10 a step with no clock is refused"),
        kind("step-before-the-polls", "loop/ctrl_loop.c", STEP_POLLS + RETRY_CALL + STEP_CALL,
             STEP_CALL + STEP_POLLS + RETRY_CALL,
             "port", "Loop.L11StepLastWithTheDeadlineReadAtTheStart", "L11 after every poll"),
        kind("step-deadline-read-at-the-end", "loop/ctrl_loop.c", "bool waits = l->step(l->step_ctx, deadline);",
             "bool waits = l->step(l->step_ctx, deadline - deadline + l->clock(l->clock_ctx) + CTRL_LOOP_SHARE_US);",
             "port",
             "Loop.L11StepLastWithTheDeadlineReadAtTheStart", "L11 the deadline is the share past the clock read as"),
        kind("step-deadline-without-the-share", "loop/ctrl_loop.c", "l->clock(l->clock_ctx) + CTRL_LOOP_SHARE_US : 0u",
             "l->clock(l->clock_ctx) : 0u", "port", "Loop.L11StepLastWithTheDeadlineReadAtTheStart",
             "L11 the deadline is the share past the clock read as"),
        kind("step-beside-input", "loop/ctrl_loop.c", "if (l->step != NULL && work == 0u) {", "if (l->step != NULL) {",
             "port", "Loop.L12StepOnlyInAPassThatTakesNoInput",
             "L12 a pass that takes a record does not take the step"),
        kind("step-owed-lets-it-sleep", "loop/ctrl_loop.c", "\t\towed = waits || owed;\n", "",
             "port", "Loop.L11StepLastWithTheDeadlineReadAtTheStart",
             "L11 a step still owed asks for the next pass at once"),
        # THE STEP's age limit (#665): past CTRL_LOOP_STEP_AGE centiseconds the step is a pass of its own
        kind("step-age-uncounted", "loop/ctrl_loop.c", "\tl->step_age += count;\n", "",
             "port", "Loop.L13AnAgedStepIsAPassOfItsOwn", "L13 the next pass takes the step though input waits"),
        kind("step-age-ignored", "loop/ctrl_loop.c", "l->step_age > CTRL_LOOP_STEP_AGE",
             "l->step_age > CTRL_LOOP_STEP_AGE + l->step_age", "port", "Loop.L13AnAgedStepIsAPassOfItsOwn",
             "L13 the next pass takes the step though input waits"),
        kind("step-age-at-the-limit", "loop/ctrl_loop.c", "l->step_age > CTRL_LOOP_STEP_AGE",
             "l->step_age >= CTRL_LOOP_STEP_AGE", "port", "Loop.L13AnAgedStepIsAPassOfItsOwn",
             "L13 the pass that dispatches one more takes its input, not the step"),
        kind("step-aged-pass-takes-input", "loop/ctrl_loop.c", GIVEN, GIVEN.replace("\t\t\treturn 1u;\n", ""),
             "port", "Loop.L13AnAgedStepIsAPassOfItsOwn", "L13 and takes nothing else"),
        kind("step-aged-pass-sleeps", "loop/ctrl_loop.c", GIVEN, GIVEN.replace("return 1u;", "return 0u;"),
             "port", "Loop.L13AnAgedStepIsAPassOfItsOwn", "L13 the step's pass asks for the next pass at once"),
        kind("step-aged-deadline-not-read", "loop/ctrl_loop.c", "(void)l->step(l->step_ctx, deadline);",
             "(void)l->step(l->step_ctx, 0u);", "port", "Loop.L13AnAgedStepIsAPassOfItsOwn",
             "L13 with the deadline read as it starts"),
        kind("step-aged-pass-uncounted", "loop/ctrl_loop.c", "\t\tl->stats.aged_passes++;\n", "",
             "port", "Loop.L13AnAgedStepIsAPassOfItsOwn", "L13 the pass is counted as an aged step's"),
        kind("step-age-kept-by-its-pass", "loop/ctrl_loop.c", STEP_AGED,
             STEP_AGED.replace("\t\t\tl->step_age = 0u;\n", ""), "port", "Loop.L13AnAgedStepIsAPassOfItsOwn",
             "L13 (a pass that takes nothing runs the step)"),
        kind("step-age-kept-after-a-step", "loop/ctrl_loop.c", "l->step_age = waits ? l->step_age : 0u;",
             "(void)0;", "port", "Loop.L13AnAgedStepIsAPassOfItsOwn",
             "L13 a step run in a pass that takes nothing starts its age again"),
        kind("step-age-reset-on-deferral", "loop/ctrl_loop.c", "l->step_age = waits ? l->step_age : 0u;",
             "l->step_age = 0u;", "port", "Loop.L13AnAgedStepIsAPassOfItsOwn",
             "L13 a step it had no room for keeps its age"),
        # the age counts the centiseconds a dispatch carries, not the dispatch: one TICK record carries every
        # centisecond counted while the event ring was held
        kind("step-age-counts-dispatches", "loop/ctrl_loop.c", "\tl->step_age += count;\n",
             "\tl->step_age += count != 0u;\n", "port", "Loop.L14TheAgeCountsCentisecondsNotDispatches",
             "L14 one dispatch of CTRL_LOOP_STEP_AGE + 1 centiseconds makes the next pass the step's alone"),
    )


def retry_mutants(kind: Callable[..., T]) -> tuple[T, ...]:
    """THE RETRY's defects."""
    return (
        # THE RETRY (#665): bound once, called only in a pass that took no input and dispatched no centisecond,
        # after its polls and before THE STEP, or after the step in an aged step's pass
        kind("retry-binds-twice", "loop/ctrl_loop.c", "if (l->retry != NULL || fn == NULL || aged == NULL) {",
             "if (fn == NULL || aged == NULL) {",
             "port", "LoopBring.L15RetryBindingRefusals", "L15 a second retry client is refused"),
        kind("retry-binds-no-function", "loop/ctrl_loop.c", "if (l->retry != NULL || fn == NULL || aged == NULL) {",
             "if (l->retry != NULL || aged == NULL) {", "port", "LoopBring.L15RetryBindingRefusals",
             "L15 a retry client with no function is refused"),
        kind("retry-binds-no-age", "loop/ctrl_loop.c", "if (l->retry != NULL || fn == NULL || aged == NULL) {",
             "if (l->retry != NULL || fn == NULL) {", "port", "LoopBring.L15RetryBindingRefusals",
             "L15 a retry client with no age is refused"),
        kind("retry-beside-input", "loop/ctrl_loop.c", "l->retry != NULL && work == 0u && l->stats.ticks == ticks",
             "l->retry != NULL && l->stats.ticks == ticks", "port", "Loop.L16TheRetryOnlyInAPassThatTakesNothing",
             "L16 a pass that takes a record does not call the retry"),
        kind("retry-beside-a-centisecond", "loop/ctrl_loop.c",
             "l->retry != NULL && work == 0u && l->stats.ticks == ticks",
             "l->retry != NULL && work == 0u && l->stats.ticks >= ticks",
             "port", "Loop.L16TheRetryOnlyInAPassThatTakesNothing",
             "L16 nor one that dispatches a centisecond, though it takes no input"),
        kind("retry-in-every-pass", "loop/ctrl_loop.c", "l->retry != NULL && work == 0u && l->stats.ticks == ticks",
             "l->retry != NULL && l->stats.ticks + work >= ticks", "port",
             "Loop.L16TheRetryOnlyInAPassThatTakesNothing", "L16 a pass that takes a record does not call the retry"),
        kind("retry-before-the-polls", "loop/ctrl_loop.c", STEP_POLLS + RETRY_CALL, RETRY_CALL + STEP_POLLS,
             "port", "Loop.L16TheRetryOnlyInAPassThatTakesNothing", "L16 after its polls"),
        kind("retry-after-the-step", "loop/ctrl_loop.c", RETRY_CALL + STEP_CALL, STEP_CALL + RETRY_CALL,
             "port", "Loop.L16TheRetryOnlyInAPassThatTakesNothing", "L16 and before THE STEP"),
        kind("retry-owed-lets-it-sleep", "loop/ctrl_loop.c", "\t\towed = round_of(l, deadline) || owed;\n",
             "\t\t(void)round_of(l, deadline);\n", "port",
             "Loop.L16TheRetryOnlyInAPassThatTakesNothing", "L16 a retry still owed asks for the next pass at once"),
        kind("retry-pass-uncounted", "loop/ctrl_loop.c", COUNTED, "", "port",
             "Loop.L16TheRetryOnlyInAPassThatTakesNothing", "L16 the pass is counted as one that called the retry"),
        # THE RETRY's pass given whole (#665): at its client's pace, beside an aged step or a build, or of its own
        kind("retry-age-ignored", "loop/ctrl_loop.c", "l->retry != NULL && l->retry_aged(l->retry_ctx)",
             "l->retry != NULL && l->retry_aged == NULL", "port", "Loop.L17AnAgedRetryIsAPassOfItsOwn",
             "L17 the next pass calls the retry though input waits"),
        kind("retry-aged-pass-takes-input", "loop/ctrl_loop.c", GIVEN, GIVEN.replace("\t\t\treturn 1u;\n", ""),
             "port", "Loop.L17AnAgedRetryIsAPassOfItsOwn", "L17 and takes nothing else"),
        kind("retry-aged-pass-sleeps", "loop/ctrl_loop.c", GIVEN, GIVEN.replace("return 1u;", "return 0u;"),
             "port", "Loop.L17AnAgedRetryIsAPassOfItsOwn", "L17 the aged retry's pass asks for the next pass at once"),
        kind("retry-aged-pass-not-a-retry-pass", "loop/ctrl_loop.c", COUNTED, "", "port",
             "Loop.L17AnAgedRetryIsAPassOfItsOwn", "L17 the pass is counted as one that called the retry"),
        kind("retry-not-after-an-aged-step", "loop/ctrl_loop.c", "\t\tif (round) {\n",
             "\t\tif (round && !stepping) {\n", "port", "Loop.L17AnAgedRetryIsAPassOfItsOwn",
             "L17 an aged step's pass takes the round after the step"),
        kind("retry-told-all-of-the-pass", "loop/ctrl_loop.c", "(int32_t)(deadline - l->clock(l->clock_ctx)) : ",
             "(int32_t)(deadline - l->clock(l->clock_ctx) * 0u) * 0 + (int32_t)CTRL_LOOP_SHARE_US : ", "port",
             "Loop.L17AnAgedRetryIsAPassOfItsOwn", "L17 a round beside a step has what the step left of the pass"),
        kind("retry-told-past-the-margin", "loop/ctrl_loop.c", "\t\t\t     (int32_t)CTRL_LOOP_SHARE_MARGIN_US;\n",
             "\t\t\t     0;\n", "port", "Loop.L17AnAgedRetryIsAPassOfItsOwn",
             "L17 a round in a pass of its own has all of it under the margin, with no clock"),
    )


def transmit_mutants(kind: Callable[..., T]) -> tuple[T, ...]:
    """THE TRANSMIT's defects."""
    bind = "if (l->transmit != NULL || fn == NULL || aged == NULL) {"
    port, l18, l20 = "port", "LoopBring.L18TransmitBindingRefusals", "Loop.L20AnOwedBuildIsAPassOfItsOwn"
    return (
        # THE TRANSMIT (#665): bound once, and a build owed is a pass given whole, ahead of an aged step
        kind("transmit-binds-twice", "loop/ctrl_loop.c", bind, "if (fn == NULL || aged == NULL) {", port, l18,
             "L18 a second transmit client is refused"),
        kind("transmit-binds-no-function", "loop/ctrl_loop.c", bind, "if (l->transmit != NULL || aged == NULL) {",
             port, l18, "L18 a transmit client with no function is refused"),
        kind("transmit-binds-no-age", "loop/ctrl_loop.c", bind, "if (l->transmit != NULL || fn == NULL) {", port, l18,
             "L18 a transmit client with no age is refused"),
        kind("transmit-due-ignored", "loop/ctrl_loop.c", "l->transmit != NULL && l->transmit_aged(l->transmit_ctx)",
             "l->transmit != NULL && l->transmit_aged == NULL", port, l20,
             "L20 the next pass calls the transmit though input waits, then an aged round"),
        kind("transmit-pass-takes-input", "loop/ctrl_loop.c", GIVEN, GIVEN.replace("\t\t\treturn 1u;\n", ""), port, l20,
             "L20 and takes nothing else: no event, no record, no poll, no centisecond"),
        kind("transmit-pass-sleeps", "loop/ctrl_loop.c", GIVEN, GIVEN.replace("return 1u;", "return 0u;"), port, l20,
             "L20 the build's pass asks for the next pass at once"),
        kind("transmit-pass-uncounted", "loop/ctrl_loop.c", BUILD,
             BUILD.replace("\t\t\tl->stats.transmit_passes++;\n", ""), port, l20,
             "L20 the pass is counted as the transmit's"),
        kind("transmit-pass-without-the-retry", "loop/ctrl_loop.c", "\t\tif (round) {\n",
             "\t\tif (round && l->transmit == NULL) {\n", port, l20,
             "L20 the next pass calls the transmit though input waits, then an aged round"),
        kind("transmit-after-an-aged-step", "loop/ctrl_loop.c", BUILD,
             BUILD.replace("l->transmit != NULL && l->transmit_aged(l->transmit_ctx)",
                           "!stepping && l->transmit != NULL && l->transmit_aged(l->transmit_ctx)"), port, l20,
             "L20 a build owed comes before an aged step"),
        kind("transmit-in-the-aged-steps-pass", "loop/ctrl_loop.c", "\t\t\t(void)l->step(l->step_ctx, deadline);\n",
             "\t\t\t(void)l->step(l->step_ctx, deadline);\n\t\t\tif (l->transmit != NULL) {\n"
             "\t\t\t\tl->transmit(l->transmit_ctx);\n\t\t\t}\n", port, l20,
             "L20 the aged step's pass may follow it, the second in a row"),
    )


def tick_mutants(kind: Callable[..., T]) -> tuple[T, ...]:
    """THE TICK's cap's defects: a pass that dispatches a centisecond takes CTRL_LOOP_RX_PER_TICK_PASS records of a
    channel (#665)."""
    cap = "l->rx_cap = ticked != 0u ? CTRL_LOOP_RX_PER_TICK_PASS : CTRL_LOOP_RX_PER_PASS;"
    l21 = "Loop.L21APassThatDispatchesACentisecondTakesOneRecordOfAChannel"
    return (
        kind("tick-pass-uncapped", "loop/ctrl_loop.c", cap, "l->rx_cap = CTRL_LOOP_RX_PER_PASS;", "port", l21,
             "L21 a pass that dispatches a centisecond takes CTRL_LOOP_RX_PER_TICK_PASS records of a channel"),
        kind("tick-cap-in-every-pass", "loop/ctrl_loop.c", cap, "l->rx_cap = CTRL_LOOP_RX_PER_TICK_PASS;", "port",
             l21, "L21 the next pass, which dispatches none, takes CTRL_LOOP_RX_PER_PASS"),
        kind("tick-cap-ignored", "loop/ctrl_loop.c",
             "l->rx_cap = ticked != 0u ? CTRL_LOOP_RX_PER_TICK_PASS : CTRL_LOOP_RX_PER_PASS;",
             "l->rx_cap = ticked != 0u ? CTRL_LOOP_RX_PER_PASS : CTRL_LOOP_RX_PER_PASS;", "port", l21,
             "L21 a pass that dispatches a centisecond takes CTRL_LOOP_RX_PER_TICK_PASS records of a channel"),
    )


def row_mutants(kind: Callable[..., T]) -> tuple[T, ...]:
    """The row passes given whole stand in, what marks it short, and THE DRAIN's defects (#665)."""
    port, l22, l23, l24 = ("port", "Loop.L22PassesGivenWholeStandApartAsInputWaits",
                           "Loop.L23TheDrainTakesItsChannelFirstWhileThePassHasRoom",
                           "Loop.L24ARecordFollowsOnlyTheEventsPostedBeforeIt")
    limit = "(int32_t)(deadline - l->clock(l->clock_ctx)) < (int32_t)(CTRL_LOOP_SHARE_US - CTRL_LOOP_DRAIN_US))) {"
    l23s = "Loop.L25WhatAPassHasLeftGoesToTheRecordsStillWaiting"
    return (
        kind("whole-row-unlimited", "loop/ctrl_loop.c", ROW, ROW.replace("l->whole < CTRL_LOOP_WHOLE_RUN && ", ""),
             port, l22, "L22 a fourth may not"),
        kind("whole-row-of-two", "loop/ctrl_loop.c", ROW,
             ROW.replace("CTRL_LOOP_WHOLE_RUN", "CTRL_LOOP_WHOLE_RUN - 1u"), port, l22, "L22 and a third"),
        kind("whole-row-beside-a-backlog", "loop/ctrl_loop.c", ROW,
             ROW.replace("(!l->backlog || l->retry_firm) && ", ""), port, l22,
             "L22 and no second while records wait and the client yields"),
        kind("whole-row-beside-events", "loop/ctrl_loop.c", ROW, ROW.replace(" && !l->events_left", ""), port, l22,
             "L22 none follows another while events wait"),
        kind("whole-row-beside-the-drain", "loop/ctrl_loop.c", ROW,
             ROW.replace("!mbx_rx_waiting(l->drain_ch - 1u, mbx_rx_mark(l->drain_ch - 1u))", "true"), port, l22,
             "L22 and none follows another while a record of THE DRAIN's channel waits"),
        kind("backlog-never-marked", "loop/ctrl_loop.c",
             "\tl->backlog = l->backlog || (n != 0u && n >= l->rx_cap);\n", "", port, l22,
             "L22 a pass that leaves a record marks the backlog"),
        kind("backlog-never-cleared", "loop/ctrl_loop.c", "\tl->backlog = false;\n", "", port, l22,
             "L22 the ring taken, the backlog is gone"),
        kind("drain-past-its-time", "loop/ctrl_loop.c", limit, "(int32_t)(deadline - l->clock(l->clock_ctx)) < 0)) {",
             port, l23, "L23 and stops once the pass has spent CTRL_LOOP_DRAIN_US"),
        kind("drain-to-the-cap-alone", "loop/ctrl_loop.c",
             "service_rx(l, l->drain_ch - 1u, CTRL_LOOP_DRAIN_RECORDS, deadline)",
             "service_rx(l, l->drain_ch - 1u, l->rx_cap, deadline)", port, l23,
             "L23 with a clock it goes past CTRL_LOOP_RX_PER_PASS"),
        kind("spare-records-beside-no-centisecond", "loop/ctrl_loop.c", "if (l->rx_cap != 0u && !l->backlog) {",
             "if (l->rx_cap != 0u && (l->rx_cap != CTRL_LOOP_RX_PER_PASS || !l->backlog)) {", port, l23s,
             "L23 a pass that dispatches a centisecond takes them too"),
        kind("spare-records-never-taken", "loop/ctrl_loop.c", "if (l->rx_cap != 0u && !l->backlog) {", "if (true) {",
             port, l23s, "L23 what a pass has left goes to the records still waiting"),
        kind("spare-records-channel-by-channel", "loop/ctrl_loop.c", "most = 1u) {",
             "most = CTRL_LOOP_DRAIN_RECORDS) {", port, l23s, "L23 one a channel in turn"),
        kind("drain-past-its-records", "loop/ctrl_loop.c",
             "service_rx(l, l->drain_ch - 1u, CTRL_LOOP_DRAIN_RECORDS, deadline)",
             "service_rx(l, l->drain_ch - 1u, 2u * CTRL_LOOP_DRAIN_RECORDS, deadline)", port, l23,
             "L23 and stops at CTRL_LOOP_DRAIN_RECORDS"),
        kind("rx-start-stays", "loop/ctrl_loop.c",
             "\tl->rx_from = l->rx_from + 1u < MBX_N_CH ? l->rx_from + 1u : 0u;\n", "", port,
             "Loop.L25WhatAPassHasLeftGoesToTheRecordsStillWaiting", "L25 each pass starts one channel on"),
        kind("rx-start-wraps-short", "loop/ctrl_loop.c", "l->rx_from + 1u < MBX_N_CH ? l->rx_from + 1u : 0u;",
             "l->rx_from + 1u < MBX_N_CH ? l->rx_from + 1u : 1u;", port,
             "Loop.L25WhatAPassHasLeftGoesToTheRecordsStillWaiting", "L25 and wraps past the last"),
        kind("rx-start-ignored", "loop/ctrl_loop.c", "ch = l->rx_from; k < MBX_N_CH;", "ch = 0u; k < MBX_N_CH;", port,
             "Loop.L25WhatAPassHasLeftGoesToTheRecordsStillWaiting",
             "L25 the channel a pass starts at has the time first"),
        kind("order-mark-read-after-the-events", "loop/ctrl_loop.c", "\t\tl->rx_order = mark;\n",
             "\t\t(void)mark;\n\t\tl->rx_order = l->drain_ch != 0u ? mbx_rx_mark(l->drain_ch - 1u) : 0u;\n", port, l24,
             "L24 the mark is read before the events"),
        kind("order-moved-past-events-left", "loop/ctrl_loop.c", "\tif (!l->events_left) {\n", "\tif (true) {\n", port,
             l24, "L24 a pass that leaves events keeps the order where it was"),
    )
