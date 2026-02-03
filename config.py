# Jumpbox details (IPv4)
jumpbox_hostname = 'jump.autobahn.comcast.com'  # Replace with the jumpbox IP
jumpbox_username = "svcAutobahn"    

# Target host details (IPv6 with password)
target_hostname = '2001:0558:600F:0000:F8FE:3159:C30E:7089'  # Replace with the target host IPv6 address
target_username = "cli"
target_password = "cli"

run_single = False

# alex 
#amp_info = ['73.153.251.212','CA008 CS Trial MB']  # eCM ac:db:48:bb:cf:10
#amp_info = ['73.34.43.92','CA017 CS Trial MB']     # eCM ac:db:48:bb:cf:14
#amp_info = ['24.8.142.214','BA018 CS Trial LE']     # eCM ac:db:48:bb:cf:e8
#amp_info = ['24.8.140.247','BA019 CS Trial MB']     # eCM 8c:76:3f:f0:79:b0
#amp_info = ['24.8.142.227','DA007 CS Trial MB']     # 10:e1:77:58:d1:88
#amp_info = ['67.174.182.116','DA010 CS Trial LE']     # ac:db:48:bb:cf:e0
#amp_info = ['24.8.142.225','DA016 CS Trial LE']     # ac:db:48:bb:cf:0c


#amp_info = ['2001:0558:6040:00CB:F921:8FE5:CA7F:5AD2','COPCDO2DOABA018 24:a1:86:00:41:78','COPCDO2DOABA018']
#amp_info = ['2001:0558:6040:00CB:5DDA:ADF4:B559:93B5','COPCD02D0CCA008 24:a1:86:00:44:68','COPCD02D0CCA008']
#amp_info = ['2001:0558:6040:00CB:1CF2:F8E9:241F:5795','COPCD02D0CCA017 24:a1:86:00:e4:4c','COPCD02D0CCA017']
#amp_info = ['2001:0558:6040:00CB:3DBF:D975:A3FE:866C','COPCDO2DOABA019 24:a1:86:00:e0:ac','COPCDO2DOABA019']

#amp_info = ['2001:0558:6026:000C:6D82:965D:EAB6:5F84','NJRADO7NOABA001 24:a1:86:00:60:7c','NJRADO7NOABA001']
#amp_info = ['2001:558:600e:2:19f1:edba:4481:88e3','Ray MB OSP eCM 24:a1:86:00:42:34','Ray MB OSP']
#amp_info = ['2001:558:600e:2:14ec:6f4e:3bee:9ca3','Ray LE OSP eCM 24:a1:86:00:c1:d8','Ray LE OSP']
#amp_info = ['2001:0558:6040:009C:AC75:75AA:F2CB:1303','Alex Special eCM 24:a1:86:00:dd:40','Alex Special']

######## Heisers Node   ############

#amp_info = ['2001:0558:6040:00CB:FD64:CC24:961B:5160','Heiser eCM 24:a1:86:00:43:f0','Heiser 24a1860043f0']  # NorthAFE 38dBmV needs recal, fafe is reset. ist active Healed $$$$$$$$$$$$$
#amp_info = ['2001:0558:6040:00CB:0954:D5BC:6A20:332E','Heiser eCM 24:a1:86:00:41:78','Heiser 24a186004178']  # north afe OK.  Fafe reset. first active.  recald $$$$
#amp_info = ['2001:0558:6040:00CB:84B3:1DE5:54E6:4D4D','Heiser eCM 24:a1:86:00:44:68','Heiser 24:a186004468']  #sick.  Marc Healed $$$$$$$$$$
#amp_info = ['2001:0558:6040:00CB:494A:FB92:B201:6EF5','Heiser eCM 24:a1:86:00:e0:ac','Heiser 24a18600e0ac']   #FAFE4 high clip count.  currently not clipping FAFE reset. direct connect recalld $$$$$$$$$
#amp_info = ['2001:0558:6040:00CB:0DB6:B442:A17B:F002','Heiser eCM 24:a1:86:00:c1:24','Heiser 24a18600c124']  #OK reset fafe
#amp_info = ['2001:0558:6040:00CB:541B:4B70:8109:3E6C','Heiser eCM 24:a1:86:00:45:54','Heiser 24a186004554']   #OK
#amp_info = ['2001:0558:6040:00CB:11F8:3215:3633:89B5','Heiser eCM 24:a1:86:00:e4:4c','Heiser 24a18600e44c']   #OK
#amp_info = ['2001:0558:6026:000C:5D72:4840:C056:6CD5','NJRAD07T0C eCM 24:a1:86:00:d5:28 ','NJRAD07T0C eCM 24a18600d528']
#amp_info = ['2001:0558:6026:000C:BC02:017A:1ECA:A08D','NJRAD07T0C eCM 24:a1:86:00:f3:34 ','NJRAD07T0C eCM 24a18600f334']

####### PACAD0400A ########
#amp_info = ['2001:0558:6035:0035:A17C:EF8C:2A65:E5EC','eCM 	24:a1:86:0c:b9:8c','Input Amp on Main']
#amp_info = ['2001:0558:6035:0035:090A:CB82:959F:B54F','eCM 	24:a1:86:0a:37:40','P3 Term LE']
#amp_info = ['2001:0558:6035:0035:C4D6:D145:0A60:DA52','eCM 	24:a1:86:0c:b6:b8','P2 Term Amp']

####### CASHD04B0A ########
#amp_info = ['2001:0558:6012:008D:69F0:F172:1BA6:317B','eCM 24:a1:86:08:f6:c4','167 Eaton Ave']
#amp_info = ['2001:0558:6012:008D:3847:A0E0:CD43:6C5B','eCM 24:a1:86:0b:80:c8','287 Eaton Ave']
#amp_info = ['2001:0558:6012:008D:DD55:A6F6:1361:D3B7','eCM 24:a1:86:0b:97:20','330 Eaton Ave']

####### ACTIVE AMP ########
#amp_info = ['2001:0558:6040:001E:2929:2B91:B08A:F236','eCM 	24:a1:86:09:be:a4','CORAD03V0CCA009']
amp_info = ['2001:0558:600D:001E:00D1:3C80:891E:E609','eCM 24:a1:86:0c:d0:54','Indy 1 MB Justice']

'''
24:a1:86:00:44:68 COPCD02D0CCA008
8c:76:3f:f0:78:d0  HSCYD05609CA001
24:a1:86:00:e4:4c COPCD02D0CCA017'''

#amp_info = ['69.254.95.24','CC38 MB2-2B eAmp, eCM 8c:76:3f:f0:79:b4']
#amp_info = ['69.254.95.28','CC38 MB3-3B eAmp, eCM ac:db:48:bb:d0:cc']
#amp_info = ['69.254.95.19','CC38 MB4-4B eAmp, eCM ac:db:48:bb:d0:c8']
#amp_info = ['','CC38 LE-5B eAmp, eCM ac:db:48:bb:d0:ac']
#amp_info = ['69.254.95.10','CC38 LE-5B eAmp, eCM 10:e1:77:58:d1:70']
#amp_info = ['xxxxxx','CC38 MB1-6B eAmp, eCM 10:e1:77:58:d1:94']

#amp_info = ['69.254.95.62','CC38 MB1-1C eAmp, eCM ac:db:48:bb:d0:bc']
#amp_info = ['','CC38 MB1-2C eAmp, eCM 10:e1:77:58:d2:c0']
#amp_info = ['2001:0558:6013:000F:4194:A3F4:BE99:B9A2','Wes DT 1st Spin3 Amp,eCM 24:a1:86:00:42:4c']
#amp_info = ['2001:0558:6013:000F:F88E:8F89:0C09:8F6B','Wes DT 1st Spin3 Amp,eCM 24:a1:86:00:40:9c','WES_409c']

Check163 = True

amp_username_scp = 'root'
amp_password_scp = 'Wallingford'
amp_username = 'cli'
amp_password = 'cli'
path = "./EC"
pathFFT = "./CS wbFFT Data"
ssh_timeout = 30000  #msec
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