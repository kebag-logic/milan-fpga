// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// The two things every self-checking Verilator harness in this tree needs:
// an owner for the Verilated model, and a checker that counts.
//
// WHY THIS EXISTS. Both were re-implemented in every harness, and both
// re-implementations were wrong in ways a reader could not see.
//
//   * OWNERSHIP. The house shape was `dut = new Vfoo;` at the top of `main`
//     and `dut->final(); delete dut;` at the bottom. Ninety-nine first-party
//     harnesses own a model that way. Seventy-five of them never call
//     `final()` at all, and seven never free the model. Worse, the shape only
//     works for the ONE path that reaches the bottom of `main`: thirty-nine
//     harnesses have a `return` before their teardown - the "give up, the DUT
//     never asserted ready" path a debugging session adds and nobody removes -
//     and every one of those skips whatever the bottom of `main` says.
//     `Model<T>` below owns the model for the scope it is declared in, so
//     `final()` runs exactly once on every path out, including a `return` from
//     the middle. This is C++ Core Guidelines R.11 (no naked `new`), R.20
//     (`unique_ptr` owns) and C.149, applied to the one object every harness
//     has.
//
//   * COUNTING. Ninety-three harnesses keep their own check/failure counters,
//     seventy of them behind a locally declared helper - `ck`, `ckq`, `chk`,
//     `check`, `expect` - and between them they print over twenty different
//     summary lines. That is not a cosmetic complaint. Those lines are the
//     sweep's evidence, `scripts/suite_tally.py` had to learn five distinct
//     shapes to read them, and before it did, the sweep's
//     `grep -o 'checks: *[0-9]*'` read ZERO from 29 of 57 suite logs - a
//     37 784-check shortfall behind a green headline. One shape, defined once,
//     is what stops the sixth shape from being invented. `Checker` prints the
//     shape `scripts/suite_tally.py` calls `checks-colon-failures-colon`, and
//     its `[FAIL]` token is the one `run_all_suites.sh --verdict` greps for.
//
// WHAT THIS DELIBERATELY IS NOT. It is not a BFM library and not a test
// framework. Clock stepping, AXI transactions and protocol modelling stay in
// the harness that owns them, because they differ per DUT and a shared
// "step()" would need a knob per suite. Only the two things that are the same
// everywhere live here.
//
// Usage:
//
//     #include "verilator_harness.hpp"
//     #include "Vmilan_csr.h"
//
//     int main(int argc, char** argv) {
//         Verilated::commandArgs(argc, argv);
//         const milan::tb::Model<Vmilan_csr> model;
//         dut = model.get();                  // the harness's own observer
//         milan::tb::Checker check{"csr"};
//         check.hex("PTP_INCR reset", axi_read(A_PTP_INCR), kPtpIncrExpect);
//         return check.report();              // prints the tally, returns 0/1
//     }
//
// The two project-owned processor submodules carry a byte-identical copy of
// this header, because a submodule cannot include a file from the superproject
// that happens to contain it. `scripts/check_cpp_idiom.py` refuses a copy that
// has drifted, so the three files are one source of truth in the sense Rule 3
// means it.

#ifndef MILAN_TB_VERILATOR_HARNESS_HPP
#define MILAN_TB_VERILATOR_HARNESS_HPP

#include <cstdint>
#include <cstdio>
#include <memory>
#include <string>

namespace milan::tb {

//! Owns one Verilated model for the scope it is declared in.
//!
//! Construction elaborates the model; destruction runs `final()` and then
//! frees it, in that order, on every path out of the scope. The harness keeps
//! an observing raw pointer (`get()`); it never owns one.
template <class Verilated_model>
class Model {
 public:
    Model() : model_(std::make_unique<Verilated_model>()) {}

    //! Name the instance when a harness elaborates more than one model, so a
    //! Verilator runtime message says which.
    explicit Model(const char* instance_name)
        : model_(std::make_unique<Verilated_model>(instance_name)) {}

    ~Model() {
        // `final()` runs the model's end-of-simulation work and must precede
        // the destructor. Calling it here rather than at the bottom of `main`
        // is the whole point: an early `return` cannot skip it.
        model_->final();
    }

    Model(const Model&) = delete;
    Model& operator=(const Model&) = delete;
    Model(Model&&) = delete;
    Model& operator=(Model&&) = delete;

    //! Observing pointer. The caller must not delete it.
    Verilated_model* get() const noexcept { return model_.get(); }

    Verilated_model* operator->() const noexcept { return model_.get(); }
    Verilated_model& operator*() const noexcept { return *model_; }

 private:
    std::unique_ptr<Verilated_model> model_;
};

//! Counts assertions and prints the one summary shape the sweep can read.
//!
//! Every comparison is made on `std::uint64_t` so a 40-bit Verilator word and
//! a plain `int` expectation compare without the caller writing a cast; the
//! two rendering forms differ only in how a value is PRINTED. `hex()` is for
//! register and bus values, `dec()` for counts and indices - pick the one a
//! reader would rather see, because that choice is the only formatting
//! decision this class leaves open.
class Checker {
 public:
    //! `suite_label` prefixes the summary line so a sweep log says which
    //! executable produced which tally. Pass nullptr for an unlabelled tally.
    explicit Checker(const char* suite_label = nullptr)
        : label_(suite_label != nullptr ? suite_label : "") {}

    //! Echo passing checks as well as failing ones. Off by default: a suite
    //! with a hundred thousand checks must not print a hundred thousand lines,
    //! and a suite with thirty is more readable when it does.
    Checker& echo_passes() noexcept {
        echo_passes_ = true;
        return *this;
    }

    //! Compare and render in hexadecimal. Returns whether the check passed, so
    //! a harness can skip dependent work without asking the counter again.
    bool hex(const char* what, std::uint64_t got, std::uint64_t expected) {
        return record(what, got, expected, Radix::hex);
    }

    //! Compare and render in decimal.
    bool dec(const char* what, std::uint64_t got, std::uint64_t expected) {
        return record(what, got, expected, Radix::dec);
    }

    //! Assert a predicate that has no interesting value to print.
    bool that(const char* what, bool condition) {
        ++checks_;
        if (!condition) {
            ++failures_;
            std::printf("  [FAIL] %s\n", what);
        } else if (echo_passes_) {
            std::printf("  [ ok ] %s\n", what);
        }
        return condition;
    }

    //! Record a failure the caller detected itself - a timeout, an unreachable
    //! branch, a parse that could not proceed. It counts as a check, because a
    //! failure that is not counted is a failure the tally cannot see.
    void fail(const char* what) {
        ++checks_;
        ++failures_;
        std::printf("  [FAIL] %s\n", what);
    }

    std::uint64_t checks() const noexcept { return checks_; }
    std::uint64_t failures() const noexcept { return failures_; }
    bool passed() const noexcept { return failures_ == 0; }

    //! Print the tally and return the process exit status: 0 pass, 1 fail.
    //!
    //! The shape is fixed. `scripts/suite_tally.py` parses
    //! `checks: N   failures: M`; inventing a sixth shape is how 37 784 checks
    //! once went uncounted behind a green sweep.
    int report() const {
        if (!label_.empty()) {
            std::printf("== %s: checks: %llu   failures: %llu ==\n", label_.c_str(),
                        static_cast<unsigned long long>(checks_),
                        static_cast<unsigned long long>(failures_));
        } else {
            std::printf("checks: %llu   failures: %llu\n",
                        static_cast<unsigned long long>(checks_),
                        static_cast<unsigned long long>(failures_));
        }
        std::printf("RESULT: %s\n", passed() ? "PASS" : "FAIL");
        return passed() ? 0 : 1;
    }

 private:
    enum class Radix { hex, dec };

    bool record(const char* what, std::uint64_t got, std::uint64_t expected, Radix radix) {
        ++checks_;
        const bool ok = (got == expected);
        if (!ok) {
            ++failures_;
        }
        if (!ok || echo_passes_) {
            const char* verdict = ok ? " ok " : "FAIL";
            if (radix == Radix::hex) {
                std::printf("  [%s] %-40s got=0x%llx exp=0x%llx\n", verdict, what,
                            static_cast<unsigned long long>(got),
                            static_cast<unsigned long long>(expected));
            } else {
                std::printf("  [%s] %-40s got=%llu exp=%llu\n", verdict, what,
                            static_cast<unsigned long long>(got),
                            static_cast<unsigned long long>(expected));
            }
        }
        return ok;
    }

    std::string label_;
    std::uint64_t checks_ = 0;
    std::uint64_t failures_ = 0;
    bool echo_passes_ = false;
};

}  // namespace milan::tb

#endif  // MILAN_TB_VERILATOR_HARNESS_HPP
