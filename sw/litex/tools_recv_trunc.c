/* Drain TCP with MSG_TRUNC (NO copy_to_user) -> RX ceiling if the copy were free. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
int main(int c,char**v){
  if(c<3){fprintf(stderr,"usage: %s ip port [cport] [secs]\n",v[0]);return 1;}
  int fd=socket(AF_INET,SOCK_STREAM,0);
  if(c>3&&atoi(v[3])){struct sockaddr_in l={0};l.sin_family=AF_INET;l.sin_port=htons(atoi(v[3]));
    int o=1;setsockopt(fd,SOL_SOCKET,SO_REUSEADDR,&o,sizeof o);bind(fd,(void*)&l,sizeof l);}
  struct sockaddr_in a={0};a.sin_family=AF_INET;a.sin_port=htons(atoi(v[2]));
  inet_pton(AF_INET,v[1],&a.sin_addr);
  if(connect(fd,(void*)&a,sizeof a)){perror("connect");return 1;}
  double secs=c>4?atof(v[4]):8.0;
  static char buf[262144]; long tot=0; struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
  for(;;){ ssize_t n=recv(fd,buf,sizeof buf,MSG_TRUNC); if(n<=0)break; tot+=n;
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double dt=(t1.tv_sec-t0.tv_sec)+(t1.tv_nsec-t0.tv_nsec)/1e9;
    if(dt>=secs){printf("MSG_TRUNC RX: %.1f Mbit/s (%ld MB / %.2fs)\n",tot*8.0/dt/1e6,tot>>20,dt);break;}
  } return 0;
}
