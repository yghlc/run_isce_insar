#!/usr/bin/env python
# Filename: check_S1A_md5 
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 08 August, 2016
"""
from optparse import OptionParser
import os,sys
import basic,io_function

md5_dict = {'FILE_NAME':'md5_string'}

def down_load_s1a(url_str,file_name):
    # basic.exec_command_args_list(['wget','--no-check-certificate','--user="yghlc"','--password="hlcinsar123"','--continue',\
    #                               '--output-document='+file_name,url_str])
    #read user name and password
    user_file = ".credentials"
    file_obj = open(user_file)
    if file_obj is None:
        basic.outputlogMessage("open % failed"%os.path.abspath(user_file))
        return False
    str_list = file_obj.readline().split()[0].split(':')
    basic.exec_command_args_list(['wget','--no-check-certificate','--user='+str_list[0],'--password='+str_list[1],'--continue',\
                                  '--output-document='+file_name,url_str])

    file_obj.close()

    # basic.exec_command_args_list(['wget', '--no-check-certificate','--https-only', \
    #                               '--user="yghlc"', '--ask-password="hlcinsar123"', '--continue', \
    #                             '--output-document=' + file_name, url_str])
    pass


def read_file_md5(file):
    md5_list_file = 'md5_list.txt'
    if os.path.isfile(md5_list_file):
        md5_file_obj = open(md5_list_file,'r')
        lines = md5_file_obj.readlines()
        for line in lines:
            line_list = line.split()
            md5_dict[line_list[0]] = line_list[1]
        md5_file_obj.close()

    if md5_dict.has_key(file):
        return md5_dict[file]
    return False

def write_file_md5():
    md5_list_file = 'md5_list.txt'
    md5_file_obj = open(md5_list_file,'w')
    for (k,v) in md5_dict.items():
        md5_file_obj.writelines(k+' '+v+'\n')
    md5_file_obj.close()

    return True



def get_file_md5(file):
    basic.outputlogMessage('cal md5 for '+file)
    #on mac
    # md5_str = os.popen('md5 '+file).read()
    # md5_list = md5_str.split()
    # if len(md5_list) !=4:
    #     basic.outputlogMessage('get md5 failed')
    #     return False
    # return md5_list[3]
    #on ubuntu
    md5_str = os.popen('md5sum '+file).read()
    md5_list = md5_str.split()
    if len(md5_list) !=2:
        basic.outputlogMessage('get md5 failed')
        return False
    return md5_list[0]

def main(options, args):
    meta_file = args[0]
    if io_function.is_file_exist(meta_file) is False:
        return False
    file_name = os.popen('grep name= '+ meta_file).readlines()
    file_md5 = os.popen('grep MD5 '+ meta_file).readlines()
    file_url = os.popen('grep https:  '+ meta_file).readlines()
    if len(file_name) != len(file_md5):
        basic.outputlogMessage("the number of file and md5 is not same")
        return False
    count = len(file_name)
    if len(file_url) != count:
        basic.outputlogMessage("the number of url is not required")
        return False

    for i in range(0,count):
        str_list = file_name[i].split('\"')
        file_name[i] = str_list[1]
        str_list = file_md5[i].split('>')
        str_list = str_list[1].split('<')
        file_md5[i] = str_list[0]
        str_list = file_url[i].split('>')
        str_list = str_list[1].split('<')
        file_url[i] = str_list[0]
        # print file_name[i],file_md5[i],file_url[i]

    if os.path.isfile('check_result.txt'):
        io_function.delete_file_or_dir('check_result.txt')

    for i in range(0, count):
        file_obj = open('check_result.txt', 'a')
        #check
        basic.outputlogMessage('check '+ file_name[i] )
        if os.path.isfile(file_name[i]) is False:
            file_obj.writelines(file_name[i] + '  not exist \n')
            basic.outputlogMessage('Begin download %s'%file_name[i])
            down_load_s1a(file_url[i],file_name[i])

        cal_md5 = read_file_md5(file_name[i])
        if cal_md5 is False:
            cal_md5 = get_file_md5(file_name[i])
            md5_dict[file_name[i]] = cal_md5
            write_file_md5()

        if cal_md5.upper() != file_md5[i].upper():
            file_obj.writelines(file_name[i] + ' not correct \n')
            basic.outputlogMessage('re-download %s' % file_name[i])
            io_function.delete_file_or_dir(file_name[i])
            down_load_s1a(file_url[i], file_name[i])
            #get and save new md5
            cal_md5 = get_file_md5(file_name[i])
            md5_dict[file_name[i]] = cal_md5
            write_file_md5()


        file_obj.close()




    pass

if __name__=='__main__':
    usage = "usage: %prog [options] download_meta4"
    parser = OptionParser(usage=usage, version="1.0 2016-8-8")
    # parser.add_option('-s', "--swatch", action="store", dest="swatch_num", default=2,
    #                   help="the swatch number of sentinel1A, eg '1'")
    # parser.add_option('-o', "--orbit_folder", action='store_true', dest='orbit_folder', default='orbit',
    #                   help="oribt folder path")

    (options, args) = parser.parse_args()
    if len(sys.argv) < 2 or len(args) < 1:
        parser.print_help()
        sys.exit(2)

    if len(args) < 1:
        basic.outputlogMessage('1 argumets is required')
        parser.print_help()
        sys.exit(2)

    main(options, args)

