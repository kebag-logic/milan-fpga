#include "Vtcam_csr_wrap.h"
#include "verilated.h"
#include "../../common/verilator_harness.hpp"
#include <cstdint>
#include <cstdio>

//! The milan_csr TCAM window, decoded by wrap.sv exactly as milan_csr does.
//! The names are the ones hdl/common/csr/milan_csr.sv uses for these offsets.
constexpr uint32_t kATcamKlo = 0x704;
constexpr uint32_t kATcamKhi = 0x708;
constexpr uint32_t kATcamMlo = 0x70C;
constexpr uint32_t kATcamMhi = 0x710;
constexpr uint32_t kATcamAct = 0x714;
constexpr uint32_t kATcamCmd = 0x718;

//! rx_mac_filter reads action[0] as "drop this match" (blacklist mode).
constexpr uint32_t kTcamActionDrop = 1;
//! A_TCAM_CMD write: commit strobe (bit 16) + entry valid (bit 8) + index 0.
constexpr uint32_t kTcamCmdWriteEntry0 = 0x00010100;

constexpr int kFrames = 2;               //! frames driven through the filter
constexpr int kBeatsPerFrame = 4;        //! beats per frame on the 64-bit lane
constexpr int kBytesPerBeat = 8;         //! TDATA_WIDTH/8
constexpr int kBitsPerByte = 8;
constexpr uint8_t kTkeepAllBytes = 0xFF; //! every lane of the beat carries data

namespace {

//! Drives the TCAM window of milan_csr and the filter behind it.
class TcamCsrHarness {
 public:
    int run();

 private:
    void step(){ dut->clk_i=0; dut->eval(); dut->clk_i=1; dut->eval(); }
    void wr(uint32_t a, uint32_t d){ dut->wr_addr_i=a; dut->wr_data_i=d; dut->wr_p_i=1; step(); dut->wr_p_i=0; step(); }

    const milan::tb::Model<Vtcam_csr_wrap> model;
    Vtcam_csr_wrap* dut = model.get();
};

int TcamCsrHarness::run(){
    dut->rst_n=0; dut->s_tvalid=0; dut->m_tready=1; step(); step();
    dut->rst_n=1; step();
    wr(kATcamKhi,0x000091E0);
    wr(kATcamKlo,0xF0000000);
    wr(kATcamMhi,0x0000FFFF);
    wr(kATcamMlo,0xFF000000);
    wr(kATcamAct,kTcamActionDrop);
    wr(kATcamCmd,kTcamCmdWriteEntry0);
    // frame 1: dmac 91:E0:F0:00:77:77 (little lane) -> expect DROP
    // frame 2: dmac 00:11:22:33:44:55 -> expect PASS
    uint64_t d1=0; uint8_t m1[kBytesPerBeat]={0x91,0xE0,0xF0,0x00,0x77,0x77,0x08,0x00};
    uint64_t d2=0; uint8_t m2[kBytesPerBeat]={0x00,0x11,0x22,0x33,0x44,0x55,0x08,0x00};
    for(int i=0;i<kBytesPerBeat;i++){ d1|=static_cast<uint64_t>(m1[i])<<(kBitsPerByte*i); d2|=static_cast<uint64_t>(m2[i])<<(kBitsPerByte*i); }
    int out1=0;
    int out2=0;
    for(int f=0; f<kFrames; f++){
        uint64_t d = f? d2 : d1;
        for(int b=0;b<kBeatsPerFrame;b++){
            dut->s_tdata = b? 0 : d; dut->s_tkeep=kTkeepAllBytes;
            dut->s_tvalid=1; dut->s_tlast=(b==kBeatsPerFrame-1);
            // sample the cut-through outputs BEFORE the clock edge: the
            // filter is combinational per beat, and sampling after the edge
            // shows the NEXT-cycle view - on the tlast beat that view is the
            // runt-SOF guard (rx_mac_filter 2026-07-19) rejecting a phantom
            // 1-beat frame, not this beat's verdict
            dut->eval();
            printf("    f%d b%d: s_tvalid=%d s_tready=%d m_tvalid=%d dropped=%d\n",
                   f,b,dut->s_tvalid,dut->s_tready,dut->m_tvalid,dut->dropped_o);
            if(dut->m_tvalid && dut->m_tready){ if(f) out2++; else out1++; }
            step();
        }
        dut->s_tvalid=0; dut->s_tlast=0; step(); step();
    }
    printf("filtered-frame beats out=%d (exp 0), other=%d (exp 4)\n",out1,out2);
    // Two verdicts: the blacklisted DMAC must be dropped whole (out1==0) and
    // the unmatched one must pass all four beats (out2==4). Emitted in the
    // shape scripts/suite_tally.py reads so this suite stops contributing a
    // structural zero to the sweep's headline check total.
    long fails = (out1!=0) + (out2!=kBeatsPerFrame);
    printf("tcam_csr: 2 checks, %ld failures\n", fails);
    return (out1==0 && out2==kBeatsPerFrame)?0:1;
}

}  // namespace

int main(int argc,char**argv){
    Verilated::commandArgs(argc,argv);
    TcamCsrHarness harness;
    return harness.run();
}
