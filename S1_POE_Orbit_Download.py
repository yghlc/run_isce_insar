#!/usr/bin/env python3
##################################
# V1.0, Aug-08, 2016, ESSC@CUHK	          
# V1.1, Apr-27, 2018, ERI@U-Tokyo
# V1.2, Aug-4, 2018, ERI@U-Tokyo
####################################################################################
#
# 1) the work path should have a text file containing the RAW data with zip list,
#    e.g., raw_list.txt,
#       S1A_IW_SLC__1SSV_20160511T205050_20160511T205117_011216_010F42_F44A.zip
#       S1A_IW_SLC__1SDV_20180101T205116_20180101T205144_019966_022010_1246.zip
#
# 2) run this script: S1_POE_Orbit_Download.py raw_list.txt  
#    A folder with name of "POE" will be created for putting the downloaded EOF files in the work path.
#
# Notes: Python3 should be pre-installed 
#        
##################################
import numpy as np
import datetime
import urllib.request
import ssl
import re
import os
import subprocess
import argparse
import sys
#################################################################################
INTRODUCTION = '''
  Python script for downloading the Sentinel-1 Precise Orbit Ephemerides (POE) data;
  Please make sure the python3 has been pre-installed in your OS env
'''

EXAMPLE = '''EXAMPLES:

  S1_POE_Orbit_Download.py raw_list.txt 

'''    

def cmdLineParse():
    parser = argparse.ArgumentParser(description='Sentinel-1 POE Orbit Data Downloading',\
                                     formatter_class=argparse.RawTextHelpFormatter,\
                                     epilog=INTRODUCTION+'\n'+EXAMPLE)

    parser.add_argument('raw_list',help="text file containing the S1 ZIP list.")

    inps = parser.parse_args()
    return inps

##################################################################################
def main(argv):
    
    work_path = os.getcwd()
    inps = cmdLineParse()
    zip_list = inps.raw_list
    im_list = np.loadtxt(zip_list,dtype=np.str,ndmin=1)
    
    POE_path = work_path+"/POE"
    os.environ['POE_path'] = str(POE_path);

# Judge whether the POE folder is existing 
    if os.path.exists(POE_path):
        print('Already having the POE foloder')
    else:
        os.popen('mkdir $POE_path')

# List the raw list data 
#    im_list=os.popen('ls $RAW_path | grep ^S1.*SAFE$').read().split()

    for im_var in im_list:
        print("Download the POE orbit file for the list Sentinel-1 image:\n", im_var)
        ###############################Read the image acquire time 
        Sensor=im_var[0:3];
        Sence_time=im_var[17:25];
        
        Year=int(Sence_time[0:4]);
        Month=int(Sence_time[4:6]);
        Day=int(Sence_time[6:8]);

        Sence_day=datetime.date(Year,Month,Day);
        Inset_Day=format(Sence_day-datetime.timedelta(days=1)); #Determine the date
##       
        url_ymd=format(Inset_Day);
        url_y=Inset_Day[0:4];
        url_ym=Inset_Day[0:7];
        url_m=int(Inset_Day[5:7]);
        url_d=int(Inset_Day[8:10]);

###Pre information
        Mon_31=[1,3,5,7,8,10,12] #Months with 31 days
        Mon_30=[4,6,9,11]        #MOnths with 30 days
        Page_Day=np.array([4,7,10,13,16,19,22,25,28,29,30,31],dtype=int)
        
###Find the Start Day (Inset_FDay) and Last Day (Inset_LDay)

        Diff_Day=Page_Day-url_d;
        idx=np.nonzero(Diff_Day>=0)[0][0]
        Inset_LDay=Page_Day[idx];

        if Inset_LDay <=28:
            Inset_FDay=Inset_LDay-3;
        elif Inset_LDay>28 and url_m in Mon_31:
            Inset_FDay=28;
            Inset_LDay=31;
        elif Inset_LDay>28 and url_m in Mon_30:
            Inset_FDay=28;
            Inset_LDay=30;
        elif Inset_LDay==29 and url_m==2:
            Inset_FDay=28;
            Inset_LDay=29;

        Start_day=format(datetime.date(int(url_y),url_m,Inset_FDay));
        End_day=format(datetime.date(int(url_y),url_m,Inset_LDay));
       
        ##############################Generate the download url

        url_pre='https://qc.sentinel1.eo.esa.int/aux_poeorb/?';
        url_poe='&validity_start='+str(url_y)+'&validity_start='+url_ym+'&validity_start='+Start_day+'..'+End_day+'&validity_start='+url_ymd;
        url_download=url_pre+url_poe;
        print(url_download)
        ###############################Download the page_info and get the POE name 
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        up=urllib.request.urlopen(url_download,context=ctx)
        cont=up.read()
        
        #file_object = open('./dl.html', 'w') 
        #file_object.write(str(cont))
        #file_object.close()
    
        ###############################Download the POE data 
        #file_object = open('text.html').read()
        pat=re.compile(Sensor+"_OPER.*.EOF");
        pat_mat=pat.search(str(cont));
        
        if pat_mat is None:
            print("****The precise oribt data for this image is not available now****")
            continue
        else:    
            mat=pat_mat.group()
            POE_name=mat[0:77];
            print();print(POE_name);print()
            POE_file=POE_path+'/'+POE_name
            if  os.path.exists(POE_file):
                print("****The orbit file for this scene has been downloaded already****")
                print("*****************************************************************")
                continue
            else:
                dl_yyyy=mat[25:29]
                dl_mm=mat[29:31]
                dl_dd=mat[31:33]
                dl_head='http://aux.sentinel1.eo.esa.int/POEORB/'+dl_yyyy+'/'+dl_mm+'/'+dl_dd+'/'
                dl_url=dl_head+POE_name;
                cmd='wget '+'-P '+POE_path+' '+dl_url+' --no-check-certificate'
                subprocess.call(cmd,shell=True)
#            data_tmp=urllib.request.urlopen(dl_url,context=ctx)
#            data_w=data_tmp.read()
#            with open(POE_file, "wb") as flg:     
#                flg.write(data_w)
###############################################################################

if __name__ == '__main__':
    main(sys.argv[1:])

