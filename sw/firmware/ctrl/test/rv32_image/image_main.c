// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// image_main.c - the control-plane firmware composed as a Mark II platform
// composes it, linked only to measure it (ctrl_image.py; #665 acceptance
// addition 6030870481). It is test equipment: no shipped image is built from
// it, and nothing here runs on a bench.
//
// It declares what a platform declares statically (the app, the pool's arena,
// the entity, the ACMP configuration of the shape's entity model) and runs the
// boot order of ctrl/README.md: ctrl_app_compose(), the binding owner on lane
// F1's store over the LiteSPI port (acmp_nvm.h), nvm_store_boot(), the store's
// centisecond service, ctrl_app_open(), then the loop. The owners the
// integrator supplies (the lock, the sources, SRP, the notifier and every
// saved-state group but the bindings) are stubs that do nothing, so the
// measure is the composition's and not theirs.
//
// A tree whose ctrl_app composes no ACMP (CTRL_APP_ACMP_FIRST_SLOT absent:
// the base before lane F3) links the same platform without ACMP: the store's
// port is the integrator's owners directly, and the app composes and opens in
// one call (ctrl_app_start), so the store boots before it.

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#include "ctrl_app.h"
#include "nvm_flash_litespi.h"
#include "nvm_klj2.h"
#include "nvm_state.h"
#include "nvm_store.h"

#ifdef CTRL_APP_ACMP_FIRST_SLOT
#include "acmp_nvm.h"
#endif

#ifndef IMAGE_SINKS
#error "IMAGE_SINKS: the shape's STREAM_INPUTs (ctrl_image.py)"
#endif
#ifndef IMAGE_SOURCES
#error "IMAGE_SOURCES: the shape's STREAM_OUTPUTs (ctrl_image.py)"
#endif

// lwSRP's pool: F4 sizes it; until then the host tests' one class.
static const struct ctrl_pool_class classes[] = {{32u, 8u}};
static max_align_t arena[(32u * 8u + sizeof(max_align_t) - 1u) / sizeof(max_align_t)];

static const struct adp_entity entity = {
	0x001B92FFFE000001ull, 0x001B920000000001ull, 0x001B92000001ull, 0x0000C588u,
	IMAGE_SOURCES, 0x4801u, IMAGE_SINKS, 0x4801u, 0u,
};

static struct ctrl_app app;

// ---- the integrator's owners, as stubs ---------------------------------------------

static int model_ready(void *ctx)
{
	(void)ctx;
	return 1;
}

static enum nvm_apply apply(void *ctx, unsigned int group, unsigned int index, const uint8_t *payload,
			    unsigned int len)
{
	(void)ctx;
	(void)group;
	(void)index;
	(void)payload;
	(void)len;
	return NVM_APPLIED;
}

static enum nvm_apply settle(void *ctx)
{
	(void)ctx;
	return NVM_APPLIED;
}

static int rollback(void *ctx, enum nvm_walk walk)
{
	(void)ctx;
	(void)walk;
	return 0;
}

static int latch(void *ctx, unsigned int group, unsigned int index, uint8_t *payload, unsigned int len)
{
	(void)ctx;
	(void)group;
	(void)index;
	(void)payload;
	(void)len;
	return 0;
}

static void release(void *ctx)
{
	(void)ctx;
}

static const struct nvm_state others = {model_ready, apply, settle, rollback, latch, release, NULL};

#ifdef CTRL_APP_ACMP_FIRST_SLOT
static bool locked(void *ctx, uint64_t *controller)
{
	(void)ctx;
	*controller = 0u;
	return false;
}

static void source(void *ctx, unsigned index, struct acmp_source_state *out)
{
	(void)ctx;
	(void)index;
	out->dest_mac_valid = false;
}

static void srp(void *ctx, unsigned sink, const struct acmp_stream *stream)
{
	(void)ctx;
	(void)sink;
	(void)stream;
}

static void persist(void *ctx, unsigned sink)
{
	(void)ctx;
	nvm_store_changed(NVM_G_BIND, sink);
}

static void changed(void *ctx, unsigned sink)
{
	(void)ctx;
	(void)sink;
}

static const struct acmp_env env = {NULL, locked, source, srp, persist, changed};
static struct acmp_config acmp_cfg;
static struct acmp_nvm binding_owner;
#endif

static void halt(void)
{
	for (;;) {
	}
}

int main(void)
{
	struct ctrl_app_config cfg = {
		.entity = &entity, .arena = arena, .arena_bytes = sizeof arena, .classes = classes, .n_classes = 1u,
#ifdef CTRL_APP_ACMP_FIRST_SLOT
		.acmp = &acmp_cfg, .acmp_env = &env,
#endif
	};
	nvm_flash_litespi_power_on();
#ifdef CTRL_APP_ACMP_FIRST_SLOT
	acmp_cfg.entity_id = entity.entity_id;
	acmp_cfg.n_interfaces = 1u;
	acmp_cfg.mac[0] = entity.mac;
	acmp_cfg.n_sinks = IMAGE_SINKS;
	acmp_cfg.n_sources = IMAGE_SOURCES;
	if (!ctrl_app_compose(&app, &cfg)) {
		halt();
	}
	acmp_nvm_init(&binding_owner, &app.acmp.acmp, NVM_G_BIND, &others);
	nvm_store_boot(&nvm_flash_litespi, &binding_owner.port);
	if (!ctrl_loop_add_tick(&app.loop, nvm_store_service) || !ctrl_app_open(&app, &cfg)) {
		halt();
	}
#else
	// the base composes in one call, so its store boots first
	nvm_store_boot(&nvm_flash_litespi, &others);
	if (!ctrl_app_start(&app, &cfg) || !ctrl_loop_add_tick(&app.loop, nvm_store_service)) {
		halt();
	}
#endif
	ctrl_loop_run(&app.loop);
	return 0;
}
