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


def mutants(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the step and of THE RETRY, built with ctrl_mutant.Mutant."""
    return (*step_mutants(kind), *retry_mutants(kind))


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
        kind("retry-before-the-polls", "loop/ctrl_loop.c", STEP_POLLS + RETRY_CALL, RETRY_CALL + STEP_POLLS,
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
        kind("retry-age-read-after-the-input", "loop/ctrl_loop.c", RETRY_AGE_NOTE + RETRY_AGE + INPUT,
             INPUT + RETRY_AGE, "port", "Loop.L17AnAgedRetryIsAPassOfItsOwn",
             "L17 the age is read once as the pass starts, before it takes any input"),
    )
