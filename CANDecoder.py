#!Python
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

global pp
pp=PdfPages('40mph Breaking.pdf')



file=open('40mph Breaking.xls','r') #opens the data file produced be the VectorHercules software and the Gryphon S3 Hardware
data=file.readlines() #Load the entire file into memory
file.close()

#initialize variables
times=[]
IDs=[]
DLCs=[]
payloads=[]
hexpayloads=[]
IDLengths={}
message = []
for line in data[5000:]: #Parse each line
    #Split each line where the commas are. This may need to be tab characters if the data was tab delimited
    entries=line.split(',')
    #print entries #(only for debugging)
    try:
        #convert timestamp (hours:minutes:seconds:millis:micros) into plain seconds
        timestamp=entries[0]
        #timeParts=timestamp.split(':')
        #time=float(timeParts[0])*3600 + float(timeParts[1])*60 + float(timeParts[2]) + float(timeParts[3])*0.001 + float(timeParts[4])*0.000001
        time=float(timestamp)
        
        #print time
        times.append(time)

        #build a list of IDs
        
        identifier=entries[6]
        #IDparts=identifier.split(':')
        IDs.append(identifier[3:6])
        
        dataLengthCode=entries[5]
        #DLCparts=dataLengthCode.split(':')
        DLCs.append(dataLengthCode[4])

        #Build the IDLength dictionary
        IDLengths[identifier[3:6]]=int(dataLengthCode[4])
        
        #parse the message
        messagetemp=entries[7].split(':')
        message=messagetemp[1].split(' ')
        data=[]
        hexdata=[]
        #print message
        for d in message[:-1]:
            data.append(int(d,16))
        #print data
        payloads.append(data)
        hexpayloads.append(message[:-1])
    except IndexError:
        pass
    

#Data Length Analysis for each ID
#print ('CAN ID (Hex) -> Data Length')
#IDList=IDLengths.keys()
#IDList.sort()
#for key in IDList:
#    print (key+' -> %g' %IDLengths[key])

#print 'CAN ID (Dec) -> Data Length'
#for key in IDList:
#    print `int(key,16)`+' -> %g' %IDLengths[key]   


#Timing Analysis
print ('CAN ID (Hex) -> Counts Per time (Hz) or ')
#totalTime=float(times[-1]-times[0])
#print totalTime
#for key in IDList:
#    occurance=IDs.count(key)
#    print key+' -> %g Hz or %g sec' %((occurances/totalTime),totalTime/float(occurances))

#calculate number of Bytes
totalBytes=0
for key in IDList:
    totalBytes+=int(IDLengths[key])
print ('There are %g unique IDs in the log file' %len(IDLengths))
print ('Total number of bytes to examine in the log: %g' %totalBytes)

def plotDatavsTime(ID,times=times,IDs=IDs,data=payloads,IDLengths=IDLengths):
        X=[]
        Y=[]
        startTime=times[0]
        endTime=times[-1]
        for location in range(IDLengths[ID]):
            Y.append([])
        for i,t,d in zip(IDs,times,data):
            if i==ID:
                X.append(t)
                for location in range(len(Y)):
                    Y[location].append(d[location])
        for location in range(IDLengths[ID]):
            outputName='Time History of CAN ID %s for byte %g' %(ID,location)
            plt.plot(X,Y[location],'.')
            plt.xlim( startTime, endTime )
            plt.title(outputName)
            plt.ylabel('Value')
            plt.xlabel('Time [sec]')
            #f=plt.savefig(outputName+'.png')
            #plt.savefig(outputName+'.pdf')
            pp.savefig()
            plt.close()
            
            #print 'File %s was written.' %outputName
                  


    
def plotEvenDatavsTime(ID,times=times,IDs=IDs,data=hexpayloads,IDLengths=IDLengths):
        X=[]
        Y=[]
        startTime=times[0]
        endTime=times[-1]
        for location in range(0,IDLengths[ID],2):
            #print location
            Y.append([])
        
        for i,t,d in zip(IDs,times,data):
            if i==ID:
                X.append(t)
                #print d
                for location in range(len(Y)):
                    try:
                        Y[location].append(int(d[2*location]+d[2*location+1],16))
                    except IndexError:
                        #print 'Something is screwy!'
                        #print location
                        #print d
                        Y.pop(location)
                        pass
                    
        for location in range(len(Y)):
            outputName='Time History of CAN ID %s for bytes %g and %g' %(ID,2*location,2*location+1)
            plt.plot(X,Y[location],'.')
            plt.xlim( startTime, endTime )
            plt.title(outputName)
            plt.ylabel('Value')
            plt.xlabel('Time [sec]')
            #f=plt.savefig(outputName+'.png')
            #plt.savefig(outputName+'.pdf')
            pp.savefig()
            plt.close()
            
            #print 'File %s was written.' %outputName
                  

def plotOddDatavsTime(ID,times=times,IDs=IDs,data=hexpayloads,IDLengths=IDLengths):
        X=[]
        Y=[]
        startTime=times[0]
        endTime=times[-1]
        for location in range(1,IDLengths[ID]-1,2):
            #print location
            Y.append([])
        for i,t,d in zip(IDs,times,data):
            if i==ID:
                X.append(t)
                for location in range(len(Y)):
                    try:
                        Y[location].append(int(d[2*location+1]+d[2*location+2],16))
                    except IndexError:
                        Y.pop(location)
                        pass
        for location in range(len(Y)):
            outputName='Time History of CAN ID %s for bytes %g and %g' %(ID,2*location+1,2*location+2)
            plt.plot(X,Y[location],'.')
            plt.xlim( startTime, endTime )
            plt.title(outputName)
            plt.ylabel('Value')
            plt.xlabel('Time [sec]')
            #f=plt.savefig(outputName+'.png')
            #plt.savefig(outputName+'.pdf')
            pp.savefig()
            plt.close()
            
            #print 'File %s was written.' %outputName
                      
for key in IDList:
#for key in ['308']:
    plotDatavsTime(key)
    plotEvenDatavsTime(key)
    plotOddDatavsTime(key)
    print ('Done Plotting Data for '+key)
            
pp.close()              
