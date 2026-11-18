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
#if AECP_MBX_OWED_SLOTS != 0u
static struct aecp_owed owed[AECP_MBX_OWED_SLOTS];
#endif
static struct aecp_mapping map_rows[AECP_ENTITY_MAP_ROWS];
static struct aecp_mapping map_scratch[AECP_ENTITY_MAP_MAX];
static struct aecp_map maps[AECP_ENTITY_MAPS] = AECP_ENTITY_MAPS_INIT(map_rows);
static const struct aecp_name_run names[AECP_ENTITY_NAME_RUNS] = AECP_ENTITY_NAME_RUNS_INIT;

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

// the loop's millisecond clock, which every module's timers already read.
// GET_AS_PATH is the face's, through the datapath's GSI window (aecp_face.h; #897)
static uint32_t random_value(void *ctx)
{
	(void)ctx;
	return mbx_now_ms();
}

// ---- the receive monitor's formats on the datapath CSR window (#946) -------
//
// The monitor judges every PDU of a stream above 0 against its context's
// format words, which nothing but this window writes, and a PDU not in them is
// UNSUPPORTED_FORMAT and discarded (Milan v1.2 Table 5.6, 4.4.2.2). So each
// AAF STREAM_INPUT above 0 (ctrl_plat_csr_sink_context) holds the current
// format in force, the one a controller reads (aecp_face.h, applied): written
// after the open's acknowledged publication, and then by each change the core
// keeps, in the change itself, before the core answers it. The core keeps a
// change the face applied at once, and one it does again after IN_PROGRESS;
// one it undoes leaves the values the contexts already hold.
//
// A context's format moves only while its input is unbound. SET_STREAM_FORMAT
// and SET_CONFIGURATION refuse a bound input (STREAM_IS_RUNNING), and a change
// that waits is not applied while an input whose context it moves is bound:
// one bound meanwhile leaves it undone, and the core keeps the values in force
// and answers ENTITY_MISBEHAVING at AECP_WAIT_MS (aecp.h, applied; IEEE
// 1722.1-2021 7.4.9). A stream reaches a context only once its binding's
// stream_id is published, after the probe, so whenever one is published its
// context holds the current format.

#define STREAM_INPUT 5u  // IEEE 1722.1-2021 Table 7-1

// The face's change and applied ports this wraps, and whether the core is
// doing a waiting change again: the applied port found it applied
static struct {
	void (*changed)(void *, enum aecp_change, uint16_t, uint16_t);
	bool (*applied)(void *);
	bool redo;
} sinks;

// Whether descriptor d has a context of its own in the configuration in
// force, and its current format
static bool sink_context(const struct aecp_descriptor *d, uint64_t *format)
{
	return ctrl_plat_csr_sink_context(d->value, d->length, d->configuration, ctrl_plat.aecp.core.configuration,
					  format);
}

// The model's STREAM_INPUTs with a context take their current format there:
// every one (SINK_ALL), or the one of descriptor index `only`.
#define SINK_ALL 0x10000u
static void sink_write(uint32_t only)
{
	const struct aecp_model *m = ctrl_plat.aecp.core.cfg.model;
	for (size_t n = 0; n < m->count; ++n) {
		const struct aecp_descriptor *d = &m->descriptors[n];
		uint64_t format = 0;
		if ((only == SINK_ALL || d->index == only) && sink_context(d, &format)) {
			ctrl_plat_csr_sink_format(ctrl_plat.env->csr, d->index, format);
		}
	}
}

// Whether the change the core holds undone may move the context of a bound
// input: that input's format (SET_STREAM_FORMAT), or every input's
// (SET_CONFIGURATION, which refuses any bound input, aecp_commands.c)
static bool sink_held(const struct aecp *core)
{
	const struct aecp_model *m = core->cfg.model;
	bool every = core->noted == AECP_CHANGE_CONFIGURATION;
	bool one = core->noted == AECP_CHANGE_FORMAT && core->noted_type == STREAM_INPUT;
	bool bound = false;
	for (size_t n = 0; n < m->count; ++n) {
		const struct aecp_descriptor *d = &m->descriptors[n];
		uint64_t format = 0;
		if ((every || (one && d->index == core->noted_index)) && sink_context(d, &format)) {
			// an input with a context is one of ACMP's sinks: the generated shape's
			struct acmp_sink_view v = {0};
			(void)acmp_view(&ctrl_plat.app.acmp.acmp, d->index, &v);
			bound |= v.bound;
		}
	}
	return bound;
}

// The face's applied port, wrapped: a waiting change that would move a bound
// input's context is not applied. Applied, the core does it again at once,
// before any other port (aecp.c, the waiting command)
static bool sink_applied(void *ctx)
{
	const struct aecp *core = &ctrl_plat.aecp.core;
	bool applied = sinks.applied(ctx) && !(core->waiting && sink_held(core));
	sinks.redo = applied && core->waiting;
	return applied;
}

// The face's change port, wrapped: a change the core keeps, one done again or
// one the face applied (else the core waits, the change undone), moves its
// contexts now: an input's format its own, a configuration every one
static void sink_changed(void *ctx, enum aecp_change kind, uint16_t type, uint16_t index)
{
	bool redo = sinks.redo;
	sinks.redo = false;
	sinks.changed(ctx, kind, type, index);
	if (redo || sinks.applied(ctx)) {
		if (kind == AECP_CHANGE_FORMAT && type == STREAM_INPUT) {
			sink_write(index);
		} else if (kind == AECP_CHANGE_CONFIGURATION) {
			sink_write(SINK_ALL);
		}
	}
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
#if AECP_MBX_OWED_SLOTS != 0u
	p->aecp_config.owed = owed;
	p->aecp_config.owed_slots = AECP_MBX_OWED_SLOTS;
	p->aecp_config.queue = &aecp_owed_queue;
#endif
	p->aecp_platform = (struct aecp_ports){.random = random_value};
	aecp_face_init(&p->face, &p->aecp_platform);
	// the receive monitor's formats follow the face's changes (#946)
	sinks.changed = p->face.ports.changed;
	sinks.applied = p->face.ports.applied;
	sinks.redo = false;
	p->face.ports.changed = sink_changed;
	p->face.ports.applied = sink_applied;
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
	(void)ctrl_loop_add_poll(&p->app.loop, ctrl_plat_console_poll, &p->console);
	// Steps 6-7: the saved state, bindings first, before anything opens. The
	// store's tick is the loop's first centisecond consumer, bound before the
	// open (acmp_nvm.h), so its table of CTRL_LOOP_MAX_TICKS has room; the
	// step it owes is THE STEP, taken in a pass that took no input and has
	// room (ctrl_loop.h)
	aecp_nvm_init(&p->state, &p->aecp.core, names, AECP_ENTITY_NAME_RUNS, map_scratch, AECP_ENTITY_MAP_MAX);
	acmp_nvm_init(&p->binding, &p->app.acmp.acmp, NVM_G_BIND, &p->state.port);
	nvm_store_boot(env->flash, &p->binding.port);
	(void)ctrl_loop_add_tick(&p->app.loop, nvm_store_tick);
	(void)ctrl_loop_set_step(&p->app.loop, nvm_store_step, NULL, nvm_store_clock, NULL);
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
	// every interface acknowledged the face: each input's format in force, before any stream is bound (#946)
	sink_write(SINK_ALL);
	// Step 9: ADP last, once AECP and ACMP accept requests
	ctrl_app_release_adp(&p->app);
	return reach(p, CTRL_PLAT_READY, CTRL_PLAT_READY_LINE);
}

void ctrl_plat_step(void)
{
	if (ctrl_plat.stage == CTRL_PLAT_READY) {
		ctrl_loop_step(&ctrl_plat.app.loop);
	} else {
		(void)ctrl_plat_console_poll(&ctrl_plat.console);
	}
}
