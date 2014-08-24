#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<lzo1x.h>

int main(void) {
  char* data = "imagefs hello world I like imagefs so much, yes yes yes!!!!!!!!!!!!! askjdhakjshdak jshkah skahsflahsdlfh asldfh saldjfhasl dhasldhk falsdhf alsjh";
  int datalen = strlen(data);
  char compressed[1000];
  char tmp[1024000];
  unsigned long complen = sizeof(compressed);
  int ret = lzo1x_999_compress(data, datalen, compressed, &complen, tmp);
  write(1, compressed, complen);
}
