#!/usr/bin/env python
# Filename: bash_run_topsApp.sh 
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 07 August, 2016
"""

import sys,os
import basic,io_function

def get_date_str_of_sentinel(sentinel_safe):
    dir_name = os.path.basename(sentinel_safe)
    # print dir_name
    # sys.exit(1)
    date_str = dir_name[17:17+8]
    return date_str

def copy_one_result_file(org_dir,dest_dir,filename):
    geo_file = os.path.join(org_dir, 'merged', filename)
    geo_xml_file = os.path.join(org_dir, 'merged', filename + '.xml')
    result_geo = os.path.join(dest_dir, org_dir + '_' + filename)
    result_geo_xml = os.path.join(dest_dir, org_dir + '_' + filename + '.xml')
    if os.path.isfile(geo_file):
        io_function.copy_file_to_dst(geo_file, result_geo)
    if os.path.isfile(geo_xml_file):
        io_function.copy_file_to_dst(geo_xml_file, result_geo_xml)
    return True

def copy_result_files(org_dir,dest_dir):
    filt_flat_geo = 'filt_topophase.flat.geo'
    filt_flat_unw_geo = 'filt_topophase.unw.geo'
    dem_geo = 'dem.crop'

    #filt_flat_geo
    copy_one_result_file(org_dir,dest_dir,filt_flat_geo)

    #filt_flat_unw_geo
    copy_one_result_file(org_dir, dest_dir, filt_flat_unw_geo)

    copy_one_result_file(org_dir, dest_dir,dem_geo)

    copy_one_result_file(org_dir,dest_dir,'filt_topophase.unw.conncomp')

    copy_one_result_file(org_dir, dest_dir, 'phsig.cor.geo')


    return True

def process_2_pass(master_dir,slave_dir):
    master_date_str = get_date_str_of_sentinel(master_dir)
    slave_date_str = get_date_str_of_sentinel(slave_dir)
    if master_date_str==slave_date_str:
        basic.outputlogMessage('the input two pair have same acquired date,skipping')
        return True
    process_dir = master_date_str+'_'+slave_date_str
    result_geo = os.path.join('result', process_dir + '_filt_topophase.flat.geo')
    result_geo_xml = os.path.join('result', process_dir + '_filt_topophase.flat.geo.xml')
    if os.path.isfile(result_geo):
        basic.outputlogMessage('result already exist, skip process')
        return True
    io_function.mkdir(process_dir)
    io_function.copy_file_to_dst('../topsApp.xml',  os.path.join(process_dir,'topsApp.xml'))

    # sys.exit(1)

    os.chdir(process_dir)
    # cmd_str = 'write_topsAppXml.py '+ 'topsApp.xml'+' ' + os.path.relpath(master_dir) + ' ' + os.path.relpath(slave_dir)
    # print cmd_str
    basic.exec_command_args_list(['write_topsAppXml.py', 'topsApp.xml',master_dir,slave_dir])

    # sys.exit(1)

    # cmd_str = 'topsApp.py --steps'
    basic.exec_command_args_list(['topsApp.py','--steps'])
    os.chdir('..')

    #copy result
    copy_result_files(process_dir,'result')

    #remove files
    #os.system('rm -r '+process_dir)
    pass

if __name__=='__main__':
    data_dir='data'
    io_function.mkdir('result')
    file_obj = open('s1a_list.txt')
    safe_dirs = file_obj.readlines()
    if safe_dirs is False:
        basic.outputlogMessage('Get sentinel safe_dirs failed')
        sys.exit(1)

    for i in range(0, len(safe_dirs)):
        safe_dirs[i] = safe_dirs[i].strip('\n')
        safe_dirs[i] = safe_dirs[i].strip('\r').strip()

    # ignore empty lines
    safe_dirs = [ item for item in  safe_dirs if len(item) > 0 ]

    # print safe_dirs
    # sys.exit(1)

    count = len(safe_dirs)
    if(count<2):
        basic.outputlogMessage('input less than 2')
        sys.exit(2)

    for i in range(0,count-1):
        basic.outputlogMessage('begin proces %s and %s'%(safe_dirs[i],safe_dirs[i+1]))
        process_2_pass(os.path.abspath(safe_dirs[i]),os.path.abspath(safe_dirs[i+1]))
