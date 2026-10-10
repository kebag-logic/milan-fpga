// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "fw_gtest.hpp"
#include <gtest/gtest.h>
#include <array>
#include <vector>
extern "C" {
#include "aecp_image.h"
#include "aecp_entity_gen.h"
}

FW_TALLY_LABEL("AECP descriptor image");

namespace {
uint32_t get(const std::vector<uint8_t>& b, size_t at, unsigned width)
{
    uint32_t value = 0;
    for (unsigned n=0; n<width; ++n) value = (value << 8) | b.at(at+n);
    return value;
}
void put(std::vector<uint8_t>& b, size_t at, uint32_t value, unsigned width)
{
    for (unsigned n=0; n<width; ++n) b.at(at+n)=value >> (8*(width-n-1));
}
uint32_t crc(const std::vector<uint8_t>& b)
{
    uint32_t c=0xffffffff;
    for (uint8_t v:b) {
        c ^= v;
        for (unsigned n=0;n<8;++n) c = c&1 ? (c>>1)^0xedb88320 : c>>1;
    }
    return ~c;
}
void checksum(std::vector<uint8_t>& b)
{
    uint32_t sum=0;
    for (unsigned n=0;n<28;n+=4) sum+=get(b,n,4);
    put(b,28,0xffffffff-sum,4);
}
struct Image : testing::Test {
    std::vector<uint8_t> blob{std::begin(aecp_entity_image),std::end(aecp_entity_image)};
    std::array<aecp_descriptor,AECP_ENTITY_DESCRIPTORS> descriptors{};
    std::array<uint8_t,AECP_ENTITY_VALUE_BYTES> values{};
    aecp_model model{};
    bool load(size_t capacity=AECP_ENTITY_DESCRIPTORS,size_t bytes=AECP_ENTITY_VALUE_BYTES) {
        return aecp_image_load(&model,blob.data(),blob.size(),crc(blob),
                               descriptors.data(),capacity,values.data(),bytes);
    }
};
}

TEST_F(Image, EveryDescriptor)
{
    ASSERT_EQ(crc(blob),AECP_ENTITY_CRC) << "image CRC matches the generated manifest";
    ASSERT_TRUE(load()) << "the shape image loads at its exact capacities";
    ASSERT_EQ(model.count,descriptors.size()) << "every shape descriptor is present";
    size_t cursor=0;
    for (const auto& d:descriptors) {
        EXPECT_EQ(std::vector<uint8_t>(d.value,d.value+d.length),
                  std::vector<uint8_t>(d.defaults,d.defaults+d.length))
                  << "descriptor defaults survive the image load";
        EXPECT_EQ(d.value,values.data()+cursor) << "descriptor storage has no alias";
        EXPECT_EQ((d.value[0]<<8)|d.value[1],d.type) << "descriptor type matches its key";
        EXPECT_EQ((d.value[2]<<8)|d.value[3],d.index) << "descriptor index matches its key";
        cursor+=d.length;
    }
    EXPECT_EQ(cursor,values.size()) << "storage size follows all descriptor lengths";
}

TEST_F(Image, RejectHeader)
{
    auto original=blob;
    for (auto [offset,width,value] : std::vector<std::array<uint32_t,3>>{
         {0,4,0},{4,2,2},{6,2,0},{20,4,31},{26,2,1}}) {
        blob=original; put(blob,offset,value,width); checksum(blob);
        EXPECT_FALSE(load()) << "invalid image header is refused";
        EXPECT_EQ(model.count,0u) << "a refused image leaves the model closed";
    }
    blob=original; blob[31]^=1;
    EXPECT_FALSE(load()) << "the header checksum is verified";
    blob=original;
    EXPECT_FALSE(aecp_image_load(&model,blob.data(),blob.size(),crc(blob)^1,
                 descriptors.data(),descriptors.size(),values.data(),values.size()))
                 << "image CRC rejects corrupted descriptor bytes";
    for (size_t bytes=0;bytes<32;++bytes) {
        blob.assign(original.begin(),original.begin()+bytes);
        EXPECT_FALSE(load()) << "truncated image header is refused before access";
    }
}

TEST_F(Image, RejectDirectory)
{
    auto original=blob;
    const uint32_t index=get(blob,12,4), names=get(blob,16,4);
    const uint32_t base=get(blob,index+8,4), length=get(blob,index+6,2);
    for (auto [offset,width,value] : std::vector<std::array<uint32_t,3>>{
         {12,4,0},{12,4,index+1},{12,4,0xfffffff8},{8,2,0xffff},
         {16,4,0xffffffff},{10,2,0xffff},{index,2,get(blob,6,2)},
         {index+4,2,0},{index+6,2,3},{index+6,2,0xffff},
         {index+14,2,length+8},{index+8,4,base+1},{index+8,4,0},
         {index+8,4,names},{index+12,2,get(blob,10,2)},
         {index+12,2,get(blob,10,2)-1},{base,2,0xffff},{base+2,2,1},
         {index+16+2,2,0xffff},{index+32+2,2,0}}) {
        SCOPED_TRACE(offset);
        blob=original;put(blob,offset,value,width);checksum(blob);
        EXPECT_FALSE(load()) << "invalid descriptor directory is refused at its boundary";
        EXPECT_EQ(model.count,0u) << "partial descriptor loads remain closed";
    }
    blob=original;
    EXPECT_FALSE(load(descriptors.size()-1)) << "descriptor pool exhaustion is refused";
    EXPECT_FALSE(load(descriptors.size(),values.size()-1)) << "byte pool exhaustion is refused";
}
