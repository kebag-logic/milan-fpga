// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vsim.h for the primary calling header

#include "Vsim__pch.h"

void Vsim_sim___nba_sequent__TOP__sim__35(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__35\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__rel 
        = (0x00007fffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r) 
                          - (IData)(0x0200U)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__in_entry 
        = (0x000fU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__rel));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__entry 
        = (0x000fU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__rel) 
                      >> 4U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_reg_w = 0U;
    if ((4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__in_entry))) {
        vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_reg_w = 1U;
    }
    if ((8U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__in_entry))) {
        vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_reg_w = 2U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_at_w = (((
                                                   (0x0200U 
                                                    <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                   & (1U 
                                                      > 
                                                      ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__rel) 
                                                       >> 8U))) 
                                                  & (0x0010U 
                                                     > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__entry))) 
                                                 & (((0U 
                                                      == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__in_entry)) 
                                                     | (4U 
                                                        == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__in_entry))) 
                                                    | (8U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bound_decode__DOT__in_entry))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__rel 
        = (0x00007fffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r) 
                          - (IData)(0x6000U)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if 
        = (0x03ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__rel));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w = (1U 
                                                  & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__rel) 
                                                     >> 0x0000000aU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w = 
        ((0x0200U <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if))
          ? 2U : ((0x0100U <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if))
                   ? 1U : 0U));
    if ((2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) {
        vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__entry 
            = (0x000007ffU & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if) 
                               - (IData)(0x0200U)) 
                              >> 4U));
        vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w 
            = (0x000fU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if) 
                          - (IData)(0x0200U)));
    } else {
        vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__entry 
            = (0x000007ffU & (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if) 
                               - (IData)(0x0100U)) 
                              >> 4U));
        vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w 
            = ((1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))
                ? (0x000fU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if) 
                              - (IData)(0x0100U))) : (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__in_if));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_s_w = (0x0000000fU 
                                                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__entry));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_k_w = (0x0000000fU 
                                                 & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__entry));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w = ((
                                                   (0x6000U 
                                                    <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                   & (1U 
                                                      > 
                                                      ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__rel) 
                                                       >> 0x0000000aU))) 
                                                  & ((((0U 
                                                        == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w)) 
                                                       & (((((((((((((((((((((((((((((((((((((0U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w)) 
                                                                                | (4U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (8U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x000cU 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0010U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0014U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0018U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x001cU 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0040U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0044U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0048U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x004cU 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0050U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0060U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                                | (0x0064U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                               | (0x0068U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                              | (0x006cU 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                             | (0x0070U 
                                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                            | (0x0074U 
                                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                           | (0x0080U 
                                                                              == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                          | (0x0084U 
                                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                         | (0x0088U 
                                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                        | (0x008cU 
                                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                       | (0x0090U 
                                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                      | (0x0094U 
                                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                     | (0x0098U 
                                                                        == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                    | (0x009cU 
                                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                   | (0x00a0U 
                                                                      == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                  | (0x00a4U 
                                                                     == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                 | (0x00c0U 
                                                                    == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                                | (0x00c4U 
                                                                   == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                               | (0x00c8U 
                                                                  == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                              | (0x00ccU 
                                                                 == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                             | (0x00d0U 
                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                            | (0x00d4U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                           | (0x00d8U 
                                                              == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                          | (0x00dcU 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w)))) 
                                                      | (((1U 
                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w)) 
                                                          & (0x0010U 
                                                             > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__entry))) 
                                                         & ((((0U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w)) 
                                                              | (4U 
                                                                 == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                             | (8U 
                                                                == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                            | (0x000cU 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))))) 
                                                     | (((2U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w)) 
                                                         & (0x0010U 
                                                            > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_decode__DOT__entry))) 
                                                        & (((0U 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w)) 
                                                            | (4U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                           | (8U 
                                                              == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__rel 
        = (0x00007fffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r) 
                          - (IData)(0x0800U)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_if 
        = (0x01ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__rel));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_srcs 
        = (0x00007fffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_if) 
                          - (IData)(0x0080U)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_sinks 
        = (0x00007fffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_if) 
                          - (IData)(0x0100U)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__src_entry 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_srcs) 
           >> 3U);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__entry 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_sinks) 
           >> 4U);
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_if_w = (1U 
                                                 & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__rel) 
                                                    >> 9U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w = (0x0100U 
                                                   <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_if));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w = ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w)) 
                                                  & (0x0080U 
                                                     <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_if)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_s_w = (0x0000000fU 
                                                & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__src_entry));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_k_w = (0x0000000fU 
                                                & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__entry));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w)
                                                   ? 
                                                  (0x000fU 
                                                   & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_sinks))
                                                   : 
                                                  ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w)
                                                    ? 
                                                   (7U 
                                                    & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_srcs))
                                                    : (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__in_if)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w = (((0x0800U 
                                                   <= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                  & (1U 
                                                     > 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__rel) 
                                                      >> 9U))) 
                                                 & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w)
                                                     ? 
                                                    ((0x0010U 
                                                      > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__entry)) 
                                                     & (((0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w)) 
                                                         | (4U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                        | (8U 
                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))))
                                                     : 
                                                    ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w)
                                                      ? 
                                                     ((0x0010U 
                                                       > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_decode__DOT__src_entry)) 
                                                      & ((0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w)) 
                                                         | (4U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))))
                                                      : 
                                                     (((((0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w)) 
                                                         | (4U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                        | (8U 
                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                       | (0x000cU 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                      | (0x0010U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))))));
    vlSelfRef.__PVT__soc_soc_rst = 0U;
    if (vlSelfRef.__PVT__soc_reset_wr_stb) {
        vlSelfRef.__PVT__soc_soc_rst = (1U & (IData)(vlSelfRef.__PVT__soc_reset_storage));
    }
    vlSelfRef.__PVT__soc_tx_fifo_do_read = (((~ (IData)(vlSelfRef.__PVT__soc_tx_fifo_readable)) 
                                             | (IData)(vlSymsp->TOP.serial_source_ready)) 
                                            & (0U != (IData)(vlSelfRef.__PVT__soc_tx_fifo_level0)));
    vlSelfRef.__PVT__soc_rx_fifo_do_read = (((~ (IData)(vlSelfRef.__PVT__soc_rx_fifo_readable)) 
                                             | (IData)(vlSelfRef.__PVT__soc_rx_clear)) 
                                            & (0U != (IData)(vlSelfRef.__PVT__soc_rx_fifo_level0)));
}

void Vsim_sim___nba_sequent__TOP__sim__36(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__36\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_107 = (((IData)(vlSelfRef.__PVT__soc_rx_fifo_readable) 
                                                   << 1U) 
                                                  | (0x10U 
                                                     != (IData)(vlSelfRef.__PVT__soc_tx_fifo_level0)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_n_w[0U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_r[0U];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_d_w 
        = (0x000000ffU & ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_mem_r
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_a_w] 
                           >> (0x0000001fU & VL_MULS_III(32, (IData)(8U), 
                                                         (3U 
                                                          & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cp_b_r))))) 
                          & (- (IData)((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w)))));
    vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value0 = 0U;
    if ((8U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
        if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value0 
                = vlSelfRef.__PVT__add_devices_mmap_clk_divisor_storage;
        } else if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value0 
                = vlSelfRef.__PVT__add_devices_mmap_clk_divisor_storage;
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value0 
                = vlSelfRef.__PVT__add_devices_mmap_clk_divisor_storage;
        }
    } else if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                         >> 2U)))) {
        if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                      >> 1U)))) {
            if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_state)))) {
                vlSelfRef.__PVT__add_devices_mmap_source_payload_clk_div_subfragments_next_value0 
                    = vlSelfRef.__PVT__add_devices_mmap_clk_divisor_storage;
            }
        }
    }
    vlSelfRef.__PVT__add_devices_mmap_source_payload_len = 0U;
    if ((1U & (~ ((IData)(vlSelfRef.__PVT__builder_litespi_state) 
                  >> 3U)))) {
        if ((4U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                    vlSelfRef.__PVT__add_devices_mmap_source_payload_len = 0x20U;
                }
            } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                vlSelfRef.__PVT__add_devices_mmap_source_payload_len 
                    = (0x0000003fU & (IData)(vlSelfRef.__PVT__add_devices_mmap_dummy_bits_storage));
            }
        } else if ((2U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
                vlSelfRef.__PVT__add_devices_mmap_source_payload_len = 0x18U;
            }
        } else if ((1U & (IData)(vlSelfRef.__PVT__builder_litespi_state))) {
            vlSelfRef.__PVT__add_devices_mmap_source_payload_len = 8U;
        }
    }
    if (((IData)(vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_valid) 
         & (~ (IData)(vlSymsp->TOP.flash_tx_ready)))) {
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_valid = 1U;
    } else if (vlSymsp->TOP.flash_tx_ready) {
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_valid = 0U;
    }
    vlSelfRef.__PVT__zero_trigger_d = (0U == vlSelfRef.__PVT__value);
    vlSelfRef.__PVT__update_value_wr_stb = vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_update_value_re;
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_en_re) {
        vlSelfRef.__PVT__en_storage = (1U & vlSelfRef.__PVT__builder_interface1_dat_w);
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_reload_re) {
        vlSelfRef.__PVT__reload_storage = vlSelfRef.__PVT__builder_interface1_dat_w;
    }
    if (vlSelfRef.__PVT__builder_csr_bankarray_csrbank4_load_re) {
        vlSelfRef.__PVT__load_storage = vlSelfRef.__PVT__builder_interface1_dat_w;
    }
    if (((IData)(vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_valid) 
         & (~ (IData)(vlSelfRef.__PVT__builder_litespi_rx_demux_sink_ready)))) {
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_valid = 1U;
    } else if (vlSelfRef.__PVT__builder_litespi_rx_demux_sink_ready) {
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_valid = 0U;
    }
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_valid = 0U;
        vlSelfRef.__PVT__zero_trigger_d = 0U;
        vlSelfRef.__PVT__update_value_wr_stb = 0U;
        vlSelfRef.__PVT__en_storage = 0U;
        vlSelfRef.__PVT__reload_storage = 0U;
        vlSelfRef.__PVT__load_storage = 0U;
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_valid = 0U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_n_w[0U] 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_roll_w)
            ? 0ULL : vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_r[0U]);
    if ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__start_w) 
          & (7U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_w))) 
         & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_if_w)))) {
        if ((0x22U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w))) {
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_n_w[0U] 
                = ((~ (1ULL << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w))) 
                   & vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_pend_n_w[0U]);
            vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_n_w[0U] 
                = (vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__ctr_seen_n_w[0U] 
                   | (0x00000007ffffffffULL & ((QData)((IData)(1U)) 
                                               << (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__src_bit_w))));
        }
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_wr_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__q_wr_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__widx_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__widx_r;
    vlSelfRef.KL_mbx__DOT____Vcellinp__u_rx__own_eid_i 
        = (((QData)((IData)(vlSelfRef.__PVT__KL_mbx__DOT__own_eid_hi_r)) 
            << 0x00000020U) | (QData)((IData)(vlSelfRef.__PVT__KL_mbx__DOT__own_eid_lo_r)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hit_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__hit_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__lane_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__lane_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__dst_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_rd_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__q_rd_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_cnt_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__q_cnt_r;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__st_r;
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v0) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_data_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_data_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_data_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_data_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_idx_r[0U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_idx_r[1U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_idx_r[2U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_idx_r[3U] = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[0U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[1U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[2U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[3U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[4U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[5U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[6U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[7U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[8U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[9U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[10U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[11U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[12U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[13U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[14U] = 0ULL;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__q_data_r__v4) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_data_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_rx__DOT__q_data_r__v4] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__q_data_r__v4;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__q_idx_r__v4) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_idx_r[vlSelfRef.__VdlyDim0__KL_mbx__DOT__u_rx__DOT__q_idx_r__v4] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__q_idx_r__v4;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v15) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[0U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v15;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v16) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[1U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v16;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v17) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[2U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v17;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v18) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[3U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v18;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v19) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[4U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v19;
    }
}

extern const VlUnpacked<CData/*0:0*/, 2> Vsim__ConstPool__TABLE_h1b85385a_0;

void Vsim_sim___nba_sequent__TOP__sim__37(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__37\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    SData/*15:0*/ __PVT__KL_mbx__DOT__u_rx__DOT__used_w;
    __PVT__KL_mbx__DOT__u_rx__DOT__used_w = 0;
    SData/*15:0*/ __PVT__KL_mbx__DOT__u_rx__DOT__cused_w;
    __PVT__KL_mbx__DOT__u_rx__DOT__cused_w = 0;
    SData/*15:0*/ __PVT__KL_mbx__DOT__u_rx__DOT__tail_w;
    __PVT__KL_mbx__DOT__u_rx__DOT__tail_w = 0;
    VlWide<3>/*95:0*/ __Vtemp_1;
    // Body
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v20) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[5U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v20;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v21) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[6U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v21;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v22) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[7U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v22;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v23) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[8U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v23;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v24) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[9U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v24;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v25) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[10U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v25;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v26) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[11U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v26;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v27) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[12U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v27;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v28) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[13U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v28;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v29) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[14U] 
            = vlSelfRef.__VdlyVal__KL_mbx__DOT__u_rx__DOT__field_r__v29;
    }
    if (vlSelfRef.__VdlySet__KL_mbx__DOT__u_rx__DOT__field_r__v30) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[0U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[1U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[2U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[3U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[4U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[5U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[6U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[7U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[8U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[9U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[10U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[11U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[12U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[13U] = 0ULL;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__field_r[14U] = 0ULL;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r 
        = vlSelfRef.__Vdly__KL_mbx__DOT__u_rx__DOT__cnt_r;
    vlSelfRef.__PVT__soc_status_status = vlSelfRef.__VdfgRegularize_h6e95ff9d_0_107;
    vlSelfRef.__PVT__soc_pending_status = vlSelfRef.__VdfgRegularize_h6e95ff9d_0_107;
    vlSelfRef.__PVT__builder_litespi_tx_mux_source_payload_len 
        = ((IData)(vlSelfRef.__PVT__builder_litespi_grant)
            ? (IData)(vlSelfRef.__PVT__add_devices_master_tx_fifo_pipe_valid_source_payload_len)
            : (IData)(vlSelfRef.__PVT__add_devices_mmap_source_payload_len));
    vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_valid 
        = vlSelfRef.__Vdly__add_devices_tx_pipe_valid_source_valid;
    vlSelfRef.__PVT__value = vlSelfRef.__Vdly__value;
    vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_valid 
        = vlSelfRef.__Vdly__add_devices_rx_pipe_valid_source_valid;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__max_words_w 
        = (0x000003ffU & (((IData)(3U) + ((4U >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                                           ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_CH_MAX_FRAME_BYTES_TBL_C
                                          [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                                           : 0U)) >> 2U));
    if ((4U >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tok_now_w 
            = (1U & (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w
                     [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r] 
                     | (0U != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r
                        [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r])));
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w 
            = (0x0000ffffU & vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_CH_RX_WORDS_TBL_C
               [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]);
    } else {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tok_now_w = 0U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w = 0U;
    }
    __Vtemp_1[0U] = (IData)((((QData)((IData)((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[3U]) 
                                                << 0x00000010U) 
                                               | vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[2U]))) 
                              << 0x00000020U) | (QData)((IData)(
                                                                (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[1U]) 
                                                                  << 0x00000010U) 
                                                                 | vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[0U])))));
    __Vtemp_1[1U] = (IData)(((((QData)((IData)((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[3U]) 
                                                 << 0x00000010U) 
                                                | vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[2U]))) 
                               << 0x00000020U) | (QData)((IData)(
                                                                 (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[1U]) 
                                                                   << 0x00000010U) 
                                                                  | vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[0U])))) 
                             >> 0x00000020U));
    __Vtemp_1[2U] = vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[4U];
    __PVT__KL_mbx__DOT__u_rx__DOT__tail_w = ((0x4fU 
                                              >= (0x0000007fU 
                                                  & ((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r) 
                                                     << 4U)))
                                              ? (0x0000ffffU 
                                                 & (((0U 
                                                      == 
                                                      (0x0000001fU 
                                                       & ((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r) 
                                                          << 4U)))
                                                      ? 0U
                                                      : 
                                                     (__Vtemp_1
                                                      [
                                                      (((IData)(0x0000000fU) 
                                                        + 
                                                        (0x0000007fU 
                                                         & ((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r) 
                                                            << 4U))) 
                                                       >> 5U)] 
                                                      << 
                                                      ((IData)(0x00000020U) 
                                                       - 
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r) 
                                                           << 4U))))) 
                                                    | (__Vtemp_1
                                                       [
                                                       (3U 
                                                        & ((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r) 
                                                           >> 1U))] 
                                                       >> 
                                                       (0x0000001fU 
                                                        & ((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r) 
                                                           << 4U)))))
                                              : 0U);
    __PVT__KL_mbx__DOT__u_rx__DOT__used_w = (0x0000ffffU 
                                             & (((4U 
                                                  >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                                                  ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r
                                                 [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                                                  : 0U) 
                                                - (IData)(__PVT__KL_mbx__DOT__u_rx__DOT__tail_w)));
    __PVT__KL_mbx__DOT__u_rx__DOT__cused_w = (0x0000ffffU 
                                              & (((4U 
                                                   >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                                                   ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_r
                                                  [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                                                   : 0U) 
                                                 - (IData)(__PVT__KL_mbx__DOT__u_rx__DOT__tail_w)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__free_w 
        = ((((IData)(__PVT__KL_mbx__DOT__u_rx__DOT__used_w) 
             > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w)) 
            | ((IData)(__PVT__KL_mbx__DOT__u_rx__DOT__cused_w) 
               > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w)))
            ? 0U : (0x0000ffffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w) 
                                   - (IData)(__PVT__KL_mbx__DOT__u_rx__DOT__used_w))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__word_w 
        = (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wacc_r 
           | ((IData)(vlSymsp->TOP.mbx_rx_data) << 
              ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__lane_r) 
               << 3U)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drop_w 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_drop_r) 
           & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rate_w 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_rate_r) 
           & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__accept_w 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_acc_r) 
           & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mis_w 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__vd_mis_r) 
           & (2U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drain_w 
        = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_done_r) 
           & ((0U != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_cnt_r)) 
              & ((0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)) 
                 | (1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__fin_ready_w 
        = ((1U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)) 
           & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_done_r) 
              & (0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_cnt_r))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__own_mac_w 
        = ((((QData)((IData)(vlSelfRef.__PVT__KL_mbx__DOT__own_mac_hi_r[0U])) 
             << 0x00000020U) | (QData)((IData)(vlSelfRef.__PVT__KL_mbx__DOT__own_mac_lo_r[0U]))) 
           & (- (QData)((IData)((1U & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r)))))));
    vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0 = (0x0000000fU 
                                                & VL_MULS_III(32, (IData)(0x00000010U), Vsim__ConstPool__TABLE_h1b85385a_0
                                                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r]));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_at_w 
        = ((0x000fU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r)) 
           | ((IData)(vlSymsp->TOP.mbx_rx_last) & (0x000eU 
                                                   == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__bad_w 
        = (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__overflow_r) 
            | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__oversize_r)) 
           | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
              > ((4U >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                  ? vlSymsp->TOP__KL_mbx_pkg.__PVT__MBX_CH_MAX_FRAME_BYTES_TBL_C
                 [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                  : 0U)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wdata_w 
        = ((3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r))
            ? (0x10000000U | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                              | ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r) 
                                 << 0x00000010U))) : 
           ((4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r))
             ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__arrival_ms_r
             : vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_data_r
            [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_rd_r]));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[0U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__0__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[1U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__1__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[2U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__2__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[3U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__3__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
}

void Vsim_sim___nba_sequent__TOP__sim__38(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__38\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __PVT__add_devices_rx_pipe_ready_source_first;
    __PVT__add_devices_rx_pipe_ready_source_first = 0;
    CData/*0:0*/ __PVT__add_devices_rx_pipe_ready_source_last;
    __PVT__add_devices_rx_pipe_ready_source_last = 0;
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[4U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__4__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[5U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__5__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[6U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__6__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[7U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__7__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[8U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__8__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[9U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__9__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[10U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__10__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[11U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__11__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[12U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__12__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[13U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__13__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[14U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__14__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w[15U] 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__g_cmp__BRA__15__KET____DOT__sr_r
        [(7U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r) 
                - (IData)(2U)))];
    if (vlSymsp->TOP.sys_reset) {
        vlSelfRef.__PVT__KL_mbx__DOT__filter_en_r = 0U;
    } else if (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__wr_w) 
                & (0x0028U == ((IData)(vlSelfRef.__PVT__add_devices_ctrlmailboxdma9) 
                               << 2U)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__filter_en_r = 
            (0x000000ffU & vlSelfRef.__PVT__add_devices_ctrlmailboxdma10);
    }
    if (vlSelfRef.__PVT__add_devices_tx_pipe_ready_valid) {
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_valid 
            = vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_valid;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_data 
            = vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_data;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_len 
            = vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_len;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_width 
            = vlSelfRef.__PVT__add_devices_tx_pipe_ready_sink_d_payload_width;
    } else {
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_valid 
            = vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_valid;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_data 
            = vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_data;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_len 
            = vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_len;
        vlSelfRef.__PVT__add_devices_tx_pipe_ready_source_payload_width 
            = vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_payload_width;
    }
    vlSelfRef.__PVT__add_devices_crossbar_source_ready 
        = (1U & (~ ((IData)(vlSelfRef.__PVT__add_devices_tx_pipe_valid_source_valid) 
                    & (IData)(vlSelfRef.__PVT__add_devices_tx_pipe_ready_valid))));
    if (vlSelfRef.__PVT__add_devices_rx_pipe_ready_valid) {
        __PVT__add_devices_rx_pipe_ready_source_first 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_first;
        __PVT__add_devices_rx_pipe_ready_source_last 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_last;
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_payload_data 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_payload_data;
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_valid 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_sink_d_valid;
    } else {
        __PVT__add_devices_rx_pipe_ready_source_first 
            = vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_first;
        __PVT__add_devices_rx_pipe_ready_source_last 
            = vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_last;
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_payload_data 
            = vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_payload_data;
        vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_valid 
            = vlSelfRef.__PVT__add_devices_rx_pipe_valid_source_valid;
    }
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__hold_w = ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tok_now_w)) 
                                                & (4U 
                                                   == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)));
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w = ((4U 
                                                   == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r)) 
                                                  & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tok_now_w));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__drain_fits_w 
        = ((((IData)(2U) + vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_idx_r
             [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_rd_r]) 
            < (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__free_w)) 
           & (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_idx_r
              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_rd_r] 
              < (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__max_words_w)));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__waddr_w 
        = (0x000003ffU & ((3U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r))
                           ? (((4U >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                                ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r
                               [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                                : 0U) & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w) 
                                         - (IData)(1U)))
                           : ((4U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__st_r))
                               ? (((IData)(1U) + ((4U 
                                                   >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))
                                                   ? vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r
                                                  [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r]
                                                   : 0U)) 
                                  & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w) 
                                     - (IData)(1U)))
                               : (((IData)(2U) + (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_idx_r
                                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__q_rd_r] 
                                                  + 
                                                  (0x0000ffffU 
                                                   & (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__wr_head_r
                                                      [vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r] 
                                                      & (- (IData)(
                                                                   (4U 
                                                                    >= (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r)))))))) 
                                  & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ring_words_w) 
                                     - (IData)(1U))))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype 
        = (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__b12_r) 
            << 8U) | (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__b13_r));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype 
        = ((0x000eU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))
            ? (IData)(vlSymsp->TOP.mbx_rx_data) : (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__sub_r));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg 
        = ((0x000fU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cnt_r))
            ? (0x0000000fU & (IData)(vlSymsp->TOP.mbx_rx_data))
            : 0U);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 0U;
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = (0x000091e0f0010000ULL == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r);
    if ((0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
    }
    if (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok) 
           & (0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
          & (0xfaU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 0U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = (0x000091e0f0010000ULL == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r);
    if ((((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
            & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
           & (0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
          & (0xfcU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 1U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r)) 
           & (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r 
              == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__own_mac_w));
    if ((((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
            & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
           & (0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
          & (0xfcU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 1U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r)) 
           & (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r 
              == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__own_mac_w));
    if ((((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
            & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
           & (0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
          & (0xfbU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 2U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = (0x000091e0f000ff00ULL == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r);
    if ((((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
            & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
           & (0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
          & (0xfeU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 3U;
    }
}

extern const VlUnpacked<CData/*0:0*/, 2> Vsim__ConstPool__TABLE_h1dda76f3_0;

void Vsim_sim___nba_sequent__TOP__sim__39(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__39\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = ((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r)) 
           & (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r 
              == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__own_mac_w));
    if ((0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
    }
    if ((((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
            & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
           & (0x22f0U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
          & (0xfeU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__subtype))) 
         & (4U >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 3U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = (0x00000180c200000eULL == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r);
    if ((0x22eaU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
    }
    if (((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
           & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
          & (0x22eaU == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 4U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok 
        = (0x00000180c2000021ULL == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__dst_r);
    if ((0x88f5U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__ctrl_et_w = 1U;
    }
    if (((((~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w)) 
           & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__unnamedblk9__DOT__unnamedblk10__DOT__dst_ok)) 
          & (0x88f5U == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__ethertype))) 
         & (0x0000ffffU >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__classify__DOT__msg)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_hit_w = 1U;
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__cls_ch_w = 4U;
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w 
        = (((((((Vsim__ConstPool__TABLE_h1dda76f3_0
                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                 & ((~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                        >> (0x0000000fU & ((IData)(0x0fU) 
                                           + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                    & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                       >> (0x0000000fU & ((IData)(0x0fU) 
                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                << 3U) | ((Vsim__ConstPool__TABLE_h1dda76f3_0
                           [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                           & ((~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                  >> (0x0000000fU & 
                                      ((IData)(0x0eU) 
                                       + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                              & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                 >> (0x0000000fU & 
                                     ((IData)(0x0eU) 
                                      + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                          << 2U)) | (((Vsim__ConstPool__TABLE_h1dda76f3_0
                                       [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                       & ((~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                              >> (0x0000000fU 
                                                  & ((IData)(0x0dU) 
                                                     + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                          & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                             >> (0x0000000fU 
                                                 & ((IData)(0x0dU) 
                                                    + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                      << 1U) | (Vsim__ConstPool__TABLE_h1dda76f3_0
                                                [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                & ((~ 
                                                    ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                     >> 
                                                     (0x0000000fU 
                                                      & ((IData)(0x0cU) 
                                                         + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                   & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                      >> 
                                                      (0x0000000fU 
                                                       & ((IData)(0x0cU) 
                                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))))) 
             << 0x0000000cU) | (((((Vsim__ConstPool__TABLE_h1dda76f3_0
                                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                    & ((~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                           >> (0x0000000fU 
                                               & ((IData)(0x0bU) 
                                                  + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                       & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                          >> (0x0000000fU 
                                              & ((IData)(0x0bU) 
                                                 + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                   << 3U) | ((Vsim__ConstPool__TABLE_h1dda76f3_0
                                              [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                              & ((~ 
                                                  ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                   >> 
                                                   (0x0000000fU 
                                                    & ((IData)(0x0aU) 
                                                       + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                 & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                    >> 
                                                    (0x0000000fU 
                                                     & ((IData)(0x0aU) 
                                                        + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                             << 2U)) 
                                 | (((Vsim__ConstPool__TABLE_h1dda76f3_0
                                      [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                      & ((~ ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                             >> (0x0000000fU 
                                                 & ((IData)(9U) 
                                                    + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                         & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                            >> (0x0000000fU 
                                                & ((IData)(9U) 
                                                   + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                     << 1U) | (Vsim__ConstPool__TABLE_h1dda76f3_0
                                               [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                               & ((~ 
                                                   ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                    >> 
                                                    (0x0000000fU 
                                                     & ((IData)(8U) 
                                                        + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                  & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                     >> 
                                                     (0x0000000fU 
                                                      & ((IData)(8U) 
                                                         + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))))) 
                                << 8U)) | ((((((Vsim__ConstPool__TABLE_h1dda76f3_0
                                                [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                & ((~ 
                                                    ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                     >> 
                                                     (0x0000000fU 
                                                      & ((IData)(7U) 
                                                         + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                   & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                      >> 
                                                      (0x0000000fU 
                                                       & ((IData)(7U) 
                                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                               << 3U) 
                                              | ((Vsim__ConstPool__TABLE_h1dda76f3_0
                                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                  & ((~ 
                                                      ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                       >> 
                                                       (0x0000000fU 
                                                        & ((IData)(6U) 
                                                           + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                     & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                        >> 
                                                        (0x0000000fU 
                                                         & ((IData)(6U) 
                                                            + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                                 << 2U)) 
                                             | (((Vsim__ConstPool__TABLE_h1dda76f3_0
                                                  [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                  & ((~ 
                                                      ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                       >> 
                                                       (0x0000000fU 
                                                        & ((IData)(5U) 
                                                           + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                     & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                        >> 
                                                        (0x0000000fU 
                                                         & ((IData)(5U) 
                                                            + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                                 << 1U) 
                                                | (Vsim__ConstPool__TABLE_h1dda76f3_0
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                   & ((~ 
                                                       ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                        >> 
                                                        (0x0000000fU 
                                                         & ((IData)(4U) 
                                                            + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                      & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                         >> 
                                                         (0x0000000fU 
                                                          & ((IData)(4U) 
                                                             + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))))) 
                                            << 4U) 
                                           | ((((Vsim__ConstPool__TABLE_h1dda76f3_0
                                                 [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                 & ((~ 
                                                     ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                      >> 
                                                      (0x0000000fU 
                                                       & ((IData)(3U) 
                                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                    & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                       >> 
                                                       (0x0000000fU 
                                                        & ((IData)(3U) 
                                                           + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                                << 3U) 
                                               | ((Vsim__ConstPool__TABLE_h1dda76f3_0
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                   & ((~ 
                                                       ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                        >> 
                                                        (0x0000000fU 
                                                         & ((IData)(2U) 
                                                            + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                      & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                         >> 
                                                         (0x0000000fU 
                                                          & ((IData)(2U) 
                                                             + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                                  << 2U)) 
                                              | (((Vsim__ConstPool__TABLE_h1dda76f3_0
                                                   [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                   & ((~ 
                                                       ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                        >> 
                                                        (0x0000000fU 
                                                         & ((IData)(1U) 
                                                            + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))) 
                                                      & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                         >> 
                                                         (0x0000000fU 
                                                          & ((IData)(1U) 
                                                             + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))))) 
                                                  << 1U) 
                                                 | (Vsim__ConstPool__TABLE_h1dda76f3_0
                                                    [vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__if_r] 
                                                    & ((~ 
                                                        ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__owed_r) 
                                                         >> (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))) 
                                                       & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                                          >> (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0))))))));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__eq_w = 
        ((((((((IData)(vlSymsp->TOP.mbx_rx_data) == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
               [(0x0000000fU & ((IData)(0x0fU) + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
              << 3U) | (((IData)(vlSymsp->TOP.mbx_rx_data) 
                         == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                         [(0x0000000fU & ((IData)(0x0eU) 
                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                        << 2U)) | ((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                     == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                     [(0x0000000fU 
                                       & ((IData)(0x0dU) 
                                          + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                    << 1U) | ((IData)(vlSymsp->TOP.mbx_rx_data) 
                                              == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                              [(0x0000000fU 
                                                & ((IData)(0x0cU) 
                                                   + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]))) 
           << 0x0000000cU) | ((((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                  == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                  [(0x0000000fU & ((IData)(0x0bU) 
                                                   + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                 << 3U) | (((IData)(vlSymsp->TOP.mbx_rx_data) 
                                            == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                            [(0x0000000fU 
                                              & ((IData)(0x0aU) 
                                                 + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                           << 2U)) 
                               | ((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                    == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                    [(0x0000000fU & 
                                      ((IData)(9U) 
                                       + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                   << 1U) | ((IData)(vlSymsp->TOP.mbx_rx_data) 
                                             == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                             [(0x0000000fU 
                                               & ((IData)(8U) 
                                                  + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]))) 
                              << 8U)) | (((((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                              == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                              [(0x0000000fU 
                                                & ((IData)(7U) 
                                                   + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                             << 3U) 
                                            | (((IData)(vlSymsp->TOP.mbx_rx_data) 
                                                == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                                [(0x0000000fU 
                                                  & ((IData)(6U) 
                                                     + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                               << 2U)) 
                                           | ((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                                == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                                [(0x0000000fU 
                                                  & ((IData)(5U) 
                                                     + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                               << 1U) 
                                              | ((IData)(vlSymsp->TOP.mbx_rx_data) 
                                                 == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                                 [(0x0000000fU 
                                                   & ((IData)(4U) 
                                                      + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]))) 
                                          << 4U) | 
                                         (((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                             == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                             [(0x0000000fU 
                                               & ((IData)(3U) 
                                                  + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                            << 3U) 
                                           | (((IData)(vlSymsp->TOP.mbx_rx_data) 
                                               == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                               [(0x0000000fU 
                                                 & ((IData)(2U) 
                                                    + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                              << 2U)) 
                                          | ((((IData)(vlSymsp->TOP.mbx_rx_data) 
                                               == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                               [(0x0000000fU 
                                                 & ((IData)(1U) 
                                                    + (IData)(vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0)))]) 
                                              << 1U) 
                                             | ((IData)(vlSymsp->TOP.mbx_rx_data) 
                                                == vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__c_tap_w
                                                [vlSelfRef.__VdfgRegularize_h6e95ff9d_0_0])))));
}

void Vsim_sim___nba_sequent__TOP__sim__40(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__40\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint1_sink_ready = 0U;
    vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint0_sink_ready = 0U;
    vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint1_source_payload_data = 0U;
    vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_payload_data = 0U;
    vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint1_source_valid = 0U;
    if (vlSelfRef.__PVT__builder_litespi_grant) {
        vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint1_sink_ready 
            = vlSelfRef.__PVT__add_devices_crossbar_source_ready;
        vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint1_source_payload_data 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_payload_data;
        vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint1_source_valid 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_valid;
    }
    vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid = 0U;
    if ((1U & (~ (IData)(vlSelfRef.__PVT__builder_litespi_grant)))) {
        vlSelfRef.__PVT__builder_litespi_tx_mux_endpoint0_sink_ready 
            = vlSelfRef.__PVT__add_devices_crossbar_source_ready;
        vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_payload_data 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_payload_data;
        vlSelfRef.__PVT__builder_litespi_rx_demux_endpoint0_source_valid 
            = vlSelfRef.__PVT__add_devices_rx_pipe_ready_source_valid;
    }
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[0U] = (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[0U] 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[0U]);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[0U];
    if ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[0U] 
         & (8U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)));
    }
    if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
          & (0U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
         | vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[0U])) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens) 
                              - (IData)(1U)));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[0U] 
        = (0x000000ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens));
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[1U] = (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[1U] 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[1U]);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[1U];
    if ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[1U] 
         & (0x0010U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)));
    }
    if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
          & (1U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
         | vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[1U])) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens) 
                              - (IData)(1U)));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[1U] 
        = (0x000000ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens));
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[2U] = (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[2U] 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[2U]);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[2U];
    if ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[2U] 
         & (0x0010U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)));
    }
    if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
          & (2U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
         | vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[2U])) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens) 
                              - (IData)(1U)));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[2U] 
        = (0x000000ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens));
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[3U] = (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[3U] 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[3U]);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[3U];
    if ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[3U] 
         & (8U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)));
    }
    if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
          & (3U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
         | vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[3U])) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens) 
                              - (IData)(1U)));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[3U] 
        = (0x000000ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens));
    vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[4U] = (vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[4U] 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__held_r[4U]);
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
        = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_r[4U];
    if ((vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__refill_w[4U] 
         & (0x0020U > (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)))) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(1U) + (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens)));
    }
    if ((((IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__commit_w) 
          & (4U == (IData)(vlSelfRef.KL_mbx__DOT__u_rx__DOT__ch_r))) 
         | vlSelfRef.KL_mbx__DOT__u_rx__DOT__rel_w[4U])) {
        vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens 
            = (0x000001ffU & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens) 
                              - (IData)(1U)));
    }
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__tokens_nx_w[4U] 
        = (0x000000ffU & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__buckets__DOT__unnamedblk18__DOT__unnamedblk19__DOT__tokens));
    vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__bound_hit_w 
        = (0U != ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__match_r) 
                  & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__live_w)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfffffff8U 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((8U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 2U) 
                                                     | (((4U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 1U) 
                                                        | (0U 
                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xffffffc7U 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((0x0014U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 5U) 
                                                     | (((0x0010U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 4U) 
                                                        | ((0x000cU 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 3U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfffffe3fU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((0x0024U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 8U) 
                                                     | (((0x0020U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 7U) 
                                                        | ((0x0018U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 6U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfffff1ffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((0x0030U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x0000000bU) 
                                                     | (((0x002cU 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000000aU) 
                                                        | ((0x0028U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 9U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xffff8fffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((0x0060U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x0000000eU) 
                                                     | (((0x0038U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000000dU) 
                                                        | ((0x0034U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x0000000cU))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfffc7fffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((0x0074U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x00000011U) 
                                                     | (((0x0070U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x00000010U) 
                                                        | ((0x0064U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x0000000fU))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xffe3ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((0x0048U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x00000014U) 
                                                     | (((0x0044U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x00000013U) 
                                                        | ((0x0040U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x00000012U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xffdfffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | ((0x0080U 
                                                      == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                     << 0x00000015U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xff3fffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_at_w) 
                                                       & (2U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_reg_w))) 
                                                      << 0x00000017U) 
                                                     | ((0x0084U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                        << 0x00000016U)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfeffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_at_w) 
                                                       & (2U 
                                                          != (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_bnd_reg_w))) 
                                                      & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__rb_vld_w)) 
                                                     << 0x00000018U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfdffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w))) 
                                                       & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w))) 
                                                      & (0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                     << 0x00000019U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xfbffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w))) 
                                                       & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w))) 
                                                      & (4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                     << 0x0000001aU));
}

void Vsim_sim___nba_sequent__TOP__sim__41(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__41\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xf7ffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w))) 
                                                       & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w))) 
                                                      & (8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                     << 0x0000001bU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xefffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w))) 
                                                       & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w))) 
                                                      & (0x000cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                     << 0x0000001cU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0xdfffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w))) 
                                                       & (~ (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w))) 
                                                      & (0x0010U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                     << 0x0000001dU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U] = ((0x3fffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[0U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w)) 
                                                       & (4U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                      << 0x0000001fU) 
                                                     | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                          & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_src_w)) 
                                                         & (0U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                        << 0x0000001eU)));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffffffcU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | (((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                        & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w)) 
                                                       & (4U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                      << 1U) 
                                                     | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                         & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w)) 
                                                        & (0U 
                                                           == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffffffbU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_at_w) 
                                                       & (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_sink_w)) 
                                                      & (8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_pub_reg_w))) 
                                                     << 2U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffffff7U 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 3U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffffefU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 4U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffffdfU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 5U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffffbfU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x000cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 6U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffff7fU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0010U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 7U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffffeffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0014U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 8U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffffdffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x001cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 9U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffffbffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0040U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000000aU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffff7ffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0044U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000000bU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffefffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x004cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000000cU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffdfffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0050U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000000dU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffffbfffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0060U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000000eU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffff7fffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0064U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000000fU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffeffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x006cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000010U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffdffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0070U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000011U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfffbffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0074U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000012U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfff7ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0080U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000013U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffefffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0084U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000014U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffdfffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0088U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000015U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xffbfffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x008cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000016U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xff7fffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0090U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000017U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfeffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x0094U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000018U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfdffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x009cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x00000019U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xfbffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00a0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000001aU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xf7ffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00a4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000001bU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xefffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00c0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000001cU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xdfffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00c4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000001dU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0xbfffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00c8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000001eU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U] = ((0x7fffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[1U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00ccU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 0x0000001fU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfffffffeU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                      & (0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                     & (0x00d4U 
                                                        == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfffffffdU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00d8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 1U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfffffffbU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (0U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x00dcU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 2U));
}

void Vsim_sim___nba_sequent__TOP__sim__42(Vsim_sim* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+      Vsim_sim___nba_sequent__TOP__sim__42\n"); );
    Vsim__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __Vfunc_mbx_place_f__162__value;
    __Vfunc_mbx_place_f__162__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__163__value;
    __Vfunc_mbx_place_f__163__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__164__value;
    __Vfunc_mbx_place_f__164__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__165__value;
    __Vfunc_mbx_place_f__165__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__166__value;
    __Vfunc_mbx_place_f__166__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__167__value;
    __Vfunc_mbx_place_f__167__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__168__value;
    __Vfunc_mbx_place_f__168__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__169__value;
    __Vfunc_mbx_place_f__169__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__170__value;
    __Vfunc_mbx_place_f__170__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__171__value;
    __Vfunc_mbx_place_f__171__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__172__value;
    __Vfunc_mbx_place_f__172__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__173__value;
    __Vfunc_mbx_place_f__173__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__174__value;
    __Vfunc_mbx_place_f__174__value = 0;
    IData/*31:0*/ __Vfunc_mbx_place_f__175__value;
    __Vfunc_mbx_place_f__175__value = 0;
    // Body
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfffffff7U 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (1U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 3U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffffffefU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (1U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 4U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffffffdfU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (1U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 5U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffffffbfU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (1U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0x000cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 6U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffffff7fU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (2U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (0U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 7U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfffffeffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (2U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (4U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 8U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfffffdffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((((IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_at_w) 
                                                       & (2U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_area_w))) 
                                                      & (8U 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_reg_w))) 
                                                     << 9U));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffffe3ffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x0108U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x0000000cU) 
                                                     | (((0x0104U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000000bU) 
                                                        | ((0x0100U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x0000000aU))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffff1fffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x0114U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x0000000fU) 
                                                     | (((0x0110U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000000eU) 
                                                        | ((0x010cU 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x0000000dU))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfff8ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x0120U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x00000012U) 
                                                     | (((0x011cU 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x00000011U) 
                                                        | ((0x0118U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x00000010U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xffc7ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x012cU 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x00000015U) 
                                                     | (((0x0128U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x00000014U) 
                                                        | ((0x0124U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x00000013U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xfe3fffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x0138U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x00000018U) 
                                                     | (((0x0134U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x00000017U) 
                                                        | ((0x0130U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x00000016U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0xf1ffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x0144U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x0000001bU) 
                                                     | (((0x0140U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000001aU) 
                                                        | ((0x013cU 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x00000019U))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0x8fffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | (((0x0150U 
                                                       == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                      << 0x0000001eU) 
                                                     | (((0x014cU 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000001dU) 
                                                        | ((0x0148U 
                                                            == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                           << 0x0000001cU))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U] = ((0x7fffffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[2U]) 
                                                  | ((0x0154U 
                                                      == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                     << 0x0000001fU));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x0003fffcU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & ((0x7ffffffeU 
                                                         & ((0x015cU 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                            << 1U)) 
                                                        | ((0x7fffffffU 
                                                            & (0x0158U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r))) 
                                                           | ((0x0154U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                              >> 1U)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x0003ffe3U 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & (((0x0168U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 4U) 
                                                        | (((0x0164U 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                            << 3U) 
                                                           | ((0x0160U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                              << 2U)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x0003ff1fU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & (((0x0174U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 7U) 
                                                        | (((0x0170U 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                            << 6U) 
                                                           | ((0x016cU 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                              << 5U)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x0003f8ffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & (((0x0180U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000000aU) 
                                                        | (((0x017cU 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                            << 9U) 
                                                           | ((0x0178U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                              << 8U)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x0003c7ffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & (((0x018cU 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x0000000dU) 
                                                        | (((0x0188U 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                            << 0x0000000cU) 
                                                           | ((0x0184U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                              << 0x0000000bU)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x00023fffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & (((0x0198U 
                                                          == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                         << 0x00000010U) 
                                                        | (((0x0194U 
                                                             == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                            << 0x0000000fU) 
                                                           | ((0x0190U 
                                                               == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                              << 0x0000000eU)))));
    vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U] = ((0x0001ffffU 
                                                   & vlSelfRef.__PVT__KL_mbx__DOT__rd_hit_w[3U]) 
                                                  | (0x0003ffffU 
                                                     & ((0x019cU 
                                                         == (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_off_r)) 
                                                        << 0x00000011U)));
    vlSelfRef.__Vfunc_mbx_place_f__161__value = (((
                                                   (vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[4U] 
                                                    != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[4U]) 
                                                   << 4U) 
                                                  | (((vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[3U] 
                                                       != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[3U]) 
                                                      << 3U) 
                                                     | ((vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[2U] 
                                                         != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[2U]) 
                                                        << 2U))) 
                                                 | (((vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[1U] 
                                                      != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[1U]) 
                                                     << 1U) 
                                                    | (vlSelfRef.__PVT__KL_mbx__DOT__rx_tail_r[0U] 
                                                       != vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__head_pub_r[0U])));
    vlSelfRef.KL_mbx__DOT____VlemCall_161__mbx_place_f 
        = (0x000000ffU & vlSelfRef.__Vfunc_mbx_place_f__161__value);
    __Vfunc_mbx_place_f__162__value = ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__head_r) 
                                       != (0x0000ffffU 
                                           & vlSelfRef.__PVT__KL_mbx__DOT__evt_tail_r));
    vlSelfRef.KL_mbx__DOT____VlemCall_162__mbx_place_f 
        = (0x00000100U & (__Vfunc_mbx_place_f__162__value 
                          << 8U));
    __Vfunc_mbx_place_f__163__value = vlSelfRef.__PVT__KL_mbx__DOT__err_r;
    vlSelfRef.KL_mbx__DOT____VlemCall_163__mbx_place_f 
        = (__Vfunc_mbx_place_f__163__value << 0x0000001fU);
    __Vfunc_mbx_place_f__164__value = vlSelfRef.__PVT__KL_mbx__DOT__now_ms_r;
    vlSelfRef.KL_mbx__DOT____VlemCall_164__mbx_place_f 
        = __Vfunc_mbx_place_f__164__value;
    __Vfunc_mbx_place_f__165__value = vlSymsp->TOP.mbx_link_up;
    vlSelfRef.KL_mbx__DOT____VlemCall_165__mbx_place_f 
        = (0x0000000fU & __Vfunc_mbx_place_f__165__value);
    __Vfunc_mbx_place_f__166__value = vlSelfRef.__PVT__KL_mbx__DOT__u_evt__DOT__head_r;
    vlSelfRef.KL_mbx__DOT____VlemCall_166__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__166__value);
    __Vfunc_mbx_place_f__167__value = vlSelfRef.__PVT__KL_mbx__DOT__bus_err_r;
    vlSelfRef.KL_mbx__DOT____VlemCall_167__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__167__value);
    __Vfunc_mbx_place_f__168__value = vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__mismatch_r;
    vlSelfRef.KL_mbx__DOT____VlemCall_168__mbx_place_f 
        = (0x0000ffffU & __Vfunc_mbx_place_f__168__value);
    __Vfunc_mbx_place_f__169__value = (IData)(vlSymsp->TOP.mbx_gm_id);
    vlSelfRef.KL_mbx__DOT____VlemCall_169__mbx_place_f 
        = __Vfunc_mbx_place_f__169__value;
    __Vfunc_mbx_place_f__170__value = vlSelfRef.__PVT__KL_mbx__DOT__gm_hi_snap_r[0U];
    vlSelfRef.KL_mbx__DOT____VlemCall_170__mbx_place_f 
        = __Vfunc_mbx_place_f__170__value;
    __Vfunc_mbx_place_f__171__value = vlSelfRef.__PVT__KL_mbx__DOT__domain_snap_r[0U];
    vlSelfRef.KL_mbx__DOT____VlemCall_171__mbx_place_f 
        = (0x000000ffU & __Vfunc_mbx_place_f__171__value);
    __Vfunc_mbx_place_f__172__value = (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__en_r) 
                                             >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__u_rx__DOT__hrk_r)));
    vlSelfRef.KL_mbx__DOT____VlemCall_172__mbx_place_f 
        = (1U & __Vfunc_mbx_place_f__172__value);
    __Vfunc_mbx_place_f__173__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__fw_busy_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_173__mbx_place_f 
        = (1U & __Vfunc_mbx_place_f__173__value);
    __Vfunc_mbx_place_f__174__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__ctr_busy_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_174__mbx_place_f 
        = (1U & __Vfunc_mbx_place_f__174__value);
    __Vfunc_mbx_place_f__175__value = ((0U >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                       && (1U & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__ctr_done_r) 
                                                 >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
    vlSelfRef.KL_mbx__DOT____VlemCall_175__mbx_place_f 
        = (2U & (__Vfunc_mbx_place_f__175__value << 1U));
    vlSelfRef.__Vfunc_mbx_place_f__176__value = ((0U 
                                                  >= (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w)) 
                                                 && (1U 
                                                     & ((IData)(vlSelfRef.__PVT__KL_mbx__DOT__ctr_tmo_r) 
                                                        >> (IData)(vlSelfRef.__PVT__KL_mbx__DOT__rd_face_if_w))));
}
