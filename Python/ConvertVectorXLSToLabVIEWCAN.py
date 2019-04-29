#-------------------------------------------------------------------------------
# Name:        Convert Vector Log Files to lABVIEW CAN Fields
# Purpose:
#
# Author:      jeremy-daily
#
# Created:     24/10/2012
# Copyright:   (c) jeremy-daily 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import os.path
import ctypes

def convertFile(f):
    fileHandle=open(f,'r')
    lines=fileHandle.readlines()
    fileHandle.close()

    #Enter the IDs to remove from the CAN stream

    #Remove non Speed VBox data
    blacklist=['301','302','303','304','305']

    #Remove all but '309', '17c', '156', '302', '1d0', '301'
    blacklist=['84','151', '165', '185', '1a4', '1a6', '1aa', '1b0', '1dc', '1ea', '1ed', '21e', '221', '255', '294', '295','301', '303', '304', '305', '306','307','308','320', '324', '328', '333', '372', '374', '377', '378', '386', '39', '3d7', '3d9', '401', '405', '40c', '428', '42d', '454', '465', '6c1']

    #Remove nothing
    #blacklist=[]


    #initialize variables
    times=[]
    IDs=[]
    DLCs=[]
    payloads=[]
    hexpayloads=[]
    IDLengths={}
    delays=[0]
    channels=[]

    for line in lines:
        entries=line.split(',')
        #print(entries) #(only for debugging)
       # try:
            #build a list of IDs
           #if entries[6][0]!='B':
        #identifierTemp=entries[6].split(':')
        identifier=entries[7] #identifierTemp[1]
        if identifier in blacklist:
                continue
                print(identifier)
        else:
                IDs.append(identifier)

        #convert timestamp (hours:minutes:seconds:millis:micros) into plain seconds
        timestamp=entries[0]
        #timeParts=timestamp.split(':')
        #time=float(timeParts[0])*3600 + float(timeParts[1])*60 + float(timeParts[2]) + float(timeParts[3])*0.001 + float(timeParts[4])*0.000001
        time=float(timestamp)
        #print time
        times.append(time)

        channel=int(entries[4][-1])-1
        channels.append(channel)
        
        dataLengthCode=entries[5]
        DLCs.append(dataLengthCode[4])

        #Build the IDLength dictionary
        IDLengths[identifier]=int(dataLengthCode[4])

        #parse the message
        #messagetemp=entries[7].split(':')
        #message=messagetemp[1].split(' ')
        hexpayloads.append(entries[9:-1])
      #  except IndexError:
      #      pass

    IDList=list(IDLengths.keys())
    IDList.sort()
    print(IDList)
    for i in range(1,len(times)):
        #compute the differences between messages in microseconds
        delays.append(int((times[i]-times[i-1])*1000000))

    newFile=open(f[0:-4]+'_ForLabVIEW_reduced.csv','w')
    for delay,ID,DLC,hexMessage,chan in zip(delays,IDs,DLCs,hexpayloads,channels):
        #print delay
        #print ID
        #print DLC
        #print(hexMessage)
        data=''
        for h in hexMessage:
            data+=h #Data[0] is the MSB
        #print(data)
        bigData=int(data,16)
        
        data2=ctypes.c_uint32(bigData).value
        #print(data2)
        #print(hex(data2))
        data1=bigData>>32
        #print(data1)
        #print(hex(data1))
        
        #print(delay)
        #print(ID)
        #print(DLC)
        newFile.write('%i,%i,%i,%i,%i,%i\n' %(delay,int(ID,16),int(DLC),data1,data2,chan))
    newFile.close()


#files=os.listdir(os.getcwd())
#for f in files:
#    if f[-3:]=='xls':
#        print(f)
#        convertFile(f)
convertFile('ford flex 31013008 vbox 12 50 mph stop w rt lane chg REDUCED.xls')
