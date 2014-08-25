import sys

from construct import *

script_struct = GreedyRange(Struct("statement",
	Anchor("start"),
	ULInt16("length"),
	Enum(ULInt16("type"),
 		RUN = 0,
 		PRINT = 3,
 		_default_ = Pass,
  ),
  If(lambda ctx: ctx.length > 0,
    Switch("args", lambda ctx: ctx.type, 
	  	{
	  		"PRINT": String("text", lambda ctx: ctx.length - 4),
				"RUN": Struct("exec", 
					Padding(6),
					ULInt8("argc"),
					ULInt8("envc"),
					CString("program"),
					Array(lambda ctx: ctx.argc, CString("arg")),
					Array(lambda ctx: ctx.envc, CString("env")),
					Anchor("end"),
					Padding(lambda ctx: ctx._.length - ctx.end + ctx._.start),
        )
	  	},
	  	default = String("unknown", lambda ctx: ctx.length - 4)
    ),
  )
))

input = open(sys.argv[1], "rb")
data = input.read()
input.close()

script = script_struct.parse(data)
for stmt in script:
	if stmt.length == 0:
		continue
	elif stmt.type == 'PRINT':
		print 'echo "%s"' % stmt.args
	elif stmt.type == 'RUN':
		print ' '.join(stmt.args.arg)
	else:
		print '# CMD%d %s' % (stmt.type, stmt.args)
	
