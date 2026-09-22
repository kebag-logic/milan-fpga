/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_aecp_engine.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/06 in full, 03 §4 dispatch record,
//                 03 §7 response buffers, 03 §8 TX arbitration + addressing)
//
//  Description : The AECP command path made whole: it POPS the dispatch
//                queue's AECP head, decodes the opcode into a µPC entry and
//                operands, runs KL_aecp_ucpu against KL_aecp_desc_store, and
//                turns the µCPU's response buffer into a byte-exact AECPDU on
//                the TX slot pool. Before this block the AECP head was handed
//                out through a top-level pop face that nothing popped.
//
//                THE DISPATCH DECISION (06 §4 specifies a dispatch ROM per
//                opcode; 06 §8 fixes its 48-bit entry shape but the tree ships
//                no ROM and no generator for it, so this is a documented
//                CHOICE, not an implementation of a written table). The
//                pop-time cone directly selects READ_DESCRIPTOR,
//                GET_COUNTERS, GET_AUDIO_MAP, and opcode-specific
//                BAD_ARGUMENTS paths. Other implemented AEM commands latch
//                discriminator bits and take a registered A_PLD-exit
//                re-dispatch after their operand bytes settle. Unsupported
//                opcodes retain the correctly sized NOT_IMPLEMENTED echo.
//
//                COMMANDS LANDED AFTER THE TIMING FINDING RESOLVE ONE STATE
//                LATER. The pop-time decode above is the measured critical
//                cone into the µcode ROM's address register, so 0x0024
//                REGISTER_UNSOLICITED_NOTIFICATION and 0x0025 DEREGISTER
//                (Milan §5.4.2.21/§5.4.2.22) keep the NOT_IMPLEMENTED echo
//                at pop and are re-dispatched at the A_PLD exit exactly
//                like the MVU sub-decode — a REGISTERED re-dispatch off a
//                discriminator flop, adding zero levels at pop. Their ops
//                run on the rgy face against KL_aecp_notify (the Milan
//                §5.3.4.2 registered-controller list), and their responses
//                ride the echo path: §7.4.37.1's response "share[s] the
//                same AECPDU format" as the command, so echoing the
//                command's own flags field (or nothing, for the 2013 format
//                the same clause obliges us to accept) IS the layout.
//
//                UNSOLICITED RESPONSES ARE ENGINE-ORIGINATED JOBS. The
//                `uns_*` face accepts one {kind, descriptor, controller,
//                mac, seq} job at a time from KL_aecp_notify, synthesizes
//                the 03 §4 record a command would have carried, runs the
//                SAME µprogram the solicited answer uses, and emits on
//                LANE_AECP_UNS with the §9.3.2.1 u bit set and the entry's
//                own sequence_id (Milan §5.4.5.1). A solicited head always
//                wins the A_IDLE arbitration.
//
//                WHERE GET_COUNTERS PUTS ITS ARGUMENTS. §7.4.42.1 puts
//                descriptor_type at @24 and descriptor_index at @26, where
//                §7.4.5's READ_DESCRIPTOR puts configuration_index and a
//                reserved field. The payload walk therefore captures @26..@27
//                into `desc_ix_r` for a counters command and @28..@31 for
//                everything else, so the SAME two operand registers serve both
//                shapes and neither costs a register of its own. A counters
//                command whose control_data_length is short of the §7.4.42.1
//                four bytes is BAD_ARGUMENTS, on the same reasoning as the
//                truncated READ_DESCRIPTOR: answering ENTITY-index-0 out of
//                whatever zeros happened to be there is a silent
//                misinterpretation, not an answer.
//
//                GET_AUDIO_MAP IS A THIRD SHAPE IN THE SAME REGISTERS.
//                §7.4.44.1 puts descriptor_type at @24, descriptor_index at
//                @26, map_index at @28 and a reserved word at @30, so an
//                `amap_r` command captures @26..@27 into `desc_ix_r` like a
//                counters command and @28..@29 into `desc_ty_r` - which for
//                this one command MEANS map_index - while @30..@31 is walked
//                and kept by nobody (without the guard the reserved word
//                would trample `desc_ix_r` through READ_DESCRIPTOR's arms).
//                A command short of the §7.4.44.1 eight bytes is
//                BAD_ARGUMENTS, same reasoning as above.
//
//                THE COUNTERS FACE IS NOT A COUNTER. This block holds no
//                counters and never will: the events Milan Table 5.6 counts
//                (media lock, sequence mismatch, late/early presentation time)
//                happen in the integrator's stream datapath, cycles and clock
//                domains away from an AEM command parser. So `ctr_*` is a READ
//                face — {descriptor_type, descriptor_index, quadlet} in,
//                32 bits out — and the integrator serves it however its
//                counters already exist: combinationally from flops, or out of
//                the context RAM they already live in, where the quadlet index
//                IS the RAM address and the mux costs nothing.
//
//                `ctr_wait_i` IS ASSERTED TO HOLD, and the polarity is the
//                point: an integrator who has not wired this face leaves it 0,
//                the gather beat completes immediately with `ctr_data_i` = 0,
//                and quadlet 32 — the counters_valid word — reads 0. That is
//                SUCCESS with an EMPTY mask: "this entity keeps no counters for
//                that object", which §7.4.42.2 defines exactly ("a bit that is
//                set means the associated quadlet exists and is valid"). Never
//                a hang, and never a block of zeros advertised as valid.
//
//                ...AND THE EMPTY MASK IS ONLY EVER SAID ABOUT A REAL OBJECT
//                (the bench probe's two strictness rules): E_GCTRS opens with
//                the store locate, so a descriptor_index the image lacks
//                answers NO_SUCH_DESCRIPTOR with the fixed body zeroed and
//                the face never asked — the store, not the face, is the
//                existence authority, exactly as it is for GET_AUDIO_MAP.
//                And a descriptor_type this build keeps no counters for
//                (anything outside STREAM_INPUT / STREAM_OUTPUT /
//                AVB_INTERFACE / CLOCK_DOMAIN, ENTITY included, whose Table 7-150 has
//                nothing but ENTITY_SPECIFIC bits) refuses NOT_SUPPORTED at
//                the registered A_PLD-exit re-dispatch, command echoed. The
//                integrator's wrong-object guard on the face stays as the
//                second line, never the answer.
//
//                THE AUDIO-MAP FACE IS THE SAME BARGAIN (06 §6.5; IEEE
//                §7.4.44, Milan §5.4.2.26). The dynamic mappings live in the
//                integrator's routing fabric - for the reference platform,
//                the render crossbar's map RAM - so `amap_*` is a second READ
//                face on the same gather bus: {descriptor_type,
//                descriptor_index, map_index, record ordinal} in, a
//                geometry word or one §7.4.44.2.1 record out. The bus is
//                routed BY COMMAND (`amap_r`), never by selector value, so
//                the two faces own disjoint commands and the whole selector
//                space each. Milan §5.4.2.26 puts the partition law on the
//                integrator ("disjoint subsets whose size does not exceed
//                176 ... fixed for a given Configuration"), and §7.4.44.1's
//                page rule is the µprogram's: map_index >= number_of_maps is
//                BAD_ARGUMENTS. An unwired face answers number_of_maps 0 for
//                every port, which the µprogram reads as NO_SUCH_DESCRIPTOR
//                only when the descriptor store AGREES the port is absent -
//                the store, not the face, is the existence authority, so
//                GET_AUDIO_MAP refuses exactly the indices READ_DESCRIPTOR
//                refuses.
//
//                BOTH STREAM PORT DIRECTIONS ARE DISPATCHED. Milan §5.4.2.26
//                demands GET_AUDIO_MAP on every Stream Port Input AND every
//                Stream Port Output with no static map; the OUTPUT side
//                re-dispatches to a two-word stub that swaps the emitted
//                type constant and falls into the same µprogram, and the
//                integrator's face routes on amap_desc_type_o to whichever
//                map store owns that direction. Any OTHER descriptor_type
//                keeps the NOT_IMPLEMENTED echo, decided at the A_PLD exit
//                exactly like the MVU sub-decode - the type field is
//                walked, not trusted at pop.
//
//                A ROM is the right shape once the hazard class, min-cdl,
//                response-size id, lock/GDI/notify flags and per-profile valid
//                bits of the 06 §8 entry have consumers; three arms of decode
//                is the right shape while they do not, and it cannot go stale
//                against a generator that does not exist. When the ROM lands
//                it replaces `upc_w`/`echo_w` here and nothing else.
//
//                THE MVU SUB-DECODE (06 §4 "MVU sub-decoder (protocol_id
//                match)") CANNOT RUN AT POP, and that is why it is a second
//                decode rather than a fourth arm above. A Milan Vendor Unique
//                command carries no AEM command_type: Milan v1.2 §5.4.3.2 puts
//                a 48-bit protocol_id at @22..@27 and the MVU command_type at
//                @28..@29, so the 03 §4 record's `opcode` field — which the
//                validator fills from @22..@23 — holds the first two bytes of
//                that protocol_id and nothing that identifies the command. The
//                bytes that do identify it are read by the payload walk, so
//                the pop-time decode stands (an MVU command starts out heading
//                for the generic echo) and A_PLD OVERRIDES it once every byte
//                is settled:
//
//                  msg_type 6 + protocol_id 00-1B-C5-0A-C1-00
//                             + r 0 + command_type 0x0000
//                             + a Figure 5.3 payload (8 B)  -> UPC_MVUINFO_C
//
//                Anything else with message_type 6 — a foreign protocol_id, an
//                MVU command_type this build does not implement, a truncated
//                one — keeps the echo and answers MVU status 1
//                NOT_IMPLEMENTED (Milan Table 5.19 = IEEE Table 9-6, which is
//                the same code the AEM path uses, so the status register needs
//                no remapping).
//
//                NOT_IMPLEMENTED IS AN ANSWER, NOT SILENCE. Every opcode this
//                block does not implement is ECHOED back with
//                message_type + 1 and status NOT_IMPLEMENTED (F06.14 "echo
//                command", IEEE §9.3.5.3.3): the emitted payload is the
//                command's own, read straight back out of its RX slot, and the
//                emitted length is the command's. So an unimplemented opcode
//                produces a well-formed, correctly-sized AECPDU — never a
//                dropped frame and never a malformed one.
//
//                WHO OWNS THE WIRE HEADER. The µCPU's BUILD_HEADER writes a
//                compact {target_eid, seq, status} record into response bytes
//                0..11 and its cursor starts at 12; that record is NOT the
//                24-byte AECPDU header (06 §8's skeleton never claimed to be
//                wire-accurate). This block owns the real header and
//                synthesises it from the 03 §4 transaction plus
//                `resp_status_o`, so response byte 12+k maps to AECPDU byte
//                24+k and `resp_len_o - 12` is the payload length. Response
//                bytes 0..11 are ignored.
//
//                WHERE THE RESPONSE BUFFER LIVES. Not here. The µCPU's `rb_*`
//                writes go to KL_aecp_resp_buf, which gathers them into
//                64-bit lanes and holds them in the integrator's MAIN MEMORY
//                at the compile-time `RESP_BASE_P`; the frame builder streams
//                the payload back out of it. As fabric state this buffer
//                measured 5,079 flip-flops and 3,495 LUTs on the reference
//                part and was the thing the placer could not pack. The
//                BIG-ENDIAN placement rule (a field VALUE right-justified in
//                `rb_wdata_o`, its WIDTH given by a low-contiguous
//                `rb_wstrb_o`, those m bytes laid out from `rb_addr_o` upward)
//                moved with it — the rule has to live in the buffer because
//                the µISA has no byte-swap operation, 06 §8 never states an
//                order, and tb/ucpu's C++ model uses the opposite convention
//                for its own convenience.
//
//                AN ECHOED PAYLOAD NEVER TOUCHES MEMORY. §9.3.5.3.3's echo is
//                a verbatim copy of the command payload, and the command is
//                still sitting in its RX slot until this block frees it — so
//                the frame builder reads those bytes straight out of the slot
//                (slot byte 24+n IS payload byte n) instead of staging them
//                through the response buffer. Only a µprogram-BUILT payload
//                is worth a memory round trip.
//
//                WHEN A GATHER FACE WEDGES. `ctr_wait_i` or `amap_wait_i`
//                held forever is the one way either face can stop a command
//                retiring, and a stalled µCPU stops READ_DESCRIPTOR too - the
//                descriptor path is the thing that must not regress. So ONE
//                shared watchdog bounds whichever face the in-flight command
//                routed to, budgeted at MEM_TIMEOUT_CYC_P like the descriptor
//                and response bridges, and expiry VOIDS the response through
//                the ENTITY_MISBEHAVING rebuild below rather than letting
//                zeros out under a mask or a mapping count that was already
//                emitted. A face that answers (including one that answers 0)
//                never arms it.
//
//                WHEN THE RESPONSE MEMORY FAILS. A wedged or absent bridge
//                raises `err_o` on the buffer. The TX slot is already
//                allocated by then and KL_pp_tx_slots has no abort arc — an
//                uncommitted slot is leaked and a zero-length commit hangs the
//                arbiter — so the builder REWRITES the frame in place as a
//                60-byte ENTITY_MISBEHAVING response (IEEE §7.4 status 10)
//                with an empty payload, built entirely from registers. Never a
//                leak, never a hang, and never a SUCCESS carrying bytes this
//                block did not read.
//
//                ADDRESSING (03 §8): an AECP response is UNICAST back to the
//                requester's src_mac. A frame shorter than the 60-octet
//                Ethernet minimum is zero-padded; `control_data_length`
//                (= 12 + payload, the offset-from-@12 convention this
//                architecture uses throughout — F06.14's "GET_COUNTERS 160 B,
//                cdl 148") still names the real length.
//
//                WHAT IT REFUSES: an AECP RESPONSE arriving as input
//                (message_type odd) is freed without a reply — this entity
//                originates no AECP command yet, and answering a response is
//                how a control plane builds a storm; and a command whose
//                target_entity_id is not ours is dropped (F06.2 MATCHED arc).
//---------------------------------------------------------------------------//
`default_nettype none

module KL_aecp_engine
  import pp_pkg::*;
  import ucpu_pkg::*;
#(
    //! µcode ROM image (hdl/aecp/ucode/gen_ucode.py). A RELATIVE name resolves
    //! against the TOOL'S RUN DIRECTORY — the parameter exists so an
    //! integrator can hand over an absolute path.
    parameter string       UCODE_HEX_P       = "ucode.hex",
    //! descriptor-image base in the integrator's memory map (compile time)
    parameter logic [31:0] DESC_BASE_P       = 32'h2000_0000,
    //! response-buffer base in the integrator's memory map (compile time).
    //! WRITTEN by this processor — it must not overlap the descriptor image.
    parameter logic [31:0] RESP_BASE_P       = 32'h2010_0000,
    parameter int unsigned LINE_BYTES_P      = 576,
    parameter int unsigned IDX_ENTRIES_P     = 32,
    parameter int unsigned NAME_ENTRIES_P    = 32,
    parameter int unsigned MEM_TIMEOUT_CYC_P = 4096,
    //! ---- the shape the dynamic-state store is sized from ---------------
    //! Milan v1.2 makes one setting per Audio Unit, per Clock Domain, per
    //! Stream Input and per Stream Output, so the store's row map is derived
    //! from the elaborated shape rather than fixed (07 §3.2's shape law).
    parameter int unsigned N_STREAM_IN_P     = 8,
    parameter int unsigned N_STREAM_OUT_P    = 8,
    parameter int unsigned N_AUDIO_UNIT_P    = 1,
    parameter int unsigned N_CLK_DOMAIN_P    = 1,
    parameter int unsigned N_CONTROL_P       = 1,
    //! RX/TX pool geometry (03 §2) — mirrors protocol_processor_top
    parameter int unsigned RX_SLOTS_P          = 4,
    parameter int unsigned RX_SLOT_BYTES_P     = 576,
    parameter int unsigned TX_STD_SLOTS_P      = 4,
    parameter int unsigned TX_STD_BYTES_P      = 576,
    parameter int unsigned TX_OVERSIZE_BYTES_P = 1600,
    //! derived — do not override
    localparam int unsigned RXS_W_C  = (RX_SLOTS_P > 1) ? $clog2(RX_SLOTS_P) : 1,
    localparam int unsigned RXA_W_C  = $clog2(RX_SLOT_BYTES_P),
    localparam int unsigned RXL_W_C  = $clog2(RX_SLOT_BYTES_P + 1),
    localparam int unsigned TXS_W_C  = $clog2(TX_STD_SLOTS_P + 1),
    localparam int unsigned TXA_W_C  = $clog2(TX_OVERSIZE_BYTES_P + 1)
) (
    input  wire         clk_i,                //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,                //! synchronous active-low reset

    //! ---- identity (02 §2 rule 4 quasi-static) ----
    input  wire  [63:0] entity_id_i,          //! own entity_id (F06.2 MATCHED)
    input  wire  [47:0] own_mac_i,            //! response source address

    //! ---- dispatch pop face (03 §4 record, KL_pp_dispatch AECP queue) ----
    input  wire                    txn_valid_i,  //! head record valid
    input  wire  [PP_TXN_W_C-1:0]  txn_i,        //! head pp_txn_t record
    output logic                   txn_ready_o,  //! engine consumes the head

    //! ---- RX slot read + free (its own lock-step pool replica) ----
    output logic [RXS_W_C-1:0] rxs_rd_slot_o,  //! payload slot to read
    output logic [RXA_W_C-1:0] rxs_rd_addr_o,  //! byte address in the slot
    output logic               rxs_rd_en_o,    //! sync-read enable
    input  wire  [7:0]         rxs_rd_data_i,  //! byte, one cycle later
    input  wire  [RXL_W_C-1:0] rxs_slot_len_i, //! committed slot length
    output logic               rxs_free_o,     //! return the consumed slot
    output logic [RXS_W_C-1:0] rxs_free_slot_o,//! which slot

    //! ---- TX slot pool client (03 §7) ----
    output logic               txs_alloc_req_o,//! slot request, held until grant
    output logic               txs_oversize_o, //! Δ8 oversize slot needed
    input  wire                txs_alloc_gnt_i,//! one-cycle grant
    input  wire  [TXS_W_C-1:0] txs_alloc_slot_i,
    output logic [TXS_W_C-1:0] txs_wr_slot_o,
    output logic [TXA_W_C-1:0] txs_wr_addr_o,
    output logic               txs_wr_valid_o,
    output logic [7:0]         txs_wr_data_o,
    output logic               txs_wr_commit_o,
    output logic [TXA_W_C-1:0] txs_wr_len_o,

    //! ---- TX arbiter lane (F03.5 LANE_AECP_SOL); held until granted ----
    output logic               txreq_valid_o,
    output logic [TXS_W_C-1:0] txreq_slot_o,
    input  wire                txreq_ready_i,

    //! ---- descriptor memory master (read-only; see KL_aecp_desc_store) ----
    output logic        mem_req_valid_o,
    input  wire         mem_req_ready_i,
    output logic [31:0] mem_req_addr_o,
    output logic  [8:0] mem_req_beats_o,
    input  wire         mem_rsp_valid_i,
    output logic        mem_rsp_ready_o,
    input  wire  [63:0] mem_rsp_data_i,
    input  wire         mem_rsp_last_i,
    input  wire         mem_rsp_err_i,

    //! ---- response-buffer memory master (read/write; see KL_aecp_resp_buf) ----
    output logic        rmem_req_valid_o,
    input  wire         rmem_req_ready_i,
    output logic [31:0] rmem_req_addr_o,
    output logic  [8:0] rmem_req_beats_o,
    input  wire         rmem_rsp_valid_i,
    output logic        rmem_rsp_ready_o,
    input  wire  [63:0] rmem_rsp_data_i,
    input  wire         rmem_rsp_last_i,
    input  wire         rmem_rsp_err_i,
    output logic        rmem_wr_valid_o,
    input  wire         rmem_wr_ready_i,
    output logic [31:0] rmem_wr_addr_o,
    output logic [63:0] rmem_wr_data_o,
    output logic  [7:0] rmem_wr_strb_o,
    input  wire         rmem_wr_done_i,
    input  wire         rmem_wr_err_i,

    //! ---- GET_COUNTERS read face (06 §6.6; IEEE §7.4.42, Milan §5.4.2.25) ----
    //! Asked once per quadlet of the response. `ctr_word_o` 0..31 is the
    //! counters_block quadlet at block byte 4·n; `ctr_word_o` = 32 is the
    //! counters_valid word itself, so ONE face carries the mask and the data
    //! and the integrator has one place to be honest about what it measures.
    output logic        ctr_req_o,            //! a quadlet is being asked for
    output logic [15:0] ctr_desc_type_o,      //! AECPDU @24 (ENTITY, STREAM_INPUT, …)
    output logic [15:0] ctr_desc_index_o,     //! AECPDU @26
    output logic  [5:0] ctr_word_o,           //! 0..31 = block quadlet, 32 = counters_valid
    input  wire  [31:0] ctr_data_i,           //! that quadlet, 1722.1 value order
    //! HOLD, not ready: 0 means "answer is on ctr_data_i now", so an unwired
    //! face answers 0 and the response carries an empty counters_valid mask
    //! rather than hanging or advertising zeros (see the banner)
    input  wire         ctr_wait_i,

    //! ---- GET_AUDIO_MAP read face (06 §6.5; IEEE §7.4.44, Milan §5.4.2.26) ----
    //! The integrator's dynamic-mapping store, asked one word at a time while
    //! a GET_AUDIO_MAP is in flight. `amap_sel_o` names the word:
    //!   0 NMAPS  - {16'd0, number_of_maps}: the addressed port's fixed
    //!              Milan §5.4.2.26 partition count; 0 = no such port here
    //!   1 GEOM   - {16'd0, number_of_maps, number_of_mappings}: the page
    //!              named by amap_map_index_o; number_of_mappings MUST read 0
    //!              for a page the store has no data for (unknown port,
    //!              map_index out of range) - the wrong-object guard
    //!   2 RECORD - mapping record `amap_rec_o` of that page as ONE
    //!              big-endian qword {stream_index, stream_channel,
    //!              cluster_offset, cluster_channel} (§7.4.44.2.1)
    //! `amap_wait_i` is the same HOLD `ctr_wait_i` is: an unwired face
    //! answers number_of_maps 0, and the µprogram turns that into
    //! NO_SUCH_DESCRIPTOR only where the descriptor store agrees.
    output logic        amap_req_o,           //! a word is being asked for
    output logic [15:0] amap_desc_type_o,     //! AECPDU @24 (STREAM_PORT_INPUT or STREAM_PORT_OUTPUT)
    output logic [15:0] amap_desc_index_o,    //! AECPDU @26
    output logic [15:0] amap_map_index_o,     //! AECPDU @28 - the page
    output logic  [1:0] amap_sel_o,           //! 0 NMAPS, 1 GEOM, 2 RECORD
    output logic  [7:0] amap_rec_o,           //! record ordinal within the page
    input  wire  [63:0] amap_data_i,          //! the word (upper 32 zero unless RECORD)
    input  wire         amap_wait_i,          //! HOLD the beat (not a ready)

    //! ---- ADD/REMOVE_AUDIO_MAPPINGS transaction face --------------------
    //! The command engine owns framing, descriptor existence, lock ordering,
    //! exact-length validation and the two-pass walk. The integrator owns the
    //! routing store and therefore decides whether a record is valid and how
    //! it projects into the live map RAM. `amap_edit_phase_o` is:
    //!   0 begin validation, 1 begin commit, 2 finish, 3 abort,
    //!   4 validate one record, 5 commit one record.
    //! A begin/validate reply returns `amap_edit_data_i[0]` = accepted. Phase
    //! 1 acceptance reserves the complete transaction and is the point of no
    //! return: phases 5 and 2 must then complete without back-pressure, and
    //! the processor ignores `amap_edit_wait_i` on those phases. A finish
    //! reply returns bit 0 = at least one mapping changed. The future
    //! SET_STREAM_FORMAT survival query uses the same value lane instead of
    //! opening a second map authority.
    output logic        amap_edit_req_o,
    output logic  [2:0] amap_edit_phase_o,
    output logic        amap_edit_remove_o,
    output logic [15:0] amap_edit_desc_type_o,
    output logic [15:0] amap_edit_desc_index_o,
    output logic [15:0] amap_edit_count_o,
    output logic  [7:0] amap_edit_rec_o,
    output logic [63:0] amap_edit_record_o,
    output logic [63:0] amap_edit_value_o,
    input  wire  [63:0] amap_edit_data_i,
    input  wire         amap_edit_wait_i,

    //! ---- Milan-info gather face (06 §6.2/§6.10; IEEE §7.4.16/§7.4.40/
    //! §7.4.41, Milan §5.4.2.10/§5.4.2.23/§5.4.2.24) ----
    //! ONE face for the three read-only Milan info commands, selector-coded
    //! like the counters face: the INTEGRATOR owns every answer word because
    //! the truth lives in its binding view, SRP registrars and gPTP plane -
    //! this parser only lays the words out. `gsi_kind_o` names the command
    //! family (0 GET_STREAM_INFO, 1 GET_AVB_INFO, 2 GET_AS_PATH), the
    //! selector the word (docs/architecture/06 §6.2/§6.10 tables), and
    //! `gsi_ord_o` the array ordinal for GET_AS_PATH's path_sequence.
    //! `gsi_wait_i` is the same HOLD the other faces use; an unwired face
    //! answers zeros, which every response carries honestly as cleared
    //! validity flags, a zero path count and zero fields - absent, never
    //! invented.
    output logic        gsi_req_o,           //! a word is being asked for
    output logic [1:0]  gsi_kind_o,          //! 0 STRI / 1 AVB / 2 ASP
    output logic [15:0] gsi_desc_type_o,     //! AECPDU @24 (STRI: 0x0005/0x0006)
    output logic [15:0] gsi_desc_index_o,    //! the addressed descriptor_index
    output logic  [3:0] gsi_sel_o,           //! word selector within the kind
    output logic  [7:0] gsi_ord_o,           //! ASP path entry ordinal
    //! the PROPOSED stream format while a SET_STREAM_FORMAT is in flight;
    //! kind 0 selector 15 asks the integrator to judge it (bit 0 = the
    //! format is supported for the addressed stream, bit 1 = every channel
    //! an existing audio mapping references survives it, Milan §5.4.2.7).
    //! The answer's LOW BYTE must be exactly 0x03 to pass - the µprogram's
    //! byte-wide CHECK_ARG refuses any other bit set in it
    output logic [63:0] gsi_prop_fmt_o,
    input  wire  [63:0] gsi_data_i,          //! the word (see the doc tables)
    input  wire         gsi_wait_i,          //! HOLD the beat (not a ready)

    //! ---- registry/lock op face (06 §6.4/§6.7; served by KL_aecp_notify) ----
    //! A GATHER-routed MUTATION face: while a REGISTER_UNSOLICITED_
    //! NOTIFICATION / DEREGISTER / LOCK_ENTITY command is in flight, its
    //! µprogram's gathers ride here instead of the counter/audio-map faces,
    //! and the op arguments are the COMMAND'S OWN identity - controller_eid
    //! and src_mac from the 03 §4 record, exactly the Milan §5.3.4.2 tuple.
    //! `rgy_wait_i` is the same HOLD the other faces use and the same gxf
    //! watchdog bounds it; the op executes once per request edge, which the
    //! µprograms guarantee by separating consecutive gathers with the
    //! COMPARE that tests the result (see KL_aecp_notify's banner).
    output logic        rgy_req_o,           //! an op / state query is presented
    output logic        rgy_state_o,         //! 1 = read the lock holder, no op
    output logic [1:0]  rgy_op_o,            //! 0 REG / 1 DEREG / 2 LOCK / 3 UNLOCK
    output logic [63:0] rgy_eid_o,           //! requesting controller entity_id
    output logic [47:0] rgy_mac_o,           //! its source MAC
    output logic        rgy_tl_o,            //! REGISTER: TIME_LIMITED flag
    input  wire  [63:0] rgy_data_i,          //! result word
    input  wire         rgy_wait_i,          //! HOLD the beat (not a ready)

    //! ---- unsolicited job face (06 §6.7; producer is KL_aecp_notify) ----
    //! One job = one AECPDU to ONE controller, run through the SAME
    //! µprograms, response buffer and frame builder as a solicited answer -
    //! the only differences are the synthesized 03 §4 record (no RX slot,
    //! no payload walk), the u bit, and the TX lane. A job is taken only
    //! when no solicited head is waiting, so notifications can never starve
    //! the command path; the producer holds `uns_valid_i` until `uns_done_o`.
    input  wire         uns_valid_i,         //! job presented, held until done
    input  wire  [3:0]  uns_kind_i,          //! pp_pkg PP_UNS_* response kind
    input  wire  [15:0] uns_desc_type_i,     //! response descriptor_type
    input  wire  [15:0] uns_desc_index_i,    //! response descriptor_index
    input  wire  [63:0] uns_ctlr_eid_i,      //! target controller entity_id
    input  wire  [47:0] uns_mac_i,           //! target unicast MAC
    input  wire  [15:0] uns_seq_i,           //! the entry's sequence_id
    input  wire         uns_amap_remove_i,
    input  wire  [15:0] uns_amap_count_i,
    input  wire  [15:0] uns_arg0_i,
    input  wire  [15:0] uns_arg1_i,
    input  wire         amap_notify_busy_i,
    output logic        uns_done_o,          //! one-cycle: job retired (sent or voided)

    //! ---- TX arbiter lane (F03.5 LANE_AECP_UNS); held until granted ----
    output logic        txreq_uns_valid_o,
    input  wire         txreq_uns_ready_i,

    //! ---- lock context (06 §6.4; KL_aecp_notify's published lock state) ----
    //! ---- the STREAM_IS_RUNNING predicate (Milan §5.3.7.3 / §5.3.8.2) ---
    //! Milan spells "running" two different ways and they are NOT
    //! interchangeable, so both arrive as their own vector:
    //!
    //!   * a Stream INPUT is **bound** — the pure ACMP bind level. §5.3.8.2
    //!     is explicit that bound "does not necessarily mean that data is
    //!     flowing", so this is neither reservation nor started.
    //!   * a Stream OUTPUT is **streaming** — §5.3.7.3: "As long as a PAAD is
    //!     declaring a Talker Advertise attribute AND receiving a Listener
    //!     Ready or Listener Ready Failed attribute for a Stream Output, it
    //!     shall be streaming AVTP packets."
    //!
    //! The integrator reduces its SRP state to that sentence; this block only
    //! consumes the answer, because the reduction belongs where the SRP
    //! records live and not in a command decoder.
    input  wire [N_STREAM_IN_P-1:0]  strm_bound_i,
    input  wire [N_STREAM_IN_P-1:0]  strm_started_i,

    //! ---- started/stopped request out (Milan §5.4.2.19 / §5.4.2.20) -----
    //! One held request per START/STOP_STREAMING, aimed at the ACMP binding
    //! record that owns the bit. Completion means the record has committed
    //! or the required no-op check has examined it. A bounded walker failure
    //! is reported so the command can return ENTITY_MISBEHAVING.
    output logic                     strm_set_valid_o,
    output logic [15:0]              strm_set_index_o,
    output logic                     strm_set_val_o,   //! 1 = started
    input  wire                      strm_set_ready_i, //! record completed it
    input  wire                      strm_set_error_i, //! completion failed
    input  wire [N_STREAM_OUT_P-1:0] strm_streaming_i,
    input  wire         lock_held_i,
    input  wire  [63:0] lock_ctlr_i,

    //! ---- effect strobes (06 §8; consumers are P4) ----
    output logic        eff_commit_o,
    output logic  [7:0] eff_nvm_mark_o,
    output logic        eff_nvm_stb_o,
    output logic  [3:0] eff_notify_class_o,
    output logic        eff_notify_stb_o,
    output logic [15:0] eff_notify_type_o,
    output logic [15:0] eff_notify_index_o,
    output logic [15:0] eff_notify_arg0_o,
    output logic [15:0] eff_notify_arg1_o,
    output logic [63:0] eff_notify_excl_eid_o,

    //! ---- observability ----
    output logic        dbg_busy_o,          //! a command is in flight
    output logic [15:0] dbg_cmd_cnt_o,       //! commands accepted
    output logic [15:0] dbg_resp_cnt_o,      //! responses committed
    output logic [15:0] dbg_drop_cnt_o,      //! frames freed without a reply
    output logic  [4:0] dbg_status_o,        //! status of the last response
    output logic [10:0] dbg_len_o,           //! AECPDU length of the last response
    output logic        dbg_img_valid_o,     //! store: header validated
    output logic  [3:0] dbg_img_fault_o,     //! store: why not
    output logic [15:0] dbg_locate_miss_o,   //! store: locates answered err
    output logic  [2:0] dbg_resp_fault_o,    //! response buffer: last fault code
    output logic [15:0] dbg_resp_err_o,      //! responses voided by that memory
    output logic [15:0] dbg_resp_lane_o,     //! response lanes written to memory

    //! ---- the dynamic state a controller has SET (Milan §5.3.x) ---------
    //! Published continuously so the fabric acts on a setting rather than
    //! being told about it: the started bits gate the listener, the clock
    //! source selects the media clock, the presentation offset feeds the
    //! talker. Every one of them reads its reset default until a controller
    //! writes it, so an integrator that ignores these ports sees exactly the
    //! behaviour it had before the store existed.
    output logic [15:0] dyn_cur_config_o,    //! ENTITY.current_configuration
    output logic  [7:0] dyn_identify_o,      //! IDENTIFY value, 0 or 255
    output logic [15:0] dyn_clk_src_index_o, //! CLOCK_DOMAIN[0] clock source
    //! per-row: value beside its valid bit, row k of the offsets at
    //! [32k +: 32] and of the formats at [64k +: 64]. A value without its
    //! valid bit is a reset zero, not a setting.
    output logic [N_STREAM_OUT_P*32-1:0] dyn_pt_offset_o,
    output logic [N_STREAM_OUT_P-1:0]    dyn_pt_offset_v_o,
    output logic [N_STREAM_IN_P*64-1:0]  dyn_fmt_in_o,
    output logic [N_STREAM_IN_P-1:0]     dyn_fmt_in_v_o,
    output logic [N_STREAM_OUT_P*64-1:0] dyn_fmt_out_o,
    output logic [N_STREAM_OUT_P-1:0]    dyn_fmt_out_v_o,
    output logic        dyn_dirty_o          //! a persisted field was written
);

  // ---- IEEE 1722.1-2021 AEM opcodes this block decodes --------------------
  localparam logic [15:0] OP_READ_DESCRIPTOR_C = 16'h0004;
  localparam logic [15:0] OP_IDENTIFY_NOTIF_C  = 16'h0026;
  localparam logic [15:0] OP_GET_COUNTERS_C    = 16'h0029;
  localparam logic [15:0] OP_GET_AUDIO_MAP_C   = 16'h002B;
  localparam logic [15:0] OP_GET_DYNAMIC_INFO_C = 16'h004B;
  localparam logic [15:0] OP_SET_NAME_C         = 16'h0010;
  localparam logic [15:0] OP_GET_NAME_C         = 16'h0011;
  //! IEEE 1722.1-2021 7.4.76.2 permits exactly these fixed-size getters in
  //! a dynamic_info list. Membership and implementation are separate:
  //! permitted getters that this profile does not serve receive a record
  //! status of NOT_SUPPORTED instead of rejecting the whole command.
  localparam logic [15:0] GDI_GET_VIDEO_FMT_C   = 16'h000B;
  localparam logic [15:0] GDI_GET_SENSOR_FMT_C  = 16'h000D;
  localparam logic [15:0] GDI_GET_ASSOC_ID_C    = 16'h0013;
  localparam logic [15:0] GDI_GET_SIGNAL_SEL_C  = 16'h001D;
  localparam logic [15:0] GDI_GET_MEM_LEN_C     = 16'h0048;
  localparam logic [15:0] GDI_GET_STREAM_BKUP_C = 16'h004A;
  localparam logic [15:0] OP_ADD_AUDIO_MAP_C   = 16'h002C;
  localparam logic [15:0] OP_REMOVE_AUDIO_MAP_C = 16'h002D;
  //! §7.4.37/§7.4.38 - the registration pair. NOT pop-time dispatch arms:
  //! both resolve through the REGISTERED A_PLD-exit re-dispatch (the MVU
  //! pattern), because the pop-time opcode-to-µPC cone is the measured
  //! critical path into the µcode ROM's address register and must never
  //! deepen. Their bit-0 difference is also the rgy op code.
  localparam logic [15:0] OP_REG_UNSOL_C       = 16'h0024;
  localparam logic [15:0] OP_DEREG_UNSOL_C     = 16'h0025;
  //! §7.4.1/§7.4.2 - same registered A_PLD-exit re-dispatch as the pair
  //! above. Milan §5.4.2.1 rules ACQUIRE_ENTITY "shall not reply SUCCESS
  //! ... It should reply with the NOT_SUPPORTED error code", and the
  //! response format IS the command's own bytes (flags echoed, owner_id 0
  //! echoed - a command carries owner_id 0 by §7.4.1.1 - descriptor echoed),
  //! so ACQUIRE rides the echo path with one status. LOCK_ENTITY is real:
  //! Milan §5.4.2.2 with the UNLOCK flag, ENTITY-descriptor-only
  //! (NOT_SUPPORTED otherwise), and the §7.4.2 60 s expiry - the state
  //! lives in KL_aecp_notify behind the rgy face.
  localparam logic [15:0] OP_ACQUIRE_C         = 16'h0000;
  localparam logic [15:0] OP_LOCK_C            = 16'h0001;
  //! §7.4.16 - Milan §5.4.2.10 replaces the IEEE response with the 80-byte
  //! Milan layout (Figure 5.1: flags_ex + pbsta/acmpsta). Same registered
  //! A_PLD-exit re-dispatch; STREAM_INPUT/STREAM_OUTPUT are the only
  //! §7.4.16 targets and anything else refuses NOT_SUPPORTED.
  localparam logic [15:0] OP_GET_STREAM_INFO_C = 16'h000F;
  localparam logic [15:0] DT_STREAM_INPUT_C    = 16'h0005;
  localparam logic [15:0] DT_STREAM_OUTPUT_C   = 16'h0006;
  //! §7.4.40/§7.4.41 - the gPTP pair, Milan §5.4.2.23/§5.4.2.24. Same
  //! registered re-dispatch; both act on AVB_INTERFACE, but §7.4.41.1's
  //! command carries the INDEX at @24 (no type field at all), so the walk's
  //! cfg_ix register holds the index for GET_AS_PATH.
  localparam logic [15:0] OP_GET_AVB_INFO_C    = 16'h0027;
  localparam logic [15:0] OP_GET_AS_PATH_C     = 16'h0028;
  localparam logic [15:0] DT_AVB_INTERFACE_C   = 16'h0009;
  localparam logic [15:0] DT_CLOCK_DOMAIN_C    = 16'h0024;
  //! §7.4.3/§7.4.8/§7.4.10/§7.4.22/§7.4.24 - the read-side set Milan §5.4.2.3,
  //! .6, .8, .14 and .16 each make a SHALL. All five re-dispatch at the A_PLD
  //! exit like everything above them; none may be added to the pop-time µPC
  //! mux. ENTITY_AVAILABLE and GET_CONFIGURATION carry NO command payload
  //! (§7.4.3.1, §7.4.8.1 both say "the command_specific_data field is zero
  //! length"), so neither has a length gate and neither walks a byte; the
  //! other three carry §7.4.42.1's {descriptor_type, descriptor_index} shape
  //! and share its cdl-16 floor and its walk-capture arms.
  localparam logic [15:0] OP_ENTITY_AVAIL_C    = 16'h0002;
  localparam logic [15:0] OP_GET_CONFIG_C      = 16'h0007;
  localparam logic [15:0] OP_GET_STREAM_FMT_C  = 16'h0009;
  localparam logic [15:0] OP_GET_SAMP_RATE_C   = 16'h0015;
  localparam logic [15:0] OP_GET_CLOCK_SRC_C   = 16'h0017;
  localparam logic [15:0] DT_ENTITY_C          = 16'h0000;
  localparam logic [15:0] DT_AUDIO_UNIT_C      = 16'h0002;
  //! ---- the SET family (Milan §5.4.2.13 / §5.4.2.15) -------------------
  //! Each shares its GET's response form (IEEE Figures 7-45 and 7-47 are
  //! command-and-response figures), carries its value at @28, and is
  //! lock-protected: Milan repeats "shall not accept a <CMD> command from a
  //! different controller" in every one of these clauses, which is what
  //! CHECK_LOCK enforces at the top of each µprogram.
  localparam logic [15:0] OP_SET_SAMP_RATE_C   = 16'h0014;
  localparam logic [15:0] OP_SET_CLOCK_SRC_C   = 16'h0016;
  //! §7.4.25/§7.4.26 — Milan §5.4.2.17/.18 scope both to the "Identify"
  //! CONTROL, and §7.3.5.2 gives that control one CONTROL_LINEAR_UINT8 value,
  //! so the response body is 5 bytes and the cdl 17 rather than the 20 the
  //! rest of this family uses. Its refusals need their own shaped stubs.
  localparam logic [15:0] OP_SET_CONTROL_C      = 16'h0018;
  localparam logic [15:0] OP_GET_CONTROL_C      = 16'h0019;
  localparam logic [15:0] DT_CONTROL_C          = 16'h001A;
  //! ---- SET_CONFIGURATION (Milan §5.4.2.5) ------------------------------
  //! §7.4.7.1's command is {reserved, configuration_index} — its @24 word is
  //! NOT a descriptor type, which is why it gets its own operand packing and
  //! why it joins the @26 capture set without joining the {type, index}
  //! SHAPE. START/STOP_STREAMING rode this same predicate and moved to
  //! their own branch behind issue #78 (started/stopped has two candidate
  //! homes and the choice is not this PR's to make).
  localparam logic [15:0] OP_SET_CONFIG_C      = 16'h0006;
  //! ---- SET_STREAM_FORMAT / SET_STREAM_INFO (Milan §5.4.2.7 / §5.4.2.9) --
  //! SET_STREAM_FORMAT rides the full SET template: the tix shape, the
  //! 8-byte @28 capture (a stream_format fills `setval_r` exactly), and a
  //! per-descriptor STREAM_IS_RUNNING route below. SET_STREAM_INFO is the
  //! one command Milan narrows to a single sub-command - a STREAM_OUTPUT
  //! with exactly the MSRP_ACC_LAT_VALID flag - so every narrowing is a
  //! dispatch route off registered walk fields and the µprogram only writes
  //! and echoes.
  localparam logic [15:0] OP_SET_STREAM_FMT_C  = 16'h0008;
  localparam logic [15:0] OP_SET_STREAM_INFO_C = 16'h000E;
  //! IEEE 1722.1-2021 Table 7-133 stream_info_flags, numbered 0 = MSB like
  //! Table 7-144: MSRP_ACC_LAT_VALID is table bit 2, wire bit 29. Milan
  //! §5.4.2.9 admits EXACTLY this flag - a command carrying any other bit,
  //! or none, is refused whole (NOT_SUPPORTED), never partially applied.
  localparam logic [31:0] SIF_ACC_LAT_C        = 32'h2000_0000;
  //! ---- START/STOP_STREAMING (Milan §5.4.2.19 / §5.4.2.20) --------------
  //! IEEE Figure 7-59 gives both the {type @24, index @26} shape and nothing
  //! else, so they join `tix_w` and their response is four bytes long — the
  //! command's own length, cdl 16, for the success arm and every refusal
  //! alike. Milan narrows IEEE §7.4.35's "STREAM_INPUT or STREAM_OUTPUT" to
  //! Stream Inputs only; a Stream Output is answered NOT_SUPPORTED, which is
  //! one instance of the wrong-type rule below rather than a case of its own.
  localparam logic [15:0] OP_START_STRM_C      = 16'h0022;
  localparam logic [15:0] OP_STOP_STRM_C       = 16'h0023;
  //! Table 7-1: the two descriptor types the audio-map µprograms serve -
  //! every other type keeps the NOT_IMPLEMENTED echo
  localparam logic [15:0] DT_STREAM_PORT_IN_C  = 16'h000E;
  localparam logic [15:0] DT_STREAM_PORT_OUT_C = 16'h000F;

  // ---- Milan Vendor Unique (Milan v1.2 §5.4.3.2, §5.4.4.1) ---------------
  //! protocol_id is the Avnu OUI-36 00-1B-C5-0A-C appended with MVU's 12-bit
  //! protocol unique identifier 0x100 (§5.4.3.2.1) = 00-1B-C5-0A-C1-00. It
  //! spans @22..@27, so its first two bytes land in `raw_ct_r` (the field an
  //! AEM command calls command_type) and its last four in the payload walk.
  localparam logic [15:0] MVU_PID_HI_C = 16'h001B;   // @22..@23
  localparam logic [15:0] MVU_PID_MD_C = 16'hC50A;   // @24..@25
  localparam logic  [7:0] MVU_PID_L1_C = 8'hC1;      // @26
  localparam logic  [7:0] MVU_PID_L0_C = 8'h00;      // @27
  //! the @28..@29 word: r = 0 (§5.4.3.2.2) + Table 5.18 command_type 0x0000
  localparam logic [15:0] MVU_GET_MILAN_INFO_C = 16'h0000;
  //! Figure 5.3 fixes the command at protocol_id + r/command_type + reserved,
  //! so its payload is 8 bytes. The walk captures index n from @22+n and the
  //! LAST capture lands in the same cycle the walk exits, so demanding the
  //! whole Figure 5.3 payload is also what guarantees @28..@29 is settled by
  //! the time the sub-decode below reads it.
  localparam logic [10:0] MVU_CMD_PLD_C = 11'd8;

  // ---- µPC entry points (hdl/aecp/ucode/gen_ucode.py) ---------------------
  localparam logic [10:0] UPC_NOTIMPL_C = 11'd560;   // E_NOTIMPL
  localparam logic [10:0] UPC_RDESC_C   = 11'd640;   // E_RDESC
  localparam logic [10:0] UPC_BADARG_C  = 11'd704;   // E_BADARG
  localparam logic [10:0] UPC_MVUINFO_C = 11'd736;   // E_MVUINFO
  localparam logic [10:0] UPC_GCTRS_C   = 11'd768;   // E_GCTRS
  localparam logic [10:0] UPC_GAMAP_C   = 11'd800;   // E_GAMAP
  localparam logic [10:0] UPC_REGUN_C   = 11'd832;   // E_REGUN
  localparam logic [10:0] UPC_DEREG_C   = 11'd844;   // E_DEREG
  localparam logic [10:0] UPC_UNSOK_C   = 11'd852;   // E_UNSOK
  localparam logic [10:0] UPC_NOSEND_C  = 11'd858;   // E_NOSEND
  localparam logic [10:0] UPC_NSUPPE_C  = 11'd864;   // E_NSUPPE
  localparam logic [10:0] UPC_LOCKEN_C  = 11'd872;   // E_LOCKEN
  localparam logic [10:0] UPC_LOCKUNS_C = 11'd896;   // E_LOCKUNS
  localparam logic [10:0] UPC_GSTRI_C   = 11'd912;   // E_GSTRI
  localparam logic [10:0] UPC_GAVB_C    = 11'd944;   // E_GAVB
  localparam logic [10:0] UPC_GASP_C    = 11'd976;   // E_GASP
  localparam logic [10:0] UPC_GAMAPO_C  = 11'd996;   // E_GAMAPO
  localparam logic [10:0] UPC_GCTRSNS_C = 11'd796;   // E_GCTRSNS
  localparam logic [10:0] UPC_EAVL_C    = 11'd1008;  // E_EAVL
  localparam logic [10:0] UPC_GCFG_C    = 11'd1024;  // E_GCFG
  localparam logic [10:0] UPC_GSFMT_C   = 11'd1056;  // E_GSFMT
  localparam logic [10:0] UPC_GSRATE_C  = 11'd1088;  // E_GSRATE
  localparam logic [10:0] UPC_GCLKS_C   = 11'd1120;  // E_GCLKS
  localparam logic [10:0] UPC_SSRATE_C  = 11'd1152;  // E_SSRATE2
  localparam logic [10:0] UPC_SCLKS_C   = 11'd1184;  // E_SCLKS
  //! ...and the two shared full-body NOT_SUPPORTED refusals: a wrong target
  //! may not answer at command length (only NOT_IMPLEMENTED may), and a
  //! zero-valued body is the same wire bytes for a rate and for a
  //! {clock_source_index, reserved} pair, so three type gates need two stubs
  localparam logic [10:0] UPC_TIZ8NS_C  = 11'd1216;  // E_TIZ8NS
  localparam logic [10:0] UPC_TIZ4NS_C  = 11'd1224;  // E_TIZ4NS
  localparam logic [10:0] UPC_LOCKED4_C = 11'd1232;  // E_LOCKED4
  localparam logic [10:0] UPC_BADARG4_C = 11'd1240;  // E_BADARG4
  localparam logic [10:0] UPC_GCTRL_C   = 11'd1248;  // E_GCTRL
  localparam logic [10:0] UPC_SCTRL_C   = 11'd1280;  // E_SCTRL
  localparam logic [10:0] UPC_LOCKED1_C = 11'd1312;  // E_LOCKED1
  localparam logic [10:0] UPC_BADARG1_C = 11'd1320;  // E_BADARG1
  localparam logic [10:0] UPC_NSUPP1_C  = 11'd1328;  // E_NSUPP1
  localparam logic [10:0] UPC_SCFG_C     = 11'd1456; // E_SCFG
  localparam logic [10:0] UPC_SCFGRUN_C  = 11'd1488; // E_SCFGRUN
  //! SET_CONFIGURATION's out-of-range arm. Its OWN program, not an offset
  //! into E_SCFGRUN's: an address that names an instruction inside another
  //! program drifts the moment a word is inserted above it, and
  //! scripts/check_upc_map.py now refuses a name that is not a place() target
  //! for exactly that reason. The refusal answers the four-byte body of
  //! §7.4.7.1 at cdl 16, like the other two arms.
  localparam logic [10:0] UPC_SCFGBAD_C  = 11'd1513; // E_SCFGBAD
  localparam logic [10:0] UPC_RDESCENT_C = 11'd1568; // E_RDESCENT
  localparam logic [10:0] UPC_STRT_C     = 11'd1600; // E_STRT
  localparam logic [10:0] UPC_STOP_C     = 11'd1632; // E_STOP
  localparam logic [10:0] UPC_STRMNS_C   = 11'd1664; // E_STRMNS
  localparam logic [10:0] UPC_STRMUNS_C  = 11'd1672; // E_STRMUNS
  localparam logic [10:0] UPC_STRMBAD_C  = 11'd1696; // E_STRMBAD
  //! MOVED with their microprograms: E_AMADD spans 34 words, so at 1632 it
  //! overlapped both E_STOP and E_STRMNS above. check_upc_map.py gates these
  //! against gen_ucode.py, so the two cannot drift apart again silently.
  localparam logic [10:0] UPC_AMADD_C    = 11'd1712; // E_AMADD
  localparam logic [10:0] UPC_AMREMOVE_C = 11'd1760; // E_AMREMOVE
  //! the name family, RENUMBERED at the setters merge: the #67 programs
  //! landed first on main and hold 1792..1939, so GET_NAME and the shared
  //! arms take the gaps between the setter slots and SET_NAME takes the
  //! tail (check_upc_map.py gates every constant against gen_ucode.py)
  localparam logic [10:0] UPC_GNAME_C    = 11'd1344; // E_GNAME
  localparam logic [10:0] UPC_SNAME_C    = 11'd1392; // E_SNAME
  localparam logic [10:0] UPC_NAMEERR_C  = 11'd1352; // E_NAMEERR
  localparam logic [10:0] UPC_NAMEBAD_C  = 11'd1384; // E_NAMEBAD
  //! the SET_STREAM_FORMAT twins (the store selector is a µcode immediate,
  //! so direction picks the program - the E_STRT/E_STOP reasoning), their
  //! dispatch-routed refusals, and SET_STREAM_INFO with its full-body
  //! short-command stub. E_SFCUR/E_SFZERO are branch targets inside the
  //! family, never dispatch entries, so they have no constant here.
  localparam logic [10:0] UPC_SFMTI_C    = 11'd1792; // E_SFMTI
  localparam logic [10:0] UPC_SFMTO_C    = 11'd1824; // E_SFMTO
  localparam logic [10:0] UPC_SINFO_C    = 11'd1856; // E_SINFO
  localparam logic [10:0] UPC_SFRUN_C    = 11'd1888; // E_SFRUN
  localparam logic [10:0] UPC_SFBAD_C    = 11'd1912; // E_SFBAD
  localparam logic [10:0] UPC_SIBAD_C    = 11'd1920; // E_SIBAD
  localparam logic [10:0] UPC_SIRUN_C    = 11'd1936; // E_SIRUN

  // ---- geometry -----------------------------------------------------------
  //! header 14 (Ethernet) + 24 (AECPDU) before the first payload byte
  localparam int unsigned ETH_HDR_C    = 14;
  localparam int unsigned AECP_HDR_C   = 24;
  localparam int unsigned FRAME_HDR_C  = ETH_HDR_C + AECP_HDR_C;      // 38
  localparam int unsigned ETH_MIN_C    = 60;
  //! response buffer: the µCPU's 12 header bytes + the 4-byte
  //! {configuration_index, reserved} prefix + one whole descriptor, rounded to
  //! the 8-byte lane the memory face moves
  localparam int unsigned RESP_BUF_C   = ((16 + LINE_BYTES_P) + 15) & ~32'd15;
  localparam int unsigned PLD_MAX_C    = RESP_BUF_C - 12;
  localparam int unsigned FRAME_MAX_C  = FRAME_HDR_C + PLD_MAX_C;

  if (FRAME_MAX_C > TX_OVERSIZE_BYTES_P) begin : gen_g_frame_fit
    $error("a maximum AECP response (%0d B) exceeds the oversize slot (%0d B)",
           FRAME_MAX_C, TX_OVERSIZE_BYTES_P);
  end

  if (RESP_BUF_C < ucpu_pkg::RESP_CAP_C) begin : gen_g_resp_cap_fit
    $error("response buffer (%0d B) is smaller than GET_DYNAMIC_INFO limit (%0d B)",
           RESP_BUF_C, ucpu_pkg::RESP_CAP_C);
  end

  pp_txn_t txn_w;
  assign txn_w = pp_txn_t'(txn_i);

  // ---- µCPU response-buffer face (served by KL_aecp_resp_buf below) -------
  logic        rb_we_w;
  logic  [9:0] rb_addr_w;
  logic [31:0] rb_wdata_w;
  logic  [3:0] rb_wstrb_w;
  logic        rb_ready_w;
  logic        urb_we_w, g_rb_we_w;
  logic  [9:0] urb_addr_w, g_rb_addr_w;
  logic [31:0] urb_wdata_w, g_rb_wdata_w;
  logic  [3:0] urb_wstrb_w, g_rb_wstrb_w;

  // ---- response-buffer lifecycle + payload read stream --------------------
  logic        rsp_open_w, rsp_seal_w;
  logic [10:0] rsp_seal_len_w;
  logic        rsp_rd_valid_w, rsp_rd_take_w;
  logic  [7:0] rsp_rd_data_w;
  logic        rsp_err_w, rsp_busy_w;

  // =======================================================================
  // the command machine
  // =======================================================================
  typedef enum logic [3:0] {
    A_IDLE, A_PLD, A_DISP, A_RUN, A_ALLOC, A_WR, A_CMT, A_TXW, A_FREE,
    A_GSCAN, A_GLOAD, A_GDEC, A_GHDR, A_GCOPY, A_GPATCH, A_GDONE
  } a_st_e;
  a_st_e a_st_r;

  pp_txn_t     cmd_r;
  logic [15:0] raw_ct_r;                 // AECPDU @22..@23 echoed verbatim
  logic [15:0] cfg_ix_r, desc_ty_r, desc_ix_r;
  logic [15:0] name_ix_r, name_cfg_r;
  logic [10:0] pld_cmd_r;                // command payload bytes
  logic [10:0] pld_r;                    // payload bytes to emit
  logic [10:0] walk_r;                   // payload walk index
  logic  [1:0] pid_lo_r;                 // AECPDU @26,@27 matched MVU's tail
  logic        echo_r, sent_r;
  logic        ctrs_r;                   // this command is a GET_COUNTERS
  logic        amap_r;                   // this command is a GET_AUDIO_MAP
  logic        amap_edit_r;              // this command edits the audio map
  logic        amap_remove_r;            // 0 ADD, 1 REMOVE
  logic        amap_uns_r;               // unsolicited reflection of staged edit
  logic        regun_r;                  // ... a REGISTER/DEREGISTER_UNSOL
  logic        acq_r;                    // ... an ACQUIRE_ENTITY
  logic        lockc_r;                  // ... a LOCK_ENTITY
  logic        gstri_r;                  // ... a GET_STREAM_INFO
  logic        gavb_r;                   // ... a GET_AVB_INFO
  logic        gasp_r;                   // ... a GET_AS_PATH
  logic        eavl_r;                   // ... an ENTITY_AVAILABLE
  logic        gcfg_r;                   // ... a GET_CONFIGURATION
  logic        gsfmt_r;                  // ... a GET_STREAM_FORMAT
  logic        gsrate_r;                 // ... a GET_SAMPLING_RATE
  logic        gclks_r;                  // ... a GET_CLOCK_SOURCE
  logic        ssrate_r;                 // ... a SET_SAMPLING_RATE
  logic        sclks_r;                  // ... a SET_CLOCK_SOURCE
  logic        ssfmt_r;                  // ... a SET_STREAM_FORMAT
  logic        ssinfo_r;                 // ... a SET_STREAM_INFO
  logic        gctrl_r;                  // ... a GET_CONTROL
  logic        sctrl_r;                  // ... a SET_CONTROL
  logic        gname_r;                  // ... a GET_NAME
  logic        sname_r;                  // ... a SET_NAME
  logic        scfg_r;                   // ... a SET_CONFIGURATION
  logic        strt_r;                   // ... a START_STREAMING
  logic        stop_r;                   // ... a STOP_STREAMING
  logic        strm_r;                   // ... either of the two
  logic        setc_r;                   // ... any SET_* that carries a value
  logic        gdi_r;                    // ... outer GET_DYNAMIC_INFO command
  //! the SET family's argument, walked out of @28..@35. Every settable field
  //! Milan v1.2 names fits in these eight bytes: a sampling rate is 4
  //! (§7.4.21.1), a clock source index is 2 (§7.4.23.1) and a stream format
  //! is 8 (§7.4.9.1). It is captured RIGHT-JUSTIFIED per command width by the
  //! walk below, because the µISA has no shift to justify it later.
  logic [63:0] setval_r;
  //! SET_STREAM_INFO's second capture: msrp_accumulated_latency sits at
  //! @48..@51 (Figure 7-40), past `setval_r`'s span, and for this command
  //! `setval_r`'s own top half holds the FLAGS word from @28. One more
  //! 32-bit register is the whole cost of reaching it; widening the shared
  //! capture to @51 for every SET would walk three commands' padding into
  //! live state instead.
  logic [31:0] silat_r;
  logic        lock_ent_ok_r;            // its target walked as ENTITY[0]
  logic        uns_r;                    // engine-originated unsolicited job
  logic  [7:0] amap_rec_r;               // records handed out this command
  logic [10:0] upc_r;
  logic [4:0]  status_r;
  logic [10:0] bidx_r;                   // frame byte being written
  logic [10:0] frame_len_r;
  logic        err_mode_r;               // rebuilding as ENTITY_MISBEHAVING
  logic [TXS_W_C-1:0] tx_slot_r;
  logic [15:0] cmd_cnt_r, resp_cnt_r, drop_cnt_r, rerr_cnt_r;

  // ---- GET_DYNAMIC_INFO two-pass iterator -------------------------------
  //! Pass 1 validates the complete record list before a getter runs. Pass 2
  //! loads one record, executes a supported getter through the same µprogram
  //! used by its standalone command, and appends the result. The RX slot is
  //! retained until the aggregate response is complete, so no duplicate
  //! payload RAM is required.
  logic        g_scan_started_r, g_rd_pending_r, g_load_data_r;
  logic  [2:0] g_hdr_ix_r;
  logic  [1:0] g_wr_phase_r;
  logic [10:0] g_total_r, g_rd_pos_r, g_data_ix_r;
  logic [10:0] g_data_start_r, g_next_pos_r;
  logic [10:0] g_out_r, g_rec_rlen_r, g_sub_end_r;
  logic [15:0] g_scan_len_r;
  logic  [7:0] g_scan_cmd_hi_r;
  logic [15:0] g_rec_len_r, g_rec_cmd_r;
  logic  [7:0] g_rec_cmd_status_r;
  logic [63:0] g_data_head_r;
  logic        g_rec_exec_r;
  logic  [4:0] g_rec_status_r;
  logic        g_shape_fault_r;

  function automatic logic gdi_allowed(input logic [15:0] command_type);
    unique case (command_type)
      OP_GET_CONFIG_C, OP_GET_STREAM_FMT_C, GDI_GET_VIDEO_FMT_C,
      GDI_GET_SENSOR_FMT_C, OP_GET_STREAM_INFO_C, OP_GET_NAME_C,
      GDI_GET_ASSOC_ID_C, OP_GET_SAMP_RATE_C, OP_GET_CLOCK_SRC_C,
      GDI_GET_SIGNAL_SEL_C, OP_GET_COUNTERS_C, GDI_GET_MEM_LEN_C,
      GDI_GET_STREAM_BKUP_C: gdi_allowed = 1'b1;
      default:              gdi_allowed = 1'b0;
    endcase
  endfunction

  logic        g_sub_exec_w;
  logic [10:0] g_sub_rlen_w, g_sub_upc_w;
  logic  [4:0] g_sub_status_w;
  logic [15:0] g_sub_type_w;
  assign g_sub_type_w = g_data_head_r[63:48];

  //! A malformed fixed getter is represented exactly as its standalone
  //! BAD_ARGUMENTS echo: the record status changes and its supplied command
  //! data is copied. Wrong-target fixed responses retain the full response
  //! shape where the standalone command does.
  always_comb begin : gdi_subcommand_decode
    g_sub_exec_w   = 1'b0;
    g_sub_rlen_w   = 11'(g_rec_len_r);
    g_sub_upc_w    = UPC_NOTIMPL_C;
    g_sub_status_w = ST_NOT_SUPPORTED_C;
    unique case (g_rec_cmd_r)
      OP_GET_CONFIG_C: begin
        g_sub_exec_w = 1'b1; g_sub_rlen_w = 11'd4;
        g_sub_upc_w = UPC_GCFG_C;
      end
      OP_GET_STREAM_FMT_C: begin
        if (g_rec_len_r < 16'd4) g_sub_status_w = ST_BAD_ARGUMENTS_C;
        else begin
          g_sub_exec_w = 1'b1; g_sub_rlen_w = 11'd12;
          g_sub_upc_w = ((g_sub_type_w == DT_STREAM_INPUT_C)
                         || (g_sub_type_w == DT_STREAM_OUTPUT_C))
                        ? UPC_GSFMT_C : UPC_TIZ8NS_C;
        end
      end
      OP_GET_STREAM_INFO_C: begin
        if (g_rec_len_r < 16'd4) g_sub_status_w = ST_BAD_ARGUMENTS_C;
        else if ((g_sub_type_w != DT_STREAM_INPUT_C)
                 && (g_sub_type_w != DT_STREAM_OUTPUT_C)) begin
          g_sub_status_w = ST_NOT_SUPPORTED_C;
        end else begin
          g_sub_exec_w = 1'b1; g_sub_rlen_w = 11'd56;
          g_sub_upc_w = UPC_GSTRI_C;
        end
      end
      OP_GET_SAMP_RATE_C: begin
        if (g_rec_len_r < 16'd4) g_sub_status_w = ST_BAD_ARGUMENTS_C;
        else begin
          g_sub_exec_w = 1'b1; g_sub_rlen_w = 11'd8;
          g_sub_upc_w = (g_sub_type_w == DT_AUDIO_UNIT_C)
                        ? UPC_GSRATE_C : UPC_TIZ4NS_C;
        end
      end
      OP_GET_CLOCK_SRC_C: begin
        if (g_rec_len_r < 16'd4) g_sub_status_w = ST_BAD_ARGUMENTS_C;
        else begin
          g_sub_exec_w = 1'b1; g_sub_rlen_w = 11'd8;
          g_sub_upc_w = (g_sub_type_w == DT_CLOCK_DOMAIN_C)
                        ? UPC_GCLKS_C : UPC_TIZ4NS_C;
        end
      end
      OP_GET_NAME_C: begin
        if (g_rec_len_r < 16'd8) g_sub_status_w = ST_BAD_ARGUMENTS_C;
        else begin
          g_sub_exec_w = 1'b1; g_sub_rlen_w = 11'd72;
          g_sub_upc_w = UPC_GNAME_C;
        end
      end
      OP_GET_COUNTERS_C: begin
        if (g_rec_len_r < 16'd4) g_sub_status_w = ST_BAD_ARGUMENTS_C;
        else begin
          g_sub_exec_w = 1'b1; g_sub_rlen_w = 11'd136;
          g_sub_upc_w = ((g_sub_type_w == DT_STREAM_INPUT_C)
                         || (g_sub_type_w == DT_STREAM_OUTPUT_C)
                         || (g_sub_type_w == DT_AVB_INTERFACE_C)
                         || (g_sub_type_w == DT_CLOCK_DOMAIN_C))
                        ? UPC_GCTRS_C : UPC_GCTRSNS_C;
        end
      end
      default: ;
    endcase
    //! info_status is a record field, not a structural delimiter. A command
    //! must supply SUCCESS, but a bad value leaves the following record
    //! parseable. IEEE 1722.1-2021 7.4.76.1 says every element is handled as
    //! an independent command, so contain this error to the record and copy
    //! its command data in the BAD_ARGUMENTS response.
    if (g_rec_cmd_status_r != 8'd0) begin
      g_sub_exec_w   = 1'b0;
      g_sub_rlen_w   = 11'(g_rec_len_r);
      g_sub_upc_w    = UPC_NOTIMPL_C;
      g_sub_status_w = ST_BAD_ARGUMENTS_C;
    end
  end
  //! An ADD/REMOVE_AUDIO_MAPPINGS command can carry at most 63 records:
  //! IEEE 1722.1-2021 9.2.2.6 caps command control_data_length at 524, and
  //! Figure 7-71 uses 20 + 8*N octets. Milan v1.2 5.4.1 lifts that limit for
  //! responses only. Keep a full byte-written copy so validation and commit
  //! walk the identical record set without rereading or releasing the slot.
  //! The 256-entry address space matches the µCPU iterator width and leaves
  //! the port contract independent of the configured RX slot size.
  (* ram_style = "block" *) logic [63:0] amap_stage_r [0:255];
  logic [63:0] amap_stage_q_r;
  logic [63:0] amap_stage_assem_r;
  logic        amap_stage_ready_r;
  logic  [7:0] amap_rsp_count_r;
  logic  [7:0] amap_rx_count_w;
  logic [10:0] amap_edit_pld_w;
  logic        amap_stage_ser_w, amap_stage_ser_load_w;
  logic        amap_stage_edit_load_w, amap_stage_name_load_w;
  logic        amap_stage_rd_en_w;
  logic  [7:0] amap_stage_raddr_w;

  //! A malformed command can still carry complete mapping records. Figure
  //! 7-71 requires the response count to describe the records actually put on
  //! the wire, never the untrusted command count. A short fixed part yields a
  //! well-formed eight-byte response body with zero records.
  assign amap_rx_count_w = (pld_cmd_r >= 11'd8)
                           ? 8'((pld_cmd_r - 11'd8) >> 3) : 8'd0;
  assign amap_edit_pld_w = 11'd8 + ({3'd0, amap_rsp_count_r} << 3);

  // ---- opcode decode = the dispatch step (see the banner) -----------------
  logic [10:0] upc_w;
  logic        echo_w, short_w, short_ct_w, short_am_w, ctrs_w, amap_w, aem_w;
  logic        gdi_w, amap_edit_w, amap_remove_w;
  //! a READ_DESCRIPTOR must carry configuration_index + reserved +
  //! descriptor_type + descriptor_index; a shorter one is BAD_ARGUMENTS, never
  //! a locate of whatever zeros happened to be there
  assign short_w = (txn_w.cdl < 11'd20);
  //! §7.4.42.1's command payload is descriptor_type + descriptor_index and
  //! nothing else, so cdl 16 is the whole command (F06.14's offset-from-@12)
  assign short_ct_w = (txn_w.cdl < 11'd16);
  //! §7.4.44.1's command runs through the reserved word at @30, so cdl 20 is
  //! the whole command; shorter never reached map_index and is BAD_ARGUMENTS
  assign short_am_w = (txn_w.cdl < 11'd20);
  //! and it must really BE an AEM command: the 03 §4 record fills `opcode`
  //! from AECPDU @22..@23, which on a VENDOR_UNIQUE message is the first two
  //! bytes of a 48-bit protocol_id, not a command_type at all
  assign ctrs_w = aem_w
                  && (txn_w.opcode == OP_GET_COUNTERS_C) && !short_ct_w;
  assign amap_w = aem_w
                  && (txn_w.opcode == OP_GET_AUDIO_MAP_C) && !short_am_w;
  assign gdi_w  = aem_w && (txn_w.opcode == OP_GET_DYNAMIC_INFO_C);
  //! The editing pair is re-dispatched after the payload walk, when the
  //! descriptor type, record count and exact variable length are registered.
  //! Keeping it out of this pop-time mux preserves the measured ROM-address
  //! timing rule used by every other variable-shape command.
  assign amap_edit_w = aem_w
                       && ((txn_w.opcode == OP_ADD_AUDIO_MAP_C)
                           || (txn_w.opcode == OP_REMOVE_AUDIO_MAP_C));
  //! THE GUARD BELONGS ON EVERY ARM, and for a long time it was on only some.
  //! `opcode` is AECPDU @22..@23, which on a VENDOR_UNIQUE message is the first
  //! two bytes of a 48-bit protocol_id. OP_READ_DESCRIPTOR_C is 0x0004, so a
  //! vendor protocol_id of 00-04-xx-xx-xx-xx collided with it and was answered
  //! with a 354-byte VENDOR_UNIQUE_RESPONSE carrying our ENTITY descriptor,
  //! its protocol_id partly overwritten by READ_DESCRIPTOR's own fields.
  //! §9.3.5.3.3 asks for "a correctly sized response and a status of
  //! NOT_IMPLEMENTED"; echoing the command WHOLE is this engine's choice, not
  //! a mandate — Clause 9 has no echo language, and §9.3.5.3.3 is itself
  //! AEM-scoped, so it is this engine's convention that carries the refusals
  //! for VENDOR_UNIQUE, AVC and EXTENDED.
  //!
  //! AND ONE SILENCE, recorded for the same reason: NOT_IMPLEMENTED is an
  //! explicit, table-backed status for message types 2, 4, 6 and 8, but
  //! Table 9-1's reserved 10..13 band and EXTENDED_COMMAND (14) have no PDU
  //! format, no state machine and no per-type status table (Table 9-2 gives
  //! NOT_IMPLEMENTED on the common header, but Table 9-1 lists 11 and 13 as
  //! RESERVED, not as response types).
  //! Answering them 11/13/15 + NOT_IMPLEMENTED is UNSPECIFIED rather than
  //! conformant-by-clause. It is the only coherent thing to do with a type
  //! that has no definition, and far better than the mis-dispatch it
  //! replaces, but the tests below pin it as this engine's contract, not as
  //! the standard's.
  //!
  //! KNOWN DEVIATION, recorded rather than hidden: §9.7.4 says an HDCP APM
  //! refusal sets hdcp_apm_length to zero and sends nothing after
  //! hdcp_apm_fragment_offset. This engine echoes message_type 8 whole like
  //! every other refusal. NOT_IMPLEMENTED is the right status (Table 9-8) and
  //! a uniform echo is a large improvement on the mis-dispatch it replaces,
  //! but the body shape is not what §9.7.4 specifies.
  //!
  //! 00:04:xx is a densely assigned OUI block, so this was reachable on a real
  //! link. It is a CLASS, and the class is this dispatch's own opcode list:
  //! 0x0026 IDENTIFY_NOTIFICATION, 0x0029 GET_COUNTERS and 0x002B
  //! GET_AUDIO_MAP collide the same way. Issue #83.
  //!
  //! WHY THE TESTS FOR THIS ARE HARD TO GET RIGHT, and why the class is now
  //! bounded rather than hoped about. Two arms re-dispatch on payload CONTENT,
  //! so a sweep that sends filler bytes cannot reach them and their guards go
  //! untested — that cost two review rounds, once for SET_SAMPLING_RATE and
  //! again for GET_AUDIO_MAP. The bound: `UPC_NOTIMPL_C` is assigned at
  //! exactly TWO places, the pop-time default below and the audio-map
  //! wrong-type arm, so only the latter can emit a refusal byte-identical to
  //! the correct one. Every other type-invalid stub differs on the wire and is
  //! therefore visible to the sweep. If a third such stub is ever added, its
  //! arm needs a real payload in tb/pp_top's M9 table.
  //!
  //! AEM AND NOTHING ELSE. `PP_PROTO_AEM` is the RX validator's RESIDUAL
  //! bucket (KL_pp_rx_validator.sv: 6/7 -> MVU, 2/3 -> AA, everything else
  //! here), so it also carries AVC_COMMAND (4), HDCP_APM_COMMAND (8), the
  //! reserved 10..13 band and EXTENDED_COMMAND (14) -- Table 9-1 types that
  //! have no command_type at @22..@23 at all. Figure 9-9 puts `avc_length`
  //! there, and an ordinary AV/C length of 20 is OP_SET_SAMP_RATE_C: guarding
  //! on the bucket alone let an AV/C command WRITE THE SAMPLING RATE and
  //! answer SUCCESS. Guarding on message_type 0 is the actual question.
  assign aem_w  = (txn_w.protocol == PP_PROTO_AEM) && (txn_w.msg_type == 4'd0);
  assign amap_remove_w = aem_w && (txn_w.opcode == OP_REMOVE_AUDIO_MAP_C);
  always_comb begin : dispatch_decode
    if (aem_w && (txn_w.opcode == OP_READ_DESCRIPTOR_C) && !short_w) begin
      upc_w  = UPC_RDESC_C;
      echo_w = 1'b0;
    end else if (ctrs_w) begin
      upc_w  = UPC_GCTRS_C;
      echo_w = 1'b0;
    end else if (amap_w) begin
      upc_w  = UPC_GAMAP_C;
      echo_w = 1'b0;
    end else if (aem_w
                 && ((txn_w.opcode == OP_IDENTIFY_NOTIF_C)
                     || ((txn_w.opcode == OP_READ_DESCRIPTOR_C) && short_w)
                     || ((txn_w.opcode == OP_GET_COUNTERS_C) && short_ct_w)
                     || ((txn_w.opcode == OP_GET_AUDIO_MAP_C) && short_am_w))) begin
      upc_w  = UPC_BADARG_C;
      echo_w = 1'b1;
    end else begin
      upc_w  = UPC_NOTIMPL_C;
      echo_w = 1'b1;
    end
  end

  //! F06.2 MATCHED arc + the response-storm guard (see the banner)
  logic drop_w;
  assign drop_w = txn_w.msg_type[0] || (txn_w.target_eid != entity_id_i);

  //! the registration pair's DISCRIMINATOR - latched at pop like ctrs_w /
  //! amap_w but feeding only its own flop, the walk-capture enables and the
  //! A_PLD-exit re-dispatch, never the pop-time µPC mux (the timing rule in
  //! the opcode table above)
  logic regun_w, acq_w, lockc_w;
  assign regun_w = aem_w
                   && ((txn_w.opcode == OP_REG_UNSOL_C)
                       || (txn_w.opcode == OP_DEREG_UNSOL_C));
  assign acq_w   = aem_w
                   && (txn_w.opcode == OP_ACQUIRE_C);
  assign lockc_w = aem_w
                   && (txn_w.opcode == OP_LOCK_C);
  logic gstri_w, gavb_w, gasp_w;
  assign gstri_w = aem_w
                   && (txn_w.opcode == OP_GET_STREAM_INFO_C);
  assign gavb_w  = aem_w
                   && (txn_w.opcode == OP_GET_AVB_INFO_C);
  assign gasp_w  = aem_w
                   && (txn_w.opcode == OP_GET_AS_PATH_C);
  //! ...and the read-side set's five, on the same terms
  logic eavl_w, gcfg_w, gsfmt_w, gsrate_w, gclks_w;
  assign eavl_w   = aem_w
                    && (txn_w.opcode == OP_ENTITY_AVAIL_C);
  assign gcfg_w   = aem_w
                    && (txn_w.opcode == OP_GET_CONFIG_C);
  assign gsfmt_w  = aem_w
                    && (txn_w.opcode == OP_GET_STREAM_FMT_C);
  assign gsrate_w = aem_w
                    && (txn_w.opcode == OP_GET_SAMP_RATE_C);
  assign gclks_w  = aem_w
                    && (txn_w.opcode == OP_GET_CLOCK_SRC_C);
  //! ...and the SET pair. `setc_w` is the shared "this command carries a
  //! value at @28" term the payload walk keys on, so a command joining the
  //! family is one name here and one arm at the A_PLD exit.
  logic ssrate_w, sclks_w, setc_w;
  assign ssrate_w = aem_w
                    && (txn_w.opcode == OP_SET_SAMP_RATE_C);
  assign sclks_w  = aem_w
                    && (txn_w.opcode == OP_SET_CLOCK_SRC_C);
  logic gctrl_w, sctrl_w;
  assign gctrl_w  = aem_w
                    && (txn_w.opcode == OP_GET_CONTROL_C);
  assign sctrl_w  = aem_w
                    && (txn_w.opcode == OP_SET_CONTROL_C);
  logic gname_w, sname_w;
  assign gname_w  = aem_w && (txn_w.opcode == OP_GET_NAME_C);
  assign sname_w  = aem_w && (txn_w.opcode == OP_SET_NAME_C);
  //! SET_STREAM_FORMAT and SET_STREAM_INFO join the value-at-@28 family:
  //! for the format that IS the argument (8 bytes, lands right-justified);
  //! for SET_STREAM_INFO the eight bytes hold the FLAGS word at the top and
  //! the argument itself rides the dedicated @48 capture (`silat_r`).
  logic ssfmt_w, ssinfo_w;
  assign ssfmt_w  = aem_w
                    && (txn_w.opcode == OP_SET_STREAM_FMT_C);
  assign ssinfo_w = aem_w
                    && (txn_w.opcode == OP_SET_STREAM_INFO_C);
  assign setc_w   = ssrate_w | sclks_w | sctrl_w | ssfmt_w | ssinfo_w;
  logic scfg_w;
  assign scfg_w   = aem_w
                    && (txn_w.opcode == OP_SET_CONFIG_C);
  //! Milan §5.4.2.19/.20. `strm_w` is the shared "this command moves the
  //! started/stopped bit" term; the two are told apart only where the
  //! direction matters, so a third such command would be one name here.
  logic strt_w, stop_w, strm_w;
  assign strt_w   = aem_w
                    && (txn_w.opcode == OP_START_STRM_C);
  assign stop_w   = aem_w
                    && (txn_w.opcode == OP_STOP_STRM_C);
  assign strm_w   = strt_w | stop_w;

  //! ---- unsolicited job synthesis (06 §6.7) -------------------------------
  //! kind -> {command_type, µPC}. A kind whose µprogram has not landed maps
  //! to E_NOSEND: the job retires without a frame (counted as a drop) rather
  //! than emitting a well-formed response with an invented empty body.
  logic [15:0] uns_ct_w;
  logic [10:0] uns_upc_w;
  always_comb begin : uns_kind_map
    unique case (uns_kind_i)
      PP_UNS_DEREG_C: begin uns_ct_w = OP_DEREG_UNSOL_C; uns_upc_w = UPC_UNSOK_C;   end
      PP_UNS_LOCK_C:  begin uns_ct_w = OP_LOCK_C;        uns_upc_w = UPC_LOCKUNS_C; end
      PP_UNS_STRI_C:  begin uns_ct_w = OP_GET_STREAM_INFO_C;
                            uns_upc_w = UPC_GSTRI_C;   end
      PP_UNS_AVB_C:   begin uns_ct_w = OP_GET_AVB_INFO_C;
                            uns_upc_w = UPC_GAVB_C;    end
      PP_UNS_ASP_C:   begin uns_ct_w = OP_GET_AS_PATH_C;
                            uns_upc_w = UPC_GASP_C;    end
      PP_UNS_AMAP_C:  begin uns_ct_w = uns_amap_remove_i
                                         ? OP_REMOVE_AUDIO_MAP_C
                                         : OP_ADD_AUDIO_MAP_C;
                            uns_upc_w = UPC_UNSOK_C;   end
      PP_UNS_CTRS_C:  begin uns_ct_w = OP_GET_COUNTERS_C;
                            uns_upc_w = UPC_GCTRS_C;   end
      PP_UNS_SRATE_C: begin uns_ct_w = OP_SET_SAMP_RATE_C;
                            uns_upc_w = UPC_GSRATE_C;  end
      PP_UNS_NAME_C:  begin uns_ct_w = OP_SET_NAME_C;
                            uns_upc_w = UPC_GNAME_C;   end
      PP_UNS_CFG_C:   begin uns_ct_w = OP_SET_CONFIG_C;
                            uns_upc_w = UPC_GCFG_C;    end
      PP_UNS_SFMT_C:  begin uns_ct_w = OP_SET_STREAM_FMT_C;
                            uns_upc_w = UPC_GSFMT_C;   end
      PP_UNS_SINFO_C: begin uns_ct_w = OP_SET_STREAM_INFO_C;
                            uns_upc_w = UPC_GSTRI_C;   end
      PP_UNS_CTRL_C:  begin uns_ct_w = OP_SET_CONTROL_C;
                            uns_upc_w = UPC_GCTRL_C;   end
      PP_UNS_CLKS_C:  begin uns_ct_w = OP_SET_CLOCK_SRC_C;
                            uns_upc_w = UPC_GCLKS_C;   end
      PP_UNS_STRM_C:  begin uns_ct_w = uns_arg0_i[0] ? OP_STOP_STRM_C
                                                      : OP_START_STRM_C;
                            uns_upc_w = UPC_STRMUNS_C; end
      default:        begin uns_ct_w = 16'd0;            uns_upc_w = UPC_NOSEND_C;  end
    endcase
  end


  //! the MVU sub-decode (see the banner): read at the A_PLD exit, where the
  //! four captured words below are settled. `pid_lo_r` is the only new state
  //! the match needs — @22..@25 and @28..@29 already have registers, held for
  //! the header echo and for READ_DESCRIPTOR's operands — and it is two
  //! comparison RESULTS rather than the two bytes, so a walk that stops before
  //! @27 leaves it 0 and cannot look like a match.
  logic mvu_get_milan_info_w;
  assign mvu_get_milan_info_w = (cmd_r.protocol == PP_PROTO_MVU)
                                && (pld_cmd_r  >= MVU_CMD_PLD_C)
                                && (raw_ct_r   == MVU_PID_HI_C)
                                && (cfg_ix_r   == MVU_PID_MD_C)
                                && (pid_lo_r   == 2'b11)
                                && (desc_ty_r  == MVU_GET_MILAN_INFO_C);

  // ---- payload sizing ------------------------------------------------------
  //! cdl is the offset-from-@12 length (F06.14), so the command payload is
  //! cdl - 12; the buffer cap and the committed slot length are the two hard
  //! ceilings. The slot arm can only be read once `rxs_rd_slot_o` names this
  //! command's slot (`slot_len_o` is indexed by `rd_slot_i`), so it is applied
  //! on the first walk cycle rather than at pop.
  //! An RX slot holds the AVTPDU, NOT the Ethernet frame: KL_pp_rx_validator
  //! starts writing at frame byte 14, so slot byte k IS AECPDU byte k and the
  //! payload begins at slot byte 24.
  logic [10:0] cdl_pld_w, slot_pld_w, pld_cap_w, pld_trim_w;
  assign cdl_pld_w  = (txn_w.cdl > 11'd12) ? (txn_w.cdl - 11'd12) : 11'd0;
  assign pld_cap_w  = (cdl_pld_w > 11'(PLD_MAX_C)) ? 11'(PLD_MAX_C) : cdl_pld_w;
  assign slot_pld_w = (32'(rxs_slot_len_i) > 32'(AECP_HDR_C))
                      ? 11'(32'(rxs_slot_len_i) - 32'(AECP_HDR_C)) : 11'd0;
  assign pld_trim_w = (pld_r > slot_pld_w) ? slot_pld_w : pld_r;

  // ---- the µCPU ------------------------------------------------------------
  logic        disp_valid_r;
  logic        disp_ready_w, ucpu_busy_w, ucpu_done_w;
  logic        resp_send_w;
  logic [10:0] resp_len_w;
  logic  [4:0] resp_status_w;
  logic [63:0] opd0_w, opd1_w;

  //! r14 = {--, descriptor_index, descriptor_type, configuration_index}: the
  //! low 16 bits are the field BUILD_FIELD emits at @24 and [47:0] is the
  //! store's locate key. r13 = {--, descriptor_type, descriptor_index}: the
  //! 4-byte {type, index} stub IEEE §7.4.5 wants on a failed READ_DESCRIPTOR
  //! (the µISA has no shift, so every field a µprogram emits has to arrive
  //! right-justified in some register).
  //! GET_COUNTERS rides the SAME two shapes as GET_STREAM_INFO now that its
  //! program opens with the store locate: r14 is the locate key and r13
  //! packs {descriptor_type, descriptor_index} so one FMT_D BUILD_FLD lays
  //! @24..@27 in wire order.
  //! GET_AUDIO_MAP is the one shape that needs a mux, because its µprogram
  //! consumes the registers TWO ways at once: r14 is the store's locate key
  //! ({index, type, cfg} - GET_AUDIO_MAP names no configuration_index, and
  //! the locate keys on 0 because the shipping image declares ONE
  //! configuration. That used to be justified by SET_CONFIGURATION being
  //! unimplemented; it now stores an index, and E_RDESCENT overlays the ENTITY
  //! descriptor so GET_CONFIGURATION and the descriptor agree. This key is
  //! still a literal 0, so on a multi-configuration image THIS command would
  //! stay pinned to configuration 0 while both of those expose the active
  //! index, the next thing to revisit when a second configuration ships),
  //! and r13 packs
  //! {descriptor_index, map_index} so ONE
  //! FMT_D BUILD_FLD lays @26..@29 in wire order while r13[15:0] is the
  //! right-justified map_index CHECK_ARG compares (the µISA has no shift).
  //! `desc_ty_r` holds map_index for this command - see the payload walk.
  //! The muxes below land in opd0_r/opd1_r on the A_DISP cycle that raises
  //! the dispatch strobe (stage-0 pipeline: operand shaping must reach the
  //! µCPU's register file from flops, never as a live mux cone - the walk
  //! registers are settled a full state earlier, so the latch costs nothing)
  //! ONE registered term for the §7.4.42.1 {descriptor_type @24,
  //! descriptor_index @26} command shape, which is now seven commands wide.
  //! It selects the operand packing below AND the walk-capture arms, so a
  //! command joining the shape is one name in one place rather than the same
  //! OR chain re-spelled in four - and the chain is built once instead of
  //! four times, which is the reason it exists and not just how it reads.
  logic [63:0] opd2_w;
  //! ---- the running predicate, reduced (Milan §5.3.7.3) ---------------
  //! §5.4.2.5's refusal is a REDUCTION over every stream — "if ONE OF the
  //! Stream Input is bound or ONE OF the Stream Output is streaming" — not a
  //! test of the descriptor a command names.
  logic any_running_w;
  assign any_running_w = (|strm_bound_i) || (|strm_streaming_i);
  //! ...and the PER-DESCRIPTOR form, shared by SET_STREAM_FORMAT (Milan
  //! §5.4.2.7 refuses a bound Stream Input or a streaming Stream Output)
  //! and SET_STREAM_INFO (§5.4.2.9 refuses a streaming Stream Output; its
  //! type route guarantees the output arm is the one consulted): the SAME
  //! vectors, indexed by the descriptor the command walked. §5.3.7.3 makes
  //! "running" bound for a Stream Input and streaming for a Stream Output.
  //! The range guard keeps an out-of-shape index from wrapping onto a live
  //! stream's bit; such an index is not running, and the µprogram's locate
  //! then answers NO_SUCH_DESCRIPTOR for it.
  logic run_this_w;
  assign run_this_w =
      (cfg_ix_r == DT_STREAM_INPUT_C)
        ? ((32'(desc_ix_r) < N_STREAM_IN_P)
           && 1'(strm_bound_i >> desc_ix_r))
        : ((32'(desc_ix_r) < N_STREAM_OUT_P)
           && 1'(strm_streaming_i >> desc_ix_r));

  //! the @26..@27 capture set. `tix_w` is the {type @24, index @26} SHAPE;
  //! SET_CONFIGURATION is not that shape (§7.4.7.1 puts `reserved` at @24) but
  //! it DOES take its argument from @26, so it joins the capture without
  //! joining the shape. Conflating the two is what made the first cut of this
  //! command store configuration 0 forever: `scfg_r` was in neither guard, so
  //! @26 was never captured AND a padded command walked @30 into the same
  //! register.
  logic ix26_w;
  logic tix_w;
  assign tix_w = ctrs_r | amap_r | amap_edit_r | gstri_r | gavb_r
                 | gsfmt_r | gsrate_r | gclks_r | setc_r | gctrl_r
                 | strm_r | ssfmt_r | ssinfo_r | gname_r | sname_r;
  assign ix26_w = tix_w | regun_r | lockc_r | scfg_r;
  assign opd0_w = (gname_r || sname_r)
                              ? {16'd0, desc_ix_r, cfg_ix_r, name_cfg_r}
                : tix_w       ? {16'd0, desc_ix_r, cfg_ix_r, 16'd0}
                : gasp_r      ? {16'd0, cfg_ix_r, DT_AVB_INTERFACE_C, 16'd0}
                : lockc_r     ? {32'd0, cfg_ix_r, desc_ix_r}
                              : {16'd0, desc_ix_r, desc_ty_r, cfg_ix_r};
  assign opd1_w = (gname_r || sname_r)   ? {cfg_ix_r, desc_ix_r,
                                             name_ix_r, name_cfg_r}
                : amap_r                 ? {32'd0, desc_ix_r, desc_ty_r}
                : tix_w                  ? {32'd0, cfg_ix_r, desc_ix_r}
                : gasp_r                 ? {48'd0, cfg_ix_r}
                : scfg_r                 ? {48'd0, desc_ix_r}
                                         : {32'd0, desc_ty_r, desc_ix_r};

  //! r12, the SET argument, re-justified per command. `setval_r` holds
  //! @28..@35 big-endian, so an 8-byte field is already right-justified and a
  //! narrower one has to be taken from the TOP. This is the one place that
  //! knows a rate is four bytes and a clock-source index is two, and it is
  //! here rather than in the µcode because the µISA has no shift.
  //! SET_CONFIGURATION's argument is not at @28 like the rest of the family:
  //! §7.4.7.1 puts `reserved` at @24 and `configuration_index` at @26, so the
  //! value is what the walk already captured into `desc_ix_r` and there is
  //! nothing to justify.
  assign opd2_w = (gname_r || sname_r) ? {48'd0, name_ix_r}
                : amap_edit_r ? {48'd0, desc_ty_r}
                : ssrate_r ? {32'd0, setval_r[63:32]}
                : sclks_r  ? {48'd0, setval_r[63:48]}
                : sctrl_r  ? {56'd0, setval_r[63:56]}
                : scfg_r   ? {48'd0, desc_ix_r}
                : ssinfo_r ? {32'd0, silat_r}
                           : setval_r;

  logic [63:0] opd0_r, opd1_r, opd2_r;

  logic        st_req_w, st_we_w, st_name_w;
  logic [19:0] st_addr_w;
  logic [63:0] st_wdata_w, st_rdata_w;
  logic  [7:0] st_wstrb_w;
  logic        st_ready_w, st_rvalid_w, st_err_w;

  //! ---- the state port has TWO slaves now (06 §8) ------------------------
  //! Regions 0x1 and 0x2 are the dynamic-state store's value and valid-flag
  //! views; everything else — RGN_DATA 0x0, NBASE 0xC, NCFG 0xD, LEN 0xE,
  //! LOCATE 0xF — is the descriptor store's. The select is combinational off
  //! the address, and that is safe because the µCPU HOLDS a request until its
  //! answer, so the address cannot move between request and response.
  //!
  //! `st_name_i` OUTRANKS the region: the name table is selected in any
  //! region (07 §3.4), so a NAME_RD/NAME_WR always belongs to the descriptor
  //! store even though its region nibble may read 0x1.
  //!
  //! The request is GATED rather than broadcast, because the descriptor
  //! store's region decode treats every unmapped code as RGN_DATA — an
  //! ungated dynamic-state read would come back as a descriptor-line read of
  //! whatever lane the field selector happened to alias.
  //! Region 0x3 is the started/stopped REQUEST channel (Milan §5.4.2.19/.20).
  //! It is WRITE-ONLY and backs no storage: a WRITE_ST here becomes one pulse
  //! to the ACMP listener, which owns `f_started` in the binding record. The
  //! dynamic-state store used to hold a copy (selector 6) and it is retired,
  //! because two writable copies of one bit disagree silently — both answer a
  //! plausible 0 or 1, and Milan §5.3.8.7 makes the state a property of the
  //! BINDING ("undefined when the Stream Input is not bound"), which only the
  //! record has. A read of this region is not a thing: it is gated to writes
  //! below, so a µprogram that tries to read it back gets the descriptor
  //! store's answer and not a stale bit that looks authoritative.
  localparam logic [3:0] RGN_DYN_C  = 4'h1;
  localparam logic [3:0] RGN_DYNV_C = 4'h2;
  localparam logic [3:0] RGN_STRQ_C = 4'h3;

  logic        dyn_sel_w;
  logic        strq_sel_w;
  logic        dyn_ready_w, dyn_rvalid_w;
  logic [63:0] dyn_rdata_w;
  logic        store_ready_w, store_rvalid_w, store_err_w;
  logic [63:0] store_rdata_w;

  assign dyn_sel_w = !st_name_w
                     && ((st_addr_w[19:16] == RGN_DYN_C)
                         || (st_addr_w[19:16] == RGN_DYNV_C));
  //! `st_we_w` is part of the select, not a qualifier applied later: without
  //! it a READ of region 3 would be claimed by a channel that never answers
  //! and the µCPU would hang waiting for an rvalid that cannot come.
  assign strq_sel_w = !st_name_w && st_we_w
                      && (st_addr_w[19:16] == RGN_STRQ_C);
  //! WHY THE REGION NIBBLE SURVIVES THE LOCATE. `WRITE_ST` addresses as
  //! `desc_base_r + imm`, and these µprograms run a DESC_ADDR first (that is
  //! the existence check), so it is fair to ask what the base holds by the
  //! time the write issues. The answer is ZERO: KL_aecp_desc_store answers a
  //! locate with `st_rdata_o = 0` (its port comment says so in as many
  //! words - "read data (0 on a locate hit)"), and `desc_base_r` is loaded
  //! from exactly that, so the sum is the immediate. That is the invariant
  //! this decode rests on, and it is stronger than "the offset is 16 bits" -
  //! a 16-bit NON-ZERO base would still be safe here only by accident of
  //! RGN_STRQ's low bits being clear. If the store ever answers a locate
  //! with a real address, this decode has to move with it: a base reaching
  //! [19:16] would divert the request to the descriptor store, drop it, and
  //! leave the command answering SUCCESS for a change that never landed.

  //! The request channel answers its own write in the same cycle it is
  //! selected. It has nothing to wait for — the pulse below is the whole of
  //! the side effect — and leaving it to the descriptor store would BOTH
  //! deadlock (the store never sees a request it was not given) and let the
  //! store's region decode read the write as a descriptor line.
  //! The request channel completes the µprogram's WRITE_ST only when the
  //! record has TAKEN it. Answering ready unconditionally would drop the
  //! request whenever the listener's walker happened to be busy, and the
  //! µprogram has already settled SUCCESS by then — a false success that no
  //! response-shape check can see, because the response is correct and only
  //! the effect is missing.
  assign st_ready_w  = strq_sel_w ? strm_set_ready_i
                     : dyn_sel_w  ? dyn_ready_w  : store_ready_w;
  assign st_rvalid_w = strq_sel_w ? 1'b0
                     : dyn_sel_w  ? dyn_rvalid_w : store_rvalid_w;
  assign st_rdata_w  = dyn_sel_w ? dyn_rdata_w  : store_rdata_w;

  //! ---- the started/stopped pulse (Milan §5.4.2.19 / §5.4.2.20) -----------
  //! One cycle, on the beat the µprogram's WRITE_ST is accepted, carrying the
  //! descriptor index the command named and the bit it asked for. The listener
  //! decides whether it applies: §5.4.2.19's "this command has no effect on a
  //! Stream Input that is not already bound" is the RECORD's rule, and asking
  //! the engine to test boundness first would give it a second copy of exactly
  //! the state this change exists to keep in one place.
  assign strm_set_valid_o = strq_sel_w && st_req_w;
  assign strm_set_index_o = desc_ix_r;
  assign strm_set_val_o   = st_wdata_w[0];
  //! the dynamic store has no locate and therefore no miss: an out-of-range
  //! index answers a CLEAR valid flag, not NO_SUCH_DESCRIPTOR, because
  //! existence is the descriptor image's ruling and never a setting's
  assign st_err_w    = strq_sel_w ? strm_set_error_i
                     : dyn_sel_w  ? 1'b0 : store_err_w;
  logic        gx_req_w, gx_valid_w;
  logic  [7:0] gx_sel_w;
  logic [63:0] gx_data_w;
  logic        ucpu_ovf_nc_w;
  logic [10:0] ucpu_upc_nc_w;
  logic  [4:0] ucpu_st_nc_w;

  KL_aecp_ucpu #(
      .UCODE_HEX_P (UCODE_HEX_P)
  ) u_ucpu (
      .clk_i              (clk_i),
      .rst_n              (rst_n),
      .disp_valid_i       (disp_valid_r),
      .disp_ready_o       (disp_ready_w),
      .disp_upc_i         (upc_r),
      .disp_ctlr_eid_i    (cmd_r.controller_eid),
      .disp_opd0_i        (opd0_r),
      .disp_opd1_i        (opd1_r),
      .disp_opd2_i        (opd2_r),
      .disp_batch_i       (gdi_r),
      .disp_resp_base_i   (10'(g_out_r + 11'd8)),
      .st_req_o           (st_req_w),
      .st_we_o            (st_we_w),
      .st_name_o          (st_name_w),
      .st_addr_o          (st_addr_w),
      .st_wdata_o         (st_wdata_w),
      .st_wstrb_o         (st_wstrb_w),
      .st_ready_i         (st_ready_w),
      .st_rvalid_i        (st_rvalid_w),
      .st_rdata_i         (st_rdata_w),
      .st_err_i           (st_err_w),
      //! the 06 §6.6/§6.5 gather bus, with TWO sources routed by command:
      //! the GET_COUNTERS read face and the GET_AUDIO_MAP read face (see
      //! the gather-faces section below). §6.2's GET_STREAM_INFO gather has
      //! none, and no µprogram that would use it is dispatched.
      .gx_req_o           (gx_req_w),
      .gx_sel_o           (gx_sel_w),
      .gx_valid_i         (gx_valid_w),
      .gx_data_i          (gx_data_w),
      .lock_held_i        (lock_held_i),
      .lock_ctlr_i        (lock_ctlr_i),
      .rb_we_o            (urb_we_w),
      .rb_addr_o          (urb_addr_w),
      .rb_wdata_o         (urb_wdata_w),
      .rb_wstrb_o         (urb_wstrb_w),
      .rb_ready_i         (rb_ready_w),
      .resp_send_o        (resp_send_w),
      .resp_len_o         (resp_len_w),
      .resp_status_o      (resp_status_w),
      //! the buffer is ours and always able to take the response: the µCPU
      //! never waits on TX, the engine does
      .tx_ready_i         (1'b1),
      .eff_commit_o       (eff_commit_o),
      .eff_nvm_mark_o     (eff_nvm_mark_o),
      .eff_nvm_stb_o      (eff_nvm_stb_o),
      .eff_notify_class_o (eff_notify_class_o),
      .eff_notify_stb_o   (eff_notify_stb_o),
      .busy_o             (ucpu_busy_w),
      .done_o             (ucpu_done_w),
      .dbg_upc_o          (ucpu_upc_nc_w),
      .dbg_status_o       (ucpu_st_nc_w),
      .dbg_ovf_o          (ucpu_ovf_nc_w)
  );

  always_comb begin : notify_effect_context
    eff_notify_type_o     = cfg_ix_r;
    eff_notify_index_o    = desc_ix_r;
    eff_notify_arg0_o     = 16'd0;
    eff_notify_arg1_o     = 16'd0;
    eff_notify_excl_eid_o = cmd_r.controller_eid;
    if (eff_notify_class_o == 4'd1) begin
      eff_notify_type_o  = DT_ENTITY_C;
      eff_notify_index_o = 16'd0;
      eff_notify_arg0_o  = desc_ix_r;
    end else if (eff_notify_class_o == 4'd7) begin
      eff_notify_arg0_o = name_ix_r;
      eff_notify_arg1_o = name_cfg_r;
    end else if (eff_notify_class_o == 4'd9) begin
      eff_notify_arg0_o = cmd_r.opcode;
    end
  end

  logic [15:0] store_fetch_nc_w, store_rowr_nc_w, store_dlen_nc_w;

  KL_aecp_desc_store #(
      .DESC_BASE_P       (DESC_BASE_P),
      .LINE_BYTES_P      (LINE_BYTES_P),
      .IDX_ENTRIES_P     (IDX_ENTRIES_P),
      .NAME_ENTRIES_P    (NAME_ENTRIES_P),
      .MEM_TIMEOUT_CYC_P (MEM_TIMEOUT_CYC_P)
  ) u_store (
      .clk_i             (clk_i),
      .rst_n             (rst_n),
      .st_req_i          (st_req_w && !dyn_sel_w && !strq_sel_w),
      .st_we_i           (st_we_w),
      .st_name_i         (st_name_w),
      .st_addr_i         (st_addr_w),
      .st_wdata_i        (st_wdata_w),
      .st_wstrb_i        (st_wstrb_w),
      .st_ready_o        (store_ready_w),
      .st_rvalid_o       (store_rvalid_w),
      .st_rdata_o        (store_rdata_w),
      .st_err_o          (store_err_w),
      .mem_req_valid_o   (mem_req_valid_o),
      .mem_req_ready_i   (mem_req_ready_i),
      .mem_req_addr_o    (mem_req_addr_o),
      .mem_req_beats_o   (mem_req_beats_o),
      .mem_rsp_valid_i   (mem_rsp_valid_i),
      .mem_rsp_ready_o   (mem_rsp_ready_o),
      .mem_rsp_data_i    (mem_rsp_data_i),
      .mem_rsp_last_i    (mem_rsp_last_i),
      .mem_rsp_err_i     (mem_rsp_err_i),
      .dbg_img_valid_o   (dbg_img_valid_o),
      .dbg_fault_o       (dbg_img_fault_o),
      .dbg_locate_miss_o (dbg_locate_miss_o),
      .dbg_fetch_cnt_o   (store_fetch_nc_w),
      .dbg_ro_write_o    (store_rowr_nc_w),
      .dbg_desc_len_o    (store_dlen_nc_w)
  );

  //! ---- the dynamic-state store (Milan §5.3.5/.7/.8/.11/.12) -------------
  //! Where every SET_* puts its argument and every GET_* looks first. The
  //! descriptor index it rows on is `desc_ix_r`, the SAME registered walk
  //! field that already addresses the counters, audio-map and Milan-info
  //! faces — see the module banner for why the index cannot ride the address.
  logic [15:0] dyn_writes_nc_w, dyn_oob_nc_w;

  KL_aecp_dyn_state #(
      .N_STREAM_IN_P  (N_STREAM_IN_P),
      .N_STREAM_OUT_P (N_STREAM_OUT_P),
      .N_AUDIO_UNIT_P (N_AUDIO_UNIT_P),
      .N_CLK_DOMAIN_P (N_CLK_DOMAIN_P),
      .N_CONTROL_P    (N_CONTROL_P)
  ) u_dyn (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .st_req_i        (st_req_w && dyn_sel_w),
      .st_we_i         (st_we_w),
      .st_addr_i       (st_addr_w),
      .st_wdata_i      (st_wdata_w),
      .st_ready_o      (dyn_ready_w),
      .st_rvalid_o     (dyn_rvalid_w),
      .st_rdata_o      (dyn_rdata_w),
      //! `desc_ix_r` means DESCRIPTOR index for every command here except
      //! SET_CONFIGURATION, whose @26 field is a CONFIGURATION index — a
      //! different namespace that happens to land in the same walk register.
      //! current_configuration is an ENTITY-level singleton with no descriptor
      //! index at all, so it must address row 0. Passing the configuration
      //! index through made the store drop the write as out-of-range for any
      //! configuration but 0, and the command answered SUCCESS anyway.
      .desc_index_i    (scfg_r ? 16'd0 : desc_ix_r),
      .cur_config_o    (dyn_cur_config_o),
      .identify_o      (dyn_identify_o),
      .clk_src_index_o (dyn_clk_src_index_o),
      .pt_offset_o     (dyn_pt_offset_o),
      .pt_offset_v_o   (dyn_pt_offset_v_o),
      .fmt_in_o        (dyn_fmt_in_o),
      .fmt_in_v_o      (dyn_fmt_in_v_o),
      .fmt_out_o       (dyn_fmt_out_o),
      .fmt_out_v_o     (dyn_fmt_out_v_o),
      .dirty_o         (dyn_dirty_o),
      .dbg_writes_o    (dyn_writes_nc_w),
      .dbg_oob_o       (dyn_oob_nc_w)
  );

  logic [15:0] resp_burst_nc_w, resp_drop_nc_w;

  //! The aggregate iterator writes record headers and copies the command data
  //! of permitted but unsupported getters. Getter data itself still comes
  //! from the µCPU. The final one-byte status patch is deliberately allowed
  //! to revisit the record-header lane after the getter has run; the response
  //! buffer serializes partial writes and preserves every other byte.
  always_comb begin : gdi_response_write
    g_rb_we_w    = 1'b0;
    g_rb_addr_w  = 10'(g_out_r);
    g_rb_wdata_w = 32'd0;
    g_rb_wstrb_w = 4'hF;
    if (a_st_r == A_GHDR) begin
      g_rb_we_w = 1'b1;
      if (g_wr_phase_r == 2'd0) begin
        g_rb_wdata_w = {5'd0, g_rec_rlen_r, 16'd0};
      end else begin
        g_rb_addr_w  = 10'(g_out_r + 11'd4);
        g_rb_wdata_w = {3'd0, g_rec_exec_r ? 5'd0 : g_rec_status_r,
                        8'd0, g_rec_cmd_r};
      end
    end else if ((a_st_r == A_GCOPY) && g_rd_pending_r) begin
      g_rb_we_w    = 1'b1;
      g_rb_addr_w  = 10'(g_out_r + 11'd8 + g_data_ix_r);
      g_rb_wdata_w = {24'd0, rxs_rd_data_i};
      g_rb_wstrb_w = 4'h1;
    end else if (a_st_r == A_GPATCH) begin
      g_rb_we_w    = 1'b1;
      g_rb_addr_w  = 10'(g_out_r + 11'd4);
      g_rb_wdata_w = {24'd0, 3'd0, g_rec_status_r};
      g_rb_wstrb_w = 4'h1;
    end
  end

  assign rb_we_w    = g_rb_we_w ? 1'b1        : urb_we_w;
  assign rb_addr_w  = g_rb_we_w ? g_rb_addr_w : urb_addr_w;
  assign rb_wdata_w = g_rb_we_w ? g_rb_wdata_w : urb_wdata_w;
  assign rb_wstrb_w = g_rb_we_w ? g_rb_wstrb_w : urb_wstrb_w;

  KL_aecp_resp_buf #(
      .RESP_BASE_P       (RESP_BASE_P),
      .RESP_BYTES_P      (RESP_BUF_C),
      .MEM_TIMEOUT_CYC_P (MEM_TIMEOUT_CYC_P)
  ) u_resp (
      .clk_i           (clk_i),
      .rst_n           (rst_n),
      .open_i          (rsp_open_w),
      .seal_i          (rsp_seal_w),
      .seal_len_i      (rsp_seal_len_w),
      .wr_we_i         (rb_we_w),
      .wr_addr_i       (rb_addr_w),
      .wr_wdata_i      (rb_wdata_w),
      .wr_wstrb_i      (rb_wstrb_w),
      .wr_ready_o      (rb_ready_w),
      .rd_valid_o      (rsp_rd_valid_w),
      .rd_data_o       (rsp_rd_data_w),
      .rd_take_i       (rsp_rd_take_w),
      .mem_req_valid_o (rmem_req_valid_o),
      .mem_req_ready_i (rmem_req_ready_i),
      .mem_req_addr_o  (rmem_req_addr_o),
      .mem_req_beats_o (rmem_req_beats_o),
      .mem_rsp_valid_i (rmem_rsp_valid_i),
      .mem_rsp_ready_o (rmem_rsp_ready_o),
      .mem_rsp_data_i  (rmem_rsp_data_i),
      .mem_rsp_last_i  (rmem_rsp_last_i),
      .mem_rsp_err_i   (rmem_rsp_err_i),
      .mem_wr_valid_o  (rmem_wr_valid_o),
      .mem_wr_ready_i  (rmem_wr_ready_i),
      .mem_wr_addr_o   (rmem_wr_addr_o),
      .mem_wr_data_o   (rmem_wr_data_o),
      .mem_wr_strb_o   (rmem_wr_strb_o),
      .mem_wr_done_i   (rmem_wr_done_i),
      .mem_wr_err_i    (rmem_wr_err_i),
      .busy_o          (rsp_busy_w),
      .err_o           (rsp_err_w),
      .dbg_fault_o     (dbg_resp_fault_o),
      .dbg_lane_wr_o   (dbg_resp_lane_o),
      .dbg_burst_o     (resp_burst_nc_w),
      .dbg_drop_o      (resp_drop_nc_w)
  );

  // =======================================================================
  // the gather faces: GET_COUNTERS (06 §6.6) + GET_AUDIO_MAP (06 §6.5)
  // =======================================================================
  //! ONE bus, routed BY COMMAND: `amap_r` is the only discriminator, so each
  //! face owns the whole 8-bit selector space while its command is in flight
  //! and neither can ever see the other's query (a GET_COUNTERS and a
  //! GET_AUDIO_MAP are never in flight together - the engine runs one
  //! command at a time by construction).
  //!
  //! Counters selector-to-quadlet is pure wiring on purpose. READ_CTRS drives
  //! gx_sel = {cnd, beat} with beat 0..3, and the µprogram walks cnd 0..7, so
  //! {cnd[2:0], beat[1:0]} IS the counters_block quadlet index 0..31 and
  //! sel[7] is free to mean "the counters_valid word instead" (GATHER_EXT
  //! cnd = 8). No decoder, no per-word ROM, no state.
  //! ONE registered-one-hot "not the counters face" term: the routing depth
  //! stays constant as commands land, and the counters face can never see a
  //! spurious query while another command's gather is in flight
  //! GET_STREAM_FORMAT joins the Milan-info face rather than opening a second
  //! path to the same fact: §7.4.10.2's stream_format IS §7.4.16's, the face
  //! already publishes it as kind 0 selector 1, and two readers of one
  //! register can never disagree the way two registers can. ENTITY_AVAILABLE
  //! joins the registry face for the lock holder (rgy_state 1 = read, no op).
  //! GET_CONFIGURATION, GET_SAMPLING_RATE and GET_CLOCK_SOURCE read only the
  //! descriptor store, run no gather at all, and so need no routing term.
  //! ONE term per face, used by the request enable AND the answer mux below,
  //! so a command joining a face cannot reach it in one direction and not the
  //! other - which is exactly the bug ENTITY_AVAILABLE hit on its first run
  //! (rgy_req_o gated on it, the gxr_data_r mux did not, so the query was
  //! asked and the counters answer came back)
  logic gx_alt_w, gsi_any_w, rgy_any_w, strm_state_w;
  //! SET_STREAM_FORMAT joins the Milan-info face for the same reason
  //! GET_STREAM_FORMAT did: its refusal arms answer "the current value",
  //! which IS kind 0 selector 1, and its verdict word (selector 15) is the
  //! integrator's ruling on the PROPOSED format presented on
  //! `gsi_prop_fmt_o` - the supported set and the mapping-survival
  //! reduction both live integrator-side, where map edits already commit.
  assign gsi_any_w = gstri_r | gavb_r | gasp_r | gsfmt_r | ssfmt_r | ssinfo_r;
  assign rgy_any_w = regun_r | lockc_r | eavl_r;
  assign strm_state_w = (strt_r || stop_r) && (gx_sel_w[7:4] == 4'hD);
  assign gx_alt_w  = amap_r | amap_edit_r | sname_r | rgy_any_w | gsi_any_w
                     | strm_state_w;

  assign ctr_req_o        = gx_req_w && !gx_alt_w;
  assign ctr_desc_type_o  = cfg_ix_r;
  assign ctr_desc_index_o = desc_ix_r;
  assign ctr_word_o       = gx_sel_w[7] ? 6'd32
                                        : {1'b0, gx_sel_w[6:4], gx_sel_w[1:0]};

  //! ...and the registry/lock face is the third command-routed client. The
  //! op code needs no register of its own: REGISTER/DEREGISTER differ in
  //! opcode bit 0 (0x0024/0x0025) and the LOCK pair rides op[1] (P2). The
  //! TIME_LIMITED flag is payload flags bit 0, which the walk left in
  //! `desc_ix_r`; a 2013-format command (§7.4.37.1 "with or without the new
  //! flags field") never walked that byte, so the cdl term keeps stray slot
  //! bytes from becoming a flag.
  //! ...the Milan-info face: selector low nibble forwarded, the kind from
  //! the discriminators, the ordinal from the shared record counter below
  assign gsi_req_o        = gx_req_w && gsi_any_w;
  assign gsi_kind_o       = (gstri_r || gsfmt_r || ssfmt_r || ssinfo_r) ? 2'd0
                                                 : (gavb_r ? 2'd1 : 2'd2);
  assign gsi_desc_type_o  = cfg_ix_r;
  assign gsi_desc_index_o = desc_ix_r;
  assign gsi_sel_o        = gx_sel_w[3:0];
  assign gsi_ord_o        = amap_rec_r;
  //! the PROPOSED stream format, valid while a SET_STREAM_FORMAT is in
  //! flight (it is that command's @28 capture, stable from the walk's end
  //! to the next pop). The integrator reads it only to answer selector 15.
  assign gsi_prop_fmt_o   = setval_r;

  assign rgy_req_o   = gx_req_w && rgy_any_w;
  assign rgy_state_o = gx_sel_w[0];
  //! LOCK rides op[1]; op[0] is UNLOCK for it (flags bit 0, walked into
  //! `desc_ix_r` exactly like TIME_LIMITED) and DEREGISTER for the pair
  assign rgy_op_o    = lockc_r ? {1'b1, desc_ix_r[0]}
                               : {1'b0, cmd_r.opcode[0]};
  assign rgy_eid_o   = cmd_r.controller_eid;
  assign rgy_mac_o   = cmd_r.src_mac;
  assign rgy_tl_o    = (cmd_r.cdl >= 11'd16) && desc_ix_r[0];

  //! ...and the audio-map selectors are three points of it (gen_ucode.py
  //! AM_NMAPS 0x00 / AM_GEOM 0x01 / AM_REC 0x10): sel[4] alone separates a
  //! record fetch from the two geometry words, sel[0] the two geometry words
  //! from each other. `desc_ty_r` HOLDS map_index for this command (see the
  //! payload walk), which is why the page rides it here.
  assign amap_req_o        = gx_req_w && amap_r;
  assign amap_desc_type_o  = cfg_ix_r;
  assign amap_desc_index_o = desc_ix_r;
  assign amap_map_index_o  = desc_ty_r;
  assign amap_sel_o        = gx_sel_w[4] ? 2'd2 : {1'b0, gx_sel_w[0]};
  assign amap_rec_o        = amap_rec_r;

  //! The edit selectors are private to the command-routed gather space:
  //! 0x20 begin validation, 0x30 begin commit, 0x22 finish, 0x23 abort,
  //! 0x40 validate one record and 0x50 commit one record. Record phases wait
  //! one cycle for the synchronous staging RAM read before reaching the
  //! integrator. External HOLD applies only before phase 1 has accepted the
  //! commit. After that reservation point, commit records and finish cannot
  //! time out between live writes.
  always_comb begin : amap_edit_phase_decode
    unique case (gx_sel_w)
      8'h20: amap_edit_phase_o = 3'd0;
      8'h30: amap_edit_phase_o = 3'd1;
      8'h22: amap_edit_phase_o = 3'd2;
      8'h23: amap_edit_phase_o = 3'd3;
      8'h40: amap_edit_phase_o = 3'd4;
      8'h50: amap_edit_phase_o = 3'd5;
      default: amap_edit_phase_o = 3'd3;
    endcase
  end
  assign amap_edit_req_o = gx_req_w && amap_edit_r
                           && ((amap_edit_phase_o < 3'd4)
                               || amap_stage_ready_r);
  assign amap_edit_remove_o     = amap_remove_r;
  assign amap_edit_desc_type_o  = cfg_ix_r;
  assign amap_edit_desc_index_o = desc_ix_r;
  assign amap_edit_count_o      = desc_ty_r;
  assign amap_edit_rec_o        = amap_rec_r;
  assign amap_edit_record_o     = amap_stage_q_r;
  assign amap_edit_value_o      = setval_r;

  //! One syntactic read port is required for Xilinx block-RAM inference. The
  //! response serializer and the transaction face are mutually exclusive, so
  //! they share one address mux without changing either consumer's latency.
  assign amap_stage_ser_w = (amap_uns_r || amap_edit_r) && (a_st_r == A_WR);
  assign amap_stage_ser_load_w = amap_stage_ser_w
      && (bidx_r >= 11'(FRAME_HDR_C + 7))
      && (bidx_r < 11'(FRAME_HDR_C) + pld_r)
      && (((bidx_r - 11'(FRAME_HDR_C + 7)) & 11'd7) == 0);
  assign amap_stage_edit_load_w = !amap_stage_ser_w && gx_req_w && amap_edit_r
                                  && (amap_edit_phase_o >= 3'd4)
                                  && !amap_stage_ready_r;
  assign amap_stage_name_load_w = !amap_stage_ser_w && gx_req_w && sname_r
                                  && (gx_sel_w[7:3] == 5'b01100)
                                  && !amap_stage_ready_r;
  assign amap_stage_rd_en_w = amap_stage_ser_load_w
                              || amap_stage_edit_load_w
                              || amap_stage_name_load_w;
  assign amap_stage_raddr_w = amap_stage_ser_w
      ? 8'((bidx_r - 11'(FRAME_HDR_C + 7)) >> 3)
      : sname_r ? {5'd0, gx_sel_w[2:0]} : amap_rec_r;

  always_ff @(posedge clk_i) begin : amap_stage_read
    if (!rst_n) begin
      amap_stage_q_r     <= 64'd0;
      amap_stage_ready_r <= 1'b0;
    end else begin
      if (amap_stage_ser_w) begin
        amap_stage_ready_r <= 1'b0;
      end else if (!gx_req_w
                   || (!(amap_edit_r && (amap_edit_phase_o >= 3'd4))
                       && !sname_r)) begin
        amap_stage_ready_r <= 1'b0;
      end else if (!amap_stage_ready_r) begin
        amap_stage_ready_r <= 1'b1;
      end
      if (amap_stage_rd_en_w) begin
        amap_stage_q_r <= amap_stage_r[amap_stage_raddr_w];
      end
    end
  end

  //! RX arrives one byte per cycle. Assemble a complete Figure 7-71 record in
  //! flops, then perform one 64-bit RAM write. A per-byte RAM write enable
  //! maps this 256x64 store into eight block memories under Yosys/Xilinx;
  //! the full-word template maps it into one while preserving wire order.
  always_ff @(posedge clk_i) begin : amap_stage_write
    if (!rst_n) begin
      amap_stage_assem_r <= 64'd0;
    end else if (a_st_r == A_IDLE) begin
      amap_stage_assem_r <= 64'd0;
    end else if ((a_st_r == A_PLD) && (amap_edit_r || sname_r)
                 && (walk_r >= 11'd11)) begin
      amap_stage_assem_r <= {amap_stage_assem_r[55:0], rxs_rd_data_i};
      if (((walk_r - 11'd11) & 11'd7) == 11'd7) begin
        amap_stage_r[8'((walk_r - 11'd11) >> 3)]
          <= {amap_stage_assem_r[55:0], rxs_rd_data_i};
      end
    end
  end

  //! bounded wait (see the banner), shared by both faces: expiry unsticks the
  //! µCPU with a zero and marks the response void, because by then the
  //! counters_valid word - or the mapping count - is already in the buffer,
  //! and zeros behind an emitted claim are the one answer worse than none
  localparam int unsigned CTO_W_C = $clog2(MEM_TIMEOUT_CYC_P + 1);
  logic [CTO_W_C-1:0] gxf_tmo_r;
  logic               gxf_fail_r;
  logic               ctr_hold_w, amap_hold_w, amap_edit_hold_w, name_hold_w;
  logic               rgy_hold_w;
  logic gsi_hold_w;
  assign ctr_hold_w  = gx_req_w && !gx_alt_w
                       && ctr_wait_i  && !gxf_fail_r;
  assign amap_hold_w = gx_req_w &&  amap_r && amap_wait_i && !gxf_fail_r;
  assign amap_edit_hold_w = gx_req_w && amap_edit_r && !gxf_fail_r
                            && (((amap_edit_phase_o >= 3'd4)
                                 && !amap_stage_ready_r)
                                || (amap_edit_req_o && amap_edit_wait_i
                                    && (amap_edit_phase_o != 3'd2)
                                    && (amap_edit_phase_o != 3'd5)));
  assign name_hold_w = gx_req_w && sname_r && !amap_stage_ready_r
                       && !gxf_fail_r;
  assign rgy_hold_w  = gx_req_w && (regun_r || lockc_r)
                       && rgy_wait_i && !gxf_fail_r;
  assign gsi_hold_w  = gx_req_w &&  gsi_any_w && gsi_wait_i && !gxf_fail_r;

  //! REGISTERED gather answer - the stage-0 pipeline cut. The integrator's
  //! wait/data cone (ctr_wait_i / amap_wait_i arrive combinationally from
  //! OUTSIDE this processor) used to run through gx_valid_w into the µCPU's
  //! E-stage stall and from there into the µcode ROM's address-register
  //! enable: measured on the reference part as the failing 12-plus-level
  //! path into u_ucpu upc_r (ENARDEN/ADDRARDADDR). The answer is now
  //! latched HERE, so the µCPU's stall sees one flop. `!gxr_valid_r` in the
  //! arm makes the valid a one-cycle pulse per answered beat - without it a
  //! multi-beat READ_CTRS would take beat n's registered data a second time
  //! while the selector was still moving to beat n+1. One extra cycle per
  //! gather beat, invisible at AECP rates.
  logic        gxr_valid_r;
  logic [63:0] gxr_data_r;

  always_ff @(posedge clk_i) begin : gather_answer
    if (!rst_n) begin
      gxr_valid_r <= 1'b0;
      gxr_data_r  <= 64'd0;
    end else begin
      gxr_valid_r <= gx_req_w && !gxr_valid_r
                     && !(ctr_hold_w || amap_hold_w || amap_edit_hold_w
                          || name_hold_w
                          || rgy_hold_w
                          || gsi_hold_w);
      gxr_data_r  <= gxf_fail_r           ? 64'd0
                   : amap_r               ? amap_data_i
                   : amap_edit_r          ? amap_edit_data_i
                   : sname_r              ? amap_stage_q_r
                   : rgy_any_w            ? rgy_data_i
                   : strm_state_w         ? ((32'(desc_ix_r) < N_STREAM_IN_P)
                                              ? {63'd0,
                                                 1'(strm_bound_i >> desc_ix_r)
                                                   && 1'(strm_started_i
                                                         >> desc_ix_r)}
                                              : 64'd0)
                   : gsi_any_w            ? gsi_data_i
                                          : {32'd0, ctr_data_i};
    end
  end

  assign gx_valid_w = gxr_valid_r;
  assign gx_data_w  = gxr_data_r;

  always_ff @(posedge clk_i) begin : gather_watchdog
    if (!rst_n) begin
      gxf_tmo_r  <= '0;
      gxf_fail_r <= 1'b0;
    end else if (a_st_r == A_IDLE) begin
      gxf_tmo_r  <= '0;
      gxf_fail_r <= 1'b0;
    end else if (ctr_hold_w || amap_hold_w || amap_edit_hold_w || name_hold_w
                 || rgy_hold_w || gsi_hold_w) begin
      if (gxf_tmo_r == CTO_W_C'(MEM_TIMEOUT_CYC_P)) gxf_fail_r <= 1'b1;
      else                                          gxf_tmo_r  <= gxf_tmo_r + CTO_W_C'(1);
    end else begin
      gxf_tmo_r <= '0;
    end
  end

  //! the record ordinal: one per COMPLETED record gather, so the loop's k-th
  //! GATHER_EXT asks for record k and the face stays stateless. Reset with
  //! the command, like the watchdog.
  //! ...now SHARED with the Milan-info face's arrays (GET_AVB_INFO's
  //! msrp_mappings, GET_AS_PATH's path_sequence): a gsi selector with bit 3
  //! set is a record-class word, and one command is in flight at a time, so
  //! one counter serves every array walk
  always_ff @(posedge clk_i) begin : amap_record_ordinal
    if (!rst_n)                 amap_rec_r <= 8'd0;
    else if (a_st_r == A_IDLE)  amap_rec_r <= 8'd0;
    else if (amap_edit_req_o && gx_valid_w
             && (amap_edit_phase_o <= 3'd1)) amap_rec_r <= 8'd0;
    else if (((amap_req_o && gx_sel_w[4])
              || (amap_edit_req_o && (amap_edit_phase_o >= 3'd4))
              || (gsi_req_o && gx_sel_w[3])) && gx_valid_w
             && (amap_rec_r != 8'hFF)) amap_rec_r <= amap_rec_r + 8'd1;
  end

  // =======================================================================
  // frame assembly: byte `bidx_r` of the response
  // =======================================================================
  logic [15:0] cdl_w;
  assign cdl_w = 16'd12 + {5'd0, pld_r};

  logic [3:0] resp_mt_w;
  assign resp_mt_w = cmd_r.msg_type | 4'd1;   // COMMAND -> its RESPONSE type

  logic [7:0] hdr_byte_w;
  always_comb begin : frame_header_byte
    unique case (bidx_r[5:0])
      6'd0:  hdr_byte_w = cmd_r.src_mac[47:40];
      6'd1:  hdr_byte_w = cmd_r.src_mac[39:32];
      6'd2:  hdr_byte_w = cmd_r.src_mac[31:24];
      6'd3:  hdr_byte_w = cmd_r.src_mac[23:16];
      6'd4:  hdr_byte_w = cmd_r.src_mac[15:8];
      6'd5:  hdr_byte_w = cmd_r.src_mac[7:0];
      6'd6:  hdr_byte_w = own_mac_i[47:40];
      6'd7:  hdr_byte_w = own_mac_i[39:32];
      6'd8:  hdr_byte_w = own_mac_i[31:24];
      6'd9:  hdr_byte_w = own_mac_i[23:16];
      6'd10: hdr_byte_w = own_mac_i[15:8];
      6'd11: hdr_byte_w = own_mac_i[7:0];
      6'd12: hdr_byte_w = 8'h22;                        // EtherType 0x22F0
      6'd13: hdr_byte_w = 8'hF0;
      6'd14: hdr_byte_w = 8'hFB;                        // AVTP subtype AECP
      6'd15: hdr_byte_w = {4'b0000, resp_mt_w};         // sv=0, version=0
      6'd16: hdr_byte_w = {status_r, cdl_w[10:8]};
      6'd17: hdr_byte_w = cdl_w[7:0];
      6'd18: hdr_byte_w = entity_id_i[63:56];           // target_entity_id
      6'd19: hdr_byte_w = entity_id_i[55:48];
      6'd20: hdr_byte_w = entity_id_i[47:40];
      6'd21: hdr_byte_w = entity_id_i[39:32];
      6'd22: hdr_byte_w = entity_id_i[31:24];
      6'd23: hdr_byte_w = entity_id_i[23:16];
      6'd24: hdr_byte_w = entity_id_i[15:8];
      6'd25: hdr_byte_w = entity_id_i[7:0];
      6'd26: hdr_byte_w = cmd_r.controller_eid[63:56];
      6'd27: hdr_byte_w = cmd_r.controller_eid[55:48];
      6'd28: hdr_byte_w = cmd_r.controller_eid[47:40];
      6'd29: hdr_byte_w = cmd_r.controller_eid[39:32];
      6'd30: hdr_byte_w = cmd_r.controller_eid[31:24];
      6'd31: hdr_byte_w = cmd_r.controller_eid[23:16];
      6'd32: hdr_byte_w = cmd_r.controller_eid[15:8];
      6'd33: hdr_byte_w = cmd_r.controller_eid[7:0];
      6'd34: hdr_byte_w = cmd_r.sequence_id[15:8];
      6'd35: hdr_byte_w = cmd_r.sequence_id[7:0];
      //! @22, AND ONLY AN AEM MESSAGE HAS A u BIT THERE. 1722.1-2021 9.3.2.1
      //! makes `u` its own 1-bit field ahead of `cr` and a 14-bit
      //! command_type -- the 2013 edition's "top bit of command_type" framing
      //! is what this comment used to say, and it is why `cr` must survive the
      //! rewrite below. A
      //! solicited response clears it. Every other message_type defines @22
      //! for itself: 9.6.2 Figure 9-12 gives a VENDOR_UNIQUE AECPDU a 48-bit
      //! protocol_id running @22..@27 with NO u bit in it, so @22 there is
      //! protocol_id[47:40] whole.
      //!
      //! This used to clear bit 7 unconditionally, under a comment claiming
      //! it "keeps a VENDOR_UNIQUE response's protocol_id bytes intact". It
      //! did the opposite. MEASURED on the AX7101 before the fix, by driving
      //! four vendor-unique commands and reading back the NOT_IMPLEMENTED
      //! echo:
      //!     sent 00-1B-C5-0A-C1-00 -> echoed 00 1b c5 0a c1 00   intact
      //!     sent 7F-1B-C5-0A-C1-00 -> echoed 7f 1b c5 0a c1 00   intact
      //!     sent FC-1B-C5-0A-C1-00 -> echoed 7c 1b c5 0a c1 00   CORRUPT
      //!     sent 80-1B-C5-0A-C1-00 -> echoed 00 1b c5 0a c1 00   CORRUPT
      //! Every OUI whose first octet has bit 7 set - half of the space - got
      //! a mangled protocol_id back, so a vendor could not match our refusal
      //! to the protocol it asked about. Milan's own 00-1B-C5 has bit 7
      //! clear, which is why GET_MILAN_INFO never showed it and why nothing
      //! in the suite caught it: every protocol_id ever tested was immune.
      //! ...and an unsolicited response is the ONE sender of u = 1 (IEEE
      //! §9.3.2.1 via the 9.3.5.4 UNSOLICITED RESPONSE arc): `uns_r` is set
      //! only for engine-originated jobs, which are AEM by construction
      //! `PP_PROTO_AEM` is the RX validator's RESIDUAL bucket, so message_type
      //! is what actually says "this word has a u bit in it". AVC_COMMAND and
      //! the rest land in the same bucket and carry a length there.
      6'd36: hdr_byte_w = (cmd_r.protocol == PP_PROTO_AEM)
                          && (cmd_r.msg_type == 4'd0)
                          ? {uns_r, raw_ct_r[14:8]}  // AEM: u = solicited?0:1
                          : raw_ct_r[15:8];          // everything else: verbatim
      6'd37: hdr_byte_w = raw_ct_r[7:0];
      default: hdr_byte_w = 8'd0;
    endcase
  end

  //! payload byte `bidx_r - FRAME_HDR_C` comes from the RX slot for an echoed
  //! response (§9.3.5.3.3 copies the command verbatim and the slot still holds
  //! it) and from the memory-backed response buffer for a µprogram-built one
  logic pay_w;
  assign pay_w = (bidx_r >= 11'(FRAME_HDR_C))
                 && (bidx_r < (11'(FRAME_HDR_C) + pld_r));

  logic [7:0] frame_byte_w;
  logic [10:0] amap_uns_pidx_w;
  logic [7:0] amap_uns_byte_w;
  logic [15:0] amap_emit_count_w;
  assign amap_emit_count_w = amap_uns_r ? desc_ty_r
                                        : {8'd0, amap_rsp_count_r};
  always_comb begin : amap_uns_payload
    amap_uns_pidx_w = bidx_r - 11'(FRAME_HDR_C);
    unique case (amap_uns_pidx_w)
      11'd0: amap_uns_byte_w = cfg_ix_r[15:8];
      11'd1: amap_uns_byte_w = cfg_ix_r[7:0];
      11'd2: amap_uns_byte_w = desc_ix_r[15:8];
      11'd3: amap_uns_byte_w = desc_ix_r[7:0];
      11'd4: amap_uns_byte_w = amap_emit_count_w[15:8];
      11'd5: amap_uns_byte_w = amap_emit_count_w[7:0];
      11'd6, 11'd7: amap_uns_byte_w = 8'd0;
      default: amap_uns_byte_w = amap_stage_q_r[
          63 - (8 * ((amap_uns_pidx_w - 11'd8) & 11'd7)) -: 8];
    endcase
  end
  always_comb begin : frame_byte
    if (bidx_r < 11'(FRAME_HDR_C))  frame_byte_w = hdr_byte_w;
    else if (pay_w)                 frame_byte_w = (amap_uns_r || amap_edit_r)
                                      ? amap_uns_byte_w
                                      : echo_r ? rxs_rd_data_i
                                               : rsp_rd_data_w;
    else                            frame_byte_w = 8'd0;   // pad
  end

  //! the builder advances only when the byte it is about to write EXISTS: the
  //! response buffer's read burst paces itself against main memory
  logic byte_ok_w;
  assign byte_ok_w = !pay_w || amap_uns_r || amap_edit_r || echo_r
                     || rsp_rd_valid_w;
  assign rsp_rd_take_w = (a_st_r == A_WR) && pay_w && !echo_r
                         && !amap_edit_r && rsp_rd_valid_w;

  // ---- RX payload walk -----------------------------------------------------
  //! A_PLD: the walk starts at AECPDU @22 (= slot byte 22) so bytes @22..@23
  //! are captured verbatim; the parsed fields sit at walk indices 2..9.
  //! A_WR: the same port PREFETCHES the echo payload one byte ahead — the pool
  //! answers a cycle after `rd_en`, and payload byte n is slot byte 24 + n.
  logic [10:0] pref_ix_w;
  logic        pref_en_w;
  assign pref_ix_w = bidx_r + 11'd1 - 11'(FRAME_HDR_C);
  assign pref_en_w = (a_st_r == A_WR) && echo_r && !amap_uns_r
                     && !amap_edit_r
                     && ((bidx_r + 11'd1) >= 11'(FRAME_HDR_C))
                     && ((bidx_r + 11'd1) < (11'(FRAME_HDR_C) + pld_r));

  assign rxs_rd_slot_o = cmd_r.rx_slot[RXS_W_C-1:0];
  assign rxs_rd_addr_o = (a_st_r inside {A_GSCAN, A_GLOAD, A_GCOPY})
                         ? RXA_W_C'(32'd24 + 32'(g_rd_pos_r))
                         : (a_st_r == A_WR)
                           ? RXA_W_C'(32'd24 + 32'(pref_ix_w))
                           : RXA_W_C'(32'd22 + 32'(walk_r));
  assign rxs_rd_en_o   = ((a_st_r == A_PLD) && (walk_r < (pld_r + 11'd2)))
                         || pref_en_w
                         || ((a_st_r == A_GSCAN) && g_scan_started_r
                             && !g_rd_pending_r && (g_rd_pos_r < g_total_r))
                         || ((a_st_r == A_GLOAD) && !g_rd_pending_r
                             && (g_rd_pos_r < g_total_r))
                         || ((a_st_r == A_GCOPY) && !g_rd_pending_r
                             && (g_data_ix_r < 11'(g_rec_len_r)));

  //! a command is only taken once the PREVIOUS response has let go of main
  //! memory: `open_i` re-arms the buffer, and re-arming it under a burst that
  //! is still in flight would leave the bridge holding a beat nobody sinks.
  //! The buffer's watchdog bounds this wait, so it can never become a hang.
  assign txn_ready_o     = (a_st_r == A_IDLE) && !rsp_busy_w
                           && !amap_notify_busy_i;
  assign txs_alloc_req_o = (a_st_r == A_ALLOC);
  assign txs_oversize_o  = (frame_len_r > 11'(TX_STD_BYTES_P));
  assign txs_wr_slot_o   = tx_slot_r;
  assign txs_wr_addr_o   = TXA_W_C'(bidx_r);
  assign txs_wr_valid_o  = (a_st_r == A_WR) && byte_ok_w;
  assign txs_wr_data_o   = frame_byte_w;
  assign txs_wr_commit_o = (a_st_r == A_CMT);
  assign txs_wr_len_o    = TXA_W_C'(frame_len_r);
  //! one slot register, two lanes: a solicited response requests
  //! LANE_AECP_SOL, an unsolicited one LANE_AECP_UNS - the F03.5 priority
  //! split without a second builder or a second slot path
  assign txreq_valid_o     = (a_st_r == A_TXW) && !uns_r;
  assign txreq_uns_valid_o = (a_st_r == A_TXW) && uns_r;
  assign txreq_slot_o      = tx_slot_r;
  assign rxs_free_o      = (a_st_r == A_FREE)
                           && (cmd_r.rx_slot != PP_SLOT_NULL_C);
  assign rxs_free_slot_o = cmd_r.rx_slot[RXS_W_C-1:0];
  //! the job retirement strobe: sent, voided or no-send all pass A_FREE
  assign uns_done_o      = (a_st_r == A_FREE) && uns_r;

  assign dbg_busy_o     = (a_st_r != A_IDLE) || ucpu_busy_w;
  assign dbg_cmd_cnt_o  = cmd_cnt_r;
  assign dbg_resp_cnt_o = resp_cnt_r;
  assign dbg_drop_cnt_o = drop_cnt_r;
  assign dbg_status_o   = status_r;
  assign dbg_len_o      = frame_len_r;
  assign dbg_resp_err_o = rerr_cnt_r;

  logic [10:0] pad_len_w;
  assign pad_len_w = (11'(FRAME_HDR_C) + pld_r < 11'(ETH_MIN_C))
                     ? 11'(ETH_MIN_C) : (11'(FRAME_HDR_C) + pld_r);

  // ---- the response-buffer lifecycle strobes -------------------------------
  //! opened when a command is accepted, sealed when its µprogram retires. An
  //! echoed payload never entered the buffer, so it is sealed with length 0
  //! and costs no read burst at all.
  assign rsp_open_w     = (a_st_r == A_IDLE) && !rsp_busy_w
                          && ((txn_valid_i && !drop_w
                               && !amap_notify_busy_i)
                              || (uns_valid_i
                                  && (!txn_valid_i
                                      || amap_notify_busy_i)));
  //! only a µprogram that actually SENT a response is worth sealing: a
  //! retirement without SEND_RESPONSE emits no frame, so it must not leave a
  //! read burst in flight for the next command's `open_i` to trample
  assign rsp_seal_w     = (((a_st_r == A_RUN) && !gdi_r && ucpu_done_w
                            && (sent_r || resp_send_w))
                           || (a_st_r == A_GDONE));
  //! ... and a response a gather face already voided has no payload to
  //! read back either: sealing it with its INTENDED length would start a
  //! read burst that the register-only error builder never consumes. Mapping
  //! edits retain their staged Figure 7-71 body, but that body also bypasses
  //! the response buffer entirely.
  assign rsp_seal_len_w = (echo_r || amap_edit_r || gxf_fail_r)
                          ? 11'd0 : pld_r;

  //! A response source failed under a frame that is already partly written.
  //! Rebuild it from registers; mapping edits also retain their staged body.
  logic rsp_fail_w;
  assign rsp_fail_w = (rsp_err_w || gxf_fail_r) && !err_mode_r
                      && (!echo_r || amap_edit_r);

  always_ff @(posedge clk_i) begin : command_machine
    if (!rst_n) begin
      a_st_r       <= A_IDLE;
      cmd_r        <= '0;
      raw_ct_r     <= 16'd0;
      cfg_ix_r     <= 16'd0;
      desc_ty_r    <= 16'd0;
      desc_ix_r    <= 16'd0;
      name_ix_r    <= 16'd0;
      name_cfg_r   <= 16'd0;
      pld_cmd_r    <= 11'd0;
      pld_r        <= 11'd0;
      amap_rsp_count_r <= 8'd0;
      walk_r       <= 11'd0;
      pid_lo_r     <= 2'b00;
      echo_r       <= 1'b0;
      ctrs_r       <= 1'b0;
      amap_r       <= 1'b0;
      amap_edit_r  <= 1'b0;
      amap_remove_r <= 1'b0;
      amap_uns_r   <= 1'b0;
      regun_r      <= 1'b0;
      acq_r        <= 1'b0;
      lockc_r      <= 1'b0;
      gstri_r      <= 1'b0;
      gavb_r       <= 1'b0;
      gasp_r       <= 1'b0;
      eavl_r       <= 1'b0;
      gcfg_r       <= 1'b0;
      gsfmt_r      <= 1'b0;
      gsrate_r     <= 1'b0;
      gclks_r      <= 1'b0;
      ssrate_r     <= 1'b0;
      sclks_r      <= 1'b0;
      ssfmt_r      <= 1'b0;
      ssinfo_r     <= 1'b0;
      gctrl_r      <= 1'b0;
      sctrl_r      <= 1'b0;
      gname_r      <= 1'b0;
      sname_r      <= 1'b0;
      scfg_r       <= 1'b0;
      strt_r       <= 1'b0;
      stop_r       <= 1'b0;
      strm_r       <= 1'b0;
      setc_r       <= 1'b0;
      gdi_r        <= 1'b0;
      setval_r     <= 64'd0;
      silat_r      <= 32'd0;
      opd2_r       <= 64'd0;
      lock_ent_ok_r <= 1'b0;
      uns_r        <= 1'b0;
      upc_r        <= 11'd0;
      status_r     <= 5'd0;
      bidx_r       <= 11'd0;
      frame_len_r  <= 11'd0;
      err_mode_r   <= 1'b0;
      tx_slot_r    <= '0;
      disp_valid_r <= 1'b0;
      opd0_r       <= 64'd0;
      opd1_r       <= 64'd0;
      sent_r       <= 1'b0;
      cmd_cnt_r    <= 16'd0;
      resp_cnt_r   <= 16'd0;
      drop_cnt_r   <= 16'd0;
      rerr_cnt_r   <= 16'd0;
      g_scan_started_r <= 1'b0;
      g_rd_pending_r   <= 1'b0;
      g_load_data_r    <= 1'b0;
      g_hdr_ix_r       <= 3'd0;
      g_wr_phase_r     <= 2'd0;
      g_total_r        <= 11'd0;
      g_rd_pos_r       <= 11'd0;
      g_data_ix_r      <= 11'd0;
      g_data_start_r   <= 11'd0;
      g_next_pos_r     <= 11'd0;
      g_out_r          <= 11'd12;
      g_rec_rlen_r     <= 11'd0;
      g_sub_end_r      <= 11'd0;
      g_scan_len_r     <= 16'd0;
      g_scan_cmd_hi_r  <= 8'd0;
      g_rec_len_r      <= 16'd0;
      g_rec_cmd_r      <= 16'd0;
      g_rec_cmd_status_r <= 8'd0;
      g_data_head_r    <= 64'd0;
      g_rec_exec_r     <= 1'b0;
      g_rec_status_r   <= ST_SUCCESS_C;
      g_shape_fault_r  <= 1'b0;
    end else begin
      unique case (a_st_r)
        A_IDLE: begin
          //! !rsp_busy_w now guards the TAKE, not just the handshake: the
          //! pop only happens when txn_ready_o is high, so advancing while
          //! the previous response's memory burst still held the buffer
          //! would process the un-popped head TWICE and double-free its RX
          //! slot. The same guard arms the unsolicited path.
          if (txn_valid_i && !rsp_busy_w && !amap_notify_busy_i) begin
            cmd_r <= txn_w;
            if (drop_w) begin
              if (drop_cnt_r != 16'hFFFF) drop_cnt_r <= drop_cnt_r + 16'd1;
              a_st_r <= A_FREE;
            end else begin
              if (cmd_cnt_r != 16'hFFFF) cmd_cnt_r <= cmd_cnt_r + 16'd1;
              upc_r      <= upc_w;
              echo_r     <= echo_w;
              ctrs_r     <= ctrs_w;
              amap_r     <= amap_w;
              amap_edit_r <= amap_edit_w;
              amap_remove_r <= amap_remove_w;
              amap_uns_r <= 1'b0;
              regun_r    <= regun_w;
              acq_r      <= acq_w;
              lockc_r    <= lockc_w;
              gstri_r    <= gstri_w;
              gavb_r     <= gavb_w;
              gasp_r     <= gasp_w;
              eavl_r     <= eavl_w;
              gcfg_r     <= gcfg_w;
              gsfmt_r    <= gsfmt_w;
              gsrate_r   <= gsrate_w;
              gclks_r    <= gclks_w;
              ssrate_r   <= ssrate_w;
              sclks_r    <= sclks_w;
              ssfmt_r    <= ssfmt_w;
              ssinfo_r   <= ssinfo_w;
              gctrl_r    <= gctrl_w;
              sctrl_r    <= sctrl_w;
              gname_r    <= gname_w;
              sname_r    <= sname_w;
              scfg_r     <= scfg_w;
              strt_r     <= strt_w;
              stop_r     <= stop_w;
              strm_r     <= strm_w;
              setc_r     <= setc_w;
              gdi_r      <= gdi_w;
              setval_r   <= 64'd0;
              silat_r    <= 32'd0;
              lock_ent_ok_r <= 1'b1;
              uns_r      <= 1'b0;
              err_mode_r <= 1'b0;
              //! an echo with no RX slot has NO payload to echo: emitting
              //! `cdl - 12` bytes of whatever the slot pool last held would put
              //! another command's bytes on the wire
              pld_cmd_r <= (txn_w.rx_slot == PP_SLOT_NULL_C) ? 11'd0
                                                             : pld_cap_w;
              pld_r     <= (txn_w.rx_slot == PP_SLOT_NULL_C) ? 11'd0
                                                             : pld_cap_w;
              amap_rsp_count_r <= 8'd0;
              cfg_ix_r  <= 16'd0;
              desc_ty_r <= 16'd0;
              desc_ix_r <= 16'd0;
              name_ix_r <= 16'd0;
              name_cfg_r <= 16'd0;
              raw_ct_r  <= gdi_w ? txn_w.opcode : 16'd0;
              walk_r    <= 11'd0;
              pid_lo_r  <= 2'b00;
              sent_r    <= 1'b0;
              g_scan_started_r <= 1'b0;
              g_rd_pending_r   <= 1'b0;
              g_load_data_r    <= 1'b0;
              g_hdr_ix_r       <= 3'd0;
              g_wr_phase_r     <= 2'd0;
              g_total_r        <= 11'd0;
              g_rd_pos_r       <= 11'd0;
              g_data_ix_r      <= 11'd0;
              g_out_r          <= 11'd12;
              g_rec_rlen_r     <= 11'd0;
              g_sub_end_r      <= 11'd0;
              g_rec_cmd_status_r <= 8'd0;
              g_shape_fault_r  <= 1'b0;
              g_data_head_r    <= 64'd0;
              a_st_r    <= gdi_w ? A_GSCAN
                          : (txn_w.rx_slot == PP_SLOT_NULL_C) ? A_DISP : A_PLD;
            end
          end else if (uns_valid_i && !rsp_busy_w) begin
            //! the unsolicited job: a phantom 03 §4 record with no RX slot
            //! and no payload walk - the solicited head always outranks it,
            //! so notifications can never starve the command path. Only the
            //! fields the response path CONSUMES are loaded (src_mac is the
            //! DESTINATION, sequence_id is the ENTRY's - Milan §5.4.5.1);
            //! muxing the whole 393-bit record for them measured about a
            //! hundred LUTs of pure waste
            cmd_r.origin         <= PP_ORIGIN_SELF;
            cmd_r.protocol       <= PP_PROTO_AEM;
            cmd_r.msg_type       <= 4'd0;        // built as its RESPONSE (+1)
            cmd_r.cdl            <= 11'd12;
            cmd_r.src_mac        <= uns_mac_i;
            cmd_r.controller_eid <= uns_ctlr_eid_i;
            cmd_r.target_eid     <= entity_id_i;
            cmd_r.sequence_id    <= uns_seq_i;
            cmd_r.opcode         <= uns_ct_w;
            cmd_r.rx_slot        <= PP_SLOT_NULL_C;
            upc_r      <= uns_upc_w;
            echo_r     <= (uns_kind_i == PP_UNS_AMAP_C);
            ctrs_r     <= (uns_kind_i == PP_UNS_CTRS_C);
            amap_r     <= 1'b0;
            amap_edit_r <= 1'b0;
            amap_remove_r <= uns_amap_remove_i;
            amap_uns_r <= (uns_kind_i == PP_UNS_AMAP_C);
            //! the LOCK notification's microprogram reads the holder off the
            //! rgy face, so the job routes the gather bus there; a state
            //! read runs no op in KL_aecp_notify
            regun_r    <= (uns_kind_i == PP_UNS_LOCK_C);
            acq_r      <= 1'b0;
            lockc_r    <= 1'b0;
            gstri_r    <= (uns_kind_i == PP_UNS_STRI_C)
                          || (uns_kind_i == PP_UNS_SINFO_C);
            gavb_r     <= (uns_kind_i == PP_UNS_AVB_C);
            gasp_r     <= (uns_kind_i == PP_UNS_ASP_C);
            //! no unsolicited job carries a read-side opcode (Table 5.22 lists
            //! none of the five), so their discriminators are cleared rather
            //! than muxed - an unsolicited GET_STREAM_FORMAT would otherwise
            //! route the Milan-info face off a stale flop
            eavl_r     <= 1'b0;
            gcfg_r     <= 1'b0;
            gsfmt_r    <= (uns_kind_i == PP_UNS_SFMT_C);
            gsrate_r   <= (uns_kind_i == PP_UNS_SRATE_C);
            gclks_r    <= (uns_kind_i == PP_UNS_CLKS_C);
            ssrate_r   <= 1'b0;
            sclks_r    <= 1'b0;
            ssfmt_r    <= 1'b0;
            ssinfo_r   <= 1'b0;
            gctrl_r    <= (uns_kind_i == PP_UNS_CTRL_C);
            sctrl_r    <= 1'b0;
            gname_r    <= (uns_kind_i == PP_UNS_NAME_C);
            sname_r    <= 1'b0;
            scfg_r     <= (uns_kind_i == PP_UNS_CFG_C);
            strt_r     <= (uns_kind_i == PP_UNS_STRM_C) && !uns_arg0_i[0];
            stop_r     <= (uns_kind_i == PP_UNS_STRM_C) && uns_arg0_i[0];
            strm_r     <= (uns_kind_i == PP_UNS_STRM_C);
            setc_r     <= 1'b0;
            gdi_r      <= 1'b0;
            g_shape_fault_r <= 1'b0;
            lock_ent_ok_r <= 1'b1;
            uns_r      <= 1'b1;
            err_mode_r <= 1'b0;
            pld_cmd_r  <= (uns_kind_i == PP_UNS_AMAP_C)
                          ? 11'd8 + (11'(uns_amap_count_i) << 3) : 11'd0;
            pld_r      <= (uns_kind_i == PP_UNS_AMAP_C)
                          ? 11'd8 + (11'(uns_amap_count_i) << 3) : 11'd0;
            amap_rsp_count_r <= 8'd0;
            cfg_ix_r   <= (uns_kind_i == PP_UNS_ASP_C) ? uns_desc_index_i
                                                        : uns_desc_type_i;
            desc_ix_r  <= (uns_kind_i == PP_UNS_CFG_C) ? uns_arg0_i
                                                        : uns_desc_index_i;
            name_ix_r  <= uns_arg0_i;
            name_cfg_r <= uns_arg1_i;
            desc_ty_r  <= (uns_kind_i == PP_UNS_AMAP_C)
                          ? uns_amap_count_i : 16'd0;
            raw_ct_r   <= uns_ct_w;
            walk_r     <= 11'd0;
            pid_lo_r   <= 2'b00;
            sent_r     <= 1'b0;
            a_st_r     <= A_DISP;
          end
        end

        // ---- GET_DYNAMIC_INFO pass 1: validate every record -------------
        A_GSCAN: begin
          if (!g_scan_started_r) begin
            //! IEEE 1722.1-2021 9.2.2.6 caps an AEM command cdl at 524.
            //! Milan 5.4.1 removes that ceiling only for responses. Refuse
            //! an oversized command before its record lengths can influence
            //! the aggregate response length or expose unwritten buffer RAM.
            if (cmd_r.cdl > 11'(ucpu_pkg::RESP_CAP_C)) begin
              upc_r   <= UPC_BADARG_C;
              echo_r  <= 1'b1;
              gdi_r   <= 1'b0;
              a_st_r  <= A_DISP;
            end else begin
              g_scan_started_r <= 1'b1;
              g_total_r        <= pld_trim_w;
              pld_r            <= pld_trim_w;
              pld_cmd_r        <= pld_trim_w;
              g_rd_pos_r       <= 11'd0;
              g_hdr_ix_r       <= 3'd0;
              g_rd_pending_r   <= 1'b0;
            end
          end else if (!g_rd_pending_r) begin
            if (g_rd_pos_r >= g_total_r) begin
              if (g_hdr_ix_r != 3'd0) begin
                upc_r   <= UPC_BADARG_C;
                echo_r  <= 1'b1;
                gdi_r   <= 1'b0;
                a_st_r  <= A_DISP;
              end else if (g_total_r == 11'd0) begin
                pld_r   <= 11'd0;
                status_r <= ST_SUCCESS_C;
                a_st_r  <= A_GDONE;
              end else begin
                //! The response starts with no dynamic_info records. Its
                //! length is owned by successful appends, never by the
                //! command payload retained for the validation pass.
                pld_r           <= 11'd0;
                g_rd_pos_r     <= 11'd0;
                g_hdr_ix_r     <= 3'd0;
                g_load_data_r  <= 1'b0;
                g_data_head_r  <= 64'd0;
                a_st_r         <= A_GLOAD;
              end
            end else if ((g_hdr_ix_r == 3'd0)
                         && ((g_total_r - g_rd_pos_r) < 11'd8)) begin
              upc_r   <= UPC_BADARG_C;
              echo_r  <= 1'b1;
              gdi_r   <= 1'b0;
              a_st_r  <= A_DISP;
            end else begin
              g_rd_pending_r <= 1'b1;
            end
          end else begin
            g_rd_pending_r <= 1'b0;
            unique case (g_hdr_ix_r)
              3'd0: begin
                g_scan_len_r[15:8] <= rxs_rd_data_i;
                g_hdr_ix_r <= 3'd1;
                g_rd_pos_r <= g_rd_pos_r + 11'd1;
              end
              3'd1: begin
                g_scan_len_r[7:0] <= rxs_rd_data_i;
                g_hdr_ix_r <= 3'd2;
                g_rd_pos_r <= g_rd_pos_r + 11'd1;
              end
              3'd2, 3'd3, 3'd5: begin
                g_hdr_ix_r <= g_hdr_ix_r + 3'd1;
                g_rd_pos_r <= g_rd_pos_r + 11'd1;
              end
              3'd4: begin
                //! SUCCESS is the required command value, but this byte does
                //! not affect record boundaries or whitelist membership. It
                //! is judged independently during pass 2.
                g_hdr_ix_r <= 3'd5;
                g_rd_pos_r <= g_rd_pos_r + 11'd1;
              end
              3'd6: begin
                g_scan_cmd_hi_r <= rxs_rd_data_i;
                g_hdr_ix_r <= 3'd7;
                g_rd_pos_r <= g_rd_pos_r + 11'd1;
              end
              default: begin
                if (!gdi_allowed({g_scan_cmd_hi_r, rxs_rd_data_i})
                    || ((17'(g_rd_pos_r) + 17'd1
                         + 17'(g_scan_len_r)) > 17'(g_total_r))) begin
                  upc_r   <= UPC_BADARG_C;
                  echo_r  <= 1'b1;
                  gdi_r   <= 1'b0;
                  a_st_r  <= A_DISP;
                end else begin
                  g_rd_pos_r <= g_rd_pos_r + 11'd1 + 11'(g_scan_len_r);
                  g_hdr_ix_r <= 3'd0;
                end
              end
            endcase
          end
        end

        // ---- GET_DYNAMIC_INFO pass 2: load one complete record ----------
        A_GLOAD: begin
          if (!g_rd_pending_r) begin
            g_rd_pending_r <= 1'b1;
          end else begin
            g_rd_pending_r <= 1'b0;
            if (!g_load_data_r) begin
              unique case (g_hdr_ix_r)
                3'd0: g_rec_len_r[15:8] <= rxs_rd_data_i;
                3'd1: g_rec_len_r[7:0]  <= rxs_rd_data_i;
                3'd4: g_rec_cmd_status_r <= rxs_rd_data_i;
                3'd6: g_rec_cmd_r[15:8] <= rxs_rd_data_i;
                3'd7: begin
                  g_rec_cmd_r[7:0] <= rxs_rd_data_i;
                  g_data_start_r   <= g_rd_pos_r + 11'd1;
                  g_next_pos_r     <= g_rd_pos_r + 11'd1
                                      + 11'(g_rec_len_r);
                  g_data_ix_r      <= 11'd0;
                  g_data_head_r    <= 64'd0;
                  g_load_data_r    <= (g_rec_len_r != 16'd0);
                  if (g_rec_len_r == 16'd0) a_st_r <= A_GDEC;
                end
                default: ;
              endcase
              g_rd_pos_r <= g_rd_pos_r + 11'd1;
              if (g_hdr_ix_r != 3'd7) g_hdr_ix_r <= g_hdr_ix_r + 3'd1;
            end else begin
              unique case (g_data_ix_r[2:0])
                3'd0: if (g_data_ix_r < 11'd8)
                        g_data_head_r[63:56] <= rxs_rd_data_i;
                3'd1: if (g_data_ix_r < 11'd8)
                        g_data_head_r[55:48] <= rxs_rd_data_i;
                3'd2: if (g_data_ix_r < 11'd8)
                        g_data_head_r[47:40] <= rxs_rd_data_i;
                3'd3: if (g_data_ix_r < 11'd8)
                        g_data_head_r[39:32] <= rxs_rd_data_i;
                3'd4: if (g_data_ix_r < 11'd8)
                        g_data_head_r[31:24] <= rxs_rd_data_i;
                3'd5: if (g_data_ix_r < 11'd8)
                        g_data_head_r[23:16] <= rxs_rd_data_i;
                3'd6: if (g_data_ix_r < 11'd8)
                        g_data_head_r[15:8] <= rxs_rd_data_i;
                default: if (g_data_ix_r < 11'd8)
                           g_data_head_r[7:0] <= rxs_rd_data_i;
              endcase
              g_rd_pos_r  <= g_rd_pos_r + 11'd1;
              g_data_ix_r <= g_data_ix_r + 11'd1;
              if ((g_data_ix_r + 11'd1) >= 11'(g_rec_len_r)) begin
                g_load_data_r <= 1'b0;
                a_st_r        <= A_GDEC;
              end
            end
          end
        end

        // ---- decide response shape, including silent overflow skip -------
        A_GDEC: begin
          if ((g_out_r + 11'd8 + g_sub_rlen_w)
              > 11'(ucpu_pkg::RESP_CAP_C)) begin
            g_rd_pos_r      <= g_next_pos_r;
            g_hdr_ix_r      <= 3'd0;
            g_load_data_r   <= 1'b0;
            g_data_head_r   <= 64'd0;
            g_rd_pending_r  <= 1'b0;
            a_st_r          <= (g_next_pos_r >= g_total_r) ? A_GDONE : A_GLOAD;
          end else begin
            g_rec_exec_r   <= g_sub_exec_w;
            g_rec_rlen_r   <= g_sub_rlen_w;
            g_rec_status_r <= g_sub_status_w;
            g_wr_phase_r   <= 2'd0;
            upc_r          <= g_sub_upc_w;
            cfg_ix_r       <= g_data_head_r[63:48];
            desc_ix_r      <= g_data_head_r[47:32];
            desc_ty_r      <= 16'd0;
            name_ix_r      <= g_data_head_r[31:16];
            name_cfg_r     <= g_data_head_r[15:0];
            ctrs_r         <= g_sub_exec_w && (g_rec_cmd_r == OP_GET_COUNTERS_C);
            amap_r         <= 1'b0;
            regun_r        <= 1'b0;
            acq_r          <= 1'b0;
            lockc_r        <= 1'b0;
            gstri_r        <= g_sub_exec_w
                              && (g_rec_cmd_r == OP_GET_STREAM_INFO_C);
            gavb_r         <= 1'b0;
            gasp_r         <= 1'b0;
            eavl_r         <= 1'b0;
            gcfg_r         <= g_sub_exec_w && (g_rec_cmd_r == OP_GET_CONFIG_C);
            gsfmt_r        <= g_sub_exec_w
                              && (g_rec_cmd_r == OP_GET_STREAM_FMT_C);
            gsrate_r       <= g_sub_exec_w
                              && (g_rec_cmd_r == OP_GET_SAMP_RATE_C);
            gclks_r        <= g_sub_exec_w
                              && (g_rec_cmd_r == OP_GET_CLOCK_SRC_C);
            ssrate_r       <= 1'b0;
            sclks_r        <= 1'b0;
            ssfmt_r        <= 1'b0;
            ssinfo_r       <= 1'b0;
            gctrl_r        <= 1'b0;
            sctrl_r        <= 1'b0;
            gname_r        <= g_sub_exec_w
                              && (g_rec_cmd_r == OP_GET_NAME_C);
            sname_r        <= 1'b0;
            scfg_r         <= 1'b0;
            setc_r         <= 1'b0;
            echo_r         <= 1'b0;
            a_st_r         <= A_GHDR;
          end
        end

        // ---- emit the record header before its command-specific data -----
        A_GHDR: begin
          if (rb_ready_w) begin
            if (g_wr_phase_r == 2'd0) begin
              g_wr_phase_r <= 2'd1;
            end else begin
              g_wr_phase_r <= 2'd0;
              if (g_rec_exec_r) begin
                a_st_r <= A_DISP;
              end else if (g_rec_len_r != 16'd0) begin
                g_rd_pos_r      <= g_data_start_r;
                g_data_ix_r     <= 11'd0;
                g_rd_pending_r  <= 1'b0;
                a_st_r          <= A_GCOPY;
              end else begin
                g_out_r <= g_out_r + 11'd8 + g_rec_rlen_r;
                pld_r   <= g_out_r + g_rec_rlen_r - 11'd4;
                g_rd_pos_r     <= g_next_pos_r;
                g_hdr_ix_r     <= 3'd0;
                g_data_head_r  <= 64'd0;
                a_st_r <= (g_next_pos_r >= g_total_r) ? A_GDONE : A_GLOAD;
              end
            end
          end
        end

        // ---- copy legal but unsupported command data unchanged -----------
        A_GCOPY: begin
          if (!g_rd_pending_r) begin
            g_rd_pending_r <= 1'b1;
          end else if (rb_ready_w) begin
            g_rd_pending_r <= 1'b0;
            g_rd_pos_r     <= g_rd_pos_r + 11'd1;
            g_data_ix_r    <= g_data_ix_r + 11'd1;
            if ((g_data_ix_r + 11'd1) >= 11'(g_rec_len_r)) begin
              g_out_r <= g_out_r + 11'd8 + g_rec_rlen_r;
              pld_r   <= g_out_r + g_rec_rlen_r - 11'd4;
              g_rd_pos_r     <= g_next_pos_r;
              g_hdr_ix_r     <= 3'd0;
              g_data_head_r  <= 64'd0;
              a_st_r <= (g_next_pos_r >= g_total_r) ? A_GDONE : A_GLOAD;
            end
          end
        end

        // ---- patch the status returned by the ordinary getter ------------
        A_GPATCH: begin
          if (rb_ready_w) begin
            g_out_r <= g_sub_end_r;
            pld_r   <= g_sub_end_r - 11'd12;
            g_rd_pos_r     <= g_next_pos_r;
            g_hdr_ix_r     <= 3'd0;
            g_data_head_r  <= 64'd0;
            g_rd_pending_r <= 1'b0;
            a_st_r <= (g_next_pos_r >= g_total_r) ? A_GDONE : A_GLOAD;
          end
        end

        // ---- one aggregate response after every record has retired -------
        A_GDONE: begin
          status_r    <= g_shape_fault_r ? ST_ENTITY_MISBEHAVING_C
                                         : ST_SUCCESS_C;
          echo_r      <= 1'b0;
          sent_r      <= 1'b1;
          bidx_r      <= 11'd0;
          frame_len_r <= pad_len_w;
          a_st_r      <= A_ALLOC;
        end

        // ---- copy the command payload out of the RX slot -----------------
        A_PLD: begin
          if (walk_r == 11'd0) begin
            pld_r     <= pld_trim_w;      // the committed-slot ceiling
            pld_cmd_r <= pld_trim_w;
          end
          if (walk_r < (pld_r + 11'd2)) begin
            walk_r <= walk_r + 11'd1;
          end else begin
            //! the MVU sub-decode, now that @22..@29 are settled: an MVU
            //! GET_MILAN_INFO leaves the generic echo for its own µprogram
            if (mvu_get_milan_info_w) begin
              upc_r  <= UPC_MVUINFO_C;
              echo_r <= 1'b0;
            end
            //! READ_DESCRIPTOR(ENTITY) overlays current_configuration from
            //! the same dynamic state GET_CONFIGURATION reads. IEEE
            //! §7.4.8.2 calls the two values equivalent, so the static image
            //! cannot remain the response source after SET_CONFIGURATION.
            //! Descriptor type is available only after this registered walk;
            //! all non-ENTITY reads retain the generic byte-exact program.
            if ((cmd_r.protocol == PP_PROTO_AEM)
                && (cmd_r.msg_type == 4'd0)
                && (cmd_r.opcode == OP_READ_DESCRIPTOR_C)
                && (cmd_r.cdl >= 11'd20)
                && (desc_ty_r == DT_ENTITY_C)) begin
              upc_r  <= UPC_RDESCENT_C;
              echo_r <= 1'b0;
            end
            //! ...and the audio-map TYPE gate at the same seam, for the same
            //! reason: descriptor_type is at @24 and cannot be judged at pop.
            //! BOTH Milan §5.4.2.26 halves are served now - the OUTPUT side
            //! re-dispatches to the two-word E_GAMAPO stub that swaps the
            //! type constant and falls into E_GAMAP's tail, and the
            //! integrator's face routes on amap_desc_type_o to the map store
            //! for that direction. Any other type keeps the NOT_IMPLEMENTED
            //! echo (`amap_r` stays set: E_NOTIMPL runs no gathers, so the
            //! gx routing it selects is never consulted on that arm).
            if (amap_r && (cfg_ix_r == DT_STREAM_PORT_OUT_C)) begin
              upc_r <= UPC_GAMAPO_C;
            end else if (amap_r && (cfg_ix_r != DT_STREAM_PORT_IN_C)) begin
              upc_r  <= UPC_NOTIMPL_C;
              echo_r <= 1'b1;
            end
            //! ADD/REMOVE_AUDIO_MAPPINGS has a variable body. The record
            //! count at @28 is authoritative only when cdl describes exactly
            //! that many 8-byte records and the committed RX slot contains
            //! the whole declared payload. This gate runs after the payload
            //! walk so a truncated command can never stage stale slot bytes.
            //! The two Milan Stream Port types are the implemented scope;
            //! every other existing descriptor type is NOT_SUPPORTED.
            if (amap_edit_r) begin
              amap_rsp_count_r <= amap_rx_count_w;
              if (({8'd0, cmd_r.cdl}
                   != (19'd20 + ({3'd0, desc_ty_r} << 3)))
                  || (cmd_r.cdl < 11'd20)
                  || (cmd_r.cdl > 11'd524)
                  || (pld_cmd_r != (cmd_r.cdl - 11'd12))) begin
                upc_r  <= UPC_BADARG_C;
                echo_r <= 1'b1;
              end else if ((cfg_ix_r != DT_STREAM_PORT_IN_C)
                           && (cfg_ix_r != DT_STREAM_PORT_OUT_C)) begin
                upc_r  <= UPC_NSUPPE_C;
                echo_r <= 1'b1;
              end else begin
                upc_r  <= amap_remove_r ? UPC_AMREMOVE_C : UPC_AMADD_C;
                echo_r <= 1'b1;
              end
            end
            //! ...and the registration pair re-dispatches HERE, off its
            //! registered discriminator - the pop decode left it on the
            //! NOT_IMPLEMENTED echo, which is also why `echo_r` is already
            //! the 1 both programs want (the REGISTER response's flags field
            //! is the command's own, §7.4.37.1 "share the same format")
            if (regun_r) begin
              upc_r <= cmd_r.opcode[0] ? UPC_DEREG_C : UPC_REGUN_C;
            end
            //! ACQUIRE_ENTITY: always the echo with NOT_SUPPORTED (Milan
            //! §5.4.2.1 - see the opcode table). LOCK_ENTITY: a §7.4.2
            //! command short of its 16-byte payload is BAD_ARGUMENTS (the
            //! truncated-READ_DESCRIPTOR reasoning); a non-ENTITY target is
            //! NOT_SUPPORTED with the command echoed; the real thing runs
            //! E_LOCKEN against the rgy face.
            if (acq_r) begin
              upc_r <= UPC_NSUPPE_C;
            end
            if (lockc_r) begin
              if (cmd_r.cdl < 11'd28)     upc_r <= UPC_BADARG_C;
              else if (!lock_ent_ok_r)    upc_r <= UPC_NSUPPE_C;
              else begin
                upc_r  <= UPC_LOCKEN_C;
                echo_r <= 1'b0;
              end
            end
            //! GET_COUNTERS' type gate, at the same registered seam (the
            //! bench probe's second strictness rule): §7.4.42.2 admits five
            //! target types and this build keeps counters for four:
            //! STREAM_INPUT, STREAM_OUTPUT, AVB_INTERFACE, CLOCK_DOMAIN.
            //! Any other type is
            //! Table 7-141's NOT_SUPPORTED ("the command is implemented but
            //! the target of the command is not supported") - carried in
            //! the FULL fixed body, because the reference stack reflects
            //! only NOT_IMPLEMENTED at command length and sizes every other
            //! non-success answer against the response form (la_avdecc
            //! checkResponsePayload; the r49a "Incorrect payload size"
            //! probe complaint was the old command-sized echo here).
            //! E_GCTRSNS runs no gathers, so the ctr routing `ctrs_r`
            //! selects is never consulted on this arm.
            if (ctrs_r && (cfg_ix_r != DT_STREAM_INPUT_C)
                && (cfg_ix_r != DT_STREAM_OUTPUT_C)
                && (cfg_ix_r != DT_AVB_INTERFACE_C)
                && (cfg_ix_r != DT_CLOCK_DOMAIN_C)) begin
              upc_r  <= UPC_GCTRSNS_C;
              echo_r <= 1'b0;
            end
            //! GET_STREAM_INFO: §7.4.16.1's command is descriptor_type +
            //! descriptor_index and nothing else, so cdl 16 is the whole
            //! command; §7.4.16 acts on STREAM_INPUT or STREAM_OUTPUT and
            //! anything else refuses NOT_SUPPORTED with the command echoed
            //! (the Milan §5.4.2.2 non-ENTITY precedent).
            if (gstri_r) begin
              if (cmd_r.cdl < 11'd16)                upc_r <= UPC_BADARG_C;
              else if ((cfg_ix_r != DT_STREAM_INPUT_C)
                       && (cfg_ix_r != DT_STREAM_OUTPUT_C))
                                                     upc_r <= UPC_NSUPPE_C;
              else begin
                upc_r  <= UPC_GSTRI_C;
                echo_r <= 1'b0;
              end
            end
            //! GET_AVB_INFO acts on AVB_INTERFACE only; GET_AS_PATH's
            //! command has no type field to gate - both demand their
            //! §7.4.40.1/§7.4.41.1 four payload bytes
            if (gavb_r) begin
              if (cmd_r.cdl < 11'd16)                 upc_r <= UPC_BADARG_C;
              else if (cfg_ix_r != DT_AVB_INTERFACE_C) upc_r <= UPC_NSUPPE_C;
              else begin
                upc_r  <= UPC_GAVB_C;
                echo_r <= 1'b0;
              end
            end
            if (gasp_r) begin
              if (cmd_r.cdl < 11'd16) upc_r <= UPC_BADARG_C;
              else begin
                upc_r  <= UPC_GASP_C;
                echo_r <= 1'b0;
              end
            end
            //! ---- the read-side set (Milan §5.4.2.3/.6/.8/.14/.16) --------
            //! ENTITY_AVAILABLE and GET_CONFIGURATION carry no payload at all
            //! (§7.4.3.1, §7.4.8.1), so there is no length to gate and no type
            //! to judge: cdl 12 IS the whole command. A controller that pads
            //! one is still answered - the walk stops at pld_trim and the
            //! programs build their own operands rather than trusting the
            //! capture registers.
            if (eavl_r) begin
              upc_r  <= UPC_EAVL_C;
              echo_r <= 1'b0;
            end
            if (gcfg_r) begin
              upc_r  <= UPC_GCFG_C;
              echo_r <= 1'b0;
            end
            //! ...and the three {type, index} reads gate on both, exactly like
            //! GET_STREAM_INFO above them. A wrong target draws the FULL-body
            //! NOT_SUPPORTED, never the command-sized E_NSUPPE echo: only
            //! NOT_IMPLEMENTED may answer at command length (§9.3.5.3.3 vs
            //! la_avdecc's checkResponsePayload, the 0x004A finding).
            if (gsfmt_r) begin
              if (cmd_r.cdl < 11'd16)                upc_r <= UPC_BADARG_C;
              else if ((cfg_ix_r != DT_STREAM_INPUT_C)
                       && (cfg_ix_r != DT_STREAM_OUTPUT_C)) begin
                upc_r  <= UPC_TIZ8NS_C;
                echo_r <= 1'b0;
              end else begin
                upc_r  <= UPC_GSFMT_C;
                echo_r <= 1'b0;
              end
            end
            if (gsrate_r) begin
              if (cmd_r.cdl < 11'd16)              upc_r <= UPC_BADARG_C;
              else if (cfg_ix_r != DT_AUDIO_UNIT_C) begin
                upc_r  <= UPC_TIZ4NS_C;
                echo_r <= 1'b0;
              end else begin
                upc_r  <= UPC_GSRATE_C;
                echo_r <= 1'b0;
              end
            end
            if (gclks_r) begin
              if (cmd_r.cdl < 11'd16)                upc_r <= UPC_BADARG_C;
              else if (cfg_ix_r != DT_CLOCK_DOMAIN_C) begin
                upc_r  <= UPC_TIZ4NS_C;
                echo_r <= 1'b0;
              end else begin
                upc_r  <= UPC_GCLKS_C;
                echo_r <= 1'b0;
              end
            end
            //! GET_NAME and SET_NAME address every named descriptor. The
            //! store validates both descriptor existence and semantic
            //! name_index, including ENTITY's second group_name slot. A SET
            //! must carry all 64 name bytes before staged RAM can be used.
            if (gname_r) begin
              upc_r <= ((cmd_r.cdl < 11'd20) || (pld_cmd_r < 11'd8))
                       ? UPC_NAMEBAD_C : UPC_GNAME_C;
              echo_r <= 1'b0;
            end
            if (sname_r) begin
              upc_r <= ((cmd_r.cdl != 11'd84) || (pld_cmd_r != 11'd72))
                       ? UPC_NAMEBAD_C : UPC_SNAME_C;
              echo_r <= 1'b0;
            end
            //! ---- the SET pair (Milan §5.4.2.13 / §5.4.2.15) ------------
            //! Their command carries a VALUE, so the length floor is the full
            //! §7.4.21.1 / §7.4.23.1 body (cdl 20), not the 16 a getter
            //! needs: a short SET never reached its argument, and storing
            //! whatever the slot happened to hold is the one outcome worse
            //! than refusing. The wrong-target refusal is the same full-body
            //! NOT_SUPPORTED the getters use.
            if (ssrate_r) begin
              if (cmd_r.cdl < 11'd20)               upc_r <= UPC_BADARG4_C;
              else if (cfg_ix_r != DT_AUDIO_UNIT_C) upc_r <= UPC_TIZ4NS_C;
              else                                  upc_r <= UPC_SSRATE_C;
              echo_r <= 1'b0;
            end
            if (sclks_r) begin
              if (cmd_r.cdl < 11'd20)                 upc_r <= UPC_BADARG4_C;
              else if (cfg_ix_r != DT_CLOCK_DOMAIN_C) upc_r <= UPC_TIZ4NS_C;
              else                                    upc_r <= UPC_SCLKS_C;
              echo_r <= 1'b0;
            end
            //! ---- the IDENTIFY pair (Milan §5.4.2.17/.18) ---------------
            //! Both are scoped to a CONTROL descriptor and both answer in the
            //! 5-byte §7.3.5.2 body, so their refusals use the cdl-17 stubs
            //! rather than the cdl-20 ones the rest of the family shares.
            //! SET_CONTROL's floor is cdl 17, the whole Figure 7-49 command.
            if (gctrl_r) begin
              if (cmd_r.cdl < 11'd16)            upc_r <= UPC_BADARG1_C;
              else if (cfg_ix_r != DT_CONTROL_C) upc_r <= UPC_NSUPP1_C;
              else                               upc_r <= UPC_GCTRL_C;
              echo_r <= 1'b0;
            end
            if (sctrl_r) begin
              if (cmd_r.cdl < 11'd17)            upc_r <= UPC_BADARG1_C;
              else if (cfg_ix_r != DT_CONTROL_C) upc_r <= UPC_NSUPP1_C;
              else                               upc_r <= UPC_SCTRL_C;
              echo_r <= 1'b0;
            end
            //! ---- SET_CONFIGURATION (Milan §5.4.2.5) --------------------
            //! The refusal is the reduction over EVERY stream, not a test of
            //! the descriptor named: "shall not accept ... if ONE OF the
            //! Stream Input is bound or ONE OF the Stream Output is
            //! streaming". §7.4.7.1's command is 4 bytes, so cdl 16 is the
            //! whole thing; §7.4.8.1, GET_CONFIGURATION's, is zero.
            if (scfg_r) begin
              if (cmd_r.cdl < 11'd16)  upc_r <= UPC_SCFGBAD_C;
              else if (any_running_w)  upc_r <= UPC_SCFGRUN_C;
              else                     upc_r <= UPC_SCFG_C;
              echo_r <= 1'b0;
            end
            //! ---- START/STOP_STREAMING (Milan §5.4.2.19 / §5.4.2.20) ----
            //! The TYPE is settled here rather than in the µprogram because
            //! the µprogram's only existence test is the DESC_ADDR locate,
            //! and a locate on a descriptor that is not a Stream Input can
            //! HIT — {ENTITY, 0} does. Routing a wrong type into the write
            //! path would move started state for a descriptor that has none.
            //! Milan's "shall not support ... for a Stream Output" is one
            //! instance of that, not a case beside it, so a Stream Output and
            //! a CLOCK_DOMAIN take the same NOT_SUPPORTED arm.
            //! §7.4.35.1's command is 4 bytes, so cdl 16 is the whole of it.
            //! ORDER, stated rather than inherited from code layout: the type
            //! refusal runs BEFORE the µprogram's locate and lock check, so a
            //! Stream Output named with a nonexistent index answers
            //! NOT_SUPPORTED rather than NO_SUCH_DESCRIPTOR, and a foreign
            //! controller naming a Stream Output under lock gets
            //! NOT_SUPPORTED rather than ENTITY_LOCKED. Neither standard
            //! orders these checks against each other, and answering "this
            //! target is not supported" first is the more specific reading of
            //! Milan's "shall not support ... for a Stream Output".
            if (strm_r) begin
              if (cmd_r.cdl < 11'd16)                 upc_r <= UPC_STRMBAD_C;
              else if (cfg_ix_r != DT_STREAM_INPUT_C) upc_r <= UPC_STRMNS_C;
              else if (strt_r)                        upc_r <= UPC_STRT_C;
              else                                    upc_r <= UPC_STOP_C;
              echo_r <= 1'b0;
            end
            //! ---- SET_STREAM_FORMAT (Milan §5.4.2.7) --------------------
            //! §7.4.9.1's command is 12 bytes, so cdl 24 is the whole of it,
            //! and the `pld_cmd_r` conjunct is the amap_edit lesson: cdl is
            //! a CLAIM, and a committed slot shorter than the claim leaves
            //! the format capture holding a fragment - refusing on the
            //! WALKED length is what keeps a fragment from being judged.
            //! The type gate takes both stream directions (Milan implements
            //! this SET for Stream Inputs AND Outputs); the per-descriptor
            //! running route sits between the type gate and the twins so a
            //! running stream refuses before lock and locate, mirroring
            //! SET_CONFIGURATION's dispatch-routed reduction arm.
            if (ssfmt_r) begin
              if ((cmd_r.cdl < 11'd24)
                  || (pld_cmd_r < 11'd12))            upc_r <= UPC_SFBAD_C;
              else if ((cfg_ix_r != DT_STREAM_INPUT_C)
                       && (cfg_ix_r != DT_STREAM_OUTPUT_C))
                                                      upc_r <= UPC_TIZ8NS_C;
              else if (run_this_w)                    upc_r <= UPC_SFRUN_C;
              else if (cfg_ix_r == DT_STREAM_INPUT_C) upc_r <= UPC_SFMTI_C;
              else                                    upc_r <= UPC_SFMTO_C;
              echo_r <= 1'b0;
            end
            //! ---- SET_STREAM_INFO (Milan §5.4.2.9) ---------------------
            //! Every narrowing is settled HERE, off registered walk fields:
            //! the length floor is 1722.1-2021 Figure 7-40's COMPLETE body
            //! (84 payload bytes, cdl 96) - Milan v1.2 references the 2021
            //! edition, so the 2013 60-byte shape is a truncated command
            //! here, refused BAD_ARGUMENTS at the full 2021 response length
            //! (the compatibility note for shorter bodies covers a
            //! controller READING an older entity's response, never this
            //! responder accepting a legacy command). The appended ip
            //! fields are walked and echoed, never interpreted. The
            //! walked-length conjunct guards the @48 capture as above; a
            //! Stream Input target is NOT_SUPPORTED (Milan implements this
            //! command for Stream Outputs only); the flags word must be
            //! EXACTLY MSRP_ACC_LAT_VALID (any other sub-command refuses the
            //! whole command, never applies a part of it); and bit 31 of the
            //! latency is outside the presentation-time range the store
            //! carries, BAD_ARGUMENTS. Command and response share the
            //! figure, so every route keeps the pop-time echo - the refusals
            //! answer at the response's own length by construction, and the
            //! success body's one updated field is the value the echo
            //! already carries.
            if (ssinfo_r) begin
              //! the short-command stub is the ONE route that must not echo:
              //! a truncated command's echo is command-sized, and a refusal
              //! has to be the size of the response it refuses, so E_SIBAD
              //! builds the full zero body itself
              if ((cmd_r.cdl < 11'd96)
                  || (pld_cmd_r < 11'd84)) begin
                upc_r  <= UPC_SIBAD_C;
                echo_r <= 1'b0;
              end
              else if (cfg_ix_r != DT_STREAM_OUTPUT_C)
                                                      upc_r <= UPC_NSUPPE_C;
              //! §5.4.2.9's own SHALL: a STREAMING output refuses the whole
              //! command with STREAM_IS_RUNNING, before the sub-command is
              //! even examined - the same route order as SET_STREAM_FORMAT
              else if (run_this_w)                    upc_r <= UPC_SIRUN_C;
              else if (setval_r[63:32] != SIF_ACC_LAT_C)
                                                      upc_r <= UPC_NSUPPE_C;
              else if (silat_r[31])                   upc_r <= UPC_BADARG_C;
              else                                    upc_r <= UPC_SINFO_C;
            end
            a_st_r <= A_DISP;
          end
          //! the RX pool answers one cycle after rd_en: byte for index
          //! walk_r-1 lands now.
          //! §7.4.42.1, §7.4.44.1 and §7.4.5 disagree about what lives where,
          //! so the three shapes are captured into the SAME registers under
          //! `ctrs_r`/`amap_r`:
          //! a counters command has {type @24, index @26} and stops there,
          //! an audio-map command has {type @24, index @26, map_index @28,
          //! reserved @30} - `desc_ty_r` MEANS map_index for it - and
          //! a READ_DESCRIPTOR has {configuration_index @24, reserved @26,
          //! type @28, index @30}. Guarding both directions matters — a
          //! counters command padded past @27 must not walk on into
          //! `desc_ty_r` and change the descriptor it is asked about, and an
          //! audio-map command's reserved word at @30 must not trample the
          //! `desc_ix_r` it captured at @26.
          if (walk_r != 11'd0) begin
            unique case (walk_r - 11'd1)
              11'd0: raw_ct_r[15:8]  <= rxs_rd_data_i;
              11'd1: raw_ct_r[7:0]   <= rxs_rd_data_i;
              11'd2: cfg_ix_r[15:8]  <= rxs_rd_data_i;
              11'd3: cfg_ix_r[7:0]   <= rxs_rd_data_i;
              //! @26..@27 carry FOUR different things and each arm takes
              //! only its own: MVU's protocol_id tail (kept as the COMPARISON,
              //! not the bytes), GET_COUNTERS' and GET_AUDIO_MAP's
              //! descriptor_index, and READ_DESCRIPTOR's reserved field,
              //! which nobody keeps
              //! ...a REGISTER command's flags[15:0] land here too: the
              //! TIME_LIMITED bit is @27 bit 0 (Table 7-147), so `desc_ix_r`
              //! holds the flags' low half for the rgy face to read
              11'd4: begin
                pid_lo_r[1] <= (rxs_rd_data_i == MVU_PID_L1_C);
                if (ix26_w) desc_ix_r[15:8] <= rxs_rd_data_i;
              end
              11'd5: begin
                pid_lo_r[0] <= (rxs_rd_data_i == MVU_PID_L0_C);
                if (ix26_w) desc_ix_r[7:0]  <= rxs_rd_data_i;
              end
              11'd6: begin
                if (!ctrs_r) desc_ty_r[15:8] <= rxs_rd_data_i;
                if (gname_r || sname_r) name_ix_r[15:8] <= rxs_rd_data_i;
                //! ...and the SET family's argument starts here, at @28. It
                //! is shifted in BIG-ENDIAN so an 8-byte stream format lands
                //! already right-justified; the narrower fields are
                //! re-justified once, at the operand mux, where the engine
                //! knows which command it is holding.
                if (setc_r) setval_r[63:56] <= rxs_rd_data_i;
              end
              11'd7: begin
                if (!ctrs_r) desc_ty_r[7:0]  <= rxs_rd_data_i;
                if (gname_r || sname_r) name_ix_r[7:0] <= rxs_rd_data_i;
                if (setc_r) setval_r[55:48] <= rxs_rd_data_i;
              end
              //! ...and the registration/lock shapes guard BACKWARD like the
              //! counters shape does: a LOCK's locked_id bytes at @30..@31
              //! (or a long REGISTER's padding) must not trample the flags
              //! captured at @26..@27 - the UNLOCK/TIME_LIMITED bit lives
              //! there (found by the pp_top L5 check: UNLOCK re-locked)
              11'd8: begin
                if (!ix26_w && !gasp_r) desc_ix_r[15:8] <= rxs_rd_data_i;
                if (gname_r || sname_r) name_cfg_r[15:8] <= rxs_rd_data_i;
                if (setc_r) setval_r[47:40] <= rxs_rd_data_i;
              end
              11'd9: begin
                if (!ix26_w && !gasp_r) desc_ix_r[7:0]  <= rxs_rd_data_i;
                if (gname_r || sname_r) name_cfg_r[7:0] <= rxs_rd_data_i;
                if (setc_r) setval_r[39:32] <= rxs_rd_data_i;
              end
              11'd10: if (setc_r) setval_r[31:24] <= rxs_rd_data_i;
              11'd11: if (setc_r) setval_r[23:16] <= rxs_rd_data_i;
              11'd12: if (setc_r) setval_r[15:8]  <= rxs_rd_data_i;
              11'd13: if (setc_r) setval_r[7:0]   <= rxs_rd_data_i;
              //! LOCK_ENTITY's descriptor_type/index live at @36..@39, past
              //! every capture register - but the CHECK is all Milan
              //! §5.4.2.2 needs ("shall not allow locking another
              //! descriptor than the ENTITY descriptor"), and ENTITY[0] is
              //! four zero bytes, so the walk keeps the comparison RESULT
              //! in one flop instead of the four bytes
              11'd14, 11'd15, 11'd16, 11'd17:
                if (lockc_r && (rxs_rd_data_i != 8'd0)) lock_ent_ok_r <= 1'b0;
              //! SET_STREAM_INFO's msrp_accumulated_latency, @48..@51
              //! (Figure 7-40). Guarded on its own discriminator so no other
              //! long command's padding can reach the register, and settled
              //! well before the A_PLD exit reads it - a cdl-96 command's
              //! walk runs to index 83.
              11'd26: if (ssinfo_r) silat_r[31:24] <= rxs_rd_data_i;
              11'd27: if (ssinfo_r) silat_r[23:16] <= rxs_rd_data_i;
              11'd28: if (ssinfo_r) silat_r[15:8]  <= rxs_rd_data_i;
              11'd29: if (ssinfo_r) silat_r[7:0]   <= rxs_rd_data_i;
              default: ;
            endcase

          end
        end

        A_DISP: begin
          //! stage-0 operand latch: the strobe rises one cycle into A_DISP,
          //! so the operand muxes settle into flops before the µCPU's
          //! preload (S_PRE1/S_PRE0) ever reads them
          if (!disp_valid_r) begin
            opd0_r <= opd0_w;
            opd1_r <= opd1_w;
            opd2_r <= opd2_w;
          end
          disp_valid_r <= 1'b1;
          if (disp_valid_r && disp_ready_w) begin
            disp_valid_r <= 1'b0;
            a_st_r       <= A_RUN;
          end
        end

        A_RUN: begin
          if (resp_send_w) begin
            if (gdi_r) begin
              g_rec_status_r <= resp_status_w;
              g_sub_end_r    <= resp_len_w;
            end else begin
              sent_r   <= 1'b1;
              status_r <= resp_status_w;
              //! the µCPU owns the payload for a command it really answers;
              //! an echoed one keeps the command's own length (§9.3.5.3.3).
              if (amap_edit_r) begin
                pld_r <= amap_edit_pld_w;
              end else if (!echo_r) begin
                pld_r <= (resp_len_w > 11'd12)
                         ? ((resp_len_w - 11'd12) > 11'(PLD_MAX_C)
                            ? 11'(PLD_MAX_C) : (resp_len_w - 11'd12))
                         : 11'd0;
              end else begin
                pld_r <= pld_cmd_r;
              end
            end
          end
          if (ucpu_done_w) begin
            if (gdi_r) begin
              //! g_rec_rlen_r is the shape selected before dispatch, while
              //! resp_len_w is the getter's actual cursor. A future getter
              //! edit must not silently misalign every following record or
              //! expose stale response memory. Void the aggregate if the two
              //! authorities disagree.
              if ((resp_send_w ? resp_len_w : g_sub_end_r)
                  != (g_out_r + 11'd8 + g_rec_rlen_r)) begin
                g_shape_fault_r <= 1'b1;
                pld_r           <= 11'd0;
                echo_r          <= 1'b0;
                a_st_r          <= A_GDONE;
              end else begin
                a_st_r <= A_GPATCH;
              end
            end else begin
              bidx_r      <= 11'd0;
              frame_len_r <= pad_len_w;
              //! a µprogram that retired without SEND_RESPONSE has no
              //! response to emit; free the slot instead.
              a_st_r      <= (sent_r || resp_send_w) ? A_ALLOC : A_FREE;
              if (!(sent_r || resp_send_w) && (drop_cnt_r != 16'hFFFF)) begin
                drop_cnt_r <= drop_cnt_r + 16'd1;
              end
            end
          end
        end

        A_ALLOC: begin
          if (rsp_fail_w) begin
            err_mode_r  <= 1'b1;
            status_r    <= ST_ENTITY_MISBEHAVING_C;
            pld_r       <= amap_edit_r ? amap_edit_pld_w : 11'd0;
            frame_len_r <= amap_edit_r
                           ? ((11'(FRAME_HDR_C) + amap_edit_pld_w
                               < 11'(ETH_MIN_C))
                              ? 11'(ETH_MIN_C)
                              : 11'(FRAME_HDR_C) + amap_edit_pld_w)
                           : 11'(ETH_MIN_C);
            bidx_r      <= 11'd0;
            if (rerr_cnt_r != 16'hFFFF) rerr_cnt_r <= rerr_cnt_r + 16'd1;
          end else if (txs_alloc_gnt_i) begin
            tx_slot_r <= txs_alloc_slot_i;
            a_st_r    <= A_WR;
          end
        end

        A_WR: begin
          //! The response memory died under a frame that is already partly
          //! written. Rewrite it from byte 0 using only registered state.
          //! Mapping edits retain Figure 7-71's fixed body and staged records.
          if (rsp_fail_w) begin
            err_mode_r  <= 1'b1;
            status_r    <= ST_ENTITY_MISBEHAVING_C;
            pld_r       <= amap_edit_r ? amap_edit_pld_w : 11'd0;
            frame_len_r <= amap_edit_r
                           ? ((11'(FRAME_HDR_C) + amap_edit_pld_w
                               < 11'(ETH_MIN_C))
                              ? 11'(ETH_MIN_C)
                              : 11'(FRAME_HDR_C) + amap_edit_pld_w)
                           : 11'(ETH_MIN_C);
            bidx_r      <= 11'd0;
            if (rerr_cnt_r != 16'hFFFF) rerr_cnt_r <= rerr_cnt_r + 16'd1;
          end else if (byte_ok_w) begin
            if (bidx_r + 11'd1 >= frame_len_r) a_st_r <= A_CMT;
            bidx_r <= bidx_r + 11'd1;
          end
        end

        A_CMT: begin
          if (resp_cnt_r != 16'hFFFF) resp_cnt_r <= resp_cnt_r + 16'd1;
          a_st_r <= A_TXW;
        end

        A_TXW: if (uns_r ? txreq_uns_ready_i : txreq_ready_i) begin
          a_st_r <= A_FREE;
        end

        A_FREE: a_st_r <= A_IDLE;

        default: a_st_r <= A_IDLE;
      endcase
    end
  end

endmodule : KL_aecp_engine
`default_nettype wire
