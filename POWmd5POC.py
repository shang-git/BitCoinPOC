'''
   Name   : POWmd5POC.py
   Ver.   : 2017-0511-00
   Author : shang
'''

import hashlib
import sys
import time

letterWithZeros = { '0' : 4, '1' : 3, '2' : 2, '3' : 2,
                    '4' : 1, '5' : 1, '6' : 1, '7' : 1,
                    '8' : 0, '9' : 0, 'A' : 0, 'B' : 0,
                    'C' : 0, 'D' : 0, 'E' : 0, 'F' : 0  }

def countHeadZeroBits( latterList ):
    zeroCount = 0
    for latter in latterList:
        zeroNum = letterWithZeros[latter]
        zeroCount = zeroCount + zeroNum
        if (zeroNum != 4):
            break
    return zeroCount

def miner( lastHashStr , powQualityLimit, hashAlgorithm ):
    headZeros      = 0
    findZeroBitNum = 0
    exeNumCount    = 0

    while (headZeros < powQualityLimit):
        findZeroBitStr = str(findZeroBitNum)
        blockHashStr = lastHashStr + findZeroBitStr

        if( hashAlgorithm == 'md5' ):
            m = hashlib.md5()
        elif ( hashAlgorithm == 'sha1' ):
            m = hashlib.sha1()
        elif ( hashAlgorithm == 'sha256' ):
            m = hashlib.sha256()
        else:
            m = hashlib.md5()

        m.update(blockHashStr.encode('utf-8'))
        hashStr = m.hexdigest().upper()
        latterList = list(hashStr)

        headZeros = countHeadZeroBits(latterList)

        findZeroBitNum += 1
        exeNumCount += 1

    return ( exeNumCount , hashStr )

##########################

hashAlgorithmOPs = { 'md5' : 1, 'sha1' : 1, 'sha256' : 1 }

##########################

initTransStr   = "Trans string"
transHashStr   = ""
# findZeroBitStr = ""

# init the 1st hash string.
m = hashlib.md5()
m.update(initTransStr.encode('utf-8'))
transHashStr = m.hexdigest().upper()
lastHashStr = transHashStr

# exec 10 times for calculating average
pocExecTimes       = 10
totalMinerCalTimes = 0
avgMinerCalTimes   = 0

if( len(sys.argv) <= 3 ):
    print("Usage : POWmd5POC.py <startBits> <endBits> <Hash Algorithm>\n")
    print("Hash Algorithm :")
    print("  md5, sha1, sha256")
    exit(0)

startBits     = int(sys.argv[1])
endBits       = int(sys.argv[2])
hashAlgorithm = sys.argv[3]

if( hashAlgorithm not in hashAlgorithmOPs ):
    print( sys.argv[3] + " is not our Hash Algorithm.")
    exit(0)

#  begins with how many num of bits
for pocThreshold in range(startBits, (endBits + 1) ):
    lastHashStr = transHashStr
    totalMinerCalTimes = 0
    execStartTime = time.time()

    # exec pocExecTimes times
    for i in range(0, pocExecTimes):
        # print(str(i + 1) + " nd round.")
        (minerCalTimes, lastHashStr) = miner(lastHashStr, pocThreshold, hashAlgorithm)
        # print(str(minerCalTimes) + " , " + lastHashStr)
        totalMinerCalTimes = totalMinerCalTimes + minerCalTimes

    execEndTime = time.time()
    exePOCTime = execEndTime - execStartTime

    avgMinerCalTimes = totalMinerCalTimes / pocExecTimes
    print( str(pocThreshold) + ", " + str(avgMinerCalTimes) + ", " + str(exePOCTime))
