# The CPU generator's region decode (#665 S2)

## VexiiSplitShippingRegions.v: shipping split region list (rom/sram 224 KiB, main_ram on m, spiflash 0x01000000, milan_csr 0x90000000, ctrl_mbx 0x90100000, csr)
size 1578221 B, sha256 e4f33e1433631702438dc27a4997b98fabcd2c850e167324ef0a36f7ed7328ac

fetch PMA fault:
  assign FetchCachelessPlugin_logic_onPma_port_rsp_fault = (! ((|{((FetchCachelessPlugin_pmaBuilder_addressBits & 32'hc0000000) == 32'h40000000),{((FetchCachelessPlugin_pmaBuilder_addressBits & 32'hff000000) == 32'h01000000),{((FetchCachelessPlugin_pmaBuilder_addressBits & _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault) == 32'h10000000),{(_zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_1 == _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_2),{_zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_3,_zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_4}}}}}) && (|FetchCachelessPlugin_pmaBuilder_onTransfers_0_hit)));
  assign _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault = 32'hfffe0000;
  assign _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_1 = (FetchCachelessPlugin_pmaBuilder_addressBits & 32'hfffc8000);
  assign _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_2 = 32'h0;
  assign _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_3 = ((FetchCachelessPlugin_pmaBuilder_addressBits & 32'hffff0000) == 32'h10020000);
  assign _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_4 = ((FetchCachelessPlugin_pmaBuilder_addressBits & 32'hffff8000) == 32'h10030000);
load/store PMA terms:
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault = 32'hff000000;
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_1 = (LsuCachelessPlugin_pmaBuilder_addressBits & 32'hffc00000);
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_2 = 32'hf0c00000;
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_3 = ((LsuCachelessPlugin_pmaBuilder_addressBits & 32'hfffe0000) == 32'hf0000000);
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_4 = ((LsuCachelessPlugin_pmaBuilder_addressBits & 32'hfffe0000) == 32'h10000000);
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_5 = {((LsuCachelessPlugin_pmaBuilder_addressBits & 32'hfffc8000) == 32'h0),{((LsuCachelessPlugin_pmaBuilder_addressBits & 32'hffff0000) == 32'h90000000),{((LsuCachelessPlugin_pmaBuilder_addressBits & _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_6) == 32'h10020000),{(_zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_7 == _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_8),(_zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_9 == _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_10)}}}};
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_6 = 32'hffff0000;
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_7 = (LsuCachelessPlugin_pmaBuilder_addressBits & 32'hffff8000);
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_8 = 32'h90100000;
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_9 = (LsuCachelessPlugin_pmaBuilder_addressBits & 32'hffff8000);
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_10 = 32'h10030000;

## VexiiTest224.v: test SoC region list as built (rom/sram 224 KiB)
size 1425204 B, sha256 e57bfe4f82ff0fc83f49d573cdf3bb6879f4bf0f6502e622ed79a44419ce3182

fetch PMA fault:
  assign FetchCachelessPlugin_logic_onPma_port_rsp_fault = (! ((|{((FetchCachelessPlugin_pmaBuilder_addressBits & 32'hff000000) == 32'h20000000),{((FetchCachelessPlugin_pmaBuilder_addressBits & 32'hfffe0000) == 32'h10000000),{((FetchCachelessPlugin_pmaBuilder_addressBits & _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault) == 32'h0),{(_zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_1 == _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_2),(_zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_3 == _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_4)}}}}) && (|FetchCachelessPlugin_pmaBuilder_onTransfers_0_hit)));
  assign _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault = 32'hfffc8000;
  assign _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_1 = (FetchCachelessPlugin_pmaBuilder_addressBits & 32'hffff0000);
  assign _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_2 = 32'h10020000;
  assign _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_3 = (FetchCachelessPlugin_pmaBuilder_addressBits & 32'hffff8000);
  assign _zz_FetchCachelessPlugin_logic_onPma_port_rsp_fault_4 = 32'h10030000;
load/store PMA terms:
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault = 32'hffc00000;
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_1 = (LsuCachelessPlugin_pmaBuilder_addressBits & 32'hfffe0000);
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_2 = 32'hf0000000;
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_3 = ((LsuCachelessPlugin_pmaBuilder_addressBits & 32'hfffe0000) == 32'h10000000);
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_4 = ((LsuCachelessPlugin_pmaBuilder_addressBits & 32'hfffc8000) == 32'h0);
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_5 = {((LsuCachelessPlugin_pmaBuilder_addressBits & 32'hffff0000) == 32'h10020000),{((LsuCachelessPlugin_pmaBuilder_addressBits & 32'hffff8000) == 32'h10030000),((LsuCachelessPlugin_pmaBuilder_addressBits & 32'hffff8000) == 32'h80000000)}};

## VexiiTest256.v: test SoC region list with the power-of-two cover (rom/sram 256 KiB)
size 1423330 B, sha256 6a2847f9de20ca617c048f56b41fff54fab3f2cb0f3198134b9387c469086da3

fetch PMA fault:
  assign FetchCachelessPlugin_logic_onPma_port_rsp_fault = (! ((|{((FetchCachelessPlugin_pmaBuilder_addressBits & 32'hff000000) == 32'h20000000),((FetchCachelessPlugin_pmaBuilder_addressBits & 32'heffc0000) == 32'h0)}) && (|FetchCachelessPlugin_pmaBuilder_onTransfers_0_hit)));
  
load/store PMA terms:
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault = 32'hffc00000;
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_1 = (LsuCachelessPlugin_pmaBuilder_addressBits & 32'heffc0000);
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_2 = 32'h0;
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_3 = ((LsuCachelessPlugin_pmaBuilder_addressBits & 32'hfffe0000) == 32'hf0000000);
  assign _zz_LsuCachelessPlugin_logic_onPma_port_rsp_fault_4 = ((LsuCachelessPlugin_pmaBuilder_addressBits & 32'hffff8000) == 32'h80000000);

## 224 KiB against 256 KiB regions
32 changed lines; outside the address-hit and PMA decode: 0
