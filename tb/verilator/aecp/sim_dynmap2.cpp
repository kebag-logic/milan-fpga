/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * MULTI-PORT dynamic audio-map harness (roadmap 23): KL_aecp_top compiled
 * against the two-dynamic-input-port shape svh (gen_dynmap2_shape.py —
 * STREAM_PORT_INPUT 0/1 both map_mode dynamic, 8 mono clusters each at
 * base_cluster 0 and 8, map_page 4 => number_of_maps 2 per port; three
 * STREAM_INPUTs, the third a CRF; STREAM_PORT_OUTPUT[0] static). Milan v1.2
 * 5.3.3.9 makes dynamic mappings a shall on EVERY Stream Port Input, so this
 * is the shape a real 4x4 / 8x8 listener build compiles. Exercises what the
 * single-port harness structurally cannot:
 *   - both ports advertise number_of_maps = 0 (1722.1-2021 7.2.13)
 *   - the store keys are GLOBAL (base_cluster + offset) but every wire
 *     cluster_offset is PORT-RELATIVE (7.2.19), so the two ports' maps are
 *     independent and port 1 mirrors into render addresses 4..7
 *   - a cluster_offset inside the GLOBAL key space but outside the addressed
 *     port's own cluster block is BAD_ARGUMENTS, not an aliased write
 *   - mapping_stream_index names ANY Stream Input (Table 7-33), the channel
 *     bound is that stream's OWN current format (Milan 5.3.10.1), a CRF or
 *     absent stream index is invalid, and SET_STREAM_FORMAT moves ONE
 *     stream's bound without touching the other's
 *   - REMOVE matches on stream_index too
 *   - an out-of-range STREAM_PORT_INPUT is NO_SUCH_DESCRIPTOR while the
 *     static output port refuses GET as well as ADD/REMOVE (5.4.2.26-28)
 *   - a mapping onto a cluster the render crossbar cannot reach (16 declared
 *     keys, depth 10) is refused, not accepted-then-dropped (7.4.45.1)
 *   - REMOVE of a mapping that is NOT PRESENT fails the whole command
 *     (7.4.46.1) while DUPLICATES still succeed (Milan 5.4.2.28)
 *   - a frame whose control_data_length promises more octets than it
 *     delivered is refused outright, so no mapping is ever committed out of
 *     the previous command's capture-buffer residue
 * Exit 0 = all pass.
 */

#include "VKL_aecp_top.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <array>
#include <vector>

static VKL_aecp_top* dut;
static long checks = 0, fails = 0;

//! chmap64 fabric-mirror recorder: every dmap_wr_p_o pulse (addr, word)
struct DmapWr { int addr, word; };
static std::vector<DmapWr> g_dmap_wrs;
static void tick() {
    dut->clk_i = 0; dut->eval();
    dut->clk_i = 1; dut->eval();
    if (dut->dmap_wr_p_o)
        g_dmap_wrs.push_back({(int)dut->dmap_wr_addr_o, (int)dut->dmap_wr_word_o});
}
static std::vector<DmapWr> take_wrs() { auto v = g_dmap_wrs; g_dmap_wrs.clear(); return v; }
static void ck(const char* what, long got, long exp) {
    checks++;
    if (got != exp) { fails++; printf("  [FAIL] %-52s got=%ld exp=%ld\n", what, got, exp); }
    else            { printf("  [ ok ] %-52s = %ld\n", what, got); }
}

static const uint8_t ENT_MAC[6] = {0x02,0x00,0x00,0xff,0xfe,0x01};
static const uint8_t CTL_MAC[6] = {0x68,0x05,0xca,0x95,0xb2,0xd1};
static const uint64_t ENTITY_ID = 0x0200'00ff'fe00'0001ULL;
static const uint64_t CTLR_ID   = 0x6805'ca95'b2d1'0000ULL;

static void put_be64(std::vector<uint8_t>& v, uint64_t x) {
    for (int i = 7; i >= 0; i--) v.push_back((x >> (8*i)) & 0xFF);
}
static void put_be16(std::vector<uint8_t>& v, uint16_t x) {
    v.push_back(x >> 8); v.push_back(x & 0xFF);
}

static std::vector<uint8_t> aem_cmd(uint16_t cmd, uint16_t seq,
                                    const std::vector<uint8_t>& payload) {
    std::vector<uint8_t> f;
    for (int i=0;i<6;i++) f.push_back(ENT_MAC[i]);
    for (int i=0;i<6;i++) f.push_back(CTL_MAC[i]);
    put_be16(f, 0x22F0);
    f.push_back(0xFB);                          // subtype AECP
    f.push_back(0x00);                          // AEM_COMMAND
    uint16_t cdl = 12 + (uint16_t)payload.size();
    f.push_back((cdl >> 8) & 0x7);
    f.push_back(cdl & 0xFF);
    put_be64(f, ENTITY_ID);
    put_be64(f, CTLR_ID);
    put_be16(f, seq);
    f.push_back((cmd >> 8) & 0x7F);
    f.push_back(cmd & 0xFF);
    for (auto b : payload) f.push_back(b);
    while (f.size() < 60) f.push_back(0x00);
    return f;
}

static void feed_rx(const std::vector<uint8_t>& f) {
    int n = f.size();
    for (int off = 0; off < n; off += 8) {
        uint64_t d = 0; uint8_t keep = 0;
        for (int l = 0; l < 8; l++)
            if (off + l < n) { d |= (uint64_t)f[off+l] << (8*l); keep |= (1<<l); }
        dut->rx_tvalid_i = 1;
        dut->rx_tdata_i  = d;
        dut->rx_tkeep_i  = keep;
        dut->rx_tlast_i  = (off + 8 >= n);
        tick();
    }
    dut->rx_tvalid_i = 0; dut->rx_tlast_i = 0; dut->rx_tkeep_i = 0;
}

static std::vector<uint8_t> collect_resp(int budget = 8000) {
    std::vector<uint8_t> b;
    int idle = 0;
    dut->m_axis_tready = 1;
    for (int c = 0; c < budget; c++) {
        dut->eval();
        if (dut->m_axis_tvalid && dut->m_axis_tready) {
            for (int l = 0; l < 8; l++)
                if ((dut->m_axis_tkeep >> l) & 1)
                    b.push_back((dut->m_axis_tdata >> (8*l)) & 0xFF);
            bool last = dut->m_axis_tlast;
            tick();
            if (last) return b;
            idle = 0;
        } else {
            tick();
            if (++idle > 500) return b;
        }
    }
    return b;
}

static int r_status(const std::vector<uint8_t>& b){ return b.size()>16 ? (b[16]>>3)&0x1F : -1; }
//! control_data_length of the response (11 bits spanning bytes 16..17)
static int b_cdl(const std::vector<uint8_t>& b){
    return b.size()>17 ? (((b[16]&0x7)<<8) | b[17]) : -1;
}
static int r_be16(const std::vector<uint8_t>& b, size_t off){
    return b.size() > off+1 ? (b[off]<<8 | b[off+1]) : -1;
}

static uint16_t seq = 0x6000;
static std::vector<uint8_t> xact(uint16_t cmd, const std::vector<uint8_t>& pl) {
    feed_rx(aem_cmd(cmd, seq++, pl));
    return collect_resp();
}

static const uint16_t CMD_READ = 4, CMD_SET_FMT = 8;
static const uint16_t CMD_GET_MAP = 43, CMD_ADD_MAP = 44, CMD_RM_MAP = 45;
static const uint16_t SPI = 0x000E, SPO = 0x000F, STRIN = 0x0005;
static const uint64_t AAF2 = 0x0205022000806000ULL;  // 48k 2ch (reset default)
static const uint64_t AAF8 = 0x0205022002006000ULL;  // 48k 8ch concrete

// GET_AUDIO_MAP payload: type(2) idx(2) map_index(2) reserved(2)
static std::vector<uint8_t> gm_pl(uint16_t t, uint16_t i, uint16_t page) {
    std::vector<uint8_t> pl;
    put_be16(pl, t); put_be16(pl, i); put_be16(pl, page); put_be16(pl, 0);
    return pl;
}
// ADD/REMOVE payload: type(2) idx(2) n(2) reserved(2) + n x {si,sc,co,cc}
static std::vector<uint8_t> am_pl(uint16_t t, uint16_t i,
                                  const std::vector<std::array<uint16_t,4>>& m) {
    std::vector<uint8_t> pl;
    put_be16(pl, t); put_be16(pl, i);
    put_be16(pl, (uint16_t)m.size()); put_be16(pl, 0);
    for (auto& r : m) { for (int k = 0; k < 4; k++) put_be16(pl, r[k]); }
    return pl;
}
// mapping row at wire offset base (GET resp: base 50)
static bool row_is(const std::vector<uint8_t>& b, size_t base, int n,
                   uint16_t si, uint16_t sc, uint16_t co, uint16_t cc) {
    size_t o = base + 8*(size_t)n;
    return r_be16(b,o) == si && r_be16(b,o+2) == sc &&
           r_be16(b,o+4) == co && r_be16(b,o+6) == cc;
}
// SET_STREAM_FORMAT on STREAM_INPUT[idx]
static std::vector<uint8_t> setfmt(uint16_t idx, uint64_t fmt) {
    std::vector<uint8_t> pl;
    put_be16(pl, STRIN); put_be16(pl, idx); put_be64(pl, fmt);
    return xact(CMD_SET_FMT, pl);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, NULL, _IONBF, 0);
    dut = new VKL_aecp_top;

    dut->rst_n = 0; dut->enable_i = 1;
    dut->srp_domain_vid_i = 0x002;
    dut->rx_tvalid_i = 0; dut->m_axis_tready = 1;
    dut->entity_id_i = ENTITY_ID; dut->entity_model_id_i = 0;
    dut->entity_caps_i = 0x00008588; dut->talker_sources_i = 1;
    dut->talker_caps_i = 0x4801; dut->listener_sinks_i = 3;
    dut->listener_caps_i = 0x4801; dut->controller_caps_i = 0;
    dut->available_index_i = 7; dut->association_id_i = 0;
    dut->gptp_gm_id_i = 0; dut->gptp_domain_i = 0; dut->pdelay_ns_i = 0;
    dut->link_up_i = 1;
    { uint64_t m=0; for(int i=0;i<6;i++) m=(m<<8)|ENT_MAC[i]; dut->station_mac_i = m; }
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    for (int i = 0; i < 4; i++) tick();

    printf("== AECP dynamic audio maps — MULTI-PORT (roadmap 23) ==\n");

    printf("\n[1] every STREAM_PORT_INPUT advertises the 7.2.13 signal\n");
    {
        for (int p = 0; p < 2; p++) {
            std::vector<uint8_t> pl; put_be16(pl,0); put_be16(pl,0);
            put_be16(pl, SPI); put_be16(pl, (uint16_t)p);
            auto r = xact(CMD_READ, pl);
            ck(p ? "SPI1 READ SUCCESS" : "SPI0 READ SUCCESS", r_status(r), 0);
            ck(p ? "SPI1 number_of_maps = 0 (dynamic)"
                 : "SPI0 number_of_maps = 0 (dynamic)", r_be16(r, 58), 0);
            //! base_cluster: port 0 owns clusters 0-3, port 1 owns 4-7
            ck(p ? "SPI1 base_cluster = 8" : "SPI0 base_cluster = 0",
               r_be16(r, 56), p ? 8 : 0);
        }
        std::vector<uint8_t> pl; put_be16(pl,0); put_be16(pl,0);
        put_be16(pl, SPO); put_be16(pl, 0);
        auto r = xact(CMD_READ, pl);
        ck("SPO0 number_of_maps = 1 (static)", r_be16(r, 58), 1);
        pl.clear(); put_be16(pl,0); put_be16(pl,0);
        put_be16(pl, 0x0017); put_be16(pl, 1);          // AUDIO_MAP[1]
        r = xact(CMD_READ, pl);
        ck("only ONE AUDIO_MAP survives (the output's)", r_status(r), 2);
    }

    printf("\n[2] GET_AUDIO_MAP paging is PER PORT (Milan 5.4.2.26)\n");
    {
        for (int p = 0; p < 2; p++) {
            auto r = xact(CMD_GET_MAP, gm_pl(SPI, (uint16_t)p, 0));
            ck("page0 SUCCESS", r_status(r), 0);
            ck("number_of_maps = 2 (8 clusters / page 4)", r_be16(r, 44), 2);
            ck("page0 number_of_mappings = 0", r_be16(r, 46), 0);
            r = xact(CMD_GET_MAP, gm_pl(SPI, (uint16_t)p, 1));
            ck("page1 SUCCESS", r_status(r), 0);
            r = xact(CMD_GET_MAP, gm_pl(SPI, (uint16_t)p, 2));
            ck("page2 BAD_ARGUMENTS (7.4.44.1)", r_status(r), 7);
        }
        auto r = xact(CMD_GET_MAP, gm_pl(SPI, 2, 0));
        ck("GET SPI2 (no such port) NO_SUCH_DESCRIPTOR", r_status(r), 2);
        //! Milan v1.2 5.4.2.26, verbatim: "If a PAAD-AE receives a
        //! GET_AUDIO_MAP command for a Stream Port Output that has Audio
        //! Map(s), the PAAD-AE shall reply with the NOT_SUPPORTED error
        //! code." The command is NOT implemented on that port - serving the
        //! ROM map there with SUCCESS is the violation this pins shut.
        r = xact(CMD_GET_MAP, gm_pl(SPO, 0, 0));
        ck("GET on the static OUTPUT port NOT_SUPPORTED (5.4.2.26)",
           r_status(r), 11);
        //! and it keeps the 7.4.44.2 12-octet response-payload floor
        ck("... at the 12-octet payload floor (cdl 24)",
           (long)b_cdl(r), 24);
        ck("... number_of_maps/mappings tail zeroed", r_be16(r, 46), 0);
    }

    printf("\n[3] the two ports are INDEPENDENT (global keys, local offsets)\n");
    {
        take_wrs();
        //! port 1, cluster_offset 1 -> GLOBAL key 8+1 = 9 = render channel 9
        auto r = xact(CMD_ADD_MAP, am_pl(SPI, 1, {{{1,1,1,0}}}));
        ck("ADD SPI1 {st1 ch1 -> cl+1} SUCCESS", r_status(r), 0);
        { auto w = take_wrs();
          ck("fabric mirror: exactly 1 map write", (long)w.size(), 1);
          if (w.size()==1) {
            ck("... addr = base_cluster 8 + offset 1 = 9", w[0].addr, 9);
            ck("... word = {en,src0,strm1,ch1} 0x89", w[0].word, 0x89); } }
        //! port 0, the SAME cluster_offset 2 -> GLOBAL key 2, a different row
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,1,2,0}}}));
        ck("ADD SPI0 {st0 ch1 -> cl+2} SUCCESS", r_status(r), 0);
        { auto w = take_wrs();
          ck("fabric mirror: exactly 1 map write", (long)w.size(), 1);
          if (w.size()==1) {
            ck("... addr = base_cluster 0 + offset 2 = 2", w[0].addr, 2);
            ck("... word = {en,src0,strm0,ch1} 0x81", w[0].word, 0x81); } }

        r = xact(CMD_GET_MAP, gm_pl(SPI, 1, 0));
        ck("SPI1 page0 lists exactly its own mapping", r_be16(r, 46), 1);
        ck("... offset is PORT-RELATIVE: {1,1,1,0}", row_is(r, 50, 0, 1,1,1,0), 1);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("SPI0 page0 lists exactly its own mapping", r_be16(r, 46), 1);
        ck("... {0,1,2,0} — port 1's row is NOT visible", row_is(r, 50, 0, 0,1,2,0), 1);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 1));
        ck("SPI0 page1 (offsets 4-7) still empty", r_be16(r, 46), 0);
    }

    printf("\n[4] cluster_offset is bounded by the PORT, not the key space\n");
    {
        take_wrs();
        //! offset 8 on port 0 would be global key 8 = port 1's cluster 0.
        //! 7.2.19 offsets are "from the base_cluster of the
        //! STREAM_PORT_INPUT", so it can never reach there: BAD_ARGUMENTS.
        auto r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,0,8,0}}}));
        ck("SPI0 offset 8 (of 8) BAD_ARGUMENTS", r_status(r), 7);
        ck("... and NOTHING was written to the fabric", (long)take_wrs().size(), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 1, 1));
        ck("SPI1 page1 untouched by the reject", r_be16(r, 46), 0);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 1, {{{1,0,8,0}}}));
        ck("SPI1 offset 8 (of 8) BAD_ARGUMENTS", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 2, {{{0,0,0,0}}}));
        ck("ADD on SPI2 NO_SUCH_DESCRIPTOR", r_status(r), 2);

        //! 7.4.45.1: "The ADDING of a mapping is subject to the validity of
        //! the mapping as defined by the vendor of the ATDECC Entity."
        //! This shape declares 16 cluster keys against a render crossbar 10
        //! deep, so port 1 offsets 2..7 (global keys 10..15) have no physical
        //! channel behind them. Accepting one would have GET_AUDIO_MAP report
        //! a route that carries no audio, so it is refused at the door.
        r = xact(CMD_ADD_MAP, am_pl(SPI, 1, {{{1,0,2,0}}}));
        ck("SPI1 offset 2 = key 10, past the crossbar: BAD_ARG", r_status(r), 7);
        ck("... nothing written", (long)take_wrs().size(), 0);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 1, {{{1,0,7,0}}}));
        ck("SPI1 offset 7 = key 15, likewise BAD_ARG", r_status(r), 7);
        //! and the LAST reachable key still works, so the bound is exact
        //! channel 0 (stream 1 is still on its 2ch reset format here)
        r = xact(CMD_ADD_MAP, am_pl(SPI, 1, {{{1,0,1,0}}}));
        ck("SPI1 offset 1 = key 9, the last reachable one: SUCCESS",
           r_status(r), 0);
        r = xact(CMD_RM_MAP, am_pl(SPI, 1, {{{1,0,1,0}}}));
        ck("... removed again (state hygiene)", r_status(r), 0);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 1, {{{1,1,1,0}}}));
        ck("... and the section-3 mapping restored", r_status(r), 0);
    }

    printf("\n[5] mapping_stream_index: any Stream Input, never a CRF\n");
    {
        take_wrs();
        //! Table 7-33: mapping_stream_index is a STREAM_INPUT descriptor
        //! index, NOT the port's own stream - port 0 may render stream 1
        auto r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{1,0,0,0}}}));
        ck("SPI0 fed from STREAM_INPUT[1] SUCCESS", r_status(r), 0);
        { auto w = take_wrs();
          ck("fabric mirror: exactly 1 map write", (long)w.size(), 1);
          if (w.size()==1) ck("... word = {en,src0,strm1,ch0} 0x88", w[0].word, 0x88); }
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("... GET echoes stream_index 1", row_is(r, 50, 0, 1,0,0,0), 1);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{2,0,1,0}}}));
        ck("stream_index 2 is the CRF sink: BAD_ARGUMENTS", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{3,0,1,0}}}));
        ck("stream_index 3 does not exist: BAD_ARGUMENTS", r_status(r), 7);
    }

    printf("\n[6] the channel bound is PER STREAM (Milan 5.3.10.1)\n");
    {
        auto r = xact(CMD_ADD_MAP, am_pl(SPI, 1, {{{1,5,0,0}}}));
        ck("st1 ch5 under the 2ch reset format BAD_ARG", r_status(r), 7);
        r = setfmt(1, AAF8);
        ck("SET_STREAM_FORMAT STREAM_INPUT[1] 8ch SUCCESS", r_status(r), 0);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 1, {{{1,5,0,0}}}));
        ck("st1 ch5 now SUCCESS (that stream's format moved)", r_status(r), 0);
        //! stream 0 was NOT reformatted: its bound must be untouched
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,5,4,0}}}));
        ck("st0 ch5 STILL BAD_ARG (stream 0 is 2ch)", r_status(r), 7);
        r = setfmt(0, AAF8);
        ck("SET_STREAM_FORMAT STREAM_INPUT[0] 8ch SUCCESS", r_status(r), 0);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,5,4,0}}}));
        ck("st0 ch5 now SUCCESS too", r_status(r), 0);

        //! A-F7 / Milan 5.3.10.1: the invariant is STANDING, so shrinking
        //! stream 0 back to 2 channels must not leave a live mapping on its
        //! channel 5. We PRUNE (see the dmp_* block in the RTL): the row is
        //! withdrawn from the store AND from the render crossbar.
        take_wrs();
        r = setfmt(0, AAF2);
        ck("SET_STREAM_FORMAT STREAM_INPUT[0] back to 2ch", r_status(r), 0);
        { auto w = take_wrs();
          ck("shrink WITHDREW the orphaned map word", (long)w.size(), 1);
          if (w.size()==1) {
            ck("... addr 4 (the ch5 row), word 0", w[0].addr*256 + w[0].word,
               4*256); } }
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 1));
        ck("... and GET no longer reports it", r_be16(r, 46), 0);
        //! the SAME command must not touch a mapping that is still in range
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("... while page0's in-range rows SURVIVE", r_be16(r, 46), 2);
        //! offset 0 = {st1,ch0} from [5] (a DIFFERENT stream: untouched),
        //! offset 2 = {st0,ch1} (same stream, channel still in range)
        ck("... {1,0,0,0} untouched (other stream)", row_is(r, 50, 0, 1,0,0,0), 1);
        ck("... {0,1,2,0} untouched (channel still in range)",
           row_is(r, 50, 1, 0,1,2,0), 1);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,5,4,0}}}));
        ck("st0 ch5 BAD_ARG again (bound followed back down)", r_status(r), 7);
        r = xact(CMD_ADD_MAP, am_pl(SPI, 1, {{{1,7,0,0}}}));
        ck("st1 ch7 STILL SUCCESS (stream 1 kept 8ch)", r_status(r), 0);
    }

    printf("\n[7] REMOVE matches stream_index as well as channel\n");
    {
        //! port 1 offset 1 currently holds {st1, ch1}; offset 0 holds ch7
        //! 7.4.46.1: "If any of the mappings in the command are invalid or
        //! not present then the command shall fail with a BAD_ARGUMENTS
        //! status and none of the mappings shall be removed." A wrong
        //! stream_index is NOT PRESENT - it used to be silently ignored.
        take_wrs();
        auto r = xact(CMD_RM_MAP, am_pl(SPI, 1, {{{0,1,1,0}}}));
        ck("REMOVE with the WRONG stream_index: BAD_ARG (7.4.46.1)",
           r_status(r), 7);
        ck("... nothing withdrawn", (long)take_wrs().size(), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 1, 0));
        ck("... mapping survives", row_is(r, 50, 1, 1,1,1,0), 1);
        //! wrong CHANNEL, right stream: also not present
        r = xact(CMD_RM_MAP, am_pl(SPI, 1, {{{1,4,1,0}}}));
        ck("REMOVE with the WRONG channel: BAD_ARG", r_status(r), 7);
        //! a cluster that was never mapped at all
        r = xact(CMD_RM_MAP, am_pl(SPI, 0, {{{0,0,7,0}}}));
        ck("REMOVE of a never-mapped cluster: BAD_ARG", r_status(r), 7);
        //! ALL-OR-NOTHING: one good record + one absent one removes NEITHER
        r = xact(CMD_RM_MAP, am_pl(SPI, 1, {{{1,1,1,0}}, {{1,3,0,0}}}));
        ck("one present + one absent: BAD_ARG, none removed", r_status(r), 7);
        ck("... nothing withdrawn", (long)take_wrs().size(), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 1, 0));
        ck("... both rows still there", r_be16(r, 46), 2);
        //! Milan 5.4.2.28 still overrides for DUPLICATES: validation
        //! completes before any commit, so both copies see it present
        r = xact(CMD_RM_MAP, am_pl(SPI, 1, {{{1,1,1,0}}, {{1,1,1,0}}}));
        ck("DUPLICATE rows SUCCESS (Milan 5.4.2.28)", r_status(r), 0);
        { auto w = take_wrs();
          ck("... withdrawn exactly once", (long)w.size(), 1);
          if (w.size()==1) {
            ck("... addr 9 (global key), word 0", w[0].addr*256 + w[0].word,
               9*256); } }
        r = xact(CMD_GET_MAP, gm_pl(SPI, 1, 0));
        ck("... and only the ch7 row is left on that page", r_be16(r, 46), 1);
        ck("... {1,7,0,0}", row_is(r, 50, 0, 1,7,0,0), 1);
    }

    printf("\n[8] multi-record ADD across a port + static-output regression\n");
    {
        take_wrs();
        //! a 4-cluster program of port 0 in ONE command (port 0's whole
        //! block is inside the crossbar; port 1 has only offsets 0/1)
        auto r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{1,0,4,0}}, {{1,1,5,0}},
                                                  {{1,2,6,0}}, {{1,3,7,0}}}));
        ck("4-record ADD on SPI0 SUCCESS", r_status(r), 0);
        { auto w = take_wrs();
          ck("fabric mirror: 4 writes", (long)w.size(), 4);
          if (w.size()==4) {
            ck("... addrs 4,5,6,7 (base 0 + 4..7)",
               w[0].addr*1000 + w[1].addr*100 + w[2].addr*10 + w[3].addr, 4567);
            ck("... word[3] = {en,src0,strm1,ch3} 0x8B", w[3].word, 0x8B); } }
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 1));
        ck("SPI0 page1 = 4 mappings", r_be16(r, 46), 4);
        //! same key twice in ONE command is still the mandated reject
        r = xact(CMD_ADD_MAP, am_pl(SPI, 0, {{{0,0,4,0}}, {{0,1,4,0}}}));
        ck("same cluster twice in one command BAD_ARG", r_status(r), 7);

        r = xact(CMD_ADD_MAP, am_pl(SPO, 0, {{{0,0,0,0}}}));
        ck("ADD on the static output NOT_SUPPORTED", r_status(r), 11);
        r = xact(CMD_RM_MAP, am_pl(SPO, 0, {{{0,0,0,0}}}));
        ck("REMOVE on the static output NOT_SUPPORTED", r_status(r), 11);
        r = xact(CMD_ADD_MAP, am_pl(SPO, 1, {{{0,0,0,0}}}));
        ck("ADD on SPO1 (absent) NO_SUCH_DESCRIPTOR", r_status(r), 2);
    }

    printf("\n[9] a frame that LIES about its length commits nothing "
           "(A-F14)\n");
    {
        //! Build a well-formed 2-record ADD, note what it does, then send a
        //! frame that declares the SAME control_data_length while carrying
        //! only part of the records. control_data_length was checked for a
        //! lower bound only, so the walk used to read the missing records out
        //! of the PREVIOUS command's capture-buffer residue and commit them.
        auto full = am_pl(SPI, 0, {{{0,0,0,0}}, {{0,1,1,0}}});
        auto r = xact(CMD_ADD_MAP, full);
        ck("reference 2-record ADD SUCCESS", r_status(r), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        //! offsets 0 and 1 from this command + offset 2 carried in
        ck("... 3 rows on page0", r_be16(r, 46), 3);

        //! now the liar: same declared cdl, 12 octets short on the wire
        take_wrs();
        auto f = aem_cmd(CMD_ADD_MAP, seq++, full);
        //! the payload's last 12 octets are the tail of record 1 + padding;
        //! truncate the FRAME without touching the header's length field
        f.resize(f.size() - 12);
        feed_rx(f);
        auto rr = collect_resp();
        ck("short frame produced NO response at all", (long)rr.size(), 0);
        ck("... and committed NOTHING to the fabric",
           (long)take_wrs().size(), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("... the store is exactly as the honest command left it",
           r_be16(r, 46), 3);
        ck("... row0 unchanged", row_is(r, 50, 0, 0,0,0,0), 1);
        ck("... row1 unchanged", row_is(r, 50, 1, 0,1,1,0), 1);
        ck("... row2 unchanged", row_is(r, 50, 2, 0,1,2,0), 1);
        //! the entity is still alive and answering afterwards
        r = xact(CMD_GET_MAP, gm_pl(SPI, 1, 0));
        ck("... and the responder still serves the next command",
           r_status(r), 0);

        //! EXACT BOUNDARY (-8), the case a wrong CDL_ORIGIN_C lets through:
        //! one 64-bit beat missing = exactly ONE mapping record forged from
        //! cbuf residue. This 2-record ADD is payload 24 -> cdl 36 -> frame
        //! 62 -> 50 stream octets, and 14 + 36 = 50 EXACTLY, so -8 must be
        //! refused while the honest frame at +-0 is accepted. With the
        //! pre-fix origin of 6 the threshold was 42 and this frame passed
        //! (Opus verify 2026-07-30). The -12 case above sits PAST the loose
        //! threshold and therefore could not expose it - the boundary is
        //! where the check has to be exact.
        take_wrs();
        auto f8 = aem_cmd(CMD_ADD_MAP, seq++, full);
        f8.resize(f8.size() - 8);
        feed_rx(f8);
        auto rr8 = collect_resp();
        ck("-8 boundary frame: NO response", (long)rr8.size(), 0);
        ck("-8 boundary frame: NOTHING committed",
           (long)take_wrs().size(), 0);
        r = xact(CMD_GET_MAP, gm_pl(SPI, 0, 0));
        ck("-8 boundary frame: store untouched", r_be16(r, 46), 3);
        ck("-8: row2 is still the honest row (not residue)",
           row_is(r, 50, 2, 0,1,2,0), 1);
        //! and the honest frame of the SAME shape still works: the check is
        //! exact, not merely conservative
        r = xact(CMD_RM_MAP, am_pl(SPI, 0, {{{0,0,0,0}}, {{0,1,1,0}}}));
        ck("-8: the honest 2-record command still SUCCEEDs", r_status(r), 0);
        r = xact(CMD_ADD_MAP, full);
        ck("-8: and re-ADDing it SUCCEEDs", r_status(r), 0);
    }

    printf("\n----------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}
