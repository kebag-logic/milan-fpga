# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""aecp_notice_mutants.py - the AECP campaign's planted defects in a STREAM_OUTPUT's GET_STREAM_INFO notice from SRP's
record of a changed Talker declaration (#936; Milan v1.2 5.4.5.2, Table 5.22): the composition's AECP bridge
(ctrl_app_aecp.c) and the SRP delivery's owed report (ctrl_app_srp.c; ctrl_loop.h, the polls). aecp_mutants.py
plants each row; every named check must fail on its own words."""

ROWS = (
    # #936: SRP's record of a changed Talker declaration is its STREAM_OUTPUT's GET_STREAM_INFO notice (Milan v1.2
    # 5.4.5.2, Table 5.22): dropped, raised for a STREAM_INPUT, raised for the next source, or never cleared
    ('app-output-notice-dropped', 'app/ctrl_app_aecp.c',
           '\t\t\t\taecp_changed(&c->aecp->core, 6, n, 1u);\n',
           '\t\t\t\t(void)n;\n',
           ('App.SrpDeclarationChangeIsItsStreamOutputsNotice',
            "a declaration changed notifies its STREAM_OUTPUT's GET_STREAM_INFO to every registered controller")),
    ('app-output-notice-as-an-input', 'app/ctrl_app_aecp.c',
           '\t\t\t\taecp_changed(&c->aecp->core, 6, n, 1u);\n',
           '\t\t\t\taecp_changed(&c->aecp->core, 5, n, 1u);\n',
           ('App.SrpDeclarationChangeIsItsStreamOutputsNotice',
            "a declaration changed notifies its STREAM_OUTPUT's GET_STREAM_INFO to every registered controller")),
    ('app-output-notice-next-source', 'app/ctrl_app_aecp.c',
           '\t\t\t\taecp_changed(&c->aecp->core, 6, n, 1u);\n',
           '\t\t\t\taecp_changed(&c->aecp->core, 6, (uint16_t)(n + 1u), 1u);\n',
           ('App.SrpDeclarationChangeIsItsStreamOutputsNotice',
            'a source the record does not name is notified nothing')),
    ('app-output-notice-kept', 'app/ctrl_app_aecp.c',
           '\t\tc->app->srp_noticed = 0u;\n',
           '\t\t(void)c;\n',
           ('App.SrpDeclarationChangeIsItsStreamOutputsNotice',
            'the bridge raises every STREAM_OUTPUT the delivery took')),
    # #936 (ctrl_loop.h, the polls): the SRP delivery's pass that takes the record reports nothing owed, so the loop
    # may sleep with the STREAM_OUTPUT's notice unsent
    ('app-output-notice-owed-unreported', 'app/ctrl_app_srp.c',
           '    bool pending = noticed;\n',
           '    bool pending = false;\n    (void)noticed;\n',
           ('App.NoPassIsIdleWhileAStreamOutputsNoticeIsOwed',
            "no pass is idle while a STREAM_OUTPUT's notice is owed")),
)
