/* Reviewer fault probes; production sources are linked without edits. */
#define main baseline_main
#include "nvm_test.c"
#undef main

static struct nvm_flash probe_flash;
static unsigned int flipped;
static int transient_read(void *ctx, uint32_t addr, uint8_t *dst, uint32_t len)
{
    int rc = nvm_fmodel_read(ctx, addr, dst, len);
    /* Slot A's fourth read: CRC already checked; body is reread here. */
    if (!rc && !flipped && addr == NVM_SLOT_A && len == NVM_IMG_LEN) {
        dst[8] ^= 8u;
        flipped = 1;
    }
    return rc;
}
static void seed_slot(uint32_t addr, uint32_t seq, uint8_t value)
{
    struct nvm_rec r = nvm_rec_of(NVM_G_NAME, 0);
    uint8_t *img = nvm_fmodel_mem + addr;
    nvm_klj2_blank(img);
    memset(img + NVM_KLJ2_HDR + r.off + NVM_REC_HDR, value, r.plen);
    nvm_rec_frame(img + NVM_KLJ2_HDR + r.off, r);
    nvm_klj2_header(img, seq);
    nvm_klj2_seal(img);
}
static void until_failed(unsigned int target)
{
    unsigned int i;
    for (i=0; i<100000u && nvm_store_status()->commits_failed < target; ++i)
        t_service();
}
static int sequence_fault(void)
{
    struct nvm_rec r = nvm_rec_of(NVM_G_NAME, 0);
    nvm_fmodel_blank();
    seed_slot(NVM_SLOT_A, 5, 0x55);
    seed_slot(NVM_SLOT_B, 6, 0x66);
    probe_flash = nvm_fmodel_port;
    probe_flash.read = transient_read;
    t.port = &probe_flash;
    t_boot();
    printf("PROBE sequence_read_fault flips=%u auth=%d published_seq=%u staged_seq=%u restored_name=%02x expected_auth=1 expected_seq=6 expected_name=66\n",
           flipped, nvm_store_status()->auth, nvm_store_status()->seq,
           nvm_klj2_seq(nvm_store_stage()), nvm_smodel_value(r.id)[0]);
    return nvm_store_status()->auth == 0 && nvm_store_status()->seq == 13 &&
        nvm_klj2_seq(nvm_store_stage()) == 5 && nvm_smodel_value(r.id)[0] == 0x55;
}
static int console_retry(void)
{
    unsigned int n;
    struct nvm_rec r = nvm_rec_of(NVM_G_NAME, 0);
    uint8_t payload[NVM_NAME_BYTES];
    memset(payload, 0x77, sizeof(payload));
    t.port = &nvm_fmodel_port;
    nvm_fmodel_blank();
    t_boot();
    nvm_fmodel_fault(NVM_F_ERASE_STUCK, 999, 0);
    t_set(r.id, payload, r.plen);
    until_failed(1);
    for (n=2; n<=4; ++n) {
        int started = nvm_store_commit_now();
        until_failed(n);
        printf("PROBE console_retry request=%u started=%d failed=%u exhausted=%d\n",
               n, started, nvm_store_status()->commits_failed, nvm_store_status()->exhausted);
    }
    for (n=1; n<nvm_fmodel_count()->erases; ++n)
        printf("PROBE erase_gap_us=%llu required_min_us=1000000\n",
               (unsigned long long)(nvm_fmodel_count()->erase_start_us[n]-nvm_fmodel_count()->erase_start_us[n-1]));
    return nvm_store_status()->commits_failed == 4 && nvm_fmodel_count()->erases == 4;
}
static int backwards_clock(void)
{
    struct nvm_rec r = nvm_rec_of(NVM_G_NAME, 0);
    uint8_t payload[NVM_NAME_BYTES];
    uint64_t before, after, real_before;
    memset(payload, 0x88, sizeof(payload));
    t.port = &nvm_flash_litespi;
    nvm_fmodel_blank();
    t_boot();
    nvm_fmodel_advance_us(3600000000ULL);
    t_set(r.id, payload, r.plen);
    before = t.port->now_us(t.port->ctx);
    /* A 60-second PHC step back, with media and firmware state retained. */
    nvm_fmodel_advance_us(0ULL - 60000000ULL);
    real_before = nvm_fmodel_now_us();
    t_run_ms(3000);
    after = t.port->now_us(t.port->ctx);
    printf("PROBE backwards_clock raw_elapsed_us=%llu port_elapsed_us=%llu erases=%u dirty=%d phase=%d\n",
           (unsigned long long)(nvm_fmodel_now_us()-real_before),
           (unsigned long long)(after-before), nvm_fmodel_count()->erases,
           nvm_store_status()->dirty, nvm_store_status()->phase);
    return after == before && nvm_fmodel_count()->erases == 0 && nvm_store_status()->dirty;
}
int main(void)
{
    int seq=sequence_fault();
    int retry=console_retry();
    int clock = backwards_clock();
    printf("REPRODUCED sequence=%d console_retry=%d backwards_clock=%d\n", seq, retry, clock);
    return !(seq && retry && clock);
}
