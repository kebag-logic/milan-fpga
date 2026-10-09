// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// nvm_suite.cpp - see nvm_suite.hpp.
//
// The fixture directory holds manifest.txt, one entry per line:
//
//     num NAME VALUE
//     list NAME VALUE...
//     blob NAME FILE            the file's bytes
//     payloads NAME FILE        records of [id u8][length u16 LE][payload]
//     text NAME WORDS...        a label, the rest of the line
//
// written by nvm_fixture.py. A missing directory or entry fails every test
// that asks for it, never passes one.

#include "nvm_suite.hpp"

#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iterator>
#include <sstream>

#include "nvm_c.hpp"

namespace nvm_test {

namespace {

Bytes read_file(const std::string& path, std::string* error) {
    std::ifstream in(path, std::ios::binary);
    if (!in) {
        *error = "cannot read " + path;
        return {};
    }
    return Bytes(std::istreambuf_iterator<char>(in), std::istreambuf_iterator<char>());
}

Payloads decode_payloads(const Bytes& raw) {
    Payloads out;
    std::size_t at = 0;
    while (at + 3u <= raw.size()) {
        const unsigned rid = raw[at];
        const std::size_t n = raw[at + 1u] | (static_cast<std::size_t>(raw[at + 2u]) << 8);
        at += 3u;
        out[rid] = Bytes(raw.begin() + static_cast<std::ptrdiff_t>(at),
                         raw.begin() + static_cast<std::ptrdiff_t>(at + n));
        at += n;
    }
    return out;
}

// The longest service call of every run, in model time: with no stall armed,
// and with a command-master stall. Printed once the binary ends, as evidence.
struct CallMax {
    long long nominal = 0;
    long long stalled = 0;
};

CallMax call_max;

class CallMaxReport final : public ::testing::Environment {
 public:
    void TearDown() override {
        std::printf("  longest service call, model time: %lld us with no stall armed, %lld us with a "
                    "command-master stall\n",
                    call_max.nominal, call_max.stalled);
    }
};

// GoogleTest takes ownership of a registered environment (its documented API).
::testing::Environment* const call_max_report = ::testing::AddGlobalTestEnvironment(new CallMaxReport);

std::vector<std::string> contract(const Result& r, const std::vector<std::string>& allow) {
    static const char* const kZero[] = {"outside",   "protected", "pagewrap", "while_busy", "descending", "sm_order",
                                        "bad",       "ls_no_wel", "ls_short", "ls_refused", "ls_unknown", "ls_hung"};
    std::vector<std::string> found;
    for (const char* key : kZero) {
        const bool allowed = std::find(allow.begin(), allow.end(), key) != allow.end();
        if (!allowed && r.at(key) != 0) {
            found.push_back(std::string("invariant ") + key + "=" + std::to_string(r.at(key)));
        }
    }
    if (r.at("step_max") > r.at("step_bound")) {
        found.push_back("invariant step_max=" + std::to_string(r.at("step_max")) +
                        " > step_bound=" + std::to_string(r.at("step_bound")));
    }
    const long long bound = r.at("ls_stalled") != 0 ? kCallBoundUs : kNominalCallUs;
    if (r.at("max_call_us") > bound) {
        found.push_back("invariant max_call_us=" + std::to_string(r.at("max_call_us")) + " > " +
                        std::to_string(bound));
    }
    for (const std::string& line : r.fails) {
        found.push_back("runner " + line);
    }
    return found;
}

}  // namespace

const Fixture& Fixture::get() {
    static const Fixture loaded = [] {
        Fixture f;
        const char* dir = std::getenv("NVM_FIXTURE");
        if (dir == nullptr) {
            f.error_ = "NVM_FIXTURE names no fixture directory";
            return f;
        }
        std::ifstream manifest(std::string(dir) + "/manifest.txt");
        if (!manifest) {
            f.error_ = std::string("no manifest.txt in ") + dir;
            return f;
        }
        std::string line;
        while (std::getline(manifest, line)) {
            std::istringstream words(line);
            std::string kind;
            std::string name;
            words >> kind >> name;
            if (kind == "num") {
                words >> f.nums_[name];
            } else if (kind == "list") {
                long long v = 0;
                std::vector<long long>& out = f.lists_[name];
                while (words >> v) {
                    out.push_back(v);
                }
            } else if (kind == "text") {
                std::getline(words >> std::ws, f.texts_[name]);
            } else if (kind == "blob" || kind == "payloads") {
                std::string file;
                words >> file;
                const Bytes raw = read_file(std::string(dir) + "/" + file, &f.error_);
                if (kind == "blob") {
                    f.blobs_[name] = raw;
                } else {
                    f.payloads_[name] = decode_payloads(raw);
                }
            }
        }
        return f;
    }();
    return loaded;
}

const Bytes& Fixture::blob(const std::string& name) const {
    static const Bytes kNone;
    const auto it = blobs_.find(name);
    if (it == blobs_.end()) {
        ADD_FAILURE() << "the fixture holds no blob " << name << " " << error_;
        return kNone;
    }
    return it->second;
}

long long Fixture::num(const std::string& name) const {
    const auto it = nums_.find(name);
    if (it == nums_.end()) {
        ADD_FAILURE() << "the fixture holds no number " << name << " " << error_;
        return 0;
    }
    return it->second;
}

const std::vector<long long>& Fixture::list(const std::string& name) const {
    static const std::vector<long long> kNone;
    const auto it = lists_.find(name);
    if (it == lists_.end()) {
        ADD_FAILURE() << "the fixture holds no list " << name << " " << error_;
        return kNone;
    }
    return it->second;
}

const Payloads& Fixture::payloads(const std::string& name) const {
    static const Payloads kNone;
    const auto it = payloads_.find(name);
    if (it == payloads_.end()) {
        ADD_FAILURE() << "the fixture holds no payload set " << name << " " << error_;
        return kNone;
    }
    return it->second;
}

const std::string& Fixture::text(const std::string& name) const {
    static const std::string kNone;
    const auto it = texts_.find(name);
    if (it == texts_.end()) {
        ADD_FAILURE() << "the fixture holds no text " << name << " " << error_;
        return kNone;
    }
    return it->second;
}

Files Fixture::files(const std::map<std::string, std::string>& as) const {
    Files out;
    for (const auto& [script_name, blob_name] : as) {
        out.blobs[script_name] = blob(blob_name);
    }
    return out;
}

std::vector<unsigned> rids() {
    std::vector<unsigned> out;
    for (const long long rid : fx().list("rids")) {
        out.push_back(static_cast<unsigned>(rid));
    }
    return out;
}

unsigned plen(unsigned rid) {
    const std::vector<long long>& ids = fx().list("rids");
    const std::vector<long long>& lens = fx().list("plens");
    for (std::size_t k = 0; k < ids.size() && k < lens.size(); ++k) {
        if (ids[k] == rid) {
            return static_cast<unsigned>(lens[k]);
        }
    }
    ADD_FAILURE() << "the shape has no record " << rid;
    return 0;
}

Result go(Port port, Files& files, std::vector<std::string> words, const std::vector<std::string>& allow) {
    if (port == Port::Litespi) {
        words.insert(words.begin(), "--litespi");
    }
    const Result r = run_script(words, files);
    long long& longest = r.at("ls_stalled") != 0 ? call_max.stalled : call_max.nominal;
    longest = std::max(longest, r.at("max_call_us"));
    for (const std::string& finding : contract(r, allow)) {
        ADD_FAILURE() << port_name(port) << ": " << finding;
    }
    return r;
}

void expect_state(const Files& files, const std::string& dump, const Payloads& saved, const std::string& what) {
    const auto it = files.states.find(dump);
    if (it == files.states.end()) {
        ADD_FAILURE() << what << "no state was kept as " << dump;
        return;
    }
    std::vector<unsigned> bad;
    for (const unsigned rid : rids()) {
        Record want{0, {}};
        const auto s = saved.find(rid);
        if (s != saved.end()) {
            want = Record{1, s->second};
        } else {
            for (unsigned j = 0; j < plen(rid); ++j) {
                want.payload.push_back(nvm_smodel_default(rid, j));
            }
        }
        const auto got = it->second.find(rid);
        if (got == it->second.end() || !(got->second == want)) {
            bad.push_back(rid);
        }
    }
    std::ostringstream ids;
    for (std::size_t k = 0; k < bad.size() && k < 6u; ++k) {
        ids << (k != 0u ? ", " : "") << "0x" << std::hex << bad[k];
    }
    EXPECT_TRUE(bad.empty()) << what << "state of records [" << ids.str() << "] (" << std::dec << bad.size()
                             << " in all) differs from the slot";
}

Payloads with(Payloads base, const Payloads& over) {
    for (const auto& [rid, payload] : over) {
        base[rid] = payload;
    }
    return base;
}

Payloads only(const Payloads& base, const std::vector<long long>& ids, bool keep) {
    Payloads out;
    for (const auto& [rid, payload] : base) {
        const bool listed = std::find(ids.begin(), ids.end(), static_cast<long long>(rid)) != ids.end();
        if (listed == keep) {
            out[rid] = payload;
        }
    }
    return out;
}

std::string set_word(unsigned rid, const Bytes& payload) {
    std::string out = std::to_string(rid) + ":";
    char pair[3];
    for (const std::uint8_t b : payload) {
        std::snprintf(pair, sizeof pair, "%02x", b);
        out += pair;
    }
    return out;
}

Bytes value(unsigned rid, unsigned seed) {
    Bytes out;
    for (unsigned j = 0; j < plen(rid); ++j) {
        out.push_back(static_cast<std::uint8_t>((rid * 13u + j * 11u + seed) & 0xFFu));
    }
    return out;
}

Bytes padded(const Bytes& image) {
    Bytes out = image;
    out.resize(NVM_SLOT_BYTES, 0xFFu);
    return out;
}

bool slot_holds(const Bytes& got, const Bytes& image) { return !image.empty() && got == padded(image); }

long long pages() { return (fx().num("img_len") + 255) / 256; }

bool in(long long value, long long lo, long long hi) { return value >= 0 && lo <= value && value <= hi; }

long long after_mark(const Result& r, std::size_t k) {
    if (r.erases.size() <= k || r.marks.empty()) {
        return -1;
    }
    return static_cast<long long>(r.erases[k]) - static_cast<long long>(r.marks.back());
}

const char* port_name(Port port) { return port == Port::Litespi ? "--litespi" : "model"; }

// The doctored binaries (test_nvm_shapes.cpp) link this file and hold no
// test of both ports; every other binary that does is graded by its tally.
GTEST_ALLOW_UNINSTANTIATED_PARAMETERIZED_TEST(NvmBoth);

INSTANTIATE_TEST_SUITE_P(Ports, NvmBoth, ::testing::Values(Port::Model, Port::Litespi),
                         [](const ::testing::TestParamInfo<Port>& info) {
                             return std::string(info.param == Port::Litespi ? "litespi" : "model");
                         });

}  // namespace nvm_test
