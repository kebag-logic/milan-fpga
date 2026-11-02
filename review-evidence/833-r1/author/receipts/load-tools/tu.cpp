#include <regex>
#include <map>
#include <string>
#include <vector>
#include <iostream>
#include <algorithm>
#include <unordered_map>
std::map<std::string, std::vector<std::regex>> table;
int main() { for (auto &[k, v] : table) std::cout << k << v.size() << '\n'; }
