| case | rc | YOSYS OK | parses | FAIL lines (first 4) |
|---|---:|---:|---|---|
| c-split | 1 | 0 |  | modules declared under hdl/ with no entry in the tops array:;  KL_r449_split; |
| c-auto | 1 | 0 |  | modules declared under hdl/ with no entry in the tops array:;  KL_r449_auto; |
| c-cmtblock | 1 | 0 |  | modules declared under hdl/ with no entry in the tops array:;  KL_r449_cmtblock; |
| c-cmtline | 1 | 0 |  | modules declared under hdl/ with no entry in the tops array:;  KL_r449_cmtline; |
| c-macro | 1 | 0 |  | modules declared under hdl/ with no entry in the tops array:;  KL_r449_macro; |
| c-attr | 0 | 42 | parsed 1 |  |
| c-attrline | 0 | 42 | parsed 1 |  |
| c-attr-top | 1 | 0 |  | tops array names modules that no longer exist under hdl/:;  KL_r449_attr; |
| c-split-top | 1 | 42 | parsed 2 | YOSYS FAIL KL_r449_split: ERROR: Module `\r449_absent_module' referenced in module `\KL_r449_split' in cell `\u_r449_absent' is not part of ; |
| c-allvauto | 1 | 0 | parsed 1 | YOSYS FAIL all.v in module automatic: all.v:20749: ERROR: syntax error, unexpected TOK_AUTOMATIC, expecting TOK_ID;YOSYS FAIL KL_r449_allvauto: not elaborated, the parse failed;YOSYS FAIL KL_aecp_desc_mem_guard: not elaborated, the parse failed;YOSYS FAIL KL_aecp_ucpu: not elaborated, the parse failed; |
| r1-c-attr | 0 | 42 | parsed 1 |  |
