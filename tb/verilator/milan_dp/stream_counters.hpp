// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Included inside NxnDatapathHarness. #726: MAC packet census, counter resets,
// 32-bit wrap, and per-descriptor/recipient notification windows. The descriptor
// image, parser, counters, arbiter, processor and response-memory path are real.
// Protocol time uses 1000 cycles/ms; the clock parameter remains 50 MHz.
// Window 0 and 1 record startup; windows 2 through 4 grade steady traffic.
// Service time runs from dirty-and-eligible to the final recipient's MAC tail.
    void counter_feed(int s,uint8_t seq) {
        const uint64_t ts=phc_now_ns()+2000000;
        std::vector<uint8_t> f(s<kNstreamsTb ? 86 : 64,0);
        gsi_put(f,0,0x91E0F0002A02ull,6);
        gsi_put(f,6,0x021122334455ull,6);
        gsi_put(f,12,0x22F0,2);
        f[16]=seq;
        gsi_put(f,18,0x0211223300000100ull+s,8);
        if(s<kNstreamsTb) {
            f[14]=2;f[15]=0x81;
            gsi_put(f,26,ts & 0xffffffffu,4);
            f[30]=2;f[31]=0x50;f[32]=2;f[33]=32;
            gsi_put(f,34,48,2);
        } else {
            f[14]=4;f[15]=0x80;f[17]=1;
            gsi_put(f,26,48000,4);gsi_put(f,30,8,2);
            gsi_put(f,32,96,2);gsi_put(f,34,ts,8);
        }
        gsi_rx_q.push_back(f);
    }

    static constexpr int ncounter = 2 * (kNstreamsTb + 1) + 2;
    struct CounterProbeState {
        std::array<uint32_t,kNstreamsTb+1> wire_tx{};
        std::array<uint32_t,kNstreamsTb+1> wire_tu{};
        std::array<uint32_t,kNstreamsTb+1> wire_mr{};
        const char* omitted_check = std::getenv("COUNTERS_OMIT_CHECK");
        std::array<long,ncounter> service_begin{};
        std::array<long,ncounter> service_max{};
        bool counter_watch_on=false;
    } counter_state;
    void counter_check(const char* group,const char* what,unsigned long got,unsigned long expected) {
        if(counter_state.omitted_check && std::strcmp(counter_state.omitted_check,group)==0) return;
        std::string name=std::string("[726 ")+group+"] "+what;
        ck(name.c_str(),got,expected);
    }
    void counter_departed(const std::vector<uint8_t>& f) {
        const int o=gsi_be(f,12,2)==0x8100 ? 4 : 0;
        if(f.size()>size_t(26+o) && gsi_be(f,12+o,2)==0x22f0 && (f[14+o]==2 || f[14+o]==4)) {
            const unsigned ix=f[14+o]==4 ? kNstreamsTb : gsi_be(f,24+o,2);
            if(ix<=kNstreamsTb) {
                ++counter_state.wire_tx[ix];
                counter_state.wire_tu[ix] += f[(f[14+o]==4 ? 15 : 17)+o] & 1;
                counter_state.wire_mr[ix] += (f[15+o] >> 3) & 1;
            }
        }
        if(!counter_state.counter_watch_on || f.size()<46 || !aecp_is_unsolicited(f) || notify_cmd(f)!=0x29) return;
        const auto ty=gsi_be(f,38,2);
        const auto s=gsi_be(f,40,2);
        const int ix=ty==5 ? s : ty==6 ? kNstreamsTb+1+s : ty==9 ? ncounter-2 : ncounter-1;
        if(ix>=ncounter || counter_state.service_begin[ix]<0)return;
        counter_state.service_max[ix]=std::max(counter_state.service_max[ix],uns_log_cycle-counter_state.service_begin[ix]);
        if(memcmp(f.data()+26,CTL_B.eid,8)==0)counter_state.service_begin[ix]=-1;
    }
    void counter_watch() {
        if(!counter_state.counter_watch_on) return;
        const auto* r=dut->rootp;
        const auto now=r->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_timer__DOT__now_ms_r;
        const auto dirty=r->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_dirty_r;
        const auto sent=r->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_sent_r;
        for(int i=0;i<ncounter;++i) {
            const auto stamp=r->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_notify__DOT__ctr_last_r[i];
            if(counter_state.service_begin[i]<0 && (dirty>>i&1) && (!(sent>>i&1) || uint32_t(now-stamp)>=1000))
                counter_state.service_begin[i]=uns_log_cycle;
        }
    }

    int stream_counter_probe() {
        const milan::tb::Model<Vmilan_datapath> model;
        dut = model.get();
        bring_the_datapath_out_of_reset();
        prove_the_identity_and_provision_the_entity_id();
        std::string why;
        if (!aemi_load(AEMI_CFG_C, &why)) {
            printf("image failure: %s\n", why.c_str()); return 2;
        }
        counter_setup();
        counter_measure();
        counter_state.counter_watch_on=false;
        axi_write(A_AAF_CTRL,0x00020002);axi_write(A_CRFT_CTRL,0);
        for(int t=0;t<5000;++t)gsi_tick();
        for(int s=0;s<=kNstreamsTb;++s) {
            const auto got=dut->rootp->milan_datapath__DOT__talker_diag__DOT__ftx_r[s];
            printf("TX_COUNT,%d,%u,%u\n",s,got,counter_state.wire_tx[s]);
            counter_check("TX","per-AVTPDU total equals wire",got,counter_state.wire_tx[s]);
            counter_check("TX","every output emitted",counter_state.wire_tx[s]>10,1);
        }
        counter_notifications();
        const auto batch_base=counter_receive_resets();
        for(int i=0;i<ncounter;++i)printf("SERVICE,%d,%ld\n",i,counter_state.service_max[i]);
        counter_restart_wrap();
        counter_batch_boundary(batch_base);
        return report();
    }

    void counter_setup() {
        dm_answering = true;
        start_the_boot_restore_walk();
        axi_write(0x644, 1); // receive-filter bypass
        axi_write(0x680, 0); // no reservation traffic in this cadence fixture
        for (int s = 0; s < kNstreamsTb; ++s) {
            axi_write(A_STRM_SEL, s);
            axi_write(A_SW_SID_LO, 0x100u + s);
            axi_write(A_SW_SID_HI, 0x02112233);
            axi_write(A_SW_FMT_LO, FMT_LO);
            axi_write(A_SW_FMT_HI, FMT_HI);
            axi_write(A_SW_CTRL, 1);
        }
        axi_write(A_CRF_SIDLO_L, 0x100u + kNstreamsTb);
        axi_write(A_CRF_SIDHI_L, 0x02112233);
        axi_write(A_CRF_CTRL_L, 1);
        for (const Ctlr* ctl : {&CTL_A, &CTL_B}) {
            const auto r = aecp_xact_from(*ctl, 0x24, 0x5000, {0,0,0,0});
            ck("[726] registered recipient", aecp_status(r), 0);
        }
    }

    void counter_measure() {
        constexpr long counter_second = 1000L * kMsCycTb;
        axi_write(A_AAF_CTRL, 0x00020003);
        axi_write(A_CRFT_CTRL, 1);
        uns_log.clear(); uns_log_when.clear(); uns_log_cycle=0;
        counter_state.service_begin.fill(-1); counter_state.counter_watch_on=true;
        std::array<uint8_t, kNstreamsTb+1> seq{};
        for (long t=0; t<5*counter_second; ++t) {
            if (t % (10*kMsCycTb)==0) {
                for (int s=0;s<=kNstreamsTb;++s) {
                    counter_feed(s,seq[s]++);
                }
            }
            gsi_tick();
        }
        // No start/stop, MR or TU update may explain the steady output pushes.
        for(int s=0;s<=kNstreamsTb;++s) {
            const auto* diag=dut->rootp;
            const auto tu=diag->milan_datapath__DOT__talker_diag__DOT__tuiv_r[s];
            const auto mr=diag->milan_datapath__DOT__talker_diag__DOT__mreset_r[s];
            const auto starts=diag->milan_datapath__DOT__talker_diag__DOT__start_r[s];
            const auto stops=diag->milan_datapath__DOT__talker_diag__DOT__stop_r[s];
            printf("OUTPUT_CONDITION,%d,%s,%u,%u,%u,%u,%u,%u\n",s,
                   COUNTERS_FRAMES_ONLY_TB ? "frames-only" : "uncertain",
                   tu,mr,starts,stops,counter_state.wire_tu[s],counter_state.wire_mr[s]);
            if(COUNTERS_FRAMES_ONLY_TB) {
                counter_check("OUTPUT_CONDITION","TU counter stays zero",tu,0);
                counter_check("OUTPUT_CONDITION","MR counter stays zero",mr,0);
                counter_check("OUTPUT_CONDITION","only initial start",starts,1);
                counter_check("OUTPUT_CONDITION","no stop during windows",stops,0);
                counter_check("OUTPUT_CONDITION","all wire tu bits clear",counter_state.wire_tu[s],0);
                counter_check("OUTPUT_CONDITION","wire mr remains at reset",counter_state.wire_mr[s],0);
            }
        }
    }

    void counter_notifications() {
        constexpr long counter_second = 1000L * kMsCycTb;
        printf("shape,type,index,recipient,window,notifications,min_gap_ms,max_gap_ms\n");
        for (int ty : {5,6}) for(int s=0;s<=kNstreamsTb;++s)
          for(int r=0;r<2;++r) {
            std::array<int,5> bins{};
            long last=-1;
            long ming=10*counter_second;
            long maxg=0;
            for(size_t j=0;j<uns_log.size();++j) {
                const auto& f=uns_log[j];const auto& ctl=r ? CTL_B : CTL_A;
                if(f.size()<46 || !aecp_is_unsolicited(f) || notify_cmd(f)!=0x29 ||
                   gsi_be(f,38,2)!=unsigned(ty) || gsi_be(f,40,2)!=unsigned(s) ||
                   memcmp(f.data()+26,ctl.eid,8)!=0) continue;
                const long at=uns_log_when[j];
                if(at/counter_second<5) ++bins[at/counter_second];
                if(last>=0) {ming=std::min(ming,at-last);maxg=std::max(maxg,at-last);}
                last=at;
            }
            const char* cadence=ty==6 && COUNTERS_FRAMES_ONLY_TB ? "OUTPUT_CADENCE" : "CADENCE";
            for(int b=2;b<5;++b) {
                counter_check(cadence,"every complete steady window notified",bins[b]>=1,1);
                counter_check("RATE","no duplicate in a complete steady window",bins[b]<=1,1);
            }
            counter_check("RATE","minimum spacing",ming>=counter_second,1);
            const int slot=(ty==5 ? 0 : kNstreamsTb+1)+s;
            counter_check(cadence,"gap bounded by measured service",maxg<=counter_second+counter_state.service_max[slot],1);
            for(int b=0;b<5;++b) printf("%d,%d,%d,%d,%d,%d,%.5f,%.5f\n",kNstreamsTb,ty,s,r,b,bins[b],
              ming/double(kMsCycTb),maxg/double(kMsCycTb));
          }
    }

    std::array<uint32_t,kNstreamsTb> counter_receive_resets() {
        gsi_ms(1010); // commit the final receive batch before its snapshot
        std::array<uint32_t,kNstreamsTb> batch_base{};
        for(int s=0;s<=kNstreamsTb;++s) {
            auto read_rx=[&]() {
                auto r=gsi_xact(CTL_A,0x29,{0,5,0,static_cast<uint8_t>(s)});
                counter_check("RX","GET_COUNTERS success",aecp_status(r),0);
                return ctr_word(r,11);
            };
            const auto received=read_rx();
            counter_check("RX","every received PDU counted",received,500);
            if(s<kNstreamsTb) {axi_write(A_STRM_SEL,s);axi_write(A_SW_CTRL,0);}
            else axi_write(A_CRF_CTRL_L,0);
            gsi_ms(1);
            counter_check("RX_RESET","unbind preserves total",read_rx(),received);
            if(s<kNstreamsTb) {
                axi_write(A_SW_SID_LO,0x100u+s);axi_write(A_SW_SID_HI,0x02112233);
                axi_write(A_SW_CTRL,1);
            } else axi_write(A_CRF_CTRL_L,1);
            gsi_ms(1);
            const auto rebound=read_rx();
            counter_check("RX_RESET","bind starts at zero",rebound,0);
            if(s<kNstreamsTb)batch_base[s]=rebound;
        }
        return batch_base;
    }

    void counter_restart_wrap() {
        // Quiesce each run before comparing MAC completions with its counter.
        for(int phase=0;phase<2;++phase) {
            counter_state.wire_tx.fill(0);
            axi_write(A_AAF_CTRL,0x00020003);axi_write(A_CRFT_CTRL,1);
            for(int t=0;t<100;++t)gsi_tick();
            std::array<uint32_t,kNstreamsTb+1> seeds{};
            for(int s=0;s<=kNstreamsTb;++s) {
                const auto start=dut->rootp->milan_datapath__DOT__talker_diag__DOT__ftx_r[s];
                counter_check("TX_RESET","talker start resets before first PDU",start,0);
                seeds[s]=phase ? UINT32_MAX-5u : start;
            }
            const uint32_t seed=UINT32_MAX-5u;
            if(phase) for(int s=0;s<=kNstreamsTb;++s)
                dut->rootp->milan_datapath__DOT__talker_diag__DOT__ftx_r[s]=seed;
            for(int t=0;t<400000;++t)gsi_tick();
            axi_write(A_AAF_CTRL,0x00020002);axi_write(A_CRFT_CTRL,0);
            for(int t=0;t<5000;++t)gsi_tick();
            for(int s=0;s<=kNstreamsTb;++s) {
                const auto got=dut->rootp->milan_datapath__DOT__talker_diag__DOT__ftx_r[s];
                printf("TX_RUN,%d,%d,%u,%u,%u\n",phase,s,seeds[s],got,counter_state.wire_tx[s]);
                counter_check("TX","restart and wrap follow wire",uint32_t(got-seeds[s]),counter_state.wire_tx[s]);
                counter_check("TX","restart/wrap emitted enough",counter_state.wire_tx[s]>6,1);
            }
        }
    }

    void counter_batch_boundary(const std::array<uint32_t,kNstreamsTb>& batch_base) {
        // Boundary seed represents already accepted packets in this interval.
        // Three real MAC packets must cross the former 16-bit saturation point.
        for(int s=0;s<kNstreamsTb;++s) {
            dut->rootp->milan_datapath__DOT__avtp_rx_monitor__DOT__frx_acc_r[s]=65534;
            for(int k=0;k<3;++k)counter_feed(s,k);
        }
        gsi_ms(1100);
        for(int s=0;s<kNstreamsTb;++s) {
            auto r=gsi_xact(CTL_A,0x29,{0,5,0,static_cast<uint8_t>(s)});
            counter_check("RX","batch crosses 65535 without loss",uint32_t(ctr_word(r,11)-batch_base[s]),65537);
        }
    }
