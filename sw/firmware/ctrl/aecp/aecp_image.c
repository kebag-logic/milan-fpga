// SPDX-License-Identifier: CERN-OHL-W-2.0
// AEMI layout 1, protocol-processor/hdl/aecp/desc/gen_desc_image.py.
#include "aecp_image.h"
#include "wire.h"
#include <string.h>

static uint32_t crc32(const uint8_t *data, size_t bytes)
{
	uint32_t crc = UINT32_MAX;
	for (size_t n = 0; n < bytes; ++n) {
		crc ^= data[n];
		for (unsigned bit = 0; bit < 8u; ++bit) {
			crc = (crc >> 1) ^ ((0u - (crc & 1u)) & 0xedb88320u);
		}
	}
	return ~crc;
}

static bool span(size_t start, size_t count, size_t bytes)
{
	return start <= bytes && count <= bytes - start;
}

static bool header(const uint8_t *image, size_t bytes, uint32_t expected_crc)
{
	if (bytes < 32u) {
		return false;
	}
	uint32_t sum = 0;
	for (unsigned n = 0; n < 32u; n += 4u) {
		sum += (uint32_t)wire_be32(image + n);
	}
	return wire_be32(image) == 0x41454d49u && wire_be16(image + 4) == 1u &&
	       wire_be16(image + 6) != 0u && wire_be32(image + 20) == bytes &&
	       wire_be16(image + 26) == 0u && sum == UINT32_MAX &&
	       crc32(image, bytes) == expected_crc;
}

static bool entries(struct aecp_model *model, const uint8_t *image, size_t bytes,
		    struct aecp_descriptor *descriptors, size_t capacity,
		    uint8_t *values, size_t value_bytes)
{
	size_t offset = (size_t)wire_be32(image + 12);
	size_t entries_count = (size_t)wire_be16(image + 8);
	size_t names = (size_t)wire_be32(image + 16);
	size_t names_count = (size_t)wire_be16(image + 10);
	if (offset < 32u || (offset & 7u) != 0u ||
	    !span(offset, entries_count * 16u, bytes) ||
	    !span(names, names_count * 64u, bytes)) {
		return false;
	}
	size_t previous_end = offset + entries_count * 16u;
	uint32_t previous_key = 0;
	size_t first_index = 0;
	size_t used = 0;
	size_t count = 0;
	for (size_t row = 0; row < entries_count; ++row) {
		const uint8_t *entry = image + offset + row * 16u;
		uint16_t configuration = (uint16_t)wire_be16(entry);
		uint16_t type = (uint16_t)wire_be16(entry + 2);
		size_t number = (size_t)wire_be16(entry + 4);
		size_t length = (size_t)wire_be16(entry + 6);
		size_t base = (size_t)wire_be32(entry + 8);
		size_t name = (size_t)wire_be16(entry + 12);
		size_t stride = (size_t)wire_be16(entry + 14);
		uint32_t key = ((uint32_t)configuration << 16) | type;
		if (configuration >= wire_be16(image + 6) ||
		    (row != 0u && key < previous_key) || number == 0u ||
		    length < 4u || length > wire_be16(image + 24) ||
		    stride != ((length + 7u) & ~(size_t)7u) ||
		    (base & 7u) != 0u || base < previous_end ||
		    !span(base, number * stride, names) ||
		    number > capacity - count || number * length > value_bytes - used) {
			return false;
		}
		if (row == 0u || key != previous_key) {
			first_index = 0;
		}
		if (name != 0xffffu &&
		    (name >= names_count || number + (type == 0u ? 1u : 0u) > names_count - name)) {
			return false;
		}
		for (size_t index = 0; index < number; ++index) {
			const uint8_t *body = image + base + index * stride;
			if (wire_be16(body) != type || wire_be16(body + 2) != first_index + index) {
				return false;
			}
			descriptors[count++] = (struct aecp_descriptor){
				configuration, type, (uint16_t)(first_index + index), (uint16_t)length,
				body, values + used
			};
			memcpy(values + used, body, length);
			used += length;
		}
		previous_key = key;
		first_index += number;
		previous_end = base + number * stride;
	}
	model->descriptors = descriptors;
	model->count = count;
	model->configurations = (uint16_t)wire_be16(image + 6);
	return true;
}

bool aecp_image_load(struct aecp_model *model, const uint8_t *image, size_t bytes,
		     uint32_t expected_crc, struct aecp_descriptor *descriptors,
		     size_t capacity, uint8_t *values, size_t value_bytes)
{
	memset(model, 0, sizeof *model);
	if (!header(image, bytes, expected_crc)) {
		return false;
	}
	return entries(model, image, bytes, descriptors, capacity, values, value_bytes);
}
