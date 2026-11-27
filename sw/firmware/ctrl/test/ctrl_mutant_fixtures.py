# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exact source fragments used by the control firmware mutation table."""

#: ctrl_app_compose and ctrl_app_open, from the pool's bind to the mailbox's
#: open: the app binds lwSRP's pool before anything reads the mailbox window.
#: The open takes every interface's own MAC; boot composes ADP, ACMP and MAAP before opening (#665).
APP_BRING = ("\tshlan_port_bind_pool(&app->pool);\n\tctrl_debug_bind(cfg->sink, cfg->sink_ctx);\n"
             "\tctrl_loop_init(&app->loop);\n"
             "\tif (!adp_mbx_init(&app->adp, cfg->entity, CTRL_APP_ADP_FIRST_SLOT, "
             "cfg->current_configuration_index) ||\n"
             "\t    !adp_mbx_attach(&app->adp, &app->loop)) {\n\t\treturn false;\n\t}\n"
             "\t// ACMP stands in front of ADP's binding of the adp channel, so it comes\n"
             "\t// after it\n"
             "\tif (cfg->acmp != NULL &&\n"
             "\t    (!acmp_mbx_init(&app->acmp, cfg->acmp, cfg->acmp_env, CTRL_APP_ACMP_FIRST_SLOT) ||\n"
             "\t     !acmp_mbx_attach(&app->acmp, &app->loop))) {\n\t\treturn false;\n\t}\n"
             "\treturn cfg->maap_allocation == NULL || maap_compose(app, cfg);\n"
             "}\n\n"
             "bool ctrl_app_open(struct ctrl_app *app, const struct ctrl_app_config *cfg)\n{\n"
             "\t// ADP sends the entity's one MAC on every interface (adp.c), so it is\n"
             "\t// every interface's own unicast address\n"
             "\tuint64_t own_mac[MBX_N_IF];\n"
             "\tfor (unsigned i = 0; i < MBX_N_IF; ++i) {\n\t\town_mac[i] = cfg->entity->mac;\n\t}\n"
             "\tif (!ctrl_loop_open(&app->loop, cfg->entity->entity_id, own_mac)) {\n\t\treturn false;\n\t}\n")

#: The model's classifier entry, and the same with a front end that strips an
#: 802.1Q C-tag before it (#665, NFR-SCOUT-08).
MODEL_CLASSIFY = "\tbool mismatch = false;\n\tint found = classify(m, frame, len, interface, &mismatch);\n"
MODEL_CLASSIFY_UNTAGGED = ("\tuint8_t stripped[MBX_FRAME_BYTES_MAX + 4u];\n"
                           "\tif (len > 16u && len <= sizeof stripped && wire_be16(frame + 12u) == 0x8100u) {\n"
                           "\t\tmemcpy(stripped, frame, 12u);\n\t\tmemcpy(stripped + 12u, frame + 16u, len - 16u);\n"
                           "\t\tframe = stripped;\n\t\tlen -= 4u;\n\t}\n" + MODEL_CLASSIFY)

#: ctrl_loop_open's identities and channel opening, and the same with the own
#: MACs written only once the channels are open.
LOOP_OWN_MAC = ("\tfor (unsigned i = 0; i < MBX_N_IF; ++i) {\n"
                "\t\t(void)mbx_filter_set_own_mac(i, own_mac[i]);    // every i is an interface of the contract\n"
                "\t}\n")
LOOP_OPEN = ("\tmbx_irq_enable(mbx_place(open, MBX_IRQ_ENABLE_RX_LSB, MBX_IRQ_ENABLE_RX_WIDTH) |\n"
             "\t\t       mbx_place(1u, MBX_IRQ_ENABLE_EVT_LSB, MBX_IRQ_ENABLE_EVT_WIDTH));\n"
             "\tmbx_tick_enable(l->n_ticks > 0u);\n\tmbx_filter_open(open);\n")

#: ctrl_loop_service's polls and THE STEP after them.
#: The model arm's test of one suite group.
MODEL_GROUP = "Suite/MbxModelGroup.PassesOnTheModel/"
#: The room the driver reads TX_TAIL for, once the room the last read showed runs short.
TX_ROOM = ("\t\tt->tail = counter(ch_reg(ch, MBX_CH_REG_TX_TAIL));\n\t\tused = (uint16_t)(head - t->tail);\n"
           "\t\tif (used > words || record > words - used) {\n")
#: The same with the pool bound only once the mailbox is open.
APP_BRING_LATE = APP_BRING.removeprefix("\tshlan_port_bind_pool(&app->pool);\n") + \
    "\tshlan_port_bind_pool(&app->pool);\n"
