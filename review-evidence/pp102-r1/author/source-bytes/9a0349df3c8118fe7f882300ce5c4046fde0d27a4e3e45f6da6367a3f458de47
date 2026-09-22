// SPDX-License-Identifier: CERN-OHL-W-2.0
// F08.4 timer-slot map + 02 §5 event-router map suite.
//
// The expectations below are the DOCUMENT, re-derived here from the 08 §5
// F08.4 table and the 02 §5 source catalog — never read back from the RTL.
// What is graded, per shape:
//
//   1. every base equals the independent re-derivation;
//   2. the groups are PAIRWISE DISJOINT — the property the literal map lost,
//      checked as real interval overlap over every pair, not as a spot check;
//   3. the map fits P-TIMER-SLOTS and the derived index width can address it;
//   4. the 8x8 shape still reproduces the historical literal map EXACTLY
//      (0/1/9/17/25/57/61/66/73/81, 89 slots; event sources 0/8/16/17/18/19/
//      27/28, 29 total) — the shipping shape must not move;
//   5. THE REGRESSION, at 9 sinks and 9 sources: the two collisions the
//      literal map had are named and shown gone —
//        listener sink SI-1 vs the talker base   (distinct owner tags, so the
//                                                 loser's deadline was lost)
//        SRP talker SO-1 vs the SRP listener base (no owner discrimination,
//                                                 so the expiry was
//                                                 MISDELIVERED)
//        event TK_ATTR_UNREGISTERED{SI-1} vs ADP EVT_TK_DISCOVERED (the
//                                                 router carries no owner
//                                                 tag at all);
//   6. the owner-tag allocation is disjoint at every legal shape, and the
//      first shape past it is named (that shape is refused at elaboration —
//      shape_elab.sh proves the refusal, this proves WHERE it starts).
#include <cstdint>
#include <cstdio>
#include <string>
#include <vector>
#include "Vtimer_map_wrap.h"
#include "verilated.h"
#include "../common/verilator_harness.hpp"

#define CHECK(cond, ...) do { \
  ++checks; \
  if (!(cond)) { ++fails; printf("FAIL: " __VA_ARGS__); printf("\n"); } \
} while (0)

// ---- F01.5 shape constants (the document, not the DUT) -----------------
constexpr unsigned N_IF = 1;
constexpr unsigned N_CTRL = 16;
constexpr unsigned CA_POOL = 4;
constexpr unsigned SRP_CAD_SLOTS = 7;   // JOIN x2 + LEAVEALL x2 + PERIODIC
                                        // + Domain and MVRP VID registrars
constexpr unsigned SINGLETONS = 5;      // LOCK, IDENT-BURST, IDENT-REARM,
                                        // CTR-OBSERVE, NVM-DEBOUNCE
constexpr unsigned MAAP_SLOTS = 2;      // MAAP probe + announce (11,
                                        // IEEE 1722-2016 B.3.4)

// ---- 08 §5 F08.4 owner-tag allocation ----------------------------------
constexpr unsigned OWN_LSTN = 0x20;
constexpr unsigned OWN_SRP_TK = 0x40;
constexpr unsigned OWN_TKR = 0x50;
constexpr unsigned OWN_SRP_LS = 0x60;
constexpr unsigned OWN_SRP_CAD = 0x80;
constexpr unsigned OWN_MAAP = 0x90;
// the owner tag rides an 8-bit expiry bus, so 256 tags is the whole space
constexpr unsigned OWN_SPACE = 256;

// map field order, mirroring the wrap's port order
constexpr unsigned M_ADV = 0;
constexpr unsigned M_NOADP = 1;
constexpr unsigned M_LSTN = 2;
constexpr unsigned M_TKR = 3;
constexpr unsigned M_REGMON = 4;
constexpr unsigned M_CAPOOL = 5;
constexpr unsigned M_SINGLE = 6;
constexpr unsigned M_MAAP = 7;
constexpr unsigned M_BASE_END = 8;
constexpr unsigned M_SRP_CAD = 9;
constexpr unsigned M_SRP_TK = 10;
constexpr unsigned M_SRP_LS = 11;
constexpr unsigned M_SRP_END = 12;
constexpr unsigned M_SLOT_AW = 13;

// event-router field order, likewise the wrap's port order
constexpr unsigned E_TKREG = 0;
constexpr unsigned E_TKUNR = 1;
constexpr unsigned E_DISC = 2;
constexpr unsigned E_DEP = 3;
constexpr unsigned E_DOMAIN = 4;
constexpr unsigned E_LSNCHG = 5;
constexpr unsigned E_GM = 6;
constexpr unsigned E_LINK = 7;
constexpr unsigned E_NSRC = 8;
constexpr unsigned E_SRCW = 9;

static unsigned clog2_of(unsigned v) {
  unsigned w = 0;
  while ((1u << w) < v) ++w;
  return w;
}

// one half-open interval of indices owned by one group
struct Grp {
  const char* name;
  unsigned base;
  unsigned count;
};


// ---- the suite ----------------------------------------------------------
// One object owns the model, the tally and the two shape indices the later
// phases read back, so every check below is a named member function rather
// than one `main` nobody can scope (Core Guidelines I.2, F.3).
namespace {
class TimerMapSuite {
 public:
  int run();

 private:
  void check_disjoint(const char* tag, const std::vector<Grp>& g);
  void check_slot_bases(const char* tag, unsigned si, unsigned so,
                        const uint32_t* m);
  void check_slot_groups_disjoint(const char* tag, unsigned si, unsigned so,
                                  const uint32_t* m);
  void check_map_fits_and_indexes(const char* tag, unsigned si,
                                  const uint32_t* m);
  void check_event_source_map(const char* tag, unsigned si, unsigned so,
                              const uint32_t* e);
  void check_owner_tags_disjoint(const char* tag, unsigned si, unsigned so,
                                 const uint32_t* m);
  void every_shape_matches_the_document();
  void the_shipping_8x8_shape_reproduces_the_historical_map();
  void the_9x9_shape_no_longer_aliases();
  void the_owner_tag_space_runs_out_where_documented();

  const milan::tb::Model<Vtimer_map_wrap> model;
  Vtimer_map_wrap* const d = model.get();
  int checks = 0;
  int fails = 0;
  int ix_8x8 = -1;   // the sweep names the two shapes phases 4 and 5 read
  int ix_9x9 = -1;
};
}  // namespace

// pairwise overlap over a group list — the property, not a spot check
void TimerMapSuite::check_disjoint(const char* tag, const std::vector<Grp>& g) {
  for (size_t i = 0; i < g.size(); ++i) {
    for (size_t j = i + 1; j < g.size(); ++j) {
      if (g[i].count == 0 || g[j].count == 0) { ++checks; continue; }
      bool ok = (g[i].base + g[i].count <= g[j].base)
                || (g[j].base + g[j].count <= g[i].base);
      CHECK(ok, "%s: %s [%u,%u) OVERLAPS %s [%u,%u)", tag,
            g[i].name, g[i].base, g[i].base + g[i].count,
            g[j].name, g[j].base, g[j].base + g[j].count);
    }
  }
}

// ---- 1. the F08.4 running sum, re-derived from the table ----------
void TimerMapSuite::check_slot_bases(const char* tag, unsigned si, unsigned so,
                                const uint32_t* m) {
  const unsigned e_adv    = 0;
  const unsigned e_noadp  = e_adv    + N_IF;
  const unsigned e_lstn   = e_noadp  + si;
  const unsigned e_tkr    = e_lstn   + si;
  const unsigned e_regmon = e_tkr    + so;
  const unsigned e_capool = e_regmon + 2 * N_CTRL * N_IF;
  const unsigned e_single = e_capool + CA_POOL;
  const unsigned e_maap   = e_single + SINGLETONS;
  const unsigned e_bend   = e_maap   + MAAP_SLOTS;
  const unsigned e_cad    = e_bend;
  const unsigned e_srptk  = e_cad    + SRP_CAD_SLOTS;
  const unsigned e_srpls  = e_srptk  + so;
  const unsigned e_end    = e_cad    + (SRP_CAD_SLOTS + si + so) * N_IF;

  CHECK(m[M_ADV]      == e_adv,    "%s adp_adv %u want %u",    tag, m[M_ADV], e_adv);
  CHECK(m[M_NOADP]    == e_noadp,  "%s adp_noadp %u want %u",  tag, m[M_NOADP], e_noadp);
  CHECK(m[M_LSTN]     == e_lstn,   "%s lstn %u want %u",       tag, m[M_LSTN], e_lstn);
  CHECK(m[M_TKR]      == e_tkr,    "%s tkr %u want %u",        tag, m[M_TKR], e_tkr);
  CHECK(m[M_REGMON]   == e_regmon, "%s regmon %u want %u",     tag, m[M_REGMON], e_regmon);
  CHECK(m[M_CAPOOL]   == e_capool, "%s capool %u want %u",     tag, m[M_CAPOOL], e_capool);
  CHECK(m[M_SINGLE]   == e_single, "%s single %u want %u",     tag, m[M_SINGLE], e_single);
  CHECK(m[M_MAAP]     == e_maap,   "%s maap %u want %u",       tag, m[M_MAAP], e_maap);
  CHECK(m[M_BASE_END] == e_bend,   "%s base_end %u want %u",   tag, m[M_BASE_END], e_bend);
  CHECK(m[M_SRP_CAD]  == e_cad,    "%s srp_cad %u want %u",    tag, m[M_SRP_CAD], e_cad);
  CHECK(m[M_SRP_TK]   == e_srptk,  "%s srp_tk %u want %u",     tag, m[M_SRP_TK], e_srptk);
  CHECK(m[M_SRP_LS]   == e_srpls,  "%s srp_ls %u want %u",     tag, m[M_SRP_LS], e_srpls);
  CHECK(m[M_SRP_END]  == e_end,    "%s srp_end %u want %u",    tag, m[M_SRP_END], e_end);
}

// ---- 2. pairwise disjointness of every SLOT group ------------------
void TimerMapSuite::check_slot_groups_disjoint(const char* tag, unsigned si, unsigned so,
                                          const uint32_t* m) {
  check_disjoint(tag, {
      {"adp_adv",   m[M_ADV],     N_IF},
      {"adp_noadp", m[M_NOADP],   si},
      {"lstn",      m[M_LSTN],    si},
      {"tkr",       m[M_TKR],     so},
      {"regmon",    m[M_REGMON],  2 * N_CTRL * N_IF},
      {"capool",    m[M_CAPOOL],  CA_POOL},
      {"single",    m[M_SINGLE],  SINGLETONS},
      {"maap",      m[M_MAAP],    MAAP_SLOTS},
      {"srp_cad",   m[M_SRP_CAD], SRP_CAD_SLOTS},
      {"srp_tk",    m[M_SRP_TK],  so},
      {"srp_ls",    m[M_SRP_LS],  si}});
}

// ---- 3. the map fits, and the index width can address it ----------
void TimerMapSuite::check_map_fits_and_indexes(const char* tag, unsigned si,
                                          const uint32_t* m) {
  CHECK(m[M_SRP_LS] + si <= m[M_SRP_END],
        "%s last group ends at %u past P-TIMER-SLOTS %u", tag,
        m[M_SRP_LS] + si, m[M_SRP_END]);
  CHECK(m[M_SLOT_AW] == clog2_of(m[M_SRP_END]),
        "%s slot width %u want %u", tag, m[M_SLOT_AW],
        clog2_of(m[M_SRP_END]));
  CHECK(m[M_SRP_END] <= (1u << m[M_SLOT_AW]),
        "%s %u slots cannot be indexed by %u bits", tag, m[M_SRP_END],
        m[M_SLOT_AW]);
}

// ---- 1b/2b. the 02 §5 event-router source map ---------------------
void TimerMapSuite::check_event_source_map(const char* tag, unsigned si, unsigned so,
                                      const uint32_t* e) {
  const unsigned f_reg  = 0;
  const unsigned f_unr  = f_reg  + si;
  const unsigned f_disc = f_unr  + si;
  const unsigned f_dep  = f_disc + 1;
  const unsigned f_dom  = f_dep  + 1;
  const unsigned f_lsn  = f_dom  + 1;
  const unsigned f_gm   = f_lsn  + so;
  const unsigned f_link = f_gm   + 1;
  const unsigned f_n    = f_link + 1;
  CHECK(e[E_TKREG]  == f_reg,  "%s evr tk_reg %u want %u",   tag, e[E_TKREG], f_reg);
  CHECK(e[E_TKUNR]  == f_unr,  "%s evr tk_unreg %u want %u", tag, e[E_TKUNR], f_unr);
  CHECK(e[E_DISC]   == f_disc, "%s evr adp_disc %u want %u", tag, e[E_DISC], f_disc);
  CHECK(e[E_DEP]    == f_dep,  "%s evr adp_dep %u want %u",  tag, e[E_DEP], f_dep);
  CHECK(e[E_DOMAIN] == f_dom,  "%s evr domain %u want %u",   tag, e[E_DOMAIN], f_dom);
  CHECK(e[E_LSNCHG] == f_lsn,  "%s evr lsn_chg %u want %u",  tag, e[E_LSNCHG], f_lsn);
  CHECK(e[E_GM]     == f_gm,   "%s evr gm %u want %u",       tag, e[E_GM], f_gm);
  CHECK(e[E_LINK]   == f_link, "%s evr link %u want %u",     tag, e[E_LINK], f_link);
  CHECK(e[E_NSRC]   == f_n,    "%s evr n_src %u want %u",    tag, e[E_NSRC], f_n);
  CHECK(e[E_SRCW]   == clog2_of(f_n), "%s evr src width %u want %u", tag,
        e[E_SRCW], clog2_of(f_n));
  check_disjoint(tag, {
      {"evr tk_reg",   e[E_TKREG],  si},
      {"evr tk_unreg", e[E_TKUNR],  si},
      {"evr adp_disc", e[E_DISC],   1},
      {"evr adp_dep",  e[E_DEP],    1},
      {"evr domain",   e[E_DOMAIN], 1},
      {"evr lsn_chg",  e[E_LSNCHG], so},
      {"evr gm_chg",   e[E_GM],     1},
      {"evr link",     e[E_LINK],   1}});
  // the ACMP listener decodes the event KIND by index range alone, so the
  // whole TK block must be one contiguous run ending at adp_dep
  CHECK(e[E_DEP] + 1 == e[E_DOMAIN],
        "%s TK block is not contiguous: dep %u, domain %u", tag,
        e[E_DEP], e[E_DOMAIN]);
}

// ---- 6. owner tags: disjoint at every shape the guard admits -------
// ADP publishes its SLOT as its owner tag, so its slot block is also an
// owner block. The listener/talker filter BY owner; SRP by slot but with
// owner bases that must not be mistaken for theirs.
void TimerMapSuite::check_owner_tags_disjoint(const char* tag, unsigned si, unsigned so,
                                         const uint32_t* m) {
  const bool own_ok = (m[M_LSTN] <= OWN_LSTN)
                      && (OWN_LSTN + si <= OWN_SRP_TK)
                      && (OWN_SRP_TK + so <= OWN_TKR)
                      && (OWN_TKR + so <= OWN_SRP_LS)
                      && (OWN_SRP_LS + si <= OWN_SRP_CAD)
                      && (OWN_SRP_CAD + SRP_CAD_SLOTS <= OWN_MAAP)
                      && (OWN_MAAP + MAAP_SLOTS <= OWN_SPACE);
  CHECK(own_ok, "%s owner tags overlap on the 8-bit expiry bus", tag);
  if (own_ok) {
    check_disjoint(tag, {
        {"own adp",     m[M_ADV],    m[M_LSTN]},
        {"own lstn",    OWN_LSTN,    si},
        {"own srp_tk",  OWN_SRP_TK,  so},
        {"own tkr",     OWN_TKR,     so},
        {"own srp_ls",  OWN_SRP_LS,  si},
        {"own srp_cad", OWN_SRP_CAD, SRP_CAD_SLOTS},
        {"own maap",    OWN_MAAP,    MAAP_SLOTS}});
  }
}

// The whole legal shape table, one pass per shape.
void TimerMapSuite::every_shape_matches_the_document() {
  d->eval();

  constexpr int N_SHAPE = 10;

  for (int g = 0; g < N_SHAPE; ++g) {
    const unsigned si = d->si_o[g];
    const unsigned so = d->so_o[g];
    char tag[64];
    snprintf(tag, sizeof tag, "SI=%u SO=%u", si, so);
    if (si == 8 && so == 8) ix_8x8 = g;
    if (si == 9 && so == 9) ix_9x9 = g;
    const uint32_t* m = &d->map_o[g][0];
    const uint32_t* e = &d->evr_o[g][0];

    check_slot_bases(tag, si, so, m);
    check_slot_groups_disjoint(tag, si, so, m);
    check_map_fits_and_indexes(tag, si, m);
    check_event_source_map(tag, si, so, e);
    check_owner_tags_disjoint(tag, si, so, m);
  }
}

// ---- 4. the shipping 8x8 shape reproduces the historical map --------
void TimerMapSuite::the_shipping_8x8_shape_reproduces_the_historical_map() {
  CHECK(ix_8x8 >= 0, "the 8x8 default shape is not in the table");
  if (ix_8x8 >= 0) {
    const uint32_t* m = &d->map_o[ix_8x8][0];
    // adp_adv..single are the historical literals that shipped and MUST NOT
    // move (landed engines' default parameters point at them); the MAAP
    // group (11) then EXTENDS the map — maap 66, base_end 68, and the SRP
    // block shifts up by exactly PP_MAAP_SLOTS_C = 2 (66/73/81/89 became
    // 68/75/83/91). Deliberate, documented in 08 SS5; this row is the record.
    constexpr unsigned want[13] = {0, 1, 9, 17, 25, 57, 61, 66, 68,
                                   68, 75, 83, 91};
    static constexpr const char* nm[13] = {
        "adp_adv", "adp_noadp", "lstn", "tkr", "regmon", "capool", "single",
        "maap", "base_end", "srp_cad", "srp_tk", "srp_ls", "srp_end"};
    for (int k = 0; k < 13; ++k)
      CHECK(m[k] == want[k], "8x8 %s moved: %u want %u (the documented map)",
            nm[k], m[k], want[k]);
    CHECK(m[M_SLOT_AW] == 7, "8x8 slot width %u want 7", m[M_SLOT_AW]);
    const uint32_t* e = &d->evr_o[ix_8x8][0];
    constexpr unsigned ewant[9] = {0, 8, 16, 17, 18, 19, 27, 28, 29};
    for (int k = 0; k < 9; ++k)
      CHECK(e[k] == ewant[k], "8x8 evr field %d moved: %u want %u", k,
            e[k], ewant[k]);
  }
}

// ---- 5. THE REGRESSION: the 9x9 shape the literals aliased ----------
void TimerMapSuite::the_9x9_shape_no_longer_aliases() {
  CHECK(ix_9x9 >= 0, "the 9x9 shape is not in the table");
  if (ix_9x9 >= 0) {
    const uint32_t* m = &d->map_o[ix_9x9][0];
    const uint32_t* e = &d->evr_o[ix_9x9][0];
    constexpr unsigned si = 9;
    constexpr unsigned so = 9;
    // the OLD literal map, written out so the collision is legible
    constexpr unsigned lit_lstn   = 9;
    constexpr unsigned lit_tkr    = 17;
    constexpr unsigned lit_srp_tk = 73;
    constexpr unsigned lit_srp_ls = 81;
    constexpr unsigned lit_unr    = 8;
    constexpr unsigned lit_disc   = 16;
    // the premise: with the literals, these three pairs SHARED an index
    CHECK(lit_lstn + (si - 1) == lit_tkr,
          "premise: literal listener sink 8 landed on the talker base");
    CHECK(lit_srp_tk + (so - 1) == lit_srp_ls,
          "premise: literal SRP talker 8 landed on the SRP listener base");
    CHECK(lit_unr + (si - 1) == lit_disc,
          "premise: literal event TK_ATTR_UNREGISTERED{8} landed on "
          "ADP EVT_TK_DISCOVERED");
    CHECK(m[M_LSTN] + si <= m[M_TKR],
          "9x9 listener sink %u (slot %u) still collides with the talker "
          "base %u — a SILENTLY LOST deadline", si - 1, m[M_LSTN] + si - 1,
          m[M_TKR]);
    CHECK(m[M_SRP_TK] + so <= m[M_SRP_LS],
          "9x9 SRP talker %u (slot %u) still collides with the SRP listener "
          "base %u — a MISDELIVERED expiry", so - 1, m[M_SRP_TK] + so - 1,
          m[M_SRP_LS]);
    CHECK(e[E_TKUNR] + si <= e[E_DISC],
          "9x9 event TK_ATTR_UNREGISTERED{%u} (source %u) still collides "
          "with ADP EVT_TK_DISCOVERED at %u", si - 1, e[E_TKUNR] + si - 1,
          e[E_DISC]);
    // and the whole 9x9 map still fits an addressable timer
    CHECK(m[M_SRP_END] == 96, "9x9 P-TIMER-SLOTS %u want 96", m[M_SRP_END]);
    CHECK(m[M_SLOT_AW] == 7, "9x9 slot width %u want 7", m[M_SLOT_AW]);
    CHECK(e[E_NSRC] == 32, "9x9 event sources %u want 32", e[E_NSRC]);
  }
}

// ---- 6b. where the owner-tag space runs out (named, not guessed) ----
// The talker owner base is 0x50 and SRP's listener base 0x60, so 16 is the
// last legal P-N-STREAM-OUT; the listener base is 0x20 and ADP publishes
// its slot as its owner, so IF + SI must stay under 0x20.
void TimerMapSuite::the_owner_tag_space_runs_out_where_documented() {
  CHECK(OWN_SRP_CAD + SRP_CAD_SLOTS <= OWN_MAAP,
        "the SRP cadence tags must stay under the MAAP tags");
  CHECK(OWN_MAAP + MAAP_SLOTS <= OWN_SPACE, "the MAAP tags must fit the bus");
  CHECK(OWN_TKR + 16 <= OWN_SRP_LS, "16 sources must be legal");
  CHECK(OWN_TKR + 17 > OWN_SRP_LS, "17 sources must be the first refused");
  CHECK(N_IF + 31 <= OWN_LSTN, "31 sinks must fit under the listener tags");
  CHECK(N_IF + 32 > OWN_LSTN, "32 sinks must be the first refused by ADP");
}

int TimerMapSuite::run() {
  every_shape_matches_the_document();
  the_shipping_8x8_shape_reproduces_the_historical_map();
  the_9x9_shape_no_longer_aliases();
  the_owner_tag_space_runs_out_where_documented();

  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  TimerMapSuite suite;
  return suite.run();
}
