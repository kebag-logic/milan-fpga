# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R532-9's eight escaping plants, re-run at R532-10 (srp_driver.py ... escape IF this.py).

Six srp_bounds.h understatements copied from the R532-9 packet scripts/bound_probes.tsv
and two code regressions from its scripts/probe_mutants.py; each through both suites
that compile the header. CAUGHT = any test of that suite fails."""
from srp_mutants import Defect

PROBES = (
    Defect('rv-poll-fixed@srp_app', '*', '(MBX_N_IF * (4u + 2u * SRP_MBX_TX_MAX))', '(MBX_N_IF * (0u + 2u * SRP_MBX_TX_MAX))', '', path='srp/srp_bounds.h', suite='srp_app.cpp'),
    Defect('rv-poll-fixed@test_acmp_mbx', '*', '(MBX_N_IF * (4u + 2u * SRP_MBX_TX_MAX))', '(MBX_N_IF * (0u + 2u * SRP_MBX_TX_MAX))', '', path='srp/srp_bounds.h', suite='test_acmp_mbx.cpp'),
    Defect('rv-poll-two-calls@srp_app', '*', '(MBX_N_IF * (4u + 2u * SRP_MBX_TX_MAX))', '(MBX_N_IF * (4u + 1u * SRP_MBX_TX_MAX))', '', path='srp/srp_bounds.h', suite='srp_app.cpp'),
    Defect('rv-poll-two-calls@test_acmp_mbx', '*', '(MBX_N_IF * (4u + 2u * SRP_MBX_TX_MAX))', '(MBX_N_IF * (4u + 1u * SRP_MBX_TX_MAX))', '', path='srp/srp_bounds.h', suite='test_acmp_mbx.cpp'),
    Defect('rv-poll-per-if@srp_app', '*', '(MBX_N_IF * (4u + 2u * SRP_MBX_TX_MAX))', '(1u * (4u + 2u * SRP_MBX_TX_MAX))', '', path='srp/srp_bounds.h', suite='srp_app.cpp'),
    Defect('rv-poll-per-if@test_acmp_mbx', '*', '(MBX_N_IF * (4u + 2u * SRP_MBX_TX_MAX))', '(1u * (4u + 2u * SRP_MBX_TX_MAX))', '', path='srp/srp_bounds.h', suite='test_acmp_mbx.cpp'),
    Defect('rv-pass-event-words@srp_app', '*', 'CTRL_LOOP_EVENTS_PER_PASS * (MBX_EV_WORDS + 2u + SRP_MBX_EVENT_MAX)', 'CTRL_LOOP_EVENTS_PER_PASS * (SRP_MBX_EVENT_MAX)', '', path='srp/srp_bounds.h', suite='srp_app.cpp'),
    Defect('rv-pass-event-words@test_acmp_mbx', '*', 'CTRL_LOOP_EVENTS_PER_PASS * (MBX_EV_WORDS + 2u + SRP_MBX_EVENT_MAX)', 'CTRL_LOOP_EVENTS_PER_PASS * (SRP_MBX_EVENT_MAX)', '', path='srp/srp_bounds.h', suite='test_acmp_mbx.cpp'),
    Defect('rv-pass-rx-count@srp_app', '*', 'CTRL_LOOP_RX_PER_PASS * (SRP_MBX_RX_RECORD_MAX', '1u * (SRP_MBX_RX_RECORD_MAX', '', path='srp/srp_bounds.h', suite='srp_app.cpp'),
    Defect('rv-pass-rx-count@test_acmp_mbx', '*', 'CTRL_LOOP_RX_PER_PASS * (SRP_MBX_RX_RECORD_MAX', '1u * (SRP_MBX_RX_RECORD_MAX', '', path='srp/srp_bounds.h', suite='test_acmp_mbx.cpp'),
    Defect('rv-pass-poll-half@srp_app', '*', 'SRP_MBX_RX_MAX) + SRP_MBX_POLL_MAX)', 'SRP_MBX_RX_MAX) + SRP_MBX_POLL_MAX / 2u)', '', path='srp/srp_bounds.h', suite='srp_app.cpp'),
    Defect('rv-pass-poll-half@test_acmp_mbx', '*', 'SRP_MBX_RX_MAX) + SRP_MBX_POLL_MAX)', 'SRP_MBX_RX_MAX) + SRP_MBX_POLL_MAX / 2u)', '', path='srp/srp_bounds.h', suite='test_acmp_mbx.cpp'),
    Defect('code-poll-extra-read@srp_app', '*', '        bool link = mbx_link_up(n);\n', '        bool link = mbx_link_up(n);\n        (void)mbx_irq_status();\n', '', path='srp/srp_mbx.c', suite='srp_app.cpp'),
    Defect('code-poll-extra-read@test_acmp_mbx', '*', '        bool link = mbx_link_up(n);\n', '        bool link = mbx_link_up(n);\n        (void)mbx_irq_status();\n', '', path='srp/srp_mbx.c', suite='test_acmp_mbx.cpp'),
    Defect('code-send-extra-read@srp_app', '*', '    if (mbx_tx_send(MBX_CH_SRP,m->owed_if,m->owed_frame,m->owed_len) != MBX_STATUS_OK) {', '    (void)mbx_irq_status();\n    if (mbx_tx_send(MBX_CH_SRP,m->owed_if,m->owed_frame,m->owed_len) != MBX_STATUS_OK) {', '', path='srp/srp_mbx.c', suite='srp_app.cpp'),
    Defect('code-send-extra-read@test_acmp_mbx', '*', '    if (mbx_tx_send(MBX_CH_SRP,m->owed_if,m->owed_frame,m->owed_len) != MBX_STATUS_OK) {', '    (void)mbx_irq_status();\n    if (mbx_tx_send(MBX_CH_SRP,m->owed_if,m->owed_frame,m->owed_len) != MBX_STATUS_OK) {', '', path='srp/srp_mbx.c', suite='test_acmp_mbx.cpp'),
)
