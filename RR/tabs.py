
#   uh, maybe use expandtabs()?
def tabs2Spaces ( sIn, tabSize = 4 ):
    sOut = ""
    parts = sIn.partition ( '\t' )
    while len ( parts[1] ) > 0:             #   more tabs ...
        sOut += parts[0]
        i = len ( sOut )
        sOut += ' ' * (tabSize - (i % tabSize))
        parts = parts[2].partition ( '\t' )
    sOut += parts[0]
    return sOut

def spaces2Tabs ( sIn, tabSize = 4 ):
    sOut = ""
    #   Substitute only if the non-space character after space(s) is at 
    #   a tab stop position.
    lenIn = len ( sIn )
    iS = 0;     iIn = sIn.find ( ' ', iS )
    while (iIn >= 0) and (iIn < lenIn):
        sOut += sIn[iS:iIn]
        #   Position of next non-space.
        iNS = iIn
        while (iNS < lenIn) and (sIn[iNS] == ' '):
            iNS += 1
            if iNS % tabSize == 0:
                sOut += "\t";   iIn = iNS
        sOut += " " * ((iNS - iIn) % tabSize)
        iS = iNS;   iIn = sIn.find ( ' ', iS )
    sOut += sIn[iS:]
    return sOut

