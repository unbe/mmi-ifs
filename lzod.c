#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<lzo1x.h>

int main(int argc, char* argv[]) {
  printf("start\n");
  printf("open: %s\n", argv[1]);
  FILE *fp = fopen(argv[1], "rb");
  if(!fp) {
    printf("COCK!\n");
    return -1;
  } 
  unsigned char *compdata = malloc(1024*1024*100);
  unsigned long complen = fread(compdata, 1, 1024*1024*100, fp);
  printf("read: %lu\n", complen);
  fclose(fp);
  
  unsigned char* dstdata = malloc(1024*1024*100);
  unsigned long dstlen = 1024*1024*100;
  unsigned char tmp[1024*100];
  int r = lzo1x_decompress(compdata, complen, dstdata, &dstlen, tmp);
  printf("r: %d\n", r);
  printf("dstlen: %ld\n", dstlen);

  fp = fopen(argv[2], "w+b");
  fwrite(dstdata, 1, dstlen, fp);
  fclose(fp);
}
