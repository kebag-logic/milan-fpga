# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_input_mutants.py - the AECP campaign's planted defects for the input-port tests (#584; Milan v1.2 5.3.3.8 and
5.4.2.28): a STREAM_PORT_INPUT served as a headless one, its number_of_clusters 0 on the wire, and a REMOVE that keeps
the rows it removed. aecp_mutants.py plants each row; each named check must fail on its own words in the app arm at
the shipping shape."""

COMMANDS = 'aecp_commands.c'
MAPS = 'aecp_maps.c'
SERVE = '\tmemcpy(out + 4, d->value, d->length);\n'
KEPT = '\t\tm->count = kept;\n'
OWNS = 'Inputs.EveryStreamPortInputOwnsAMonoCluster'
REMOVES = 'Inputs.EveryStreamPortInputRemovesANonEmptyList'

ROWS = (
    # the 8x8 before #584 on the wire: a Stream Port Input that owns no AUDIO_CLUSTER
    ('input-port-served-headless', COMMANDS, SERVE,
     SERVE + '\tif (type == 14u) {\n\t\tout[16] = out[17] = 0;\n\t}\n',
     (OWNS, 'STREAM_PORT_INPUT 0 owns an AUDIO_CLUSTER (Milan v1.2 5.3.3.8)')),
    # a REMOVE_AUDIO_MAPPINGS that answers SUCCESS and leaves its rows in the port's map
    ('remove-keeps-its-rows', MAPS, KEPT, '',
     (REMOVES, 'STREAM_PORT_INPUT 0: the removed list leaves the page empty')),
)
