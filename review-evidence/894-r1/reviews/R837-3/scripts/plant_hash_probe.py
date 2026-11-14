#!/usr/bin/env python3
"""Plant the disposable firmware probe Core.MapEditWorkProbeBuilderGeometry into a clone's test_aecp.cpp
(argv[1] = the clone, argv[2] = the initializer line hash_keys.py prints for 8 streams x 32 channels).
Run it with: aecp_arms.py --output OUT --work --config configs/endstation_ax7101_8x8.yaml
--filter 'Core.MapEditWork*'; then restore the file (git checkout -- sw/firmware/ctrl/test/test_aecp.cpp)."""
import sys
path = sys.argv[1] + '/sw/firmware/ctrl/test/test_aecp.cpp'
src = open(path).read()
probe = '''TEST_F(Core, MapEditWorkProbeBuilderGeometry)
{
    for(unsigned s=0;s<8;++s){
        auto &stream=desc(6,s);uint64_t format=get(stream.value+74,8);
        ASSERT_EQ(format>>56,2u);put(stream.value+74,(format&~(uint64_t(1023)<<22))|(uint64_t(32)<<22),8);
    }
    std::vector<aecp_mapping> keys=KEYS;
    Bytes body=target(15,0,8+8*keys.size());put(body,4,keys.size(),2);
    for(size_t k=0;k<keys.size();++k){put(body,8+8*k,keys[k].stream,2);put(body,10+8*k,keys[k].channel,2);}
    maps[1].count=0;aecp_map_work=0;ask(44,body,0);
    std::printf("PROBE 8 streams x 32 channels, an ADD of %zu distinct legal keys: %u visits (2 (n + R) %zu); held %zu\\n",
                keys.size(),aecp_map_work,2*keys.size(),(size_t)maps[1].count);
}
#endif
'''.replace('KEYS', sys.argv[2])
i = src.index("Each stream's format is widened to 64 channels")
j = src.index('#endif\n', i)
open(path, 'w').write(src[:j] + probe + src[j + len('#endif\n'):])
