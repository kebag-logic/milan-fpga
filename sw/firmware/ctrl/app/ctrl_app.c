// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_app.c - the bare-metal composition (see ctrl_app.h).

#include "ctrl_app.h"

#include "shlan_port.h"

// The three runs of slots fit the fabric's timer bank, so no module's own
// check can refuse its first slot.
_Static_assert(CTRL_APP_MAAP_FIRST_SLOT + MBX_N_IF <= MBX_N_TIMERS, "every module needs its own timer slots");

// MAAP on every interface, claiming the entity's talker sources, after F2's
// refusal of a preferred range outside the B.4 pool.
static bool maap_compose(struct ctrl_app *app, const struct ctrl_app_config *cfg)
{
	uint16_t count = cfg->entity->talker_stream_sources;
	uint64_t preferred = cfg->maap_preferred;
	uint64_t mac[MBX_N_IF];
	for (unsigned k = 0; k < MBX_N_IF; ++k) {
		mac[k] = cfg->entity->mac;
	}
	if (preferred != 0u && (preferred < MAAP_POOL_BASE ||
	    preferred > MAAP_POOL_BASE + MAAP_POOL_SIZE - count)) {
		return false;
	}
	return maap_mbx_init(&app->maap, mac, count, CTRL_APP_MAAP_FIRST_SLOT, cfg->maap_allocation, cfg->maap_ctx) &&
	       maap_mbx_attach(&app->maap, &app->loop);
}

bool ctrl_app_compose(struct ctrl_app *app, const struct ctrl_app_config *cfg)
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
	// ACMP stands in front of ADP's binding of the adp channel, so it comes
	// after it
	if (cfg->acmp != NULL &&
	    (!acmp_mbx_init(&app->acmp, cfg->acmp, cfg->acmp_env, CTRL_APP_ACMP_FIRST_SLOT) ||
	     !acmp_mbx_attach(&app->acmp, &app->loop))) {
		return false;
	}
	return cfg->maap_allocation == NULL || maap_compose(app, cfg);
}

bool ctrl_app_open(struct ctrl_app *app, const struct ctrl_app_config *cfg)
{
	// ADP sends the entity's one MAC on every interface (adp.c), so it is
	// every interface's own unicast address
	uint64_t own_mac[MBX_N_IF];
	for (unsigned i = 0; i < MBX_N_IF; ++i) {
		own_mac[i] = cfg->entity->mac;
	}
	if (!ctrl_loop_open(&app->loop, cfg->entity->entity_id, own_mac)) {
		return false;
	}
	// the bindings the store restored between compose and open, into the
	// adp channel's bound-talker table, before any protocol starts
	if (cfg->acmp != NULL) {
		acmp_mbx_open(&app->acmp);
	}
	adp_mbx_set_enable(&app->adp, true);
	// MAAP reads each interface's link and begins once the channels are open
	// (maap_mbx.h); compose refused a preferred range it would refuse
	if (cfg->maap_allocation != NULL) {
		(void)maap_mbx_start(&app->maap, cfg->maap_preferred);
	}
	return true;
}

bool ctrl_app_start(struct ctrl_app *app, const struct ctrl_app_config *cfg)
{
	return ctrl_app_compose(app, cfg) && ctrl_app_open(app, cfg);
}

bool ctrl_app_start_maap(struct ctrl_app *app, const struct ctrl_app_config *cfg,
			 maap_allocation_fn allocation, void *ctx, uint64_t preferred)
{
	struct ctrl_app_config with = *cfg;
	with.maap_allocation = allocation;
	with.maap_ctx = ctx;
	with.maap_preferred = preferred;
	return allocation != NULL && ctrl_app_start(app, &with);
}
