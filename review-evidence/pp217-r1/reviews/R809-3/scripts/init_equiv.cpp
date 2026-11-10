// Both default member initializer forms of the bench's adp_last_aidx, checked
// at compile time under C++17: every element of both is zero.
#include <cstdint>
struct A { uint32_t v[4] = {}; };
struct B { uint32_t v[4] = {0, 0, 0, 0}; };
constexpr A a{};
constexpr B b{};
static_assert(a.v[0] == 0 && a.v[1] == 0 && a.v[2] == 0 && a.v[3] == 0, "= {} zeroes");
static_assert(b.v[0] == 0 && b.v[1] == 0 && b.v[2] == 0 && b.v[3] == 0, "= {0,0,0,0} zeroes");
static_assert(sizeof(a.v) == sizeof(b.v), "same shape");
int main() { A x; B y; for (int i = 0; i < 4; ++i) if (x.v[i] != y.v[i]) return 1; return 0; }
