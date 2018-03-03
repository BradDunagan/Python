import sys
import os
import re

import tabs


print ( "1234567812345678123456781234567812345678123456781234567812345678" )
st = "12345678\tmore\tlast"
print ( st + "  " + str ( len ( st ) ) )
ss = tabs.tabs2Spaces ( st, 8 )
print ( ss + "  " + str ( len ( ss ) ) )
st = tabs.spaces2Tabs ( ss, 8 )
print ( st + "  " + str ( len ( st ) ) )

st = "12345678\t\tm o r e\t\tlast"
print ( st + "  " + str ( len ( st ) ) )
ss = tabs.tabs2Spaces ( st, 8 )
print ( ss + "  " + str ( len ( ss ) ) )
st = tabs.spaces2Tabs ( ss, 8 )
print ( st + "  " + str ( len ( st ) ) )


msg = "Hello?"
print ( msg )

#   Fix error macros.
#
#   Change error macros that look like this -
#       #define	AE_RSP_ENT_NOT_SELECTED		(-3601)
#   to this -
#       #define	AE_RSP_ENT_NOT_SELECTED		(AE_USER_ERROR | 0x00046001)

inFilePath = sys.argv[1]

inFileExt   = os.path.splitext ( inFilePath )

outFilePath = inFilePath + ".fix" + inFileExt[1]

print ( "inFilePath:  " + inFilePath )
print ( "outFilePath: " + outFilePath )

#   File ops -
#       https://docs.python.org/3.6/library/functions.html#open
#
#   Formatting -
#       https://docs.python.org/3.6/library/stdtypes.html#str.format
#       https://docs.python.org/3.6/library/string.html#formatstrings

inFile  = open ( inFilePath )

outFile = open ( outFilePath, 'w' )

bFirstGroup = 1

for lineIn in inFile:
    ss = tabs.tabs2Spaces ( lineIn, 4 )
    if not ss.startswith ( "#define AE_" ):
        outFile.write ( lineIn )
        continue
    print ( ss )
    #   ss is expected to be something like -
    #   #define	AE_RSP_EDITOR_IS_CLOSED		(-3010)
    i = ss.find ( "(-" )
    if i < 0:
        outFile.write ( lineIn )
        continue
    lineOut = ss[:i]
    i += 2
    if bFirstGroup:
        j = i;      n = ""
        while ss[j].isdigit():
            n += ss[j];     j += 1
        if len ( n ) < 3:
            #   Must be a first group error number.
            lineOut += "(AE_USER_ERROR | 0x000100{:02X})\n".format ( int ( n ) )
            outFile.write ( tabs.spaces2Tabs ( lineOut, 4 ) )
            continue
        bFirstGroup = 0     #   End of first group.

    #   expect four digits
    if not ss[i:i+4].isnumeric():
        outFile.write ( lineIn )
        continue
    group    = int ( ss[i] ) + 1
    subgroup = int ( ss[i+1] )
    n        = int ( ss[i+2:i+4] )
    lineOut += "(AE_USER_ERROR | 0x000{:X}{:X}{:03X})\n".format ( group, subgroup, n )
    outFile.write ( tabs.spaces2Tabs ( lineOut, 4 ) )

inFile.close();     outFile.close()

print ( "done" )

