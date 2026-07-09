/* TCP zero-copy receive via TCP_ZEROCOPY_RECEIVE (mmap page-flip, no copy_to_user).
   Reports throughput AND the zero-copied fraction (high => driver delivers page-aligned;
   low => copybreak/frag misalignment falls back to copy). Sender = tools_tcp_blast. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <poll.h>
#include <sys/socket.h>
#include <sys/mman.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <linux/tcp.h>
#ifndef TCP_ZEROCOPY_RECEIVE
#define TCP_ZEROCOPY_RECEIVE 35
#endif
#define PGA 4096UL
#define ALIGN_UP(p,a) (((unsigned long)(p)+(a)-1)&~((a)-1))
int main(int c,char**v){
  if(c<3){fprintf(stderr,"usage: %s ip port [cport] [secs]\n",v[0]);return 1;}
  int fd=socket(AF_INET,SOCK_STREAM,0);
  if(c>3&&atoi(v[3])){struct sockaddr_in l={0};l.sin_family=AF_INET;l.sin_port=htons(atoi(v[3]));
    int o=1;setsockopt(fd,SOL_SOCKET,SO_REUSEADDR,&o,sizeof o);bind(fd,(void*)&l,sizeof l);}
  struct sockaddr_in a={0};a.sin_family=AF_INET;a.sin_port=htons(atoi(v[2]));
  inet_pton(AF_INET,v[1],&a.sin_addr);
  if(connect(fd,(void*)&a,sizeof a)){perror("connect");return 1;}
  double secs=c>4?atof(v[4]):8.0;
  size_t CHUNK=2UL<<20;
  char *rbuf=malloc(1<<20);
  char *raddr=mmap(NULL,CHUNK+PGA,PROT_READ,MAP_SHARED,fd,0);
  if(raddr==(void*)-1){perror("mmap(socket)");return 2;}
  char *addr=(char*)ALIGN_UP(raddr,PGA);
  long zc=0,cp=0; struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
  for(;;){
    struct pollfd pf={.fd=fd,.events=POLLIN}; poll(&pf,1,2000);
    struct tcp_zerocopy_receive z; memset(&z,0,sizeof z);
    z.address=(unsigned long)addr; z.length=CHUNK; socklen_t zl=sizeof z;
    if(getsockopt(fd,IPPROTO_TCP,TCP_ZEROCOPY_RECEIVE,&z,&zl)==-1){perror("TCP_ZEROCOPY_RECEIVE");break;}
    if(z.length){ zc+=z.length; madvise(addr,z.length,MADV_DONTNEED); }
    if(z.recv_skip_hint){ ssize_t n=recv(fd,rbuf,z.recv_skip_hint<(1<<20)?z.recv_skip_hint:(1<<20),0); if(n<=0)break; cp+=n; }
    else if(!z.length){ ssize_t n=recv(fd,rbuf,1<<20,0); if(n<=0)break; cp+=n; }
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double dt=(t1.tv_sec-t0.tv_sec)+(t1.tv_nsec-t0.tv_nsec)/1e9;
    if(dt>=secs){ long tot=zc+cp;
      printf("ZEROCOPY RX: %.1f Mbit/s | zero-copied %.1f%% (%ldMB zc / %ldMB copy)\n",
             tot*8.0/dt/1e6, tot?100.0*zc/tot:0.0, zc>>20, cp>>20); break; }
  }
  return 0;
}
