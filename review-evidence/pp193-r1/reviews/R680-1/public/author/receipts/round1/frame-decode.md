# Item 1 measurement: decode of the DUT's MSRP frame with two sinks settled on one StreamID

Source: `m193-measure.log`, "two-settled frame 0 @403 ms" (frames 1 and 2 have the
same structure; frame 2 carries JoinMt instead of New). Processor 21601694, srp_top
suite bench (real KL_srp_top, KL_srp_encoder and KL_pp_tx_slots; the bytes are read
off the slot serializer, as the processor top hands them to the TX arbiter).

Scenario: sinks 0 and 1 settled on the same {stream_id 11:22:33:44:55:66:00:01,
DA 91:E0:F0:11:22:33, VID 2} (DECLARE_LISTENER, Ready); the peer then sends one
Talker Advertise JoinIn for that triple. Both sinks register it (tk_reg {1,1},
registrar {IN, IN}) and both declare Ready (ls_decl {2,2}).

```
01 80 c2 00 00 0e  0a 0b 0c 0d 0e 0f  22 ea      Ethernet DA (MSRP), SA, EtherType
00                                               ProtocolVersion
03 08 00 1a                                      Message: AttributeType 3 (Listener), AttributeLength 8,
                                                 AttributeListLength 26 = 2 x 12 + EndMark 2
00 01  11 22 33 44 55 66 00 01  00  80           VectorAttribute 1: NumberOfValues 1, FirstValue = stream_id,
                                                 ThreePacked 0x00 = New, FourPacked 0x80 = Ready
00 01  11 22 33 44 55 66 00 01  00  80           VectorAttribute 2: the SAME FirstValue, New, Ready
00 00                                            AttributeList EndMark
00 00                                            MRPDU EndMark
```

Reference: the independent builder's one-declaration frame for the same value is 35 B
(`03 08 00 0e 00 01 11 22 33 44 55 66 00 01 00 80 00 00 00 00`). The DUT's is 47 B with
the vector repeated.

Result: the transmit path does NOT merge the two sinks' declarations. One MRPDU
carries two Listener declarations (two VectorAttributes) for one attribute value.
Cause, by reading: each sink has its own Table 10-3 applicant
(`hdl/srp/KL_srp_listener_fsm.sv:365-374`), the tick walk pushes one encoder event
per sink with a message (`:731-736`), and the encoder folds only +1 successors into a
run (`hdl/srp/KL_srp_encoder.sv:186-214`, `:388-391`); an equal FirstValue breaks the
run and is emitted as its own VectorAttribute in the same message (`:641-659`).

The same log shows the issue's behaviour: after the unbind of sink 0 alone, the next
frame (@1402 ms) carries only `b4 80` = Lv, Ready for the value sink 1 still wants; the
remaining sink's next declaration of it is the periodic JoinMt @2003 ms
(ThreePacked `6c` = JoinMt).
