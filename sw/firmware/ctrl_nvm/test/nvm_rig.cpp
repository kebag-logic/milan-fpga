// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// nvm_rig.cpp - the scenario rig (see nvm_rig.hpp): the runner of the
// hand-rolled suite (test/nvm_test.c), word for word, run in the test's own
// process.
//
// --powercut is the one loop that runs here rather than in a test: for every
// media effect of one commit (the erase and each page program) and four
// points inside it, the power fails, the board boots again and the restored
// values must be the old set or the new set exactly; then a change must
// commit and boot back, so the store recovers from every cut.

#include "nvm_rig.hpp"

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iterator>

#include "nvm_c.hpp"

namespace nvm_test {

namespace {

constexpr std::uint64_t kLoopUs = 100u;           // the event loop's own time per iteration
constexpr std::uint64_t kIdleLimitUs = 60000000u;  // the longest a run waits to go idle
constexpr std::uint32_t kJournal = 2u * NVM_SLOT_BYTES;
constexpr unsigned kTimes = 16u;                   // failure and commit times kept per run

struct Knobs {
    std::string boot_fault;  // a flash-model fault armed at power on
    bool not_ready = false;
    bool apply_fault = false;
    unsigned apply_fault_id = 0;
    bool settle_fault = false;
    bool rollback_fault = false;
    bool unbind_fault = false;
    std::vector<unsigned> refuse;
};

// One run's state: the runner's static `t`, which a process started afresh.
struct Rig {
    const nvm_flash* port = &nvm_fmodel_port;
    Knobs knobs;
    std::uint64_t max_call_us = 0;
    unsigned max_polls_call = 0;
    unsigned service_calls = 0;
    unsigned commit_tries = 0;
    unsigned commit_refused = 0;
    unsigned bad = 0;
    Result run;
    Bytes snapshot;
    Bytes new_image;  // the reference commit's container
    std::uint32_t new_slot = 0;
    std::vector<State> states;  // the power-cut enumeration's state snapshots 0, 1 and 2
};

Rig* rig;

void fail(const char* what, unsigned a, unsigned b) {
    char line[160];
    std::snprintf(line, sizeof line, "FAIL %s %u %u", what, a, b);
    rig->run.fails.emplace_back(line);
    rig->bad++;
}

void note(std::vector<std::uint64_t>& times) {
    if (times.size() < kTimes) {
        times.push_back(nvm_fmodel_now_us());
    }
}

// ---- power, boot and the event loop -----------------------------------------

void power_on() {
    nvm_fmodel_power_on();
    nvm_fmodel_window(NVM_SLOT_A, NVM_SLOT_A + kJournal);
    litespi_model_reset();
    nvm_flash_litespi_power_on();
    nvm_smodel_reset();
}

void fault_arg(const std::string& arg);

void boot() {
    power_on();
    if (!rig->knobs.boot_fault.empty()) {
        fault_arg(rig->knobs.boot_fault);
    }
    nvm_smodel_ready(rig->knobs.not_ready ? 0 : 1);
    if (rig->knobs.apply_fault) {
        nvm_smodel_fault_apply(rig->knobs.apply_fault_id);
    }
    nvm_smodel_fault_settle(rig->knobs.settle_fault ? 1 : 0);
    if (rig->knobs.rollback_fault) {
        nvm_smodel_fault_rollback(NVM_W_D3);
    }
    if (rig->knobs.unbind_fault) {
        nvm_smodel_fault_rollback(NVM_W_BIND);
    }
    for (const unsigned id : rig->knobs.refuse) {
        nvm_smodel_refuse(id);
    }
    nvm_store_boot(rig->port, &nvm_smodel_port);
}

void service() {
    const std::uint64_t before = nvm_fmodel_now_us();
    const unsigned polls = nvm_fmodel_count()->busy_polls;
    const unsigned failed = nvm_store_status()->commits_failed;
    const unsigned ok = nvm_store_status()->commits_ok;
    nvm_store_service();
    if (nvm_store_status()->commits_failed != failed) {
        note(rig->run.fail_at);
    }
    if (nvm_store_status()->commits_ok != ok) {
        note(rig->run.ok_at);
    }
    if (nvm_fmodel_now_us() - before > rig->max_call_us) {
        rig->max_call_us = nvm_fmodel_now_us() - before;
    }
    if (nvm_fmodel_count()->busy_polls - polls > rig->max_polls_call) {
        rig->max_polls_call = nvm_fmodel_count()->busy_polls - polls;
    }
    nvm_fmodel_advance_us(kLoopUs);
    rig->service_calls++;
}

void run_ms(std::uint64_t ms) {
    const std::uint64_t until = nvm_fmodel_now_us() + ms * 1000u;
    while (nvm_fmodel_now_us() < until && !nvm_fmodel_dead()) {
        service();
    }
}

// Nothing left to do: no writer, a held one, or no change waits and what is
// in flight is written or has spent its attempts.
bool settled() {
    const nvm_status* s = nvm_store_status();
    return s->phase == NVM_P_OFF || s->phase == NVM_P_HELD ||
           (s->phase == NVM_P_IDLE && !s->dirty && (!s->pending || s->exhausted));
}

void until_idle() {
    const std::uint64_t until = nvm_fmodel_now_us() + kIdleLimitUs;
    do {
        service();
    } while (!settled() && nvm_fmodel_now_us() < until && !nvm_fmodel_dead());
}

// Serve until the write path reaches phase p.
void until_phase(unsigned p) {
    const std::uint64_t until = nvm_fmodel_now_us() + kIdleLimitUs;
    while (static_cast<unsigned>(nvm_store_status()->phase) != p && nvm_fmodel_now_us() < until &&
           !nvm_fmodel_dead()) {
        service();
    }
    if (static_cast<unsigned>(nvm_store_status()->phase) != p) {
        fail("phase_not_reached", p, static_cast<unsigned>(nvm_store_status()->phase));
    }
}

// ---- changes -------------------------------------------------------------------

void set(unsigned id, const std::uint8_t* value, unsigned len) {
    const nvm_rec r = nvm_rec_by_id(id);
    if (!r.ok) {
        fail("set_unknown_record", id, 0);
        return;
    }
    nvm_smodel_set(id, value, len < r.plen ? len : r.plen);
    nvm_store_changed(r.group, r.index);
}

// Every record (all) or the first of each group, payload byte j of record
// id = id * 131 + j * 17 + seed: the arithmetic rule of nvm_klj2.py's
// payload_bytes at seed 0, the rule the recorded vectors are made with.
void set_pattern(unsigned seed, bool all) {
    std::uint8_t payload[NVM_PAYLOAD_MAX];
    for (nvm_rec r = nvm_rec_first(); r.ok; r = nvm_rec_next(r)) {
        if (all || r.index == 0u) {
            for (unsigned j = 0; j < r.plen; ++j) {
                payload[j] = static_cast<std::uint8_t>(r.id * 131u + j * 17u + seed);
            }
            set(r.id, payload, r.plen);
        }
    }
}

// ---- the power-cut enumeration ---------------------------------------------

State capture_state() {
    State st;
    for (nvm_rec r = nvm_rec_first(); r.ok; r = nvm_rec_next(r)) {
        const std::uint8_t* v = nvm_smodel_value(r.id);
        st[r.id] = Record{nvm_smodel_valid(r.id), Bytes(v, v + r.plen)};
    }
    return st;
}

void restore_snapshot() { std::memcpy(nvm_fmodel_mem + NVM_SLOT_A, rig->snapshot.data(), kJournal); }

void protect_auth() {
    const int auth = nvm_store_status()->auth;
    nvm_fmodel_protect(auth < 0 ? 0u : (auth != 0 ? NVM_SLOT_B : NVM_SLOT_A));
}

// The reference commit: the old state (0), the new one (1), and how many
// media effects one commit has.
unsigned reference() {
    restore_snapshot();
    boot();
    rig->states.assign(3, State{});
    rig->states[0] = capture_state();
    set_pattern(0x33u, false);
    until_idle();
    const unsigned effects = nvm_fmodel_count()->effects;
    if (nvm_store_status()->commits_ok != 1u) {
        fail("powercut_reference_commit", nvm_store_status()->commits_ok, 1);
    }
    rig->new_slot = nvm_store_status()->auth != 0 ? NVM_SLOT_B : NVM_SLOT_A;
    rig->new_image.assign(nvm_fmodel_mem + rig->new_slot, nvm_fmodel_mem + rig->new_slot + NVM_IMG_LEN);
    boot();
    rig->states[1] = capture_state();
    if (rig->states[1] == rig->states[0]) {
        fail("powercut_reference_vacuous", 0, 0);
    }
    return effects;
}

// After a cut: the board boots the old set, or the new set when the new
// container reached the media whole (strictly the new set once every effect
// landed), never a mix; then the next change commits.
bool after_cut(bool whole, unsigned* old, unsigned* new_set) {
    const bool complete = std::memcmp(nvm_fmodel_mem + rig->new_slot, rig->new_image.data(), NVM_IMG_LEN) == 0;
    boot();
    const State now = capture_state();
    if (now == rig->states[1] && complete) {
        (*new_set)++;
    } else if (now == rig->states[0] && !whole) {
        (*old)++;
    } else {
        return false;
    }
    set_pattern(0x77u, false);
    until_idle();
    if (nvm_store_status()->commits_ok != 1u || nvm_store_status()->stale) {
        return false;
    }
    rig->states[2] = capture_state();
    boot();
    return capture_state() == rig->states[2] && nvm_store_status()->terminal == NVM_T_COMPLETE;
}

// One cut: the commit of state 1 with the power failing in effect k.
bool one_cut(unsigned k, unsigned frac, unsigned* old, unsigned* new_set) {
    restore_snapshot();
    boot();
    protect_auth();
    if (k != 0u) {
        nvm_fmodel_cut(k, frac);
    }
    set_pattern(0x33u, false);
    if (k != 0u) {
        until_idle();
    } else {
        // every effect landed; the power fails during the read-back
        while (nvm_store_status()->phase != NVM_P_VERIFY && !settled()) {
            service();
        }
    }
    if (nvm_fmodel_count()->protected_hit || nvm_fmodel_count()->outside) {
        return false;
    }
    return after_cut(k == 0u, old, new_set);
}

void powercut() {
    static constexpr unsigned kFracs[4] = {0u, 1u, 128u, 255u};
    unsigned cases = 0;
    unsigned old = 0;
    unsigned new_set = 0;
    unsigned bad = 0;
    rig->snapshot.assign(nvm_fmodel_mem + NVM_SLOT_A, nvm_fmodel_mem + NVM_SLOT_A + kJournal);
    const unsigned effects = reference();
    for (unsigned k = 0; k <= effects; ++k) {
        for (unsigned f = 0; f < 4u && (k != 0u || f == 0u); ++f) {
            cases++;
            if (!one_cut(k, kFracs[f], &old, &new_set)) {
                char line[96];
                std::snprintf(line, sizeof line, "POWERCUT-BAD effect=%u frac=%u", k, kFracs[f]);
                rig->run.fails.emplace_back(line);
                bad++;
            }
        }
    }
    rig->run.powercut = {{"effects", effects}, {"cases", cases}, {"old", old}, {"new", new_set}, {"bad", bad}};
    restore_snapshot();
}

// ---- files and the guard --------------------------------------------------------

void load(Files& files, const std::string& name, std::uint32_t slot) {
    const auto it = files.blobs.find(name);
    if (it == files.blobs.end()) {
        fail(("no file " + name).c_str(), 0, 0);
        return;
    }
    std::memset(nvm_fmodel_mem + slot, 0xff, NVM_SLOT_BYTES);
    const std::size_t n = it->second.size() < NVM_SLOT_BYTES ? it->second.size() : NVM_SLOT_BYTES;
    std::memcpy(nvm_fmodel_mem + slot, it->second.data(), n);
}

void dump(Files& files, const std::string& name, const std::uint8_t* src, std::size_t n) {
    files.blobs[name] = Bytes(src, src + n);
}

// The port refuses to program or erase outside the journal: the first block
// of the device holds the bitstream.
void port_guard() {
    static constexpr std::uint8_t kPage[4] = {0u, 0u, 0u, 0u};
    long long took = 0;
    nvm_fmodel_window(0u, NVM_FMODEL_BYTES);
    took += rig->port->erase(rig->port->ctx, 0u) == 0;
    took += rig->port->program(rig->port->ctx, 0u, kPage, sizeof kPage) == 0;
    took += rig->port->erase(rig->port->ctx, NVM_SLOT_A - 1u) == 0;
    took += rig->port->program(rig->port->ctx, NVM_SLOT_A + 2u * NVM_SLOT_BYTES, kPage, sizeof kPage) == 0;
    nvm_fmodel_window(NVM_SLOT_A, NVM_SLOT_A + kJournal);
    rig->run.guard = took;
}

// ---- the script --------------------------------------------------------------

int hex_digit(char c) {
    if (c >= '0' && c <= '9') {
        return c - '0';
    }
    if (c >= 'a' && c <= 'f') {
        return c - 'a' + 10;
    }
    return (c >= 'A' && c <= 'F') ? c - 'A' + 10 : -1;
}

unsigned long number(const char* text, char** end) { return std::strtoul(text, end, 0); }

// ID:HEX, the new payload of one record.
void set_arg(const std::string& arg) {
    std::uint8_t payload[NVM_PAYLOAD_MAX];
    char* end = nullptr;
    const unsigned long id = number(arg.c_str(), &end);
    unsigned n = 0;
    const char* hex = (end != nullptr && *end == ':') ? end + 1 : "";
    while (hex[0] != '\0' && hex[1] != '\0' && n < NVM_PAYLOAD_MAX) {
        const int hi = hex_digit(hex[0]);
        const int lo = hex_digit(hex[1]);
        if (hi < 0 || lo < 0) {
            break;
        }
        payload[n++] = static_cast<std::uint8_t>((hi << 4) | lo);
        hex += 2;
    }
    set(static_cast<unsigned>(id), payload, n);
}

// The name at the head of MODE[:...] in names, or -1.
int name_of(const std::string& arg, const std::vector<std::string>& names) {
    const std::string head = arg.substr(0, arg.find(':'));
    for (std::size_t i = 0; i < names.size(); ++i) {
        if (names[i] == head) {
            return static_cast<int>(i);
        }
    }
    fail("unknown_mode", 0, 0);
    return -1;
}

// The numbers after MODE: COUNT (1 unless given), then SKIP and a last one.
void fields(const std::string& arg, unsigned long* v) {
    v[0] = 1u;
    v[1] = 0u;
    v[2] = 0u;
    const std::size_t colon = arg.find(':');
    const char* p = colon == std::string::npos ? nullptr : arg.c_str() + colon;
    for (unsigned i = 0; i < 3u && p != nullptr && *p == ':'; ++i) {
        char* end = nullptr;
        v[i] = number(p + 1, &end);
        p = end;
    }
}

// MODE[:COUNT[:SKIP[:AT]]]: arm a flash-model fault; AT places erase-stuck,
// read-fail-at, read-flip-at and read-vary-at.
void fault_arg(const std::string& arg) {
    static const std::vector<std::string> kNames = {
        "none",      "erase-hang",   "erase-stuck", "program-hang", "program-drop",   "program-flip", "read-fail",
        "read-flip", "read-flip-at", "read-alias",  "program-refuse", "erase-refuse", "read-fail-at", "read-vary-at",
    };
    unsigned long v[3];
    const int i = name_of(arg, kNames);
    fields(arg, v);
    if (i < 0) {
        return;
    }
    nvm_fmodel_fault(static_cast<nvm_fault>(i), static_cast<unsigned>(v[0]), static_cast<unsigned>(v[1]));
    if (v[2] != 0u) {
        nvm_fmodel_fault_at(static_cast<std::uint32_t>(v[2]));
    }
}

// KIND[:COUNT[:SKIP[:POLLS]]]: arm a command-master stall.
void stall_arg(const std::string& arg) {
    static const std::vector<std::string> kNames = {"none", "tx", "rx", "drain"};
    unsigned long v[3];
    const int i = name_of(arg, kNames);
    fields(arg, v);
    if (i >= 0) {
        litespi_model_stall(static_cast<litespi_stall>(i), static_cast<unsigned>(v[0]), static_cast<unsigned>(v[1]),
                            static_cast<unsigned>(v[2]));
    }
}

void flip_arg(const std::string& arg) {
    char* end = nullptr;
    const unsigned long addr = number(arg.c_str(), &end);
    const unsigned long bit = (end != nullptr && *end == ':') ? number(end + 1, nullptr) : 0u;
    nvm_fmodel_flip(static_cast<std::uint32_t>(addr), static_cast<unsigned>(bit));
}

void times_arg(const std::string& arg) {
    char* end = nullptr;
    const unsigned long erase_ms = number(arg.c_str(), &end);
    const unsigned long program_us = (end != nullptr && *end == ':') ? number(end + 1, nullptr) : 1000u;
    nvm_fmodel_times(static_cast<std::uint64_t>(erase_ms) * 1000u, program_us);
}

// A console commit: start one now and run until it settles.
void commit() {
    if (nvm_store_commit_now() == 0) {
        fail("commit_not_started", static_cast<unsigned>(nvm_store_status()->phase), 0);
    }
    until_idle();
}

// A console commit that may be refused: count the try and its answer.
void commit_try() {
    rig->commit_tries++;
    if (nvm_store_commit_now() == 0) {
        rig->commit_refused++;
    }
}

// GROUP:INDEX, nvm_store_changed() as a caller may call it: for a group or
// an index the shape has no record of too.
void change_arg(const std::string& arg) {
    char* end = nullptr;
    const unsigned long group = number(arg.c_str(), &end);
    const unsigned long index = (end != nullptr && *end == ':') ? number(end + 1, nullptr) : 0u;
    nvm_store_changed(static_cast<unsigned>(group), static_cast<unsigned>(index));
}

// A change that leaves the value as it was (DR2b).
void touch_arg(const std::string& arg) {
    const nvm_rec r = nvm_rec_by_id(static_cast<unsigned>(number(arg.c_str(), nullptr)));
    nvm_store_changed(r.group, r.index);
}

// One script word with no argument.
bool word(const std::string& a) {
    if (a == "--litespi") {
        rig->port = &nvm_flash_litespi;
    } else if (a == "--not-ready") {
        rig->knobs.not_ready = true;
    } else if (a == "--settle-fault") {
        rig->knobs.settle_fault = true;
    } else if (a == "--rollback-fault") {
        rig->knobs.rollback_fault = true;
    } else if (a == "--unbind-fault") {
        rig->knobs.unbind_fault = true;
    } else if (a == "--commit-try") {
        commit_try();
    } else if (a == "--mark") {
        rig->run.marks.push_back(nvm_fmodel_now_us());
    } else if (a == "--clock") {
        rig->run.clocks.emplace_back(rig->port->now_us(rig->port->ctx), nvm_fmodel_now_us());
    } else if (a == "--boot") {
        boot();
    } else if (a == "--blank") {
        nvm_fmodel_blank();
    } else if (a == "--until-idle") {
        until_idle();
    } else if (a == "--commit") {
        commit();
    } else if (a == "--protect-auth") {
        protect_auth();
    } else if (a == "--powercut") {
        powercut();
    } else if (a == "--port-guard") {
        port_guard();
    } else {
        return false;
    }
    return true;
}

// One script word with its argument.
bool word_arg(const std::string& a, const std::string& v, Files& files) {
    if (a == "--slot-a") {
        load(files, v, NVM_SLOT_A);
    } else if (a == "--slot-b") {
        load(files, v, NVM_SLOT_B);
    } else if (a == "--times") {
        times_arg(v);
    } else if (a == "--refuse") {
        rig->knobs.refuse.push_back(static_cast<unsigned>(number(v.c_str(), nullptr)));
    } else if (a == "--apply-fault") {
        rig->knobs.apply_fault = true;
        rig->knobs.apply_fault_id = static_cast<unsigned>(number(v.c_str(), nullptr));
    } else if (a == "--until-phase") {
        until_phase(static_cast<unsigned>(number(v.c_str(), nullptr)));
    } else if (a == "--phc-step") {
        litespi_model_phc_step(static_cast<std::int64_t>(std::strtoll(v.c_str(), nullptr, 0)));
    } else if (a == "--ls-stall") {
        stall_arg(v);
    } else if (a == "--set") {
        set_arg(v);
    } else if (a == "--set-pattern") {
        set_pattern(static_cast<unsigned>(number(v.c_str(), nullptr)), true);
    } else if (a == "--touch") {
        touch_arg(v);
    } else if (a == "--change") {
        change_arg(v);
    } else if (a == "--service") {
        for (unsigned long k = number(v.c_str(), nullptr); k > 0u; --k) {
            service();
        }
    } else if (a == "--run-ms") {
        run_ms(std::strtoull(v.c_str(), nullptr, 0));
    } else if (a == "--fault") {
        fault_arg(v);
    } else if (a == "--boot-fault") {
        rig->knobs.boot_fault = v;
    } else if (a == "--flip") {
        flip_arg(v);
    } else if (a == "--dump-slot-a") {
        dump(files, v, nvm_fmodel_mem + NVM_SLOT_A, NVM_SLOT_BYTES);
    } else if (a == "--dump-slot-b") {
        dump(files, v, nvm_fmodel_mem + NVM_SLOT_B, NVM_SLOT_BYTES);
    } else if (a == "--dump-stage") {
        dump(files, v, nvm_store_stage(), NVM_IMG_LEN);
    } else if (a == "--dump-state") {
        files.states[v] = capture_state();
    } else {
        return false;
    }
    return true;
}

// The summary under the runner's names (its SUMMARY lines).
void summarise() {
    const nvm_status* s = nvm_store_status();
    const struct nvm_fmodel_count* fc = nvm_fmodel_count();
    const struct nvm_smodel_count* sc = nvm_smodel_count();
    const struct litespi_model_count* lc = litespi_model_count();
    rig->run.s = {
        {"terminal", s->terminal}, {"cause", s->cause}, {"vd_a", s->verdict_a}, {"vd_b", s->verdict_b},
        {"last", s->last_verdict}, {"first", s->first_failed}, {"seq_a", s->seq_a}, {"seq_b", s->seq_b},
        {"seq", s->seq}, {"auth", s->auth}, {"applied", s->applied}, {"refused", s->refused},
        {"blank", s->blank}, {"releases", s->releases}, {"ok", s->commits_ok}, {"failed", s->commits_failed},
        {"skipped", s->commits_skipped}, {"attempts", s->attempts}, {"exhausted", s->exhausted},
        {"stale", s->stale}, {"dirty", s->dirty}, {"pending", s->pending}, {"phase", s->phase},
        {"step_max", s->step_bytes_max}, {"step_bound", NVM_STEP_BOUND}, {"steps", s->steps},
        {"bind_terminal", s->bind_terminal}, {"bind_cause", s->bind_cause}, {"withheld", s->withheld},
        {"abandoned", s->abandoned}, {"abandoned_vd", s->abandoned_vd}, {"unread", s->unread},
        {"read_faults", s->read_faults}, {"erases", fc->erases}, {"programs", fc->programs},
        {"effects", fc->effects}, {"outside", fc->outside}, {"protected", fc->protected_hit},
        {"pagewrap", fc->pagewrap}, {"while_busy", fc->while_busy}, {"descending", fc->descending},
        {"sm_applies", sc->applies}, {"sm_applied", sc->applied}, {"sm_refused", sc->refused},
        {"sm_settles", sc->settles}, {"sm_rollbacks", sc->rollbacks}, {"sm_unbinds", sc->unbinds},
        {"sm_releases", sc->releases}, {"sm_order", sc->order}, {"ls_wren", lc->wren}, {"ls_pp", lc->pp},
        {"ls_se", lc->se}, {"ls_no_wel", lc->no_wel}, {"ls_short", lc->short_cmd}, {"ls_refused", lc->refused},
        {"ls_unknown", lc->unknown}, {"ls_stalled", lc->stalled}, {"ls_max_withheld", lc->max_withheld},
        {"ls_hung", lc->hung}, {"max_call_us", static_cast<long long>(rig->max_call_us)},
        {"max_polls_call", rig->max_polls_call}, {"calls", rig->service_calls},
        {"now_ms", static_cast<long long>(nvm_fmodel_now_us() / 1000u)}, {"commit_tries", rig->commit_tries},
        {"commit_refused", rig->commit_refused}, {"img_len", NVM_IMG_LEN}, {"n_rec", NVM_N_REC},
        {"clock_hz", CONFIG_CLOCK_FREQUENCY}, {"ls_call_ticks", nvm_flash_litespi_call_ticks}, {"bad", rig->bad},
    };
    for (unsigned i = 0; i < fc->erases && i < 16u; ++i) {
        rig->run.erases.push_back(fc->erase_start_us[i]);
    }
}

}  // namespace

long long Result::at(const char* key) const {
    const auto it = s.find(key);
    return it == s.end() ? -999999 : it->second;
}

std::string Result::text() const {
    std::string out = "{";
    for (const auto& [key, value] : s) {
        out += (out.size() > 1 ? ", '" : "'") + key + "': " + std::to_string(value);
    }
    return out + "}";
}

Result run_script(const std::vector<std::string>& words, Files& files) {
    Rig state;
    rig = &state;
    // as the runner's main() began: power on, blank media, a fresh state model
    nvm_fmodel_power_on();
    nvm_fmodel_blank();
    nvm_smodel_reset();
    litespi_model_reset();
    for (std::size_t i = 0; i < words.size(); ++i) {
        if (word(words[i])) {
            continue;
        }
        if (i + 1 < words.size() && word_arg(words[i], words[i + 1], files)) {
            ++i;
            continue;
        }
        fail(("unknown or incomplete script word " + words[i]).c_str(), 0, 0);
        break;
    }
    summarise();
    rig = nullptr;
    return state.run;
}

}  // namespace nvm_test
