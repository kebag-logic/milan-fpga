57b8c867 -> 57b8c8676864e2564a1c867a2ee6623018a33002
3f05559f593d2f3b0aad632590ed257616714b6c
| `[C]` | Item 1: 76 s bound across five DUT and five switch LeaveAll MRPDUs, the last 45 s or more held by the registration alone. No self-Leave, no licence drop, and no gap over 1.5 CRF periods. Every DUT LeaveAll flags all four MSRP attribute types. |
LeaveAll period is not modelled. This station's leavealltimer does not
restart on a received LeaveAll (processor issue 108), and nothing here
measures that. The silicon rerun of #530 is the acceptance.
    ck_true("the registration alone held the DA gate for >= 45 s (probe window + 15 s closed)",
            peer[kUidCrf].last_probe + ms(15000) + ms(45000) <= cyc);
    printf("  [i]    %ld DUT and %ld switch LeaveAll MRPDUs in this phase\n", dut_la - la0, bridge_la - bla0);
    ck_true("the DUT sent >= 4 LeaveAll MRPDUs", dut_la - la0 >= 4);
    ck("every DUT LeaveAll flagged all four MSRP attribute types (802.1Q-2014 10.7.5.20)",
       static_cast<uint64_t>(dut_la_not_all_types), 0);
    ck_true("the switch sent >= 4 of its own, Listener JoinMt first", bridge_la - bla0 >= 4);
    ck("the Listener registration still reads Ready", lstn_reg(kUidCrf), 2);
c951a9ff0cb5851fb159d33e966e5a2a9a188fe3
9e3ccbfb -> 9e3ccbfb9c22d24db48787cbcfd574974edb5e42
3f05559f593d2f3b0aad632590ed257616714b6c
| `[C]` | Item 1: 76 s bound across five DUT and five switch LeaveAll MRPDUs, the last 45 s or more held by the registration alone. No self-Leave, no licence drop, and no gap over 1.5 CRF periods. Every DUT LeaveAll flags all four MSRP attribute types. |
LeaveAll period is not modelled. This station's leavealltimer does not
restart on a received LeaveAll (processor issue 108), and nothing here
measures that. The silicon rerun of #530 is the acceptance.
    ck_true("the registration alone held the DA gate for >= 45 s (probe window + 15 s closed)",
            peer[kUidCrf].last_probe + ms(15000) + ms(45000) <= cyc);
    printf("  [i]    %ld DUT and %ld switch LeaveAll MRPDUs in this phase\n", dut_la - la0, bridge_la - bla0);
    ck_true("the DUT sent >= 4 LeaveAll MRPDUs", dut_la - la0 >= 4);
    ck("every DUT LeaveAll flagged all four MSRP attribute types (802.1Q-2014 10.7.5.20)",
       static_cast<uint64_t>(dut_la_not_all_types), 0);
    ck_true("the switch sent >= 4 of its own, Listener JoinMt first", bridge_la - bla0 >= 4);
    ck("the Listener registration still reads Ready", lstn_reg(kUidCrf), 2);
c951a9ff0cb5851fb159d33e966e5a2a9a188fe3
