#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/wait.h>
int main(int c,char**v){ signal(SIGPIPE,SIG_IGN); signal(SIGCHLD,SIG_IGN);
  int ls=socket(AF_INET,SOCK_STREAM,0),o=1; setsockopt(ls,SOL_SOCKET,SO_REUSEADDR,&o,sizeof o);
  struct sockaddr_in a={0};a.sin_family=AF_INET;a.sin_port=htons(atoi(v[1]));a.sin_addr.s_addr=INADDR_ANY;
  bind(ls,(void*)&a,sizeof a); listen(ls,8);
  static char buf[262144];
  for(;;){ int fd=accept(ls,0,0); if(fd<0)continue;
    if(fork()==0){ close(ls); while(send(fd,buf,sizeof buf,0)>0){} close(fd); _exit(0); }
    close(fd); }
}
