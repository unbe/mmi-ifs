import sys
from construct import *

# http://www.qnx.com/developers/docs/660/index.jsp?topic=%2Fcom.qnx.doc.neutrino.building%2Ftopic%2Fload_process_Boot_header.html

boot_header = Struct("boot_header",
  Enum(ULInt32("signature"),
		CORRECT = 0x00FF7EEB,
		_default_ = Pass,
	),
  ULInt16("version"),
  BitStruct("flags1",
		Flag("STARTUP_HDR_FLAGS1_VIRTUAL"),
		Flag("STARTUP_HDR_FLAGS1_BIGENDIAN"),
		Enum(BitField("Compression", 4),
			STARTUP_HDR_FLAGS1_COMPRESS_NONE = 0,
			STARTUP_HDR_FLAGS1_COMPRESS_ZLIB = 0x01,
			STARTUP_HDR_FLAGS1_COMPRESS_LZO  = 0x02,
			STARTUP_HDR_FLAGS1_COMPRESS_UCL  = 0x03,
		  _default_ = Pass
 		),
		Padding(2),
  ),
  ULInt8("flags2_unused"),
  ULInt16("header_size"),
  Enum(ULInt16("machine"),
		EM_NONE = 0,
		EM_M32 = 1,                 # /* AT&T WE 32100 */
		EM_SPARC = 2,               # /* Sun SPARC */
		EM_386 = 3,                 # /* Intel 80386 */
		EM_68k = 4,                 # /* Motorola 68000 */
		EM_88k = 5,                 # /* Motorola 88000 */
		EM_486 = 6,                 # /* Intel 80486 */
		EM_860 = 7,                 # /* Intel i860 */
		EM_MIPS = 8,                # /* MIPS RS3000 Big-Endian */
		EM_S370 = 9,                # /* IBM system 370 */
		EM_MIPS_RS3_LE = 10, # /* MIPS RS3000 Little-Endian */
		EM_RS6000 = 11,              # /* RS6000 */
		EM_UNKNOWN12 = 12,
		EM_UNKNOWN13 = 13,
		EM_UNKNOWN14 = 14,
		EM_PA_RISC = 15,             # /* PA_RISC */
		EM_nCUBE = 16,               # /* nCUBE */
		EM_VPP500 = 17,              # /* Fujitsu VPP500 */
		EM_SPARC32PLUS = 18, # /* Sun Sparc 32+ */
		EM_UNKNOWN19 = 19,
		EM_PPC = 20,                 # /* Power PC */
		EM_ARM = 40,    # /* ARM */
		EM_SH = 42,             # /* Hitachi SH */
		_default_ = Pass
	),
  ULInt32("startup_vaddr"),
  ULInt32("paddr_bias"),
  ULInt32("image_paddr"),
  ULInt32("ram_paddr"),
  ULInt32("ram_size"),
  ULInt32("startup_size"),
  ULInt32("stored_size"),
  ULInt32("imagefs_paddr"),
  ULInt32("imagefs_size"),
  ULInt16("preboot_size"),
  ULInt16("zero0"),
  Array(3, ULInt32("zero3"))
)

input = open(sys.argv[1], "rb")
data = input.read()
input.close()

header = boot_header.parse(data)
print header
if header.stored_size == len(data):
	print "stored_size OK"
else:
	print "stored_size NOK"

stored_imagefs = header.stored_size - header.startup_size
if stored_imagefs == header.imagefs_size:
	print "imagefs_size OK, uncompressed"
elif stored_imagefs < header.imagefs_size:
	print "imagefs_size OK, compressed %d -> %d" % (header.imagefs_size, stored_imagefs)
if stored_imagefs > header.imagefs_size:
	print "imagefs_size NOK: imagefs %d, stored %d" % (header.imagefs_size, stored_imagefs)

startup = open(sys.argv[1] + ".startup", "wb")
startup.write(data[:header.startup_size])
print "Wrote " + str(startup)
startup.close()

imagefs = open(sys.argv[1] + ".imagefs", "wb")
imagefs_data = data[header.startup_size:]
imagefs.write(imagefs_data)
print "Wrote " + str(imagefs)
imagefs.close()

if header.flags1.Compression == 'STARTUP_HDR_FLAGS1_COMPRESS_LZO': 
	import lzo
	print "Attempting LZO decompression"
	d_imagefs_data = lzo.decompress(imagefs_data)
	print "Decompressed %d -> %d" % (len(imagefs_data), len(d_imagefs_data))
	print "imagefs size %s" % ("OK" if len(d_imagefs_data) == header.imagefs_size else "NOK") 

