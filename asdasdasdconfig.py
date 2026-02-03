# Jumpbox details (IPv4)
jumpbox_hostname = 'jump.autobahn.comcast.com'  # Replace with the jumpbox IP
jumpbox_username = "svcAutobahn"    

# Target host details (IPv6 with password)
target_hostname = '2001:0558:600F:0000:F8FE:3159:C30E:7089'  # Replace with the target host IPv6 address
target_username = "cli"
target_password = "cli"

run_single = False

# wesDT
#amp_info = ['2001:0558:6013:000F:28AE:32F9:1333:EE39','N+6 MB 1,eCM 24:a1:86:00:c1:fc']
#amp_info = ['2001:0558:6013:000F:10F3:002E:8C63:D25C','N+6 MB 2,eCM 24:a1:86:00:c2:84']
#amp_info = ['2001:0558:6013:000F:3063:6C1F:EB54:5523','N+6 MB 3,eCM 24:a1:86:00:42:5c']
#amp_info = ['2001:0558:6013:000F:E5C5:2503:50ED:4601','N+6 MB 4,eCM 24:a1:86:00:c2:40']
#amp_info = ['2001:0558:6013:000F:2840:F3B9:4BF0:3DEE','N+6 LE 1,eCM 24:a1:86:00:c2:b8']
#amp_info = ['2001:0558:6013:000F:481C:BFF2:8E5C:5356','N+6 LE 2,eCM 24:a1:86:00:42:d8']
#amp_info = ['2001:0558:6013:000F:150C:238F:1E2C:9AE9','DeskAmp,eCM 24:a1:86:00:c2:bc']
#amp_info = ['2001:0558:6013:000F:D8A8:7B6B:192C:AF8C','LE 1,eCM 24:a1:86:00:c0:5c']
#amp_info = ['2001:0558:6013:000F:B984:3D5F:1D71:F728','LE 2,eCM 24:a1:86:00:c0:60']
#amp_info = ['2001:0558:6013:000F:F88E:8F89:0C09:8F6B','LE 3,eCM 24:a1:86:00:40:9c']
#amp_info = ['2001:0558:6013:000F:9C61:024F:DCF3:E5E3','MB 1 N+6,eCM 24:a1:86:00:c1:fc']

# N+6 CC38 Replica
#amp_info = ['2001:0558:6013:000F:A0DE:56D1:1A69:915B','N+6 MB 1,eCM 24:a1:86:00:40:80']
#amp_info = ['2001:0558:6013:000F:2DC8:AAD1:BD7B:50B7','N+6 MB 1,eCM 24:a1:86:00:c2:bc']
#amp_info = ['2001:0558:6013:000F:28AE:32F9:1333:EE39','N+6 MB 1,eCM 24:a1:86:00:c1:fc']
#amp_info = ['2001:0558:6013:000F:28AE:32F9:1333:EE39','N+6 MB 1,eCM 24:a1:86:00:c1:fc']
#amp_info = ['2001:0558:6013:000F:28AE:32F9:1333:EE39','N+6 MB 1,eCM 24:a1:86:00:c1:fc']
#p_info = ['2001:0558:6013:000F:58DE:EE86:3015:C1AD','N+6 MB 1,eCM 24:a1:86:00:40:7c']

# Single Amp Testing Station
#amp_info = ['2001:0558:6013:000F:695F:4BD7:24DC:3FED','eCM 24:a1:86:00:40:9c']
#amp_info = ['2001:0558:6013:000F:608A:CA4D:46C2:D86E','eCM 24:a1:86:0a:a1:c4']
#amp_info = ['2001:0558:6013:000F:0828:AD7A:C17E:E4E9','eCM 24:a1:86:00:c2:a0']
#amp_info = ['2001:0558:6017:01B0:5109:9A99:EE16:3877','eCM 24:a1:86:00:42:24']
#amp_info = ['2001:0558:6026:0031:6530:7527:9594:32EE','eCM 24:a1:86:0c:80:80']

######  My Amps #####

#amp_info = ['2001:0558:6027:0072:4D69:FE9C:D9E4:5819',' eCM 24:a1:86:00:42:a4']


Check163 = True

amp_username_scp = 'root'
amp_password_scp = 'Wallingford'
amp_username = 'cli'
amp_password = 'cli'
path = "./EC"
pathFFT = "./CS wbFFT Data"
ssh_timeout = 6000  #msec
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
ecStat_list = [1,5,6,7,8]  #this is the telemetry list to gather
ec_subBandId = [0,1,2]   #this list is which subbands will be gathered
createTDR = True
createCSV = True
createFAFE = True
plotFreq = True  #Do you want to plot the data within python (frequency vectors)
plotTime = True  #Do you want to plot the time analysis
minpeak = -35.0  #This is the threshold used for Echo Peak Search

RLSP = 8.0  #RLSP/6.4MHz