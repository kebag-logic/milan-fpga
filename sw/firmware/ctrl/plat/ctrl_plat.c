// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_plat.c - the split placement's control firmware on its target (see
// ctrl_plat.h). The pools are sized by the generated shape: aecp_entity_gen.h
// (the AEM image), adp_entity_gen.h (the entity) and srp_entity_gen.h (the
// stream counts, force-included as SRP requires).

#include "ctrl_plat.h"

#include <string.h>

#include "acmp_nvm.h"
#include "adp_entity_gen.h"
#include "aecp_entity_gen.h"
#include "aecp_image.h"
#include "ctrl_plat_io.h"
#include "mbx_hal.h"
#include "nvm_store.h"
#include "wire.h"

struct ctrl_plat ctrl_plat;

static const struct adp_entity entity = ADP_ENTITY_GEN_INIT;
_Alignas(max_align_t) static unsigned char arena[SRP_POOL_ARENA_BYTES];
static struct aecp_model model;
static struct aecp_descriptor descriptors[AECP_ENTITY_DESCRIPTORS];
static uint8_t values[AECP_ENTITY_VALUE_BYTES];
static struct aecp_event events[AECP_ENTITY_DESCRIPTORS];
static uint32_t latency[AECP_ENTITY_OUTPUTS];
static struct aecp_mapping map_rows[AECP_ENTITY_MAP_ROWS];
static struct aecp_mapping map_scratch[AECP_ENTITY_MAP_MAX];
static struct aecp_map maps[AECP_ENTITY_MAPS] = AECP_ENTITY_MAPS_INIT(map_rows);
static const struct aecp_value names[AECP_ENTITY_NAMES] = AECP_ENTITY_NAMES_INIT;

_Static_assert(CTRL_SRP_SOURCES <= ACMP_MAX_SOURCES && CTRL_SRP_SINKS <= ACMP_MAX_SINKS,
	       "the generated stream counts fit ACMP");

void ctrl_plat_generated_image(struct ctrl_plat_env *env)
{
	env->aem = aecp_entity_image;
	env->aem_bytes = sizeof aecp_entity_image;
	env->aem_crc = AECP_ENTITY_CRC;
}

// ---- MAAP's allocation port on the datapath CSR window --------------------

static uint32_t window_read(void *ctx, unsigned interface, uint32_t offset)
{
	struct ctrl_plat *p = ctx;
	// the datapath has one stream window, interface 0's (ctrl_plat.h)
	return interface == 0u ? ctrl_plat_io_read32(p->env->csr + offset) : 0u;
}

static void window_write(void *ctx, unsigned interface, uint32_t offset, uint32_t value)
{
	struct ctrl_plat *p = ctx;
	if (interface == 0u) {
		ctrl_plat_io_write32(p->env->csr + offset, value);
	} else {
		++p->csr_dropped;
	}
}

// maap_allocation_fn: the window first, then the allocation ACMP's source
// port reports, so no source reports an address the window does not hold
static void allocation(void *ctx, unsigned interface, uint64_t base, uint16_t count, bool valid)
{
	struct ctrl_plat *p = ctx;
	maap_csr_allocation(&p->maap_csr, interface, base, count, valid);
	p->allocation[interface] = (struct ctrl_plat_allocation){base, count, valid};
}

// ---- the platform's ACMP owner (the innermost acmp_env) --------------------

// STREAM_OUTPUT n's stream_id: the entity's MAC and the output's unique ID
// (IEEE 1722.1-2021 7.2.3, the STREAM_OUTPUT's stream_id)
static uint64_t stream_id(const struct ctrl_plat *p, unsigned n)
{
	return entity.mac << 16 | p->env->streams[n].unique_id;
}

// AECP's lock replaces this one (ctrl_app_aecp.c); it holds no lock of its own
static bool locked(void *ctx, uint64_t *owner)
{
	(void)ctx;
	*owner = 0;
	return false;
}

// Milan v1.2 5.5.4.1: a source's destination is valid once MAAP holds its
// interface's range, address base + n (maap_csr.h)
static void source(void *ctx, unsigned n, struct acmp_source_state *out)
{
	struct ctrl_plat *p = ctx;
	const struct ctrl_plat_allocation *a = &p->allocation[p->acmp.source_interface[n]];
	out->dest_mac_valid = a->valid && n < a->count;
	out->stream = (struct acmp_stream){stream_id(p, n), a->base + n, (uint16_t)p->env->policy->sr_vid};
	out->asking_failed = false;
}

// SRP's request, persistence and change notices are the wrappers' (the SRP
// delivery, the AECP bridge); the platform keeps no state for them
static void stream(void *ctx, unsigned n, const struct acmp_stream *value)
{
	(void)ctx;
	(void)n;
	(void)value;
}

static void notice(void *ctx, unsigned n)
{
	(void)ctx;
	(void)n;
}

// ---- AECP's platform observations -----------------------------------------

// the loop's millisecond clock, which every module's timers already read
static uint32_t random_value(void *ctx)
{
	(void)ctx;
	return mbx_now_ms();
}

// GET_AS_PATH has no split source at this base: an explicit unavailable answer
static bool path(void *ctx, unsigned interface, uint16_t index, uint64_t *v, size_t cap, size_t *count)
{
	(void)ctx;
	(void)interface;
	(void)index;
	(void)v;
	(void)cap;
	(void)count;
	return false;
}

// ---- SRP -------------------------------------------------------------------

static void licence(void *ctx, unsigned interface, unsigned n, bool active)
{
	struct ctrl_plat *p = ctx;
	p->licences[interface] = active ? p->licences[interface] | 1u << n : p->licences[interface] & ~(1u << n);
}

// Every interface declares every source: its stream from the generated table,
// on the entity's VID; unallocated until MAAP's range is in force
static void configure_sources(struct ctrl_plat *p)
{
	for (unsigned i = 0; i < MBX_N_IF; ++i) {
		p->srp_config.mac[i] = entity.mac;
		p->srp_config.sources[i] = p->sources[i];
		for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
			const struct ctrl_plat_stream *s = &p->env->streams[n];
			struct msrp_talker_adv *v = &p->sources[i][n].value;
			wire_put_be(v->stream_id.bytes, stream_id(p, n), 8);
			v->vlan_id = (uint16_t)p->env->policy->sr_vid;
			v->max_frame_size = s->max_frame_size;
			v->max_interval_frames = s->max_interval_frames;
			v->priority_and_rank = s->priority_and_rank;
		}
	}
	p->srp_config.link_rate_bps = p->env->link_rate_bps;
	p->srp_config.licence = licence;
	p->srp_config.ctx = p;
}

// ---- the REBOOT (ctrl_plat.h) ----------------------------------------------

// ADP's ring has handed every frame committed to it to the datapath
static bool adp_drained(void)
{
	const uint32_t ch = MBX_CH_BASE + MBX_CH_ADP * MBX_CH_STRIDE;
	return (uint16_t)mbx_hal_read32(ch + MBX_CH_REG_TX_TAIL) == (uint16_t)mbx_hal_read32(ch + MBX_CH_REG_TX_HEAD);
}

// Once the REBOOT's frames are out, ADP's SHUTDOWN; once its ENTITY_DEPARTINGs
// are out too, the reset port (IEEE 1722.1-2021 7.4.43; Milan v1.2 5.6.3.3).
// The loop, and so this poll, runs only until the port fires (ctrl_plat_step).
static bool reboot_step(struct ctrl_plat *p)
{
	if (p->reboot == 0u) {
		if (!aecp_reboot_due(&p->aecp.core)) {
			return false;
		}
		adp_mbx_set_enable(&p->app.adp, false);
		p->reboot = 1u;
		return true;
	}
	for (unsigned i = 0; i < MBX_N_IF; ++i) {
		if (p->app.adp.ifs[i].adp.departing_owed != 0u) {
			return true;
		}
	}
	if (!adp_drained()) {
		return true;
	}
	ctrl_plat_io_write32(p->env->reboot, 1u);
	p->reboot = 2u;
	return false;
}

// The console's poll, which also runs the REBOOT's sequence
static bool poll(void *ctx)
{
	struct ctrl_plat *p = ctx;
	bool owed = ctrl_plat_console_poll(&p->console);
	return reboot_step(p) || owed;
}

// ---- the boot --------------------------------------------------------------

static enum ctrl_plat_stage reach(struct ctrl_plat *p, enum ctrl_plat_stage stage, const char *line)
{
	ctrl_plat_console_puts(&p->console, line);
	p->stage = stage;
	return stage;
}

// After steps 2-3, the one MAAP owner: the allocation port's invalid report
// clears the fabric allocator's enable and the talkers' admission before the
// core's MAAP starts (maap_csr.c)
static bool maap_owner(struct ctrl_plat *p)
{
	const struct ctrl_plat_env *env = p->env;
	struct maap_csr_port port = {p, window_read, window_write};
	if (!maap_csr_init(&p->maap_csr, port, env->aaf_outputs, env->crf_output, env->policy->aaf_ctrl,
			   env->policy->crf_tx_ctrl)) {
		return false;
	}
	for (unsigned i = 0; i < MBX_N_IF; ++i) {
		allocation(p, i, 0, 0, false);
	}
	return true;
}

// MAAP's preferred first range (ctrl_app.h). The image never defines it, so
// MAAP draws its range (IEEE 1722-2016 B.3.6.1); only a simulation pins it, as
// #665's two-placement comparison requires of both placements
#ifndef CTRL_PLAT_MAAP_PREFERRED
#define CTRL_PLAT_MAAP_PREFERRED 0u
#endif

// Step 5: the application, AECP and its face, bound into one loop
static bool compose(struct ctrl_plat *p)
{
	p->acmp = (struct acmp_config){.entity_id = entity.entity_id, .n_interfaces = MBX_N_IF,
		.n_sinks = CTRL_SRP_SINKS, .n_sources = CTRL_SRP_SOURCES};
	for (unsigned i = 0; i < MBX_N_IF; ++i) {
		p->acmp.mac[i] = entity.mac;
		p->aecp_config.mac[i] = entity.mac;
	}
	for (unsigned n = 0; n < CTRL_SRP_SINKS; ++n) {
		p->acmp.sink_interface[n] = (uint8_t)(n % MBX_N_IF);
	}
	for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
		p->acmp.source_interface[n] = (uint8_t)(n % MBX_N_IF);
	}
	p->acmp_env = (struct acmp_env){p, locked, source, stream, notice, notice};
	p->config = (struct ctrl_app_config){.entity = &entity, .arena = arena, .arena_bytes = sizeof arena,
		.classes = srp_pool_classes, .n_classes = SRP_POOL_N_CLASSES, .acmp = &p->acmp,
		.acmp_env = &p->acmp_env, .maap_allocation = allocation, .maap_ctx = p,
		.maap_preferred = CTRL_PLAT_MAAP_PREFERRED};
	p->aecp_config.entity_id = entity.entity_id;
	p->aecp_config.interfaces = MBX_N_IF;
	p->aecp_config.model = &model;
	p->aecp_config.maps = maps;
	p->aecp_config.map_count = AECP_ENTITY_MAPS;
	p->aecp_config.events = events;
	p->aecp_config.latency = latency;
	p->aecp_config.reboot = p->env->reboot != 0u;
	p->aecp_platform = (struct aecp_ports){.random = random_value, .path = path};
	aecp_face_init(&p->face, &p->aecp_platform);
	return ctrl_app_compose(&p->app, &p->config) &&
	       ctrl_app_compose_aecp(&p->app, &p->bridge, &p->aecp, &p->aecp_config, &p->face.ports, &p->state) &&
	       ctrl_app_aecp_attach_face(&p->bridge, &p->face);
}

enum ctrl_plat_stage ctrl_plat_boot(const struct ctrl_plat_env *env)
{
	struct ctrl_plat *p = &ctrl_plat;
	memset(p, 0, sizeof *p);
	p->env = env;
	ctrl_plat_console_init(&p->console, &env->uart, env->csr);
	ctrl_plat_console_puts(&p->console, CTRL_PLAT_BANNER);
	if (!ctrl_plat_csr_identity(env->csr, &p->version)) {
		return reach(p, CTRL_PLAT_IDENTITY, "Milan split: CSR identity mismatch; fabric remains disabled\r\n");
	}
	ctrl_plat_csr_policy(env->csr, env->policy);
	if (!maap_owner(p)) {
		return reach(p, CTRL_PLAT_COMPOSE, "Milan split: MAAP port refused; entity disabled\r\n");
	}
	p->console.aem_loaded = aecp_image_load(&model, env->aem, env->aem_bytes, env->aem_crc, descriptors,
						AECP_ENTITY_DESCRIPTORS, values, sizeof values);
	if (!p->console.aem_loaded) {
		return reach(p, CTRL_PLAT_IMAGE, "Milan split: AEM image refused; entity disabled\r\n");
	}
	if (!compose(p)) {
		return reach(p, CTRL_PLAT_COMPOSE, "Milan split: composition refused; entity disabled\r\n");
	}
	// The console's poll, before SRP's two. It is refused only by a full table,
	// and ctrl_app_attach_srp below refuses unless two more slots are free, so
	// a composition that leaves the console no slot stops at SRP, by name
	(void)ctrl_loop_add_poll(&p->app.loop, poll, p);
	// Steps 6-7: the saved state, bindings first, before anything opens. The
	// store's service is the loop's first centisecond consumer, bound before
	// the open (acmp_nvm.h), so its table of CTRL_LOOP_MAX_TICKS has room
	aecp_nvm_init(&p->state, &p->aecp.core, names, AECP_ENTITY_NAMES, map_scratch, AECP_ENTITY_MAP_MAX);
	acmp_nvm_init(&p->binding, &p->app.acmp.acmp, NVM_G_BIND, &p->state.port);
	nvm_store_boot(env->flash, &p->binding.port);
	(void)ctrl_loop_add_tick(&p->app.loop, nvm_store_service);
	if (!ctrl_app_open_held(&p->app, &p->config)) {
		return reach(p, CTRL_PLAT_MAILBOX, "Milan split: mailbox contract mismatch; entity disabled\r\n");
	}
	configure_sources(p);
	if (!srp_mbx_init(&p->srp, &p->srp_config) || !ctrl_app_attach_srp(&p->app, &p->srp)) {
		return reach(p, CTRL_PLAT_SRP, "Milan split: SRP refused; entity disabled\r\n");
	}
	// Step 8: AECP only at an accepted terminal, its face acknowledged
	if (!ctrl_app_open_aecp(&p->bridge)) {
		return reach(p, CTRL_PLAT_AECP, "Milan split: AECP not released; entity disabled\r\n");
	}
	// Step 9: ADP last, once AECP and ACMP accept requests
	ctrl_app_release_adp(&p->app);
	return reach(p, CTRL_PLAT_READY, CTRL_PLAT_READY_LINE);
}

// Once the reset port has fired, the store alone, on the loop's centisecond,
// and its F_NVM, which the drain reads. No frame or event is taken, so nothing
// becomes dirty and no journal write starts during the PHY hold, when the
// reload may read the flash (docs/design/REBOOT_RESET.md section 4; #871).
static void quiet(struct ctrl_plat *p)
{
	const uint32_t now = mbx_now_ms();
	if ((uint32_t)(now - p->quiet_ms) >= 10u) {
		p->quiet_ms = now;
		nvm_store_service();
	}
	uint32_t restore = 0;
	uint32_t nvm = 0;
	bool dirty = false;
	ctrl_app_aecp_store_words(nvm_store_status(), &restore, &nvm, &dirty);
	aecp_face_status(&p->face, restore, nvm, dirty);
	(void)aecp_face_poll(&p->face);
	(void)ctrl_plat_console_poll(&p->console);
}

void ctrl_plat_step(void)
{
	if (ctrl_plat.stage != CTRL_PLAT_READY) {
		(void)ctrl_plat_console_poll(&ctrl_plat.console);
	} else if (ctrl_plat.reboot == 2u) {
		quiet(&ctrl_plat);
	} else {
		ctrl_loop_step(&ctrl_plat.app.loop);
	}
}
