// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0

// Decode one complete Ethernet AECP GET_COUNTERS response with the pinned
// L-Acoustics LA_avdecc implementation. This intentionally uses the official
// parser entry point instead of restating its wire decoder in this repository.

#include "protocol/protocolAemPayloads.hpp"

#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    if (argc != 2) {
        std::fprintf(stderr, "usage: %s response.bin\n", argv[0]);
        return 2;
    }

    std::ifstream input(argv[1], std::ios::binary);
    const std::vector<std::uint8_t> frame((std::istreambuf_iterator<char>(input)),
                                          std::istreambuf_iterator<char>());
    constexpr std::size_t PayloadOffset = 38;
    constexpr std::size_t ResponseBytes = 174;
    if (!input.good() && !input.eof()) {
        std::fprintf(stderr, "cannot read %s\n", argv[1]);
        return 2;
    }
    if (frame.size() != ResponseBytes) {
        std::fprintf(stderr, "response is %zu bytes, expected %zu\n",
                     frame.size(), ResponseBytes);
        return 1;
    }

    try {
        const la::avdecc::protocol::AemAecpdu::Payload payload{
            frame.data() + PayloadOffset, frame.size() - PayloadOffset};
        const auto [descriptorType, descriptorIndex, valid, counters] =
            la::avdecc::protocol::aemPayload::deserializeGetCountersResponse(
                la::avdecc::entity::LocalEntity::AemCommandStatus::Success,
                payload);

        const auto type = static_cast<std::uint16_t>(descriptorType);
        std::printf("descriptor_type=0x%04x descriptor_index=0x%04x "
                    "valid=0x%08x\n",
                    type, descriptorIndex, valid);
        for (std::size_t q = 0; q < 5; ++q)
            std::printf("counter[%zu]=%u\n", q, counters[q]);

        bool validResponse = type == 0x0006u && descriptorIndex == 0u &&
                             valid == 0x0000001Fu;
        for (std::size_t q = 5; q < counters.size(); ++q)
            validResponse = validResponse && counters[q] == 0u;
        if (!validResponse) {
            std::fprintf(stderr, "decoded response violates Milan Table 5.17\n");
            return 1;
        }
    } catch (std::exception const& error) {
        std::fprintf(stderr, "LA_avdecc rejected the response: %s\n", error.what());
        return 1;
    }
    return 0;
}
