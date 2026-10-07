// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_app.c - the bare-metal composition (see ctrl_app.h).

#include "ctrl_app.h"

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
