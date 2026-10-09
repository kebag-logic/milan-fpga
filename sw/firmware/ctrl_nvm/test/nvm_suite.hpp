// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// nvm_suite.hpp - what every test of the saved-state store's GoogleTest suite
// shares (#665 lanes F1 and FT): the fixture, a run held to the port
// contract, and the state comparison.
//
// THE FIXTURE is the oracle. nvm_fixture.py writes it for the shape this
// binary is built for, from scripts/nvm_klj2.py (the reference encoder and
// decoder), the builder's inventory and the recorded vectors of
// tb/verilator/nvm_backend: every container a test loads or compares with,
// every payload set a restore must leave, and the shape's facts. The binary
// reads it from the directory NVM_FIXTURE names. A test never assembles or
// decodes a container itself, and never asks the store what the bytes should
// be.
//
// THE CONTRACT every run keeps, whatever the test is about: the journal only,
// never the authoritative slot, no program across a page or while busy, pages
// in ascending order, the step bound, the state port's order, one call's
// latency (the nominal figure with no stall armed, the cumulative bound with
// one), and on the LiteSPI port a write enable before every PP and SE.

#ifndef NVM_SUITE_HPP
#define NVM_SUITE_HPP

#include <gtest/gtest.h>

#include <cstdint>
#include <map>
#include <string>
#include <vector>

#include "nvm_rig.hpp"

namespace nvm_test {

enum class Port { Model, Litespi };

//! record id -> payload: what a restore leaves valid.
using Payloads = std::map<unsigned, Bytes>;

//! Boot reads of one slot, judgements or re-stages (nvm_store.h NVM_READ_TRIES).
constexpr unsigned kReadTries = 3;
//! The LiteSPI port's deadline on one call, in timer0 time (LS_CALL_US).
constexpr long long kLsCallUs = 2000;
//! The link time of one page program, (5 + 256) bytes at 0.64 us, rounded up.
constexpr long long kPageLinkUs = 168;
//! One page program's 1,050-odd command-master accesses at 40 ns.
constexpr long long kPageAccessUs = 42;
//! The longest one service call may hold the loop, in model time, whatever
//! the master does (README, "The service bound").
constexpr long long kCallBoundUs = kLsCallUs + 3 + kPageAccessUs + kPageLinkUs;
//! A call with no stall armed: one page program's link time and accesses.
constexpr long long kNominalCallUs = 250;
constexpr long long kMs = 1000;

//! The shape's facts and reference images, from nvm_fixture.py.
class Fixture {
 public:
    static const Fixture& get();

    const Bytes& blob(const std::string& name) const;
    long long num(const std::string& name) const;
    const std::vector<long long>& list(const std::string& name) const;
    const Payloads& payloads(const std::string& name) const;
    const std::string& text(const std::string& name) const;
    //! A file set holding the named blobs under the names a script uses.
    Files files(const std::map<std::string, std::string>& as) const;

 private:
    std::map<std::string, Bytes> blobs_;
    std::map<std::string, long long> nums_;
    std::map<std::string, std::vector<long long>> lists_;
    std::map<std::string, Payloads> payloads_;
    std::map<std::string, std::string> texts_;
    std::string error_;
};

inline const Fixture& fx() { return Fixture::get(); }

//! The shape's records in ascending id, and the payload length of each.
std::vector<unsigned> rids();
unsigned plen(unsigned rid);

//! Run `words` on `port`, failing the test on every contract finding (except
//! the counters `allow` names).
Result go(Port port, Files& files, std::vector<std::string> words, const std::vector<std::string>& allow = {});

//! The state the script kept as `dump` holds exactly `saved` (valid) and the
//! state model's image default (not valid) for every other record.
void expect_state(const Files& files, const std::string& dump, const Payloads& saved, const std::string& what = "");

//! `base` with `over` written over it.
Payloads with(Payloads base, const Payloads& over);
//! The payloads of `base` whose record is (`keep`) or is not in `ids`.
Payloads only(const Payloads& base, const std::vector<long long>& ids, bool keep);

//! "ID:HEX", the argument of --set.
std::string set_word(unsigned rid, const Bytes& payload);
//! A payload for record rid that no golden frame carries.
Bytes value(unsigned rid, unsigned seed);
//! A dumped slot, and an image as a slot holds it (the rest erased).
Bytes padded(const Bytes& image);
//! Whether `got`, a dumped slot, holds `image` followed by erased bytes.
bool slot_holds(const Bytes& got, const Bytes& image);
//! The pages one commit programs.
long long pages();

//! lo <= value <= hi, and a value at all.
bool in(long long value, long long lo, long long hi);
//! The k-th erase's start, in us after the run's last mark (-1 when there is none).
long long after_mark(const Result& r, std::size_t k);

const char* port_name(Port port);

//! The three port populations of the suite: the checks whose subject is the
//! media face run on both ports; the read faults reach the store through the
//! model's port only; the PHC, timer0 and the command master exist on the
//! LiteSPI port only.
class NvmBoth : public ::testing::TestWithParam<Port> {
 protected:
    Port port() const { return GetParam(); }
};
class NvmModel : public ::testing::Test {
 protected:
    static Port port() { return Port::Model; }
};
class NvmLitespi : public ::testing::Test {
 protected:
    static Port port() { return Port::Litespi; }
};

}  // namespace nvm_test

#endif  // NVM_SUITE_HPP
