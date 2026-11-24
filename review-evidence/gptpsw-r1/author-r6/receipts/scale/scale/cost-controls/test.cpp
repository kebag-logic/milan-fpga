#include <cstdint>
constexpr unsigned h1_cost_count=1;
constexpr std::uint32_t h1_cost_pc[]={0x10};
const char* h1_cost_name[]={"unit"};
#include "harts_cost.hpp"
int main() {
 HartsCost c; c.sample(0x10,0x100,1); c.sample(0x104,0x10,11);
 c.sample(0x10,0x200,15); c.sample(0x204,0x10,40); c.sample(0x10,0x300,50);
 c.report(); const auto& s=c.items[0];
 return !(s.count==2 && s.sum==35 && s.max==25 && s.active);
}
