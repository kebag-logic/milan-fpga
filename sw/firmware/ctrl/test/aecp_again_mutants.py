# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_again_mutants.py - the AECP campaign's planted defects in the checks a waiting command makes again once the
platform applied it (#950; IEEE 1722.1-2021 7.4.9, 8.2): a SET_STREAM_FORMAT's running check at the wait's end,
before the change is done again. aecp_mutants.py plants each row; every named check must fail on its own words, in
Core.AWaitingFormatChangeMakesItsRunningCheckAgainOnceApplied at two interfaces."""

#: The test, the words of its status check, and the check aecp_again makes, as aecp_commands.c holds it.
TEST = 'Core.AWaitingFormatChangeMakesItsRunningCheckAgainOnceApplied'
WORDS = 'a waiting SET_STREAM_FORMAT makes its running check again once applied: '
CHECK = 'running(a, a->noted_type, a->noted_index) : AECP_SUCCESS;'

ROWS = (
    # the shipped core's re-run without the check first
    ('again-unchecked', 'aecp.c',
     'unsigned status = taken ? aecp_again(a) : AECP_ENTITY_MISBEHAVING;',
     'unsigned status = taken ? AECP_SUCCESS : AECP_ENTITY_MISBEHAVING;',
     (TEST, WORDS + 'STREAM_INPUT 0, bound meanwhile'),
     (TEST, 'STREAM_INPUT 0: the check is made again')),
    ('again-other-command', 'aecp_commands.c',
     'return a->noted == AECP_CHANGE_FORMAT ?', 'return a->noted == AECP_CHANGE_CONFIGURATION ?',
     (TEST, WORDS + 'STREAM_INPUT 0, bound meanwhile')),
    ('again-input-judged-by-streaming', 'aecp_commands.c', CHECK,
     'running(a, 6u, a->noted_index) : AECP_SUCCESS;',
     (TEST, WORDS + 'STREAM_INPUT 0, bound meanwhile')),
    ('again-unobservable-taken', 'aecp_commands.c', CHECK,
     '(running(a, a->noted_type, a->noted_index) == AECP_STREAM_IS_RUNNING ? AECP_STREAM_IS_RUNNING : '
     'AECP_SUCCESS) : AECP_SUCCESS;',
     (TEST, WORDS + 'STREAM_INPUT 0, not observable once applied')),
    ('again-refusal-done-again', 'aecp.c',
     '\t\tif (status == AECP_SUCCESS) {\n\t\t\tswap(a);\n\t\t}\n', '\t\tif (taken) {\n\t\t\tswap(a);\n\t\t}\n',
     (TEST, 'a refused waiting SET_STREAM_FORMAT stays undone: STREAM_INPUT 0, bound meanwhile')),
    ('again-refusal-notified', 'aecp.c',
     'a->notify = status == AECP_SUCCESS;', 'a->notify = taken;',
     (TEST, 'STREAM_INPUT 0, bound meanwhile: one final response, no notification')),
    ('again-refusal-misbehaving', 'aecp.c',
     'refuse(a, status);', 'refuse(a, AECP_ENTITY_MISBEHAVING);',
     (TEST, WORDS + 'STREAM_INPUT 0, bound meanwhile')),
)
