| case file | mode | cases | refused | accepted | refused by | pins ok | at 11b1b86c (R273-5 receipt) |
|---|---|---|---|---|---|---|---|
| bom | absent | 11 | 10 | 1 | allowlist 7, other rule 3 | - | 8 refused / 3 accepted |
| bom | sdk | 11 | 11 | 0 | allowlist 7, other rule 4 | - | 10 refused / 1 accepted |
| cases_accepted | absent | 11 | 0 | 11 |  | - |  |
| cases_accepted | sdk | 11 | 0 | 11 |  | - |  |
| cases_r1 | absent | 14 | 4 | 10 | other rule 4 | - |  |
| cases_r1 | sdk | 14 | 13 | 1 | other rule 13 | - |  |
| cases_r2 | absent | 5 | 3 | 2 | other rule 3 | - |  |
| cases_r2 | sdk | 5 | 5 | 0 | other rule 5 | - |  |
| cases_r3 | absent | 5 | 2 | 3 | other rule 2 | - |  |
| cases_r3 | sdk | 5 | 4 | 1 | other rule 4 | - |  |
| cases_r4 | absent | 3 | 0 | 3 |  | - |  |
| cases_r4 | sdk | 3 | 0 | 3 |  | - |  |
| extra | absent | 4 | 1 | 3 | other rule 1 | - | 1 refused / 3 accepted |
| extra | sdk | 4 | 3 | 1 | other rule 3 | - | 3 refused / 1 accepted |
| hi | absent | 9 | 8 | 1 | S:__has_include 6, other rule 2 | - | 8 refused / 1 accepted |
| hi | sdk | 9 | 9 | 0 | S:__has_include 6, other rule 3 | - | 9 refused / 0 accepted |
| md | absent | 10 | 8 | 2 | S:$ 1, allowlist 7 | - | 4 refused / 6 accepted |
| md | sdk | 10 | 9 | 1 | S:$ 1, allowlist 7, other rule 1 | - | 8 refused / 2 accepted |
| published | absent | 74 | 25 | 49 | other rule 25 | - | 25 refused / 49 accepted |
| published | sdk | 74 | 52 | 22 | other rule 52 | - | 52 refused / 22 accepted |
| r2-cases | absent | 15 | 10 | 5 | allowlist 2, digraph ban 7, other rule 1 | - | 9 refused / 6 accepted |
| r2-cases | sdk | 15 | 14 | 1 | allowlist 2, digraph ban 7, other rule 5 | - | 13 refused / 2 accepted |
| round1-accepted | absent | 10 | 0 | 10 |  | - |  |
| round1-accepted | sdk | 10 | 0 | 10 |  | - |  |
| round1-all_head | absent | 26 | 6 | 20 | other rule 6 | - | 6 refused / 20 accepted |
| round1-all_head | sdk | 26 | 14 | 12 | other rule 14 | - | 14 refused / 12 accepted |
| round1-grader | absent | 6 | 3 | 3 | other rule 3 | - |  |
| round1-grader | sdk | 6 | 3 | 3 | other rule 3 | - |  |
| round1-hostile | absent | 14 | 6 | 8 | other rule 6 | - |  |
| round1-hostile | sdk | 14 | 13 | 1 | other rule 13 | - |  |
| round1-listing_head | absent | 2 | 0 | 2 |  | - |  |
| round1-listing_head | sdk | 2 | 1 | 1 | other rule 1 | - |  |
| round1-verify_r272 | absent | 12 | 3 | 9 | other rule 3 | - |  |
| round1-verify_r272 | sdk | 12 | 9 | 3 | other rule 9 | - |  |
| unread | absent | 2 | 1 | 1 | digraph ban 1 | - | 1 refused / 1 accepted |
| unread | sdk | 2 | 1 | 1 | digraph ban 1 | - | 1 refused / 1 accepted |

Verdict changes against 11b1b86c:

- bom (absent): B5 BOM: a literal-address cast store macro behind a BOM, invoked in a UART command handler -- ACCEPTED -> REFUSED
- bom (absent): B6 BOM alone at offset 0, nothing else changed (benign control) -- ACCEPTED -> REFUSED
- bom (sdk): B6 BOM alone at offset 0, nothing else changed (benign control) -- ACCEPTED -> REFUSED
- md (absent): MD1 literal-address cast store into the CSR window in a UART handler, hidden by U+00B7 in two directive names -- ACCEPTED -> REFUSED
- md (absent): MD1a the same store hidden by U+0387 -- ACCEPTED -> REFUSED
- md (absent): MD1b the same store hidden by U+203F -- ACCEPTED -> REFUSED
- md (absent): MD5 benign control: a printf in a UART handler, hidden by U+00B7 -- ACCEPTED -> REFUSED
- md (sdk): MD5 benign control: a printf in a UART handler, hidden by U+00B7 -- ACCEPTED -> REFUSED
- r2-cases (absent): B1 a byte order mark before the first line, nothing else -- ACCEPTED -> REFUSED
- r2-cases (sdk): B1 a byte order mark before the first line, nothing else -- ACCEPTED -> REFUSED
