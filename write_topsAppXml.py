#!/usr/bin/env python
# Filename: write_topsAppXml.py 
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 07 August, 2016
"""
import sys,basic,io_function
from xml_rw import XmlClass
from optparse import OptionParser



def main(options, args):
    template_xml = args[0]
    if io_function.is_file_exist(template_xml) is False:
        return False

    master_input_SAFE = args[1]
    slave_input_SAFE = args[2]

    xml_obj = XmlClass(template_xml)
    xml_obj.phrase_xml()
    topsinsar_nodes = xml_obj.get_sub_element(xml_obj.root,'component')
    sub_component_nodes = xml_obj.get_sub_element(topsinsar_nodes[0],'component')


    #master
    sub_master_property = xml_obj.get_sub_element(sub_component_nodes[0],'property')
    xml_obj.set_exist_element_text(sub_master_property[3],master_input_SAFE)

    #slave
    sub_master_property = xml_obj.get_sub_element(sub_component_nodes[1],'property')
    xml_obj.set_exist_element_text(sub_master_property[3],slave_input_SAFE)


    xml_obj = None

    pass


if __name__=='__main__':
    usage = "usage: %prog [options] old_xml master slave"
    parser = OptionParser(usage=usage, version="1.0 2016-8-7")
    parser.add_option('-s',"--swatch",action="store",dest="swatch_num",default=2,
                      help="the swatch number of sentinel1A, eg '1'")
    parser.add_option('-o',"--orbit_folder",action='store_true',dest='orbit_folder',default='orbit',
                      help="oribt folder path")

    (options, args) = parser.parse_args()
    if len(sys.argv) < 2 or len(args) < 1:
        parser.print_help()
        sys.exit(2)

    if len(args) < 3:
        basic.outputlogMessage('3 argumets is required')
        parser.print_help()
        sys.exit(2)

    main(options, args)