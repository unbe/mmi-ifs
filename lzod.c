#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<lzo/lzo1x.h>

int main() {
  long buflen = 64*1024*1024;  // <64k blocks
  unsigned char *compdata = malloc(buflen);
  long bytes;
  long complen = 0;
  while ((bytes = read(0, compdata + complen, buflen))) {
    if (bytes < 0) {
      perror("Read");
      return -1;
    }
    complen += bytes;
    buflen -= bytes;
    if (buflen <= 0) {
      fprintf(stderr, "Input file too long\n");
      return -1;
    }
  }
  fprintf(stderr, "compressed length: %ld\n", complen);
  
  // No idea what's the decompressed size. 50x should be safe.
  unsigned long dstlen = complen*50;
  unsigned char* dstdata = malloc(dstlen);

  unsigned char tmp[1024*1024];
  int r = lzo1x_decompress(compdata, complen, dstdata, &dstlen, tmp);
  fprintf(stderr, "result: %d\n", r);
  fprintf(stderr, "uncompressed length: %ld\n", dstlen);

  write(1, dstdata, dstlen);
  return r;
}
