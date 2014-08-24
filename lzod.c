#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<lzo/lzo1x.h>
#include<sys/stat.h>

int main(int argc, char* argv[]) {
  struct stat st;
  stat(argv[1], &st);

  if (argc < 2) {
    fprintf(stderr, "Usage: lzod <input> <output>");
    return -1;
  }

  FILE *fp = fopen(argv[1], "rb");
  if (!fp) {
    perror(argv[1]);
    return -1;
  } 

  unsigned long complen = st.st_size;
  unsigned char *compdata = malloc(complen);
  if (complen != fread(compdata, 1, complen, fp)) {
    perror("Read");
  }
  fprintf(stderr, "read: %lu\n", complen);
  fclose(fp);
  
  unsigned long dstlen = complen*10;
  unsigned char* dstdata = malloc(dstlen);
  unsigned char* tmp = malloc(dstlen);
  int r = lzo1x_decompress(compdata, complen, dstdata, &dstlen, tmp);
  fprintf(stderr, "result: %d\n", r);
  fprintf(stderr, "uncompressed length: %ld\n", dstlen);

  fp = fopen(argv[2], "w+b");
  if (!fp) {
    perror(argv[2]);
    return -1;
  } 
  if (fwrite(dstdata, 1, dstlen, fp) != dstlen) {
    perror("Write");
  }
  fclose(fp);
  
  return r;
}
