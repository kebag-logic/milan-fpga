// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_app.c - the bare-metal composition (see ctrl_app.h).

#include "ctrl_app.h"

#include "mbx_wire.h"
#include "shlan_port.h"

bool ctrl_app_start(struct ctrl_app *app, const struct ctrl_app_config *cfg)
{
	if (!ctrl_pool_init(&app->pool, cfg->arena, cfg->arena_bytes, cfg->classes, cfg->n_classes)) {
		return false;
	}
	shlan_port_bind_pool(&app->pool);
	ctrl_debug_bind(cfg->sink, cfg->sink_ctx);
	ctrl_loop_init(&app->loop);
	if (!adp_mbx_init(&app->adp, cfg->entity, CTRL_APP_ADP_FIRST_SLOT, cfg->current_configuration_index) ||
	    !adp_mbx_attach(&app->adp, &app->loop)) {
		return false;
	}
	// ADP sends the entity's one MAC on every interface (adp.c), so it is
	// every interface's own unicast address
	uint64_t own_mac[MBX_N_IF];
	for (unsigned i = 0; i < MBX_N_IF; ++i) {
		own_mac[i] = cfg->entity->mac;
	}
	if (!ctrl_loop_open(&app->loop, cfg->entity->entity_id, own_mac)) {
		return false;
	}
	adp_mbx_set_enable(&app->adp, true);
	return true;
}

bool ctrl_app_start_maap(struct ctrl_app *app, const struct ctrl_app_config *cfg,
			 maap_allocation_fn allocation, void *ctx, uint64_t preferred)
{
	uint16_t count = cfg->entity->talker_stream_sources;
	uint64_t mac[MBX_N_IF];
	for (unsigned k = 0; k < MBX_N_IF; ++k) {
		mac[k] = cfg->entity->mac;
	}
	if (preferred != 0u && (preferred < MAAP_POOL_BASE ||
	    preferred > MAAP_POOL_BASE + MAAP_POOL_SIZE - count)) {
		return false;
	}
	if (!maap_mbx_init(&app->maap, mac, count, MBX_N_IF, allocation, ctx) ||
	    !ctrl_app_start(app, cfg)) {
		return false;
	}
	// F0 just initialized the tables and bound one sink and one poll.
	(void)maap_mbx_attach(&app->maap, &app->loop);
	(void)maap_mbx_start(&app->maap, preferred);
	uint32_t channels = (1u << MBX_CH_ADP) | (1u << MBX_CH_MAAP);
	mbx_irq_enable(mbx_place(channels, MBX_IRQ_ENABLE_RX_LSB, MBX_IRQ_ENABLE_RX_WIDTH) |
		       mbx_place(1u, MBX_IRQ_ENABLE_EVT_LSB, MBX_IRQ_ENABLE_EVT_WIDTH));
	mbx_filter_open(channels);
	return true;
}
