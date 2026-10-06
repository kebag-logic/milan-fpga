// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// nvm_rig.hpp - the scenario rig of the saved-state store's GoogleTest suite
// (#665 lanes F1 and FT).
//
// The store is compiled as it ships, over either flash port: the host flash
// model directly, or (--litespi) the on-chip LiteSPI implementation over a
// model of the command master over the same flash model. The state port is
// the host state model. A script is a list of words run left to right, the
// words of the runner this replaces (test/nvm_test.c until #665 FT), and one
// run starts as one run of that runner did: blank media, every model and the
// store fresh. What a run leaves behind is returned, never printed: the
// summary under the runner's own names, the power-cut tally, the times, and
// the slots, stage and state a script asked to keep.
//
// The rig takes no verdict. Every one is taken by the tests against the
// fixture scripts/nvm_klj2.py wrote for the shape (nvm_fixture.hpp), never
// against the store's own idea of the bytes.

#ifndef NVM_RIG_HPP
#define NVM_RIG_HPP

#include <cstdint>
#include <map>
#include <string>
#include <utility>
#include <vector>

namespace nvm_test {

using Bytes = std::vector<std::uint8_t>;

//! One record of the state model: its valid flag and its payload.
struct Record {
    int valid = 0;
    Bytes payload;
    bool operator==(const Record&) const = default;
};

//! record id -> what the state model holds for it.
using State = std::map<unsigned, Record>;

//! Byte images a script loads by name (--slot-a NAME) and keeps by name
//! (--dump-slot-a NAME, --dump-stage NAME), and the states it keeps
//! (--dump-state NAME).
struct Files {
    std::map<std::string, Bytes> blobs;
    std::map<std::string, State> states;
};

//! What one run left behind.
struct Result {
    std::map<std::string, long long> s;          //!< the summary, under the runner's names
    std::map<std::string, long long> powercut;   //!< effects, cases, old, new, bad
    long long guard = -1;                        //!< writes outside the journal the port took
    std::vector<std::uint64_t> erases;           //!< model time of the first sixteen erases
    std::vector<std::uint64_t> fail_at;          //!< failed attempts and verified commits
    std::vector<std::uint64_t> ok_at;
    std::vector<std::uint64_t> marks;            //!< each --mark
    std::vector<std::pair<std::uint64_t, std::uint64_t>> clocks;  //!< each --clock: port, model
    std::vector<std::string> fails;              //!< the rig's own refusals of a script

    //! One summary value; a key the rig does not publish is a failed test.
    long long at(const char* key) const;
    //! The summary as one line, for a failure's message.
    std::string text() const;
};

//! Run one script. False words or a missing file refuse the run (a fail line).
Result run_script(const std::vector<std::string>& words, Files& files);

}  // namespace nvm_test

#endif  // NVM_RIG_HPP
