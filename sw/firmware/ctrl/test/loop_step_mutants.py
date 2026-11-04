# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the loop's step (#665, THE STEP in ctrl_loop.h): its binding, its place last in the pass with
the deadline read as the pass starts, its pass that takes no input, and its age limit; and of THE RETRY: its
binding, and its call only in a pass that took no input and dispatched no centisecond, after an aged step, or in a
pass of its own once its age limit is reached.
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
              "\t\towed = l->retry(l->retry_ctx) || owed;\n\t\tl->stats.retry_passes++;\n\t}\n")
#: THE RETRY's call after the aged step.
RETRY_AGED = ("\t\t// THE RETRY after the step: under input that leaves no pass empty, no other pass is free\n"
              "\t\t// of input\n"
              "\t\tif (l->retry != NULL) {\n\t\t\t(void)l->retry(l->retry_ctx);\n"
              "\t\t\tl->stats.retry_passes++;\n\t\t}\n")
#: THE STEP's age limit: the pass given whole to an aged step, which calls THE RETRY after it (ctrl_loop.c).
STEP_AGED = ("\tif (l->step != NULL && l->step_age > CTRL_LOOP_STEP_AGE) {\n\t\tl->step_age = 0u;\n"
             "\t\t(void)l->step(l->step_ctx, deadline);\n" + RETRY_AGED +
             "\t\tl->stats.passes++;\n\t\tl->stats.aged_passes++;\n"
             "\t\treturn 1u;\n\t}\n")
#: THE RETRY's age limit: the pass given whole to an aged retry, read after THE STEP's (ctrl_loop.c).
RETRY_AGE = ("\tif (l->retry != NULL && l->retry_aged(l->retry_ctx)) {\n\t\t(void)l->retry(l->retry_ctx);\n"
             "\t\tl->stats.retry_passes++;\n\t\tl->stats.passes++;\n\t\tl->stats.retry_aged_passes++;\n"
             "\t\treturn 1u;\n\t}\n")
#: THE RETRY's age limit's comment, which stands between the two aged passes.
RETRY_AGE_NOTE = ("\t// THE RETRY's age limit: a retry its client has held CTRL_LOOP_RETRY_AGE_MS past the time "
                  "it came due is this\n\t// whole pass, before any input, so a backlog or input that leaves no "
                  "pass empty holds it off no longer\n")
#: The events and the receive rings, the input a pass takes after the two aged passes.
INPUT = ("\tconst uint32_t ticks = l->stats.ticks;\n\tunsigned work = service_events(l);\n"
         "\tfor (unsigned ch = 0; ch < MBX_N_CH; ++ch) {\n\t\tif (l->rx[ch].fn != NULL) {\n"
         "\t\t\twork += service_rx(l, ch);\n\t\t}\n\t}\n")
#: THE TRANSMIT's pass, marked before the polls, and its call between the polls and THE RETRY (ctrl_loop.c).
TX_PASS = ("\t// THE TRANSMIT's pass, which its client's poll reads: one that took no record, at most "
           "CTRL_LOOP_TX_EVENTS\n\t// events and no centisecond\n"
           "\tl->tx_pass = l->transmit != NULL && l->stats.rx_records == records &&\n"
           "\t             l->stats.events - events <= CTRL_LOOP_TX_EVENTS && l->stats.ticks == ticks;\n")
TRANSMIT_CALL = ("\t// THE TRANSMIT, only in its pass, after the polls and before THE RETRY and THE STEP, "
                 "whose deadline counts its\n\t// time\n"
                 "\tif (l->tx_pass) {\n\t\towed = l->transmit(l->transmit_ctx) || owed;\n"
                 "\t\tl->stats.transmit_passes++;\n\t}\n")
#: The owed output a pass starts its polls with.
OWED = "\tbool owed = l->ticks_owed != 0u;\n"
#: THE TRANSMIT's age limit: the pass given whole to an aged build, read after THE RETRY's (ctrl_loop.c).
TRANSMIT_AGE = ("\tif (l->transmit != NULL && l->ordinary == l->stats.passes && l->transmit_aged(l->transmit_ctx)) "
                "{\n\t\t(void)l->transmit(l->transmit_ctx);\n" + RETRY_AGED.replace("\t\t// THE RETRY after the "
                "step: under input that leaves no pass empty, no other pass is free\n\t\t// of input\n", "") +
                "\t\tl->stats.transmit_passes++;\n\t\tl->stats.transmit_aged_passes++;\n\t\tl->stats.passes++;\n"
                "\t\treturn 1u;\n\t}\n")
#: Its comment, which stands between THE RETRY's aged pass and it.
TRANSMIT_AGE_NOTE = ("\t// THE TRANSMIT's age limit: a build its client has held more than CTRL_LOOP_TX_AGE "
                     "centiseconds is this whole\n\t// pass, before any input, with THE RETRY after it, once the pass "
                     "before was not given whole\n")
#: The counts a pass reads as it starts, which decide THE TRANSMIT's pass.
SNAPSHOT = "\tconst uint32_t events = l->stats.events;\n\tconst uint32_t records = l->stats.rx_records;\n"


def mutants(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the step, of THE RETRY and of THE TRANSMIT, built with ctrl_mutant.Mutant."""
    return (*step_mutants(kind), *retry_mutants(kind), *transmit_mutants(kind), *tick_mutants(kind))


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
        kind("step-before-the-polls", "loop/ctrl_loop.c", STEP_POLLS + TRANSMIT_CALL + RETRY_CALL + STEP_CALL,
             STEP_CALL + STEP_POLLS + TRANSMIT_CALL + RETRY_CALL,
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
        kind("step-aged-pass-takes-input", "loop/ctrl_loop.c", STEP_AGED,
             STEP_AGED.replace("\t\treturn 1u;\n", ""), "port", "Loop.L13AnAgedStepIsAPassOfItsOwn",
             "L13 and takes nothing else"),
        kind("step-aged-pass-sleeps", "loop/ctrl_loop.c", STEP_AGED, STEP_AGED.replace("return 1u;", "return 0u;"),
             "port", "Loop.L13AnAgedStepIsAPassOfItsOwn", "L13 the step's pass asks for the next pass at once"),
        kind("step-aged-deadline-not-read", "loop/ctrl_loop.c", "(void)l->step(l->step_ctx, deadline);",
             "(void)l->step(l->step_ctx, 0u);", "port", "Loop.L13AnAgedStepIsAPassOfItsOwn",
             "L13 with the deadline read as it starts"),
        kind("step-aged-pass-uncounted", "loop/ctrl_loop.c", "\t\tl->stats.aged_passes++;\n", "",
             "port", "Loop.L13AnAgedStepIsAPassOfItsOwn", "L13 the pass is counted as an aged step's"),
        kind("step-age-kept-by-its-pass", "loop/ctrl_loop.c", STEP_AGED,
             STEP_AGED.replace("\t\tl->step_age = 0u;\n", ""), "port", "Loop.L13AnAgedStepIsAPassOfItsOwn",
             "L13 the next pass takes the input it held off"),
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
        kind("retry-before-the-polls", "loop/ctrl_loop.c", STEP_POLLS + TRANSMIT_CALL + RETRY_CALL,
             RETRY_CALL + STEP_POLLS + TRANSMIT_CALL,
             "port", "Loop.L16TheRetryOnlyInAPassThatTakesNothing", "L16 after its polls"),
        kind("retry-after-the-step", "loop/ctrl_loop.c", RETRY_CALL + STEP_CALL, STEP_CALL + RETRY_CALL,
             "port", "Loop.L16TheRetryOnlyInAPassThatTakesNothing", "L16 and before THE STEP"),
        kind("retry-owed-lets-it-sleep", "loop/ctrl_loop.c", "\t\towed = l->retry(l->retry_ctx) || owed;\n",
             "\t\t(void)l->retry(l->retry_ctx);\n", "port", "Loop.L16TheRetryOnlyInAPassThatTakesNothing",
             "L16 a retry still owed asks for the next pass at once"),
        kind("retry-pass-uncounted", "loop/ctrl_loop.c", RETRY_CALL,
             RETRY_CALL.replace("\t\tl->stats.retry_passes++;\n", ""), "port",
             "Loop.L16TheRetryOnlyInAPassThatTakesNothing", "L16 the pass is counted as one that called the retry"),
        kind("retry-not-after-an-aged-step", "loop/ctrl_loop.c", STEP_AGED, STEP_AGED.replace(RETRY_AGED, ""),
             "port", "Loop.L16TheRetryOnlyInAPassThatTakesNothing",
             "L16 the pass given whole to an aged step calls it after the step"),
        kind("retry-before-the-aged-step", "loop/ctrl_loop.c",
             "\t\t(void)l->step(l->step_ctx, deadline);\n" + RETRY_AGED,
             RETRY_AGED + "\t\t(void)l->step(l->step_ctx, deadline);\n", "port",
             "Loop.L16TheRetryOnlyInAPassThatTakesNothing",
             "L16 the pass given whole to an aged step calls it after the step"),
        # THE RETRY's age limit (#665): a retry held CTRL_LOOP_RETRY_AGE_MS past its time is a pass of its own
        kind("retry-age-ignored", "loop/ctrl_loop.c", "l->retry != NULL && l->retry_aged(l->retry_ctx)",
             "l->retry != NULL && l->retry_aged == NULL", "port", "Loop.L17AnAgedRetryIsAPassOfItsOwn",
             "L17 the next pass calls the retry though input waits"),
        kind("retry-aged-pass-takes-input", "loop/ctrl_loop.c", RETRY_AGE, RETRY_AGE.replace("\t\treturn 1u;\n", ""),
             "port", "Loop.L17AnAgedRetryIsAPassOfItsOwn", "L17 and takes nothing else"),
        kind("retry-aged-pass-sleeps", "loop/ctrl_loop.c", RETRY_AGE, RETRY_AGE.replace("return 1u;", "return 0u;"),
             "port", "Loop.L17AnAgedRetryIsAPassOfItsOwn", "L17 the aged retry's pass asks for the next pass at once"),
        kind("retry-aged-pass-uncounted", "loop/ctrl_loop.c", "\t\tl->stats.retry_aged_passes++;\n", "",
             "port", "Loop.L17AnAgedRetryIsAPassOfItsOwn", "L17 the pass is counted as an aged retry's"),
        kind("retry-aged-pass-not-a-retry-pass", "loop/ctrl_loop.c", RETRY_AGE,
             RETRY_AGE.replace("\t\tl->stats.retry_passes++;\n", ""), "port", "Loop.L17AnAgedRetryIsAPassOfItsOwn",
             "L17 and as one that called the retry"),
        kind("retry-age-before-the-step-age", "loop/ctrl_loop.c", STEP_AGED + RETRY_AGE_NOTE + RETRY_AGE,
             RETRY_AGE_NOTE + RETRY_AGE + STEP_AGED, "port", "Loop.L17AnAgedRetryIsAPassOfItsOwn",
             "L17 an aged step's pass, read first, takes the round after the step"),
        kind("retry-age-read-after-the-input", "loop/ctrl_loop.c",
             RETRY_AGE_NOTE + RETRY_AGE + TRANSMIT_AGE_NOTE + TRANSMIT_AGE + SNAPSHOT + INPUT,
             TRANSMIT_AGE_NOTE + TRANSMIT_AGE + SNAPSHOT + INPUT + RETRY_AGE, "port",
             "Loop.L17AnAgedRetryIsAPassOfItsOwn",
             "L17 the age is read once as the pass starts, before it takes any input"),
    )


def transmit_mutants(kind: Callable[..., T]) -> tuple[T, ...]:
    """THE TRANSMIT's defects."""
    bind = "if (l->transmit != NULL || fn == NULL || aged == NULL) {"
    cond = "l->stats.events - events <= CTRL_LOOP_TX_EVENTS && l->stats.ticks == ticks;"
    aged = "l->transmit != NULL && l->ordinary == l->stats.passes && l->transmit_aged(l->transmit_ctx)"
    port, l18, l19, l20 = ("port", "LoopBring.L18TransmitBindingRefusals",
                           "Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord", "Loop.L20AnAgedTransmitIsAPassOfItsOwn")
    return (
        # THE TRANSMIT (#665): bound once, called only in a pass that took no record, at most CTRL_LOOP_TX_EVENTS
        # events and no centisecond, after its polls and before THE RETRY and THE STEP
        kind("transmit-binds-twice", "loop/ctrl_loop.c", bind, "if (fn == NULL || aged == NULL) {", port, l18,
             "L18 a second transmit client is refused"),
        kind("transmit-binds-no-function", "loop/ctrl_loop.c", bind, "if (l->transmit != NULL || aged == NULL) {",
             port, l18, "L18 a transmit client with no function is refused"),
        kind("transmit-binds-no-age", "loop/ctrl_loop.c", bind, "if (l->transmit != NULL || fn == NULL) {", port, l18,
             "L18 a transmit client with no age is refused"),
        kind("transmit-beside-records", "loop/ctrl_loop.c",
             "l->transmit != NULL && l->stats.rx_records == records &&\n",
             "l->transmit != NULL && l->stats.rx_records >= records &&\n", port, l19,
             "L19 a pass that takes a record does not call the transmit"),
        kind("transmit-beside-a-backlog", "loop/ctrl_loop.c", cond,
             cond.replace("<= CTRL_LOOP_TX_EVENTS", "<= CTRL_LOOP_EVENTS_PER_PASS"), port, l19,
             "L19 nor one that takes more than CTRL_LOOP_TX_EVENTS events"),
        kind("transmit-without-an-event", "loop/ctrl_loop.c", cond,
             cond.replace("<= CTRL_LOOP_TX_EVENTS", "< CTRL_LOOP_TX_EVENTS"), port, l19,
             "L19 a pass that takes one event and no record calls it"),
        kind("transmit-beside-a-centisecond", "loop/ctrl_loop.c", cond, cond.replace("== ticks;", ">= ticks;"),
             port, l19, "L19 nor one that dispatches a centisecond, though it takes no input"),
        kind("transmit-pass-marked-after-the-polls", "loop/ctrl_loop.c", TX_PASS + OWED + STEP_POLLS,
             OWED + STEP_POLLS + TX_PASS, port, l19, "L19 its polls read the pass as THE TRANSMIT's"),
        kind("transmit-before-the-polls", "loop/ctrl_loop.c", STEP_POLLS + TRANSMIT_CALL, TRANSMIT_CALL + STEP_POLLS,
             port, l19, "L19 after its polls"),
        kind("transmit-after-the-retry", "loop/ctrl_loop.c", TRANSMIT_CALL + RETRY_CALL, RETRY_CALL + TRANSMIT_CALL,
             port, l19, "L19 before THE RETRY and THE STEP"),
        kind("transmit-owed-lets-it-sleep", "loop/ctrl_loop.c", "\t\towed = l->transmit(l->transmit_ctx) || owed;\n",
             "\t\t(void)l->transmit(l->transmit_ctx);\n", port, l19,
             "L19 a transmit still owed asks for the next pass at once"),
        kind("transmit-pass-uncounted", "loop/ctrl_loop.c", TRANSMIT_CALL,
             TRANSMIT_CALL.replace("\t\tl->stats.transmit_passes++;\n", ""), port, l19,
             "L19 the pass is counted as one that called the transmit"),
        kind("transmit-in-the-aged-steps-pass", "loop/ctrl_loop.c", "\t\t(void)l->step(l->step_ctx, deadline);\n",
             "\t\t(void)l->step(l->step_ctx, deadline);\n\t\tif (l->transmit != NULL) {\n"
             "\t\t\t(void)l->transmit(l->transmit_ctx);\n\t\t}\n", port, l19,
             "L19 the pass given whole to an aged step does not call it"),
        # THE TRANSMIT's age limit (#665): a build held more than CTRL_LOOP_TX_AGE centiseconds is a pass of its own,
        # after one not given whole
        kind("transmit-age-ignored", "loop/ctrl_loop.c", aged, aged.replace("l->transmit_aged(l->transmit_ctx)",
             "l->transmit_aged == NULL"), port, l20,
             "L20 the next pass calls the transmit though input waits, then THE RETRY"),
        kind("transmit-aged-pass-takes-input", "loop/ctrl_loop.c", TRANSMIT_AGE,
             TRANSMIT_AGE.replace("\t\treturn 1u;\n", ""), port, l20,
             "L20 and takes nothing else: no event, no record, no poll, no centisecond"),
        kind("transmit-aged-pass-sleeps", "loop/ctrl_loop.c", TRANSMIT_AGE,
             TRANSMIT_AGE.replace("return 1u;", "return 0u;"), port, l20,
             "L20 the aged transmit's pass asks for the next pass at once"),
        kind("transmit-aged-pass-uncounted", "loop/ctrl_loop.c", "\t\tl->stats.transmit_aged_passes++;\n", "",
             port, l20, "L20 the pass is counted as an aged transmit's"),
        kind("transmit-aged-pass-not-a-transmit-pass", "loop/ctrl_loop.c", TRANSMIT_AGE,
             TRANSMIT_AGE.replace("\t\tl->stats.transmit_passes++;\n", ""), port, l20,
             "L20 and as one that called the transmit"),
        kind("transmit-aged-pass-without-the-retry", "loop/ctrl_loop.c", TRANSMIT_AGE,
             TRANSMIT_AGE.replace(RETRY_AGED.replace("\t\t// THE RETRY after the step: under input that leaves no "
                                                     "pass empty, no other pass is free\n\t\t// of input\n", ""), ""),
             port, l20, "L20 the next pass calls the transmit though input waits, then THE RETRY"),
        kind("transmit-aged-back-to-back", "loop/ctrl_loop.c", aged, aged.replace("l->ordinary == l->stats.passes && ",
             ""), port, l20, "L20 without reading the age after a pass given whole"),
        kind("transmit-ordinary-pass-unmarked", "loop/ctrl_loop.c", "\tl->ordinary = l->stats.passes;\n", "",
             port, l20, "L20 the next pass calls the transmit though input waits, then THE RETRY"),
        kind("transmit-age-before-the-retry-age", "loop/ctrl_loop.c",
             RETRY_AGE_NOTE + RETRY_AGE + TRANSMIT_AGE_NOTE + TRANSMIT_AGE,
             TRANSMIT_AGE_NOTE + TRANSMIT_AGE + RETRY_AGE_NOTE + RETRY_AGE, port, l20,
             "L20 an aged retry's pass, read first, takes its round alone"),
        kind("transmit-age-before-the-step-age", "loop/ctrl_loop.c",
             STEP_AGED + RETRY_AGE_NOTE + RETRY_AGE + TRANSMIT_AGE_NOTE + TRANSMIT_AGE,
             TRANSMIT_AGE_NOTE + TRANSMIT_AGE + STEP_AGED + RETRY_AGE_NOTE + RETRY_AGE, port, l20,
             "L20 an aged step's pass, read first, takes no build"),
        kind("transmit-age-read-after-the-input", "loop/ctrl_loop.c",
             TRANSMIT_AGE_NOTE + TRANSMIT_AGE + SNAPSHOT + INPUT, SNAPSHOT + INPUT + TRANSMIT_AGE, port, l20,
             "L20 the age is read once as the pass starts, before it takes any input"),
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
        kind("tick-cap-ignored", "loop/ctrl_loop.c", "\t\tif (k >= l->rx_cap) {\n\t\t\tbreak;\n\t\t}\n", "",
             "port", l21,
             "L21 a pass that dispatches a centisecond takes CTRL_LOOP_RX_PER_TICK_PASS records of a channel"),
    )
