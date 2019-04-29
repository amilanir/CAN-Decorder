#!Python
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

filesOfInterest=[]
pathOfInterest=os.getcwd()
#pathOfInterest="C:\\Users\\dailyadmin\\Documents\\Dropbox\\2013 Ford Flex EDR Accuracy\\2014 Flex Data Runs Oct 13 2013"
print(pathOfInterest)
os.chdir(pathOfInterest)
for filename in os.listdir(pathOfInterest):
    if filename[-3:]=='xls':
        filesOfInterest.append(filename)
filesOfInterest=['ford flex 31013017 vbox 21 figure 8.xls']
    
print(filesOfInterest)


global pp
for filename in filesOfInterest[0:]:
    pp=PdfPages(filename+' VBOX Output.pdf')
    
    
    
    file=open(filename,'r') 
    data=file.readlines() #Load the entire file into memory
    file.close()
    
    #initialize variables
    times=[]
    IDs=[]
    DLCs=[]
    payloads=[]
    hexpayloads=[]
    IDLengths={}
    
    for line in data[3:]: #Parse each line
        #Split each line where the commas are. This may need to be tab characters if the data was tab delimited
        entries=line.split(',')
        #print entries #(only for debugging)
     #   try:
        timestamp=float(entries[0])
        times.append(timestamp)
    
        #build a list of IDs
        
        identifier=entries[7]
        IDs.append(identifier)
        
        dataLengthCode=entries[5]
        DLCs.append(dataLengthCode[4])
    
        #Build the IDLength dictionary
        IDLengths[identifier]=int(dataLengthCode[4])
        
        #parse the message
        message=entries[9:]
        data=[]
        hexdata=[]
        #print message
        for d in message[:-1]:
            data.append(int(d,16))
        #print data
        payloads.append(data)
        hexpayloads.append(message[:-1])
        #except IndexError:
      #      pass
        
    
    
    #Data Length Analysis for each ID
    print('CAN ID (Hex) -> Data Length')
    IDList=sorted(IDLengths.keys())
   
    for key in IDList:
        print(key+' -> %g' %IDLengths[key])
    
    #print 'CAN ID (Dec) -> Data Length'
    #for key in IDList:
    #    print `int(key,16)`+' -> %g' %IDLengths[key]   
    
    
    #Timing Analysis
    print('CAN ID (Hex) -> Counts Per time (Hz) or ')
   
    totalTime=float(times[-1]-times[0])
    print( totalTime)
    for key in IDList:
        occurances=IDs.count(key)
        print (key+' -> %g Hz or %g sec' %((occurances/totalTime),totalTime/float(occurances)))
    
    #calculate number of Bytes
    totalBytes=0
    for key in IDList:
        totalBytes+=int(IDLengths[key])
    print( 'There are %g unique IDs in the log file' %len(IDLengths))
    print( 'Total number of bytes to examine in the log: %g' %totalBytes)
    
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
                plt.plot(X,Y[location],'.',rasterized=True)
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
                plt.plot(X,Y[location],'.',rasterized=True)
                plt.xlim( startTime, endTime )
                plt.title(outputName)
                plt.ylabel('Value')
                plt.xlabel('Time [sec]')
                #f=plt.savefig(outputName+'.png')
                #plt.savefig(outputName+'.pdf')
                #plt.show()
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
                plt.plot(X,Y[location],'.',rasterized=True)
                plt.xlim( startTime, endTime )
                plt.title(outputName)
                plt.ylabel('Value')
                plt.xlabel('Time [sec]')
                #f=plt.savefig(outputName+'.png')
                #plt.savefig(outputName+'.pdf')
                pp.savefig()
                plt.close()
                
                #print 'File %s was written.' %outputName
                          
    #for key in IDList:
    #try:
    #for key in ['74','84','3a8']:
    for key in ['302']:
        #plotDatavsTime(key)
        plotEvenDatavsTime(key)
        #plotOddDatavsTime(key)
        print ('Done Plotting Data for '+key)
    #except KeyError:
    #    pass            
    pp.close() 
    #plt.show()             
    print('Done graphing '+filename)
print('Done Converting all Files.')