### lib for amp
import time
import numpy as np
import re

import config

from scp import SCPClient
from datetime import datetime
from scipy.signal import find_peaks
import glob
import pandas as pd

'''Initial Release V1p0
   11/25/2024 added support for 16.3 CommScope Code, changes for 96MHz subband,
     and changed time offset to fixed -0.194uS per BCM guidance.

12/09/2024.  Added support for capturing North Monitor AFE  stats (LAFE core0)
'''



# def complex_to_mag_db(real, imag):
#     """Converts complex data (real and imaginary parts) to magnitude in dB."""
#     data = []
#     for real, im in zip(real,imag):
#         # Calculate magnitude using Euclidean distance (sqrt(real^2 + imag^2))
#         magnitude = np.sqrt(re**2 + im**2)
#         # Convert magnitude to dB (20 * log10(magnitude))
#         magnitude_db = 20 * np.log10(magnitude)
#         data.append(magnitude_db)
#     return data

# def split_list_in_half(lst):'
#     """Splits a list into two halves."""
#     midpoint = len(lst) // 2  # Use floor division to get the middle index
#     first_half = lst[:midpoint]
#     second_half = lst[midpoint:]
#     return [first_half, second_half]


# def hal_comm(channel, command):
#     # get into the hal> and send the command
#     channel.send('\r\n')
#     time.sleep(.1)
#     output = channel.recv(4096).decode("utf-8")
#     print(output)
#     while True:
#         match = re.search("# ",output)  # if current location is in root
#         if match:
#             channel.send('exit\n')
#             time.sleep(2)
#             output = channel.recv(4096).decode("utf-8")
#             print(output)
#             continue
#         match = re.search("login:",output)  # if current location is login
#         if match:
#             channel.send('cli\n')
#             time.sleep(1)
#             output = channel.recv(4096).decode("utf-8")
#             print(output)
#             continue
#         match = re.search("Password:",output)   # if current location is password
#         if match:
#             channel.send('cli\n')
#             time.sleep(1)
#             output = channel.recv(4096).decode("utf-8")
#             print(output)
#             continue
#         match = re.search("FDX-AMP>",output)    # if current location is FDX-AMP>
#         if match:
#             channel.send('hal\n')
#             time.sleep(1)
#             channel.send('\r\n')
#             time.sleep(1)
#             output = channel.recv(4096).decode("utf-8")
#             print(output)
#             continue
#         match = re.search("FDX-AMP\(",output)   # if current location is somewhere else in FDX-AMP
#         if match:
#             channel.send('exit\n')
#             time.sleep(1)
#             output = channel.recv(4096).decode("utf-8")
#             print(output)
#             continue
#         match = re.search("hal/",output)    # if current location is in some hal subdirectory
#         if match:
#             channel.send('cd \\ \r\n')   # getting back to the root directory in the hal, in case hal was left in another directory
#             time.sleep(2)
#             channel.send('\r\n')
#             #time.sleep(1)
#             output = channel.recv(128000).decode("utf-8")
#             print(output)
#             return(output)
#         channel.send('\r\n')
#         #time.sleep(1)
#         output = channel.recv(4096).decode("utf-8")
#         print(output)
#         match = re.search("hal>",output)    # if current location is in hal>
#         if match:
#             channel.send(f'{command} \r\n')   # type
#             time.sleep(2)
#             channel.send('\r\n')
#             #time.sleep(1)
#             output = channel.recv(128000).decode("utf-8")
#             print(output)
#             return(output)
#         channel.send('\r\n')
#         #time.sleep(1)
#         output = channel.recv(4096).decode("utf-8")
#         print(output)


# def rf_comm(channel, command):
#     # get into the FDX-AMP(rfboard)> and send the command
#     channel.send('\n')
#     output = channel.recv(12800)
#     print(output.decode())


# def root_comm(channel, command):
#     # get into the # and send the command
#     channel.send('\r\n')
#     time.sleep(1)
#     output = channel.recv(4096).decode("utf-8")
#     #print(output)
#     while True:
#         match = re.search("# ",output)  # if current location is in root
#         if match:
#             channel.send(f'{command} \n')   # type
#             time.sleep(2)
#             channel.send('\n')
#             #time.sleep(1)
#             output = channel.recv(128000).decode("utf-8")
#             #print(output)
#             return(output)
#         match = re.search("login:",output)  # if current location is login
#         if match:
#             channel.send('root\n')
#             time.sleep(1)
#             output = channel.recv(4096).decode("utf-8")
#             #print(output)
#             continue
#         match = re.search("Password:",output)   # if current location is password
#         if match:
#             channel.send('Wallingford\n')
#             time.sleep(1)
#             output = channel.recv(4096).decode("utf-8")
#             #print(output)
#             continue
#         match = re.search("FDX-AMP>",output)    # if current location is FDX-AMP>
#         if match:
#             channel.send('exit\n')
#             time.sleep(2)
#             output = channel.recv(4096).decode("utf-8")
#             #print(output)
#             continue
#         match = re.search("FDX-AMP\(",output)   # if current location is somewhere else in FDX-AMP
#         if match:
#             channel.send('exit\n')
#             time.sleep(1)
#             output = channel.recv(4096).decode("utf-8")
#             #print(output)
#             continue
#         match = re.search("hal>",output)    # if current location is in hal>
#         if match:
#             channel.send('exit\r\n')   # type
#             time.sleep(1)
#             channel.send('exit\n')   # type
#             time.sleep(1)
#             output = channel.recv(4096).decode("utf-8")
#             #print(output)
#             continue
#         channel.send('\r\n')
#         #time.sleep(1)
#         output = channel.recv(4096).decode("utf-8")
#         #print(output)


# def hal_comm_console(channel, command):
#     # get into the hal> and send the command
#     channel.write('\r\n'.encode())
#     time.sleep(1)
#     output = channel.read_all().decode("utf-8")
#     #print(output)
#     while True:
#         match = re.search("# ",output)  # if current location is in root
#         if match:
#             channel.write('exit\n'.encode())
#             time.sleep(2)
#             output = channel.read_all().decode("utf-8")
#             #print(output)
#             continue
#         match = re.search("login:",output)  # if current location is login
#         if match:
#             channel.write('cli\n'.encode())
#             time.sleep(1)
#             output = channel.read_all().decode("utf-8")
#             #print(output)
#             continue
#         match = re.search("Password:",output)   # if current location is password
#         if match:
#             channel.write('cli\n'.encode())
#             time.sleep(1)
#             output = channel.read_all().decode("utf-8")
#             #print(output)
#             continue
#         match = re.search("FDX-AMP>",output)    # if current location is FDX-AMP>
#         if match:
#             channel.write('hal\n'.encode())
#             time.sleep(1)
#             channel.write('\r\n'.encode())
#             time.sleep(1)
#             output = channel.read_all().decode("utf-8")
#             #print(output)
#             continue
#         match = re.search("FDX-AMP\(",output)   # if current location is somewhere else in FDX-AMP
#         if match:
#             channel.write('exit\n'.encode())
#             time.sleep(1)
#             output = channel.read_all().decode("utf-8")
#             #print(output)
#             continue
#         match = re.search("hal>",output)    # if current location is in hal>
#         if match:
#             channel.write(f'{command} \r\n'.encode())   # type
#             time.sleep(2)
#             channel.write('\r\n'.encode())
#             #time.sleep(1)
#             output = channel.read_all().decode("utf-8")
#             #print(output)
#             return(output)
#         channel.write('\r\n'.encode())
#         #time.sleep(1)
#         output = channel.read_all().decode("utf-8")
#         #print(output)



def amp_readback(channel,command,prompt='FDX-AMP>',maxTime=8.0):
    error = False
    channel.send(f'{command}\r\n'.encode())   # type
    start_time = time.time()
    time.sleep(0.2)

    if not channel.recv_ready():  # sit and wait until recv is ready
        time.sleep(0.1)
    if channel.recv_ready():
        output = channel.recv(128000).decode("utf-8")

    #print(f'chunk above while loop is: \r\n {chunk}')
    while not prompt in output:  #loop until command prompt read back
        channel.send('\r\n')
        time.sleep(0.1)
        if not channel.recv_ready():  # sit and wait until recv is ready
            time.sleep(0.1)
        if channel.recv_ready():
            #chunk=channel.recv(128000).decode("utf-8")
            output += channel.recv(128000).decode("utf-8")
       # print(f'in while loop, output is: {output} ')
       # print(f'in while loop, chunk is: {chunk} ')
        time.sleep(.5)
        if time.time() > start_time + maxTime:
            print(f'ERROR: {command} failed to return prompt {prompt}')
            error=True
            print('output is: ' + output)

    channel.send('\r\n')  #write return one last time
    time.sleep(0.1)
    if channel.recv_ready():
        #chunk=channel.recv(128000).decode("utf-8")
        output += channel.recv(128000).decode("utf-8")
        print(output)
    return[output,error]



def hal_gather_telemetry(channel,command):
    maxTime=12.0
    channel.send(f'{command} \r\n'.encode())   # type
    start_time = time.time()
    time.sleep(0.1)

    if not channel.recv_ready():  # sit and wait until recv is ready
        time.sleep(0.1)

    if channel.recv_ready():  # recv is ready, now do this.
        output = channel.recv(128000).decode("utf-8")

    #print(f'chunk above while loop is: \r\n {chunk}')
    while not ("SUCCESS" in output and output.count('INFO') > 12):  #loop until hal telemetry command was completely executed
        channel.send('\r\n')
        time.sleep(0.1)
        if not channel.recv_ready():  # sit and wait until recv is ready
            time.sleep(0.1)

        if channel.recv_ready():  # recv is ready, now read
            #chunk=channel.recv(128000).decode("utf-8")
            output += channel.recv(128000).decode("utf-8")
       # print(f'in while loop, output is: {output} ')
       # print(f'in while loop, chunk is: {chunk} ')
        time.sleep(.5)
        if time.time() > start_time+maxTime:

            print(f'{command} failed to return SUCCESS. Closing shell and stopping execution')
            exit
        if 'ERROR EcPnmStats' in output:

            print(f'{command} returned with ERROR in response. Closing shell and stopping execution')
            channel.close()
            exit

        # test1="SUCCESS" in output
        # outCount=output.count('INFO')
        # testINFO=output.count('INFO') > 12
        # print(f'Number of INFO occurances is: {outCount}')
        # print(f'SUCCESS Test check result: {test1}')
        # print(f'INFO Test check result: {testINFO}')
    channel.send('\r\n')  #write return one last time
    time.sleep(0.1)
    if channel.recv_ready():
        #chunk=channel.recv(128000).decode("utf-8")
        output += channel.recv(128000).decode("utf-8")
        print(output)



def hal_gather_telemetry_16p3(channel,command):
    maxTime=12.0
    start_time = time.time()
    channel.send(f'{command} \r\n'.encode())   # type
    time.sleep(0.2)
    channel.send('\r\n')
    output=''
    match_check = False
    timeout = False

    while not channel.recv_ready():  # sit and wait until recv is ready
        #channel.send('\r\n')
        time.sleep(0.25)

    if channel.recv_ready():  # recv is ready, now do this.
        output = channel.recv(128000).decode("utf-8")
        print(output)

    if output.count('INFO') > 5:
        match_check = True

    #print(f'chunk above while loop is: \r\n {chunk}')

    while not (match_check or timeout):  #loop until hal telemetry command was completely executed
        channel.send('\r\n')
        time.sleep(0.25)
        if not channel.recv_ready():
            #channel.send('\r\n')
            time.sleep(0.2)

        if channel.recv_ready():  # recv is ready, now do this.
            time.sleep(0.1)
            output = channel.recv(128000).decode("utf-8")
            print(output)


        #time.sleep(0.1)
          #if channel.recv_ready():  # recv is ready, now read

        # print(f'in while loop, output is: {output} ')
        # print(f'in while loop, chunk is: {chunk} ')
        #time.sleep(.5)
        if output.count('INFO') > 5:
            match_check = True

        if time.time() > start_time + maxTime:
                print(output)
                print(f'{command} failed to return within timout period')
                timeout = True


    if 'ERROR EcPnmStats' in output:
        print(f'{command} returned with ERROR in response. Closing shell and stopping execution')
        channel.close()
    time.sleep(1.5)
    channel.send('\r\n')
    time.sleep(0.25)
    output += channel.recv(128000).decode("utf-8")
    if output.count('INFO') > 5:
        match_check = True




    if channel.recv_ready():
        #chunk=channel.recv(128000).decode("utf-8")
        output += channel.recv(128000).decode("utf-8")
        print(output)

    return match_check


def triggerAmpTelemetry(ssh,statsList,subBands,command='',timeout=6000,path='"./EC"'):
    fafeList=[]
    channel = ssh.invoke_shell()
    channel.settimeout(timeout)
    command='setNorthPortSwitch Downstream'
    amp_readback(channel,command,prompt='FDX-AMP>$',maxTime=8.0)
    time.sleep(1.0)
    command=''
    amp_readback(channel,command,prompt='FDX-AMP>$',maxTime=8.0)
    time.sleep(0.5)
    command='hal\r\n'
    amp_readback(channel,command,prompt='hal',maxTime=12.0)
    command='cd /'
    amp_readback(channel,command,prompt='hal>',maxTime=8.0)

    ######### gather the telemetry metrics.
    for statsType in statsList:
        for subband in subBands:
            check_telemetry = False
            i=1
            filename = f"EC_{statsType}_{subband}.dat"
            print(f"Filename: {filename}")
            # use the command to execute EC collecting activities
            command = f"ec_pnm_stats {statsType} {subband} /tmp/{filename}"
            print(f'Sending command: {command} to hal>')
            #hal_comm(channel,command)
            while not check_telemetry or i > 3:  # retry getting telemetry up to 3 times, with output valid check
                check_telemetry = hal_gather_telemetry_16p3(channel, command)
                i +=1
                time.sleep(.5)
    ########################

    if config.createFAFE:
        fafe_core0 = amp_readback(channel,'/leap/fafe_show_status 0',prompt='NcInputPower         = ',maxTime=8.0)[0]
        time.sleep(0.5)
        fafe_core4 = amp_readback(channel,'/leap/fafe_show_status 4',prompt='NcInputPower         = ',maxTime=8.0)[0]
        time.sleep(0.5)
        lafe_core0 = amp_readback(channel,'/leap/lafe_show_status 0',prompt='RxInputPower       = ',maxTime=8.0)[0]
        time.sleep(0.5)
        fafeList.append(fafe_core0)
        fafeList.append(fafe_core4)
        fafeList.append(lafe_core0)

     ####exit the hal
    amp_readback(channel, 'exit')
    return fafeList


def triggerAmpTelemetry_wJump(channel,statsList,subBands,command='',timeout=6000,path='"./EC"'):
    fafeList=[]

    command='setNorthPortSwitch Downstream'
    amp_readback(channel,command,prompt='FDX-AMP>$',maxTime=8.0)
    time.sleep(1.0)
    command=''
    amp_readback(channel,command,prompt='FDX-AMP>$',maxTime=8.0)
    time.sleep(0.5)
    command='hal\r\n'
    amp_readback(channel,command,prompt='hal',maxTime=12.0)
    command='cd /'
    amp_readback(channel,command,prompt='hal>',maxTime=8.0)

    ######### gather the telemetry metrics.
    for statsType in statsList:
        for subband in subBands:
            check_telemetry = False
            i=1
            filename = f"EC_{statsType}_{subband}.dat"
            print(f"Filename: {filename}")
            # use the command to execute EC collecting activities
            command = f"ec_pnm_stats {statsType} {subband} /tmp/{filename}"
            print(f'Sending command: {command} to hal>')
            #hal_comm(channel,command)
            while not check_telemetry or i > 3:  # retry getting telemetry up to 3 times, with output valid check
                check_telemetry = hal_gather_telemetry_16p3(channel, command)
                i +=1
                time.sleep(.5)
    ########################

    if config.createFAFE:
        fafe_core0 = amp_readback(channel,'/leap/fafe_show_status 0',prompt='NcInputPower         = ',maxTime=8.0)[0]
        time.sleep(0.5)
        fafe_core4 = amp_readback(channel,'/leap/fafe_show_status 4',prompt='NcInputPower         = ',maxTime=8.0)[0]
        time.sleep(0.5)
        lafe_core0 = amp_readback(channel,'/leap/lafe_show_status 0',prompt='RxInputPower       = ',maxTime=8.0)[0]
        time.sleep(0.5)
        fafeList.append(fafe_core0)
        fafeList.append(fafe_core4)
        fafeList.append(lafe_core0)

     ####exit the hal
    amp_readback(channel, 'exit')
    return fafeList




def copyAmpTelemetry(ssh,statsList,subBands,path):
    fileList=[]
    for statsType in statsList:
        for subband in subBands:
            with SCPClient(ssh.get_transport()) as scp:
                filename = f"EC_{statsType}_{subband}.dat"
                source = f"/tmp/{filename}"
                destination = f'{path}/{filename}'
                print(f"SCP file from {source} to {destination}.")
                scp.get(source, destination)
                fileList.append(filename)
                time.sleep(.2)
    return fileList


def data_crunch(path):
    """
    Created on Mon Sep 30 13:50:44 2024

    @author: mmorri890

    This program scrapes the Amp EC Coeficients in freq domain, and performs TDR analysis on that data set.

    Also generates an Excel File with the TDR response with Plot

    Also adds a 2nd tab with the DS PSD, Echo PSD, Residual Echo PSD, and US psd
    """


    ###  In order to have interactive plots, open a Consoles/Special Consoles : Pylab
    ### and issue this command in the Pylab console:
    ###    %matplotlib qt5
    ###    this will gide you a new window for plotting:

    # import paramiko
    # import sys
    # from paramiko import SSHClient
    # from scp import SCPClient
    # import os
    # import csv
    # import re
    #import matplotlib.pyplot as plt
    import numpy as np
    from datetime import datetime
    from scipy.signal import find_peaks
    import glob
    import pandas as pd
    import re
    import config
    '''
    ec_pnm_stats [statsType] [subBandId] [filename] - Collect EC stats
    statsType - EC PNM statistics type:
        1 - EC Coefficient in freq. domain
        2 - EC Coefficient in time domain
        3 - EC Cancellation Depth
        5 - Echo PSD
        6 - Residual Echo PSD
        7 - Downstream PSD
        8 - Upstream PSD
    subBandId - sub-band id (0=default, 1, 2)
    filename  - path and filename to write to
        /tmp/ec_pnm_stats_output_XX.dat (default)
    '''


    path = "./EC"
    FreqEC_pattern = 'EC_1_*'
    EchoPwr_pattern = 'EC_5_*'
    ResEcho_pattern = 'EC_6_*'
    DSpsd_pattern = 'EC_7_*'
    USpsd_pattern = 'EC_8_*'
    ampinfo = config.amp_info

    #### Get latest EC Coeficients files vs freq. and echo power vs freq.

    fSamp=100000  # frequency bin sizing in data set
    timeSpan = 1/fSamp

    minpeak = config.minpeak     # threshold for searching for Echo peaks.  Only data that is >minpeak will be able to be called a peak

    VoP = .87    #Velocity of Propagation  87% for P3 hardline , 82% for RG6
    SoL = 299792458*3.28084  # Speed of light in a vaccum in feet/sec
    SolCoax = VoP*SoL  # feet/sec
    timestamp = datetime.now().strftime('%Y_%m_%d_%Hh%Mm%Ss')
    ampinfo.append(timestamp)


    ECfreqFiles = glob.glob(f'{path}/{FreqEC_pattern}')
    ECfreqFiles.sort()
    EchoPwrFiles = glob.glob(f'{path}/{EchoPwr_pattern}')
    EchoPwrFiles.sort()
    ResEchoFiles = glob.glob(f'{path}/{ResEcho_pattern}')
    ResEchoFiles.sort()
    DSpsdFiles = glob.glob(f'{path}/{DSpsd_pattern}')
    DSpsdFiles.sort()
    USpsdFiles = glob.glob(f'{path}/{USpsd_pattern}')
    USpsdFiles.sort()

    ##### All metrics will be processed subband by subband with this outer loop
    fileList=[]  #list of excel files that will be generated

    for file1,file5,file6,file7,file8 in zip(ECfreqFiles,EchoPwrFiles,ResEchoFiles,DSpsdFiles,USpsdFiles):

        #########first obtain the starting frequency of the subband and # of bins

        with open(file5) as fp:
            content=fp.readlines()
            bins_text=content[1]
            startF_text=content[2]
            deltaF_text=content[3]

            bins = int(bins_text.split(':')[1])
            startF = float(startF_text.split(':')[1])/1e6
            deltaF = float(re.findall(r'\d+',deltaF_text)[0])/1000.0


    ################  create np arrays from the telemetry data

        EC_freq = np.genfromtxt(file1,skip_header=4,delimiter=',')
        EchoPsd = np.genfromtxt(file5,skip_header=4,delimiter=',')
        resPsd = np.genfromtxt(file6,skip_header=4,delimiter=',')
        dsPsd = np.genfromtxt(file7,skip_header=4,delimiter=',')
        usPsd = np.genfromtxt(file8,skip_header=4,delimiter=',')

        psdFreq_array = np.arange(startF,startF+bins*deltaF-deltaF,deltaF)
        if len(psdFreq_array) == 955:
            psdFreq_array = np.append(psdFreq_array,(psdFreq_array[954]+deltaF))
        freqLength = psdFreq_array.size

        # EC coeficients.  creates an array of complex #s from the array of number pairs
        complex_EC_freq = np.array([complex(a, b) for a, b in EC_freq])
        linMag_EC_freq = np.abs(complex_EC_freq)
        for i,element in enumerate(linMag_EC_freq):
            if element < 1e-6:
                linMag_EC_freq[i]=linMag_EC_freq[i]+1e-6
        EC_freq_dB = 20.0*np.log10(linMag_EC_freq)


        ###### This is using the EC filter coeficients vs Freq. to obtain the inpulse response of the South Port Network Segment + internal echo
        complex_EC_impulse = np.fft.ifft(complex_EC_freq,norm='backward')
        tcp_impulse = np.sum(np.abs(complex_EC_impulse))
        tcp_impulse_db = 20.0*np.log10(tcp_impulse)

        length=len(complex_EC_impulse)
        timeStep = (timeSpan/length)
        timeMax = timeSpan - timeStep
        timeArray = np.arange(0,timeMax,timeStep)  # round trip time array, starting at 0, incrementing by deltaT
        if len(timeArray) == 955:
            timeArray = np.append(timeArray,timeMax)
#        timeArray.append(timeMax+timeStep)  # round trip time array, starting at 0, incrementing by deltaT.  add this for 96MHz subband
        mag_EC_impulse =20.0*np.log10(np.abs(complex_EC_impulse)) # array of impulse response mag(dB)
        timeLength = mag_EC_impulse.size



    ################################## finding a collection of peaks in the impulse response
        impulse_peaks =find_peaks(mag_EC_impulse,height=minpeak)  #index[0] is location array, [1] is the values array
        while impulse_peaks[0].size == 0:
            minpeak = minpeak - 3.0
            impulse_peaks =find_peaks(mag_EC_impulse,height=minpeak)
        # ampLaunchTime = timeArray[impulse_peaks[0][0]]   #1st peak in the peak location array is the amp launch
        ampLaunchTime = 0.198744769874477e-6 # fixed offset per BCM 0.194uS but set to closest time bin location
        timeNormArray = (timeArray - ampLaunchTime)/2  # this is 1/2 the round trip time array values normalized to the Amp South Port launch time
        distFtNormArray = timeNormArray*SolCoax

        impulse_peaks_time = []
        impulse_peaks_feet = []
        impulse_peaks_delta_feet = []
        impulse_peaks_dB = []


        for i in impulse_peaks[0]:
            impulse_peaks_time.append(timeArray[i])
            impulse_peaks_feet.append(distFtNormArray[i])
            impulse_peaks_dB.append(mag_EC_impulse[i])

        # lists to arrays
        impulse_peaks_time = np.asarray(impulse_peaks_time)
        impulse_peaks_feet = np.asarray(impulse_peaks_feet)
        impulse_peaks_dB = np.asarray(impulse_peaks_dB)

        #create the list of interspan lengths then cast as array
        for i in range(len(impulse_peaks_feet)):
            if i == 0:
                impulse_peaks_delta_feet.append(impulse_peaks_feet[i])
            else:
                impulse_peaks_delta_feet.append(impulse_peaks_feet[i] - impulse_peaks_feet[i-1])

        impulse_peaks_delta_feet = np.asarray(impulse_peaks_delta_feet)


        ##### build out final time arrays and cast as dataframe record to archive as excel file.....1st Tab for this time data.

        impulse_response_array = np.column_stack((timeArray*1e6,timeNormArray,distFtNormArray,mag_EC_impulse))
        impulse_response_df = pd.DataFrame(impulse_response_array)
        impulse_response_df.columns = ['RTT(uS)','OneWayNorm Time(s)','OneWay Dist(ft)','Mag(dB)']

        impulse_peaks_array = np.column_stack((impulse_peaks_time*1e6,impulse_peaks_feet,impulse_peaks_delta_feet,impulse_peaks_dB))
        impulse_peaks_df = pd.DataFrame(impulse_peaks_array)
        impulse_peaks_df.columns = ['Peak RTT(uS)','Peak Total Dist(ft)','Peak Span Dist(ft)','Peak Mag(dB)']
        ####adding impulse tcp value to record
        impulse_peaks_df['Coef tcp(dB)']=''
        impulse_peaks_df.loc[0,'Coef tcp(dB)'] = tcp_impulse_db


        time_write_df = pd.concat([impulse_response_df,impulse_peaks_df,pd.DataFrame({'Data Source':ampinfo})],axis=1)

        if config.plotTime: time_write_df.plot(2,3)


        ######## Now Generate dataframe record for frequency data for 2nd tab of excel file.

        freq_response_array = np.column_stack((psdFreq_array,EchoPsd,resPsd,dsPsd,usPsd,EC_freq_dB))
        freq_response_df = pd.DataFrame(freq_response_array)
        freq_response_df.columns = ['Freq(MHz)','Echo PSD(dBmV)','ResEcho PSD(dBmV)','DS PSD(dBmV)','US PSD(dBmV)','EC Coef(dB)']
        freq_response_df = pd.concat([freq_response_df,pd.DataFrame({'Data Source':ampinfo})],axis=1)  # tacking the source into to last column

     ############  Now write out everything to the Excel file.

        subbandID = str(ECfreqFiles.index(file1))
        basefile = 'EC_Data_'
        filename = basefile +'SB'+subbandID + '_' + timestamp + '.xlsx'
        fileList.append(filename)
        summaryFileName = 'EC_Summary_'+ timestamp + '.xlsx'
        sheetnameTimeData = 'TDR_SubBand'+subbandID
        sheetnameFreqData = 'PSD_SubBand'+subbandID

        if config.plotFreq:
            freq_response_df.plot(x="Freq(MHz)",y=['Echo PSD(dBmV)','ResEcho PSD(dBmV)','DS PSD(dBmV)','US PSD(dBmV)'],ylim=(-60,60))

        with pd.ExcelWriter(filename,engine="xlsxwriter") as writer:
        #with pd.ExcelWriter(filename,engine="openpyxl") as writer:

            #### time data and echo plot to the 1st Excel Tab
            time_write_df.to_excel(writer,sheet_name = sheetnameTimeData,index=False)
            workbook = writer.book
            worksheet = writer.sheets[sheetnameTimeData]
            chart = workbook.add_chart({'type':'scatter'})
            # seriesName = 'SubBand'+subbandID
            # xSeries = sheetnameTimeData + '!$C2:$C850'
            # yData = sheetnameTimeData + '!$D2:$D850'
            seriesName = 'SubBand'+subbandID
            lastcell = str(int(2+timeLength))
            xSeries = sheetnameTimeData + '!$C2:$C'+lastcell
            yData = sheetnameTimeData + '!$D2:$D850'+lastcell

            chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
            chart.set_x_axis({'name':'OneWay Dist(ft)','major_gridlines':{'visible':True},'major_unit': 100,'min':0,'max':1000,'crossing':-1000})
            chart.set_y_axis({'name': 'Mag(dB)','crossing':-1000})
            chart.set_title({'name':'Amp EC Time Response'})
            chart.set_size({'width': 1280,'height': 576})
            worksheet.insert_chart('L2',chart)

            #copy this tab to the data summary excel file


            ## frequency data and plot to the 2nd Excel tab
            freq_response_df.to_excel(writer,sheet_name = sheetnameFreqData,index=False)
            workbook = writer.book
            worksheet = writer.sheets[sheetnameFreqData]
            chart = workbook.add_chart({'type':'scatter'})
            chart.set_x_axis({'name':'Freq(MHz)','major_gridlines':{'visible':True},'major_unit': 96,'min':108,'max':685,'crossing':-1000})
            chart.set_y_axis({'name': 'Mag(dBmV)','crossing':-1000})
            chart.set_title({'name':'Amp EC Frequency Data'})
            chart.set_size({'width': 1280,'height': 576})

            #xSeries = sheetnameFreqData + '!$A2:$A1915'
            xSeries = sheetnameFreqData + '!$A2:$A'+ lastcell

            seriesName = 'Echo-SB'+subbandID
            #yData = sheetnameFreqData + '!$B2:$B1915'
            yData = sheetnameFreqData + '!$B2:$B'+ lastcell
            chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
            seriesName = 'EC_Noise-SB'+subbandID
            #yData = sheetnameFreqData + '!$C2:$C1915'
            yData = sheetnameFreqData + '!$C2:$C' + lastcell
            chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
            seriesName = 'DS PSD-SB'+subbandID
            #yData = sheetnameFreqData + '!$D2:$D1915'
            yData = sheetnameFreqData + '!$D2:$D' + lastcell
            chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
            seriesName = 'US PSD-SB'+subbandID
            #yData = sheetnameFreqData + '!$E2:$E1915'
            yData = sheetnameFreqData + '!$E2:$E' + lastcell
            chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
            worksheet.insert_chart('L2',chart)

    return(fileList,timestamp,ampinfo)

def dataTDR_summary(crunchData,fafe_data):
    '''
    this function takes the excel files that were created under data_crunch() which are for individual subbands and creates a summary
    excel file of the EC frequency data for the entire FDX band.
         '''


    #crunchData is this list[Subfilelist,timestamp]
    timestamp = crunchData[1]
    sbFiles=crunchData[0]
    ampinfo_df=pd.DataFrame([crunchData[2],crunchData[2]]).T


    # core0_FDXSouthAFElines=fafe_data[0].splitlines()[8:33]
    # core0_NCpathlines=fafe_data[0].splitlines()[34:57]
    # core4_NorthAFElines=fafe_data[1].splitlines()[8:]


    # fafe_df = pd.DataFrame(fafe_data)
    # fafe_df = fafe_df.T
    # fafe_df_ext=pd.concat([ampinfo_df,fafe_df],ignore_index=True)
    # fafe_df_ext.columns = ['FAFE Core0','FAFE Core4','LAFE Core0']



    fafe_core0fname = config.amp_info[2] + ' FAFE Core0_'+ timestamp + '.txt'
    fafe_core4fname = config.amp_info[2] + ' FAFE Core4_'+ timestamp + '.txt'
    lafe_core0fname = config.amp_info[2] + ' LAFE Core0_'+ timestamp + '.txt'

    if config.createFAFE:


        core0_FDXSouthAFElines=fafe_data[0].splitlines()[8:33]
        core0_NCpathlines=fafe_data[0].splitlines()[34:57]
        core4_NorthAFElines=fafe_data[1].splitlines()[8:]


        fafe_df = pd.DataFrame(fafe_data)
        fafe_df = fafe_df.T
        fafe_df_ext=pd.concat([ampinfo_df,fafe_df],ignore_index=True)
        fafe_df_ext.columns = ['FAFE Core0','FAFE Core4','LAFE Core0']


        fafe_df_ext['FAFE Core0'].to_csv(fafe_core0fname,index=False,header=False)
        fafe_df_ext['FAFE Core4'].to_csv(fafe_core4fname,index=False,header=False)
        fafe_df_ext['LAFE Core0'].to_csv(lafe_core0fname,index=False,header=False)




    # fafe_core0 = crunchData[1][0]
    # fafe_core4 = crunchData[1][1]


    # core0fdxSouthlines=fafe_data[0].splitlines()[8:33]
    # core0ncpathlines=fafe_data[0].splitlines()[34:57]
    # core4lines=fafe_data[1].splitlines()[8:]


    RLSP = config.RLSP  #RLSP/6.4MHz
    RLSP_100k = RLSP - 18.0618  #per 100kHz

    dfList=[]  # list of data frames containing PSD data for each subband
    dftList=[]
    TCP_dBmVList=[]
    echoPwrList=[]
    dsPwrList=[]
    resEchoList=[]
    resEchoPwrAvgList=[]
    C2NList=[]
    bandIDList=[]

    for i,sbfile in enumerate(sbFiles):
        df=pd.read_excel(sbfile,sheet_name=1)
        dft=pd.read_excel(sbfile,sheet_name=0)
        dfList.append(df)
        dftList.append(dft)

        ampinfo=df['Data Source']
        freq = df['Freq(MHz)']
        freqspan=freq[freq.shape[0]-1] - freq[0]
        echoPwr = df['Echo PSD(dBmV)']
        echoPwrlow=echoPwr.iloc[0:int(echoPwr.shape[0]/2)]    # lower 1/2 of subband
        echoPwrhi=echoPwr.iloc[int(echoPwr.shape[0]/2):echoPwr.shape[0]]    # upper 1/2 of subband

        echoPwrList.append(echoPwr)
        echoPwrLin = 10**(echoPwr/10.0)
        echoPwrTot=echoPwrLin.sum()


        dsPwr=df['DS PSD(dBmV)']
        dsPwrList.append(dsPwr)
        dsPwrLin = 10**(echoPwr/10.0)

        resEcho=df['ResEcho PSD(dBmV)']
        resEcholow=resEcho.iloc[0:int(resEcho.shape[0]/2)]    # lower 1/2 of subband
        resEchohi=resEcho.iloc[int(resEcho.shape[0]/2):resEcho.shape[0]]    # upper 1/2 of subband

        resEchoList.append(resEcho)
        bandIDList.extend([f'SB{i}_low',f'SB{i}_High'])

        resEcholowLin=10**(resEcholow/10.0)
        resEcholow_avg=10.0*np.log10(np.average(resEcholowLin))
        C2NList.append(RLSP_100k -  resEcholow_avg)
        resEchoPwrAvgList.append(resEcholow_avg)

        resEchohiLin=10**(resEchohi/10.0)
        resEchohi_avg=10.0*np.log10(np.average(resEchohiLin))
        C2NList.append(RLSP_100k -  resEchohi_avg)
        resEchoPwrAvgList.append(resEchohi_avg)



    full_df=pd.concat(dfList) # 1st concatinate all of the data from each subband
    full_dft=pd.concat(dftList)

    # ext_df=pd.concat([full_df,pd.DataFrame({'BandID':bandIDList}), \
    #                   pd.DataFrame({'AvgResEcho':resEchoPwrAvgList}), \
    #                       pd.DataFrame({'Avg C2N':C2NList})],axis=1)

    ext_df=pd.concat([full_df,pd.DataFrame({'BandID':bandIDList}), \
                      pd.DataFrame({'AvgResEcho':resEchoPwrAvgList}), \
                          pd.DataFrame({'Avg C2N':C2NList})],axis=1)

    if config.plotFreq:
        ext_df.plot(x="Freq(MHz)",y=['Echo PSD(dBmV)','ResEcho PSD(dBmV)','DS PSD(dBmV)','US PSD(dBmV)'],ylim=(-60,60))
        dftList[0].plot(x='OneWay Dist(ft)',y=['Mag(dB)'])

         ############  Now write out everything to the Excel file.



    summaryFileName = config.amp_info[2] + ' EC_Summary_' + timestamp + '.xlsx'
    sheetnameTimeData = 'TDR_Summary'
    sheetnameFreqData = 'PSD_Summary'
    sheetnameFAFECore0 = 'FAFE Core 0'
    sheetnameFAFECore4 = 'FAFE Core 4'

    with pd.ExcelWriter(summaryFileName,engine="xlsxwriter") as writer:
    #with pd.ExcelWriter(filename,engine="openpyxl") as writer:

        #### time data and echo plot to the 1st Excel Tab
        full_dft.to_excel(writer,sheet_name = sheetnameTimeData,index=False)
        rows,columns = full_dft.shape
        workbook = writer.book
        worksheet = writer.sheets[sheetnameTimeData]
        chart = workbook.add_chart({'type':'scatter'})

        seriesName = 'SubBand0'
        start = 2
        end = start + int(rows/3 -1)
        xcells = '!$C'+str(start)+':$C'+str(end)
        ycells = '!$D'+str(start)+':$D'+str(end)
        xSeries = sheetnameTimeData + xcells
        yData = sheetnameTimeData + ycells

        # xSeries = sheetnameTimeData + '!$C2:$C850'
        # yData = sheetnameTimeData + '!$D2:$D850'
        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
        chart.set_x_axis({'name':'OneWay Dist(ft)','major_gridlines':{'visible':True},'major_unit': 100,'min':0,'max':1000,'crossing':-1000})
        chart.set_y_axis({'name': 'Mag(dB)','crossing':-1000})
        chart.set_title({'name':'Amp EC Time Response'})
        chart.set_size({'width': 1280,'height': 576})

        seriesName = 'SubBand1'
        start=end + 1
        end=start + int(rows/3 -1)
        xcells = '!$C'+str(start)+':$C'+str(end)
        ycells = '!$D'+str(start)+':$D'+str(end)
        xSeries = sheetnameTimeData + xcells
        yData = sheetnameTimeData + ycells
        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
        chart.set_x_axis({'name':'OneWay Dist(ft)','major_gridlines':{'visible':True},'major_unit': 100,'min':0,'max':1000,'crossing':-1000})
        chart.set_y_axis({'name': 'Mag(dB)','crossing':-1000})
        chart.set_title({'name':'Amp EC Time Response'})
        chart.set_size({'width': 1280,'height': 576})

        seriesName = 'SubBand2'
        start=end + 1
        end=start + int(rows/3 -1)
        xcells = '!$C'+str(start)+':$C'+str(end)
        ycells = '!$D'+str(start)+':$D'+str(end)
        xSeries = sheetnameTimeData + xcells
        yData = sheetnameTimeData + ycells
        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
        chart.set_x_axis({'name':'OneWay Dist(ft)','major_gridlines':{'visible':True},'major_unit': 100,'min':0,'max':1000,'crossing':-1000})
        chart.set_y_axis({'name': 'Mag(dB)','crossing':-1000})
        chart.set_title({'name':'Amp EC Time Response'})
        chart.set_size({'width': 1280,'height': 576})

        worksheet.insert_chart('L2',chart)

        #copy this tab to the data summary excel file


        ## frequency data and plot to the 2nd Excel tab
        full_df.to_excel(writer,sheet_name = sheetnameFreqData,index=False)
        workbook = writer.book
        worksheet = writer.sheets[sheetnameFreqData]
        chart = workbook.add_chart({'type':'scatter'})
        chart.set_x_axis({'name':'Freq(MHz)','major_gridlines':{'visible':True},'major_unit': 96,'min':108,'max':685,'crossing':-1000})
        chart.set_y_axis({'name': 'Mag(dBmV/100kHz)','major_unit': 10,'min':-60,'max':50,'crossing':-1000})
        chart.set_title({'name':'Amp EC Frequency Data'})
        chart.set_size({'width': 1280,'height': 576})

        start=2
        end=start + int(rows -1)
        xcells = '!$A'+str(start)+':$A'+str(end)
        ycells = '!$B'+str(start)+':$B'+str(end)
        xSeries = sheetnameFreqData + xcells
        yData = sheetnameFreqData + ycells
        seriesName = 'Echo PSD'


        # xSeries = sheetnameFreqData + '!$A2:$A5737'
        # seriesName = 'Echo PSD'
        # yData = sheetnameFreqData + '!$B2:$B5737'

        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})

        seriesName = 'ResEcho PSD'
        # yData = sheetnameFreqData + '!$C2:$C5737'
        ycells = '!$C'+str(start)+':$C'+str(end)
        yData = sheetnameFreqData + ycells
        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})

        seriesName = 'DS PSD'
        # yData = sheetnameFreqData + '!$D2:$D5737'
        ycells = '!$D'+str(start)+':$D'+str(end)
        yData = sheetnameFreqData + ycells
        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})

        seriesName = 'US PSD'
        # yData = sheetnameFreqData + '!$E2:$E5737'
        ycells = '!$E'+str(start)+':$E'+str(end)
        yData = sheetnameFreqData + ycells
        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
        worksheet.insert_chart('L2',chart)

        #Write FAFE DATA to their own tabs
        # fafe_df_ext['FAFE Core0'].to_excel(writer,sheet_name = sheetnameFAFECore0,index=False)
        # fafe_df_ext['FAFE Core4'].to_excel(writer,sheet_name = sheetnameFAFECore4,index=False)
        return [[summaryFileName,fafe_core0fname,fafe_core4fname],fafe_df]

        xSeries = sheetnameTimeData + '!$C2:$C850'
        yData = sheetnameTimeData + '!$D2:$D850'
        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
        chart.set_x_axis({'name':'OneWay Dist(ft)','major_gridlines':{'visible':True},'major_unit': 100,'min':0,'max':1000,'crossing':-1000})
        chart.set_y_axis({'name': 'Mag(dB)','crossing':-1000})
        chart.set_title({'name':'Amp EC Time Response'})
        chart.set_size({'width': 1280,'height': 576})

        seriesName = 'SubBand1'
        start=1914
        end=start+848
        xcells = '!$C'+str(start)+':$C'+str(end)
        ycells = '!$D'+str(start)+':$D'+str(end)
        xSeries = sheetnameTimeData + xcells
        yData = sheetnameTimeData + ycells
        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
        chart.set_x_axis({'name':'OneWay Dist(ft)','major_gridlines':{'visible':True},'major_unit': 100,'min':0,'max':1000,'crossing':-1000})
        chart.set_y_axis({'name': 'Mag(dB)','crossing':-1000})
        chart.set_title({'name':'Amp EC Time Response'})
        chart.set_size({'width': 1280,'height': 576})

        seriesName = 'SubBand2'
        start=1914+1912
        end=start+848
        xcells = '!$C'+str(start)+':$C'+str(end)
        ycells = '!$D'+str(start)+':$D'+str(end)
        xSeries = sheetnameTimeData + xcells
        yData = sheetnameTimeData + ycells
        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
        chart.set_x_axis({'name':'OneWay Dist(ft)','major_gridlines':{'visible':True},'major_unit': 100,'min':0,'max':1000,'crossing':-1000})
        chart.set_y_axis({'name': 'Mag(dB)','crossing':-1000})
        chart.set_title({'name':'Amp EC Time Response'})
        chart.set_size({'width': 1280,'height': 576})

        worksheet.insert_chart('L2',chart)

        #copy this tab to the data summary excel file


        ## frequency data and plot to the 2nd Excel tab
        full_df.to_excel(writer,sheet_name = sheetnameFreqData,index=False)
        workbook = writer.book
        worksheet = writer.sheets[sheetnameFreqData]
        chart = workbook.add_chart({'type':'scatter'})
        chart.set_x_axis({'name':'Freq(MHz)','major_gridlines':{'visible':True},'major_unit': 96,'min':108,'max':685,'crossing':-1000})
        chart.set_y_axis({'name': 'Mag(dBmV/100kHz)','major_unit': 10,'min':-60,'max':50,'crossing':-1000})
        chart.set_title({'name':'Amp EC Frequency Data'})
        chart.set_size({'width': 1280,'height': 576})

        xSeries = sheetnameFreqData + '!$A2:$A5737'

        seriesName = 'Echo PSD'
        yData = sheetnameFreqData + '!$B2:$B5737'
        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
        seriesName = 'ResEcho PSD'
        yData = sheetnameFreqData + '!$C2:$C5737'
        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
        seriesName = 'DS PSD'
        yData = sheetnameFreqData + '!$D2:$D5737'
        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
        seriesName = 'US PSD'
        yData = sheetnameFreqData + '!$E2:$E5737'
        chart.add_series({'name': seriesName,'categories': xSeries,'values': yData,'line':{'none':False},'marker':{'type':'none'}})
        worksheet.insert_chart('L2',chart)

        #Write FAFE DATA to their own tabs
        # fafe_df_ext['FAFE Core0'].to_excel(writer,sheet_name = sheetnameFAFECore0,index=False)
        # fafe_df_ext['FAFE Core4'].to_excel(writer,sheet_name = sheetnameFAFECore4,index=False)
        return [[summaryFileName,fafe_core0fname,fafe_core4fname],fafe_df]
