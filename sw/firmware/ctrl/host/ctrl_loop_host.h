// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// ctrl_loop_host.h - THE HOST PLATFORM's shape (#983): the figures ctrl_loop.h
// states per shape (THE SHAPES), for a build that runs this firmware as a host
// program on the mailbox model (mbx_model.c) at the descriptor-only host
// profile's shape (endstation_builder.py HOST_TARGET, configs/host). Such a
// build defines CTRL_HOST_PLATFORM, which no image of this repository does.
// ctrl_loop.h includes this header in place of THE SHAPES, and only for that
// build at that shape, so the FPGA table and its readers (shape_costs.py) never
// see these rows.
//
// The shape is one interface, one talker source (an AAF STREAM_OUTPUT) and two
// listener sinks (an AAF and a CRF STREAM_INPUT).
// Its figures are a STATED HOST SCHEDULING PROFILE, not a measurement of the
// host. Each is 1x1/1if's, measured on the RV32 at 100 cycles a microsecond
// with one talker source more (the CRF output) over the same two sinks: this
// shape has one SRP Talker declaration fewer to build and one STREAM_OUTPUT
// fewer to notify for. The host platform states that it serves the loop from
// one thread, at a real-time priority below only its time owner's, on a CPU
// that runs this code at least as fast as that RV32, and it holds these
// figures as the loop's budgets on its microsecond clock. Two things are not
// measured by any harness here and are not claimed: the costs that follow the
// descriptor set rather than the streams, and the preemption of that thread,
// on which the millisecond bounds (CTRL_LOOP_QUEUED_MS, CTRL_LOOP_TX_MS) rest.
#ifndef CTRL_LOOP_HOST_H
#define CTRL_LOOP_HOST_H

#if !defined(CTRL_HOST_PLATFORM) || !defined(CTRL_LOOP_SHAPE)
#error "ctrl_loop_host.h: the host platform's shape is for a CTRL_HOST_PLATFORM build, through ctrl_loop.h"
#elif !CTRL_LOOP_SHAPE(1u, 1u, 2u)
#error "ctrl_loop_host.h: the host platform's shape is (1, 1, 2) alone"
#endif

#define CTRL_LOOP_SLICE_US 950u
#define CTRL_LOOP_BUILD_PASS_US 1010u
#define CTRL_LOOP_BUILD_ONE_PASS_US 735u
#define CTRL_LOOP_SRP_UNIT_US 285u
#define CTRL_LOOP_RETRY_COLD_US 85u
#define CTRL_LOOP_RETRY_ATTEMPT_US 34u
#define CTRL_LOOP_QUEUED_MS 130u
#define CTRL_LOOP_TX_MS 35u

#endif // CTRL_LOOP_HOST_H
