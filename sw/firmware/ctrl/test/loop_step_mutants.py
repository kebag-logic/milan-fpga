# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the loop's step (#665, THE STEP in ctrl_loop.h): its binding, its place last in the pass with
the deadline read as the pass starts, its pass that takes no input, and its age limit. ctrl_mutants.py plants them
with the rest of the control table; each must fail its named test on its own words.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

STEP_POLLS = ("\tfor (unsigned i = 0; i < l->n_polls; ++i) {\n"
              "\t\towed = l->polls[i].fn(l->polls[i].ctx) || owed;\n\t}\n")
STEP_CALL = ("\t// THE STEP, only in a pass that took no input: no input's service waits on it\n"
             "\tif (l->step != NULL && work == 0u) {\n\t\tbool waits = l->step(l->step_ctx, deadline);\n"
             "\t\tl->step_age = waits ? l->step_age : 0u;\n\t\towed = waits || owed;\n\t}\n")
#: THE STEP's age limit: the pass given whole to an aged step (ctrl_loop.c).
STEP_AGED = ("\tif (l->step != NULL && l->step_age > CTRL_LOOP_STEP_AGE) {\n\t\tl->step_age = 0u;\n"
             "\t\t(void)l->step(l->step_ctx, deadline);\n\t\tl->stats.passes++;\n\t\tl->stats.aged_passes++;\n"
             "\t\treturn 1u;\n\t}\n")


def mutants(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every defect of the step, built with ctrl_mutant.Mutant."""
    return (
        # THE STEP (#665): bound once, last in the pass, with the deadline read as the pass starts
        kind("step-binds-twice", "loop/ctrl_loop.c", "if (l->step != NULL || fn == NULL", "if (fn == NULL",
             "port", "LoopBring.L10StepBindingRefusals", "L10 a second step is refused"),
        kind("step-binds-no-function", "loop/ctrl_loop.c", "|| fn == NULL || clock == NULL) {", "|| clock == NULL) {",
             "port", "LoopBring.L10StepBindingRefusals", "L10 a step with no function is refused"),
        kind("step-binds-no-clock", "loop/ctrl_loop.c", "|| fn == NULL || clock == NULL) {", "|| fn == NULL) {",
             "port", "LoopBring.L10StepBindingRefusals", "L10 a step with no clock is refused"),
        kind("step-before-the-polls", "loop/ctrl_loop.c", STEP_POLLS + STEP_CALL, STEP_CALL + STEP_POLLS,
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
