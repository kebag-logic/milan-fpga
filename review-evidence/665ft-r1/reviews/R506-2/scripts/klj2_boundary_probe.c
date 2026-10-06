// R506-2 probe of nvm_klj2_check_body at a loaded prefix's record-header boundary.
// (a) AddressSanitizer: the blank container, a buffer of exactly NVM_KLJ2_HDR + NVM_REC_HDR bytes,
//     loaded = that size (the erased-record branch reads the payload past `loaded`).
// (b) the guard's exact boundary: a CRC-closed container whose first record header claims a
//     payload past the end; loaded = that header's end. The header's own verdict (VD_LEN) is
//     reachable only when the guard passes at loaded == pos + NVM_REC_HDR.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "nvm_klj2.h"
int main(int argc, char **argv) {
    static uint8_t img[NVM_IMG_LEN];
    nvm_klj2_blank(img);
    if (argc > 1 && strcmp(argv[1], "asan") == 0) {
        uint32_t n = NVM_KLJ2_HDR + NVM_REC_HDR;
        uint8_t *buf = malloc(n);
        memcpy(buf, img, n);
        enum nvm_verdict v = nvm_klj2_check_body(buf, NVM_IMG_LEN, n);
        printf("asan case: verdict %d\n", (int)v);
        free(buf);
        return 0;
    }
    uint8_t *p = img + NVM_KLJ2_HDR;
    struct nvm_rec r = nvm_rec_first();
    p[0] = (uint8_t)(NVM_REC_MAGIC >> 8); p[1] = (uint8_t)NVM_REC_MAGIC; p[2] = (uint8_t)MILAN_NVM_REC_LAYOUT;
    p[3] = r.id; p[4] = 0xff; p[5] = 0xff; p[6] = 0; p[7] = 0;
    nvm_klj2_seal(img);
    printf("crc-closed: check=%d\n", (int)nvm_klj2_check(img, NVM_IMG_LEN));
    printf("loaded = first header's end: check_body=%d (VD_LEN=%d, VD_REC=%d)\n",
           (int)nvm_klj2_check_body(img, NVM_IMG_LEN, NVM_KLJ2_HDR + NVM_REC_HDR), NVM_VD_LEN, NVM_VD_REC);
    return 0;
}
