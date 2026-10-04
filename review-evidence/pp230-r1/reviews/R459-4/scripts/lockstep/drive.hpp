// SPDX-License-Identifier: CERN-OHL-W-2.0
// Seeded input model for the base-versus-head lockstep (reviewer probe).
// Every input of the module is drawn here by name; unknown names get fresh
// random bits every cycle. Matcher keys (stream_id, DA, VLAN) come from one
// four-entry table shared by the gate, control and decoder faces, so
// declarations, settles and received values meet.
#pragma once
#include <cstdint>
#include <cstring>
#include <map>
#include <string>
#include <vector>
#include "Vls_wrap.h"

struct Drv {
  uint64_t s;
  uint64_t cyc = 0;
  int n;
  int rst_hold = 5;
  int kg = 0, kc = 0, ke = 0;
  uint64_t req = 0, inv = 0, sradm = 0;
  std::vector<uint16_t> mfs, mif;
  std::map<std::string, std::vector<uint32_t>> held;
  std::map<std::string, std::vector<uint32_t>> cache;
  uint64_t sid[4] = {0x02AABBCC00010001ull, 0x02AABBCC00010002ull, 0x0011223344550007ull, 0x02AABBCC0001FFFFull};
  uint64_t da[4] = {0x91E0F0000001ull, 0x91E0F0000002ull, 0x91E0F0AA0007ull, 0x91E0F0000003ull};
  uint16_t vid[4] = {2, 2, 0x123, 0xFFE};

  Drv(uint64_t seed, int nctx) : s(seed * 0x9E3779B97F4A7C15ull + 1), n(nctx), mfs(nctx, 224), mif(nctx, 1) {}

  uint64_t r() { s ^= s >> 12; s ^= s << 25; s ^= s >> 27; return s * 0x2545F4914F6CDD1Dull; }
  bool p(double q) { return (r() >> 11) * (1.0 / 9007199254740992.0) < q; }
  uint64_t mask(int w) { return w >= 64 ? ~0ull : ((1ull << w) - 1); }

  bool in_reset() const { return rst_hold > 0; }

  void begin_cycle() {
    cache.clear();
    if (rst_hold > 0) rst_hold--;
    else if (p(1.0 / 40000)) rst_hold = 1 + static_cast<int>(r() % 4);
    kg = r() % 4; kc = r() % 4; ke = r() % 4;
    inv = 0;
    for (int i = 0; i < n; ++i) {
      if (p(0.0015)) { req ^= 1ull << i; inv |= 1ull << i; }
      if (p(0.002)) {
        mfs[i] = static_cast<uint16_t>(r() % 1600);
        mif[i] = static_cast<uint16_t>(r() % 9);
        if (p(0.9)) inv |= 1ull << i;
      }
      if (p(0.001)) inv |= 1ull << i;
      if (p(0.004)) sradm ^= 1ull << i;
    }
    cyc++;
  }

  std::vector<uint32_t> fresh(const std::string& nm, int w) {
    std::vector<uint32_t> v((w + 31) / 32, 0);
    auto put = [&](uint64_t x) { v[0] = static_cast<uint32_t>(x); if (v.size() > 1) v[1] = static_cast<uint32_t>(x >> 32); };
    auto ends = [&](const char* suf) { size_t l = std::strlen(suf); return nm.size() >= l && nm.compare(nm.size() - l, l, suf) == 0; };
    if (nm == "rst_n") put(in_reset() ? 0 : 1);
    else if (nm == "gate_valid_i" || nm == "ctl_valid_i") put(p(0.25));
    else if (nm == "evt_valid_i") put(p(0.3));
    else if (nm == "exp_valid_i") put(p(0.1));
    else if (nm == "evt_msrp_i") put(p(0.85));
    else if (nm == "evt_attr_type_i") { static const uint8_t t[5] = {1, 2, 3, 4, 0x10}; put(t[r() % 5]); }
    else if (nm == "gate_stream_id_i") put(sid[kg]);
    else if (nm == "ctl_stream_id_i") put(sid[kc]);
    else if (nm == "evt_stream_id_i") put(sid[ke]);
    else if (nm == "gate_da_i") put(p(0.1) ? r() : da[kg]);
    else if (nm == "ctl_da_i") put(p(0.1) ? r() : da[kc]);
    else if (nm == "evt_da_i") put(p(0.1) ? r() : da[ke]);
    else if (nm == "gate_vid_i") put(vid[kg]);
    else if (nm == "ctl_vid_i") put(vid[kc]);
    else if (nm == "evt_vid_i") put(p(0.2) ? 0 : vid[ke]);
    else if (nm == "evt_mrp_event_i") put(r() % 8);
#ifndef LS_ANY_INDEX
    // KL_srp_top offers a gate or control op only for an index below the
    // context count (its req_index_i checks); an idle face may hold any index
    else if (nm == "gate_src_i") put(get("gate_valid_i", 1)[0] ? r() % n : r());
    else if (nm == "ctl_sink_i") put(get("ctl_valid_i", 1)[0] ? r() % n : r());
#endif
    else if (nm == "exp_slot_i") put(r() % (n + 3));
    else if (nm == "now_ms_i") put(cyc / 37);
    else if (nm == "join_tick_i") put(p(0.02));
    else if (nm == "periodic_tick_i") put(p(0.003));
    else if (nm == "leaveall_own_i") put(p(0.005));
    else if (nm == "leaveall_rx_i") put((p(0.003) ? 1 : 0) | (p(0.003) ? 2 : 0) | (p(0.003) ? 4 : 0) | (p(0.003) ? 8 : 0));
    else if (nm == "ev_ready_i") put(p(0.7));
    else if (nm == "user_ready_i") put(p(0.6));
    else if (nm == "own_mac_i") put(0x02AABBCCDDEEull);
    else if (nm == "sr_admitted_i") put(sradm);
    else if (nm == "req_i") put(req);
    else if (nm == "invalidate_i") put(inv);
    else if (nm == "port_rate_bps_i") put((cyc / 400000) % 2 ? 100000000u : 1000000000u);
    else if (nm == "max_frame_i" || nm == "interval_frames_i") {
      const auto& src = nm == "max_frame_i" ? mfs : mif;
      for (int i = 0; i < n; ++i) v[i / 2] |= static_cast<uint32_t>(src[i]) << (16 * (i % 2));
    } else if (nm == "p2p_i" || nm == "vid_sent_i" || nm == "vid_val_i") {
      auto it = held.find(nm);
      if (it == held.end() || p(0.002)) {
        std::vector<uint32_t> h(v.size(), 0);
        if (nm == "p2p_i") h[0] = p(0.95);
        else if (nm == "vid_sent_i") h[0] = static_cast<uint32_t>(r());
        else { uint64_t x = 0; for (int i = 0; i < 4; ++i) x |= static_cast<uint64_t>(vid[r() % 4]) << (12 * i); h[0] = static_cast<uint32_t>(x); if (h.size() > 1) h[1] = static_cast<uint32_t>(x >> 32); }
        held[nm] = h;
      }
      v = held[nm];
    } else {
      (void)ends;
      for (auto& x : v) x = static_cast<uint32_t>(r());
    }
    int top = w % 32;
    if (top) v.back() &= (1u << top) - 1;
    return v;
  }

  const std::vector<uint32_t>& get(const char* nm, int w) {
    auto it = cache.find(nm);
    if (it == cache.end()) it = cache.emplace(nm, fresh(nm, w)).first;
    return it->second;
  }
  uint64_t value(const char* nm, int w) {
    const auto& v = get(nm, w);
    uint64_t x = v[0];
    if (v.size() > 1) x |= static_cast<uint64_t>(v[1]) << 32;
    return x & mask(w);
  }
  uint32_t word(const char* nm, int i, int w) { return get(nm, w)[i]; }
};

void drive_inputs(Vls_wrap* d, Drv& g);
extern const char* OUT_NAMES[];
extern const int N_OUT;
extern const int N_CTX;
