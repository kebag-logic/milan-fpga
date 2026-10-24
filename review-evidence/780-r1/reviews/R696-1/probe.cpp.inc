    // Issue #780 / processor #200; IEEE 1722.1-2021 Table 7-141.
    // Exercise command-sized unsupported-target replies at the MAC boundary.
    void grade_adoption_probe() {
        struct Row { uint16_t type, index; unsigned bytes, status; };
        const Row rows[] = {
            {0,0,4,11}, {1,0,4,11}, {2,0,4,11}, {5,0,4,11},
            {6,0,4,11}, {8,0,4,11}, {10,0,4,11}, {36,0,4,11},
            {36,65535,4,11}, {0x0109,0,4,11}, {0x8009,0,4,11},
            {0xffff,0xffff,4,11}, {36,0,8,11}, {36,0,64,11},
            {0,0,0,7}, {0,0,1,7}, {0x0109,0,3,7},
            {9,65535,4,2}, {36,0,4,11}
        };
        uint16_t seq = 0x7000;
        for (const Row& row : rows) {
            std::vector<uint8_t> payload(row.bytes, 0xa5);
            if (row.bytes >= 2) { payload[0] = row.type >> 8; payload[1] = row.type; }
            if (row.bytes >= 4) { payload[2] = row.index >> 8; payload[3] = row.index; }
            uint8_t request[160] = {};
            const size_t n = build_aecp(request, 0, TEST_EID, 0x0027, seq,
                                        payload.data(), payload.size());
            const size_t at = tx_frames.size();
            inject_rx(request, n, 400);
            run_idle(12000);
            const int k = last_aecp(at);
            const std::vector<uint8_t> actual = k >= 0 ? tx_frames[k].bytes
                                                     : std::vector<uint8_t>{};
            printf("ADOPTION type=%04x index=%u cdl=%u expected=%u actual=%u bytes=%zu\n",
                   row.type, row.index, 12+row.bytes, row.status,
                   actual.size()>16 ? actual[16]>>3 : 255u, actual.size());
            ck("adoption matching response", actual.size()>=38 && get_be(actual,34,2)==seq
               && get_be(actual,36,2)==0x0027, 1);
            ck("adoption status", actual.size()>16 ? actual[16]>>3 : 255u, row.status);
            if (row.status == 11 || row.status == 7) {
                std::vector<uint8_t> expected(request, request + 38 + row.bytes);
                for (unsigned i=0;i<6;i++) { expected[i]=CTLR_MAC[i]; expected[i+6]=request[i]; }
                expected[15] = 1;
                expected[16] = (row.status << 3) | (request[16] & 7u);
                if (expected.size() < 60) expected.resize(60, 0);
                ck("adoption byte-exact command echo", actual == expected, 1);
            }
            ++seq;
        }
    }
