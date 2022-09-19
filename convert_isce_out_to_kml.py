#!/usr/bin/env python
# Filename: convert_isce_out_to_kml 
"""
introduction:

authors: Huang Lingcao
email:huanglingcao@gmail.com
add time: 08 August, 2016
"""

from optparse import OptionParser
import os,sys,json
import subprocess
import basic,io_function
from RSImage import RSImageclass
import RSImage

def draw_raster_data_by_gmt(gmt_bash,raster_tif,max_value):
    # if os.path.isfile(gmt_bash) is False:
    #     basic.outputlogMessage('file not exist: '+ gmt_bash)
    #     return False

    if os.path.isfile(raster_tif) is False:
        basic.outputlogMessage('file not exist: ' +raster_tif)
        return False

    Out_ps_file = os.path.splitext(raster_tif)[0]+ '.ps'
    Out_jpg_file = os.path.splitext(raster_tif)[0]+ '.jpg'
    if os.path.isfile(Out_ps_file):
        basic.outputlogMessage('GMT result file %s already exist, skip GMT draw'%Out_ps_file)
        return False

    #convet tiff to grd
    # exefile = '/home/hlc/programs/FWTools-2.0.6/bin_safe/gdal_translate'
    exefile = 'gdal_translate'
    OutputGrdfile =  os.path.splitext(raster_tif)[0]+ '.grd'
    CommandString = exefile + ' -of GMT ' + raster_tif + ' '+OutputGrdfile;
    basic.outputlogMessage(CommandString)
    (status, result) = subprocess.getstatusoutput(CommandString)
    basic.outputlogMessage(result)
    if os.path.isfile(OutputGrdfile) is False:
        return False

    #elimate the nan data
    OutputGrd_NaN_file  =  os.path.splitext(OutputGrdfile)[0]+ '_nan.grd'
    CommandString = 'grdclip ' +OutputGrdfile+ ' -Sb-99999/NaN ' +'-G'+OutputGrd_NaN_file
    basic.outputlogMessage(CommandString)
    (status, result) = subprocess.getstatusoutput(CommandString)
    basic.outputlogMessage(result)
    if os.path.isfile(OutputGrd_NaN_file) is False:
        return False

    #draw map
    #colorfile derived from gmt bash codes
    # colorfile = 'color.cpt'
    # if os.path.isfile(colorfile) is False:
    #     colorcptfile = os.path.join(exec_dir,colorfile)
    #     basic.copyfiletodir(colorcptfile,'.')
    #
    # if os.path.isfile(colorfile) is False:
    #     basic.outputlogMessage('file not exist : '+os.path.abspath(colorfile))
    #     return False


    offsetimg = RSImageclass()
    if offsetimg.open(raster_tif) is False:
        return False
    width = offsetimg.GetWidth()
    height = offsetimg.GetHeight()

    # max_offset_per_year = parameters.get_max_Offset_per_year()
    #os.path.join(exec_dir,'plot_abs_m.sh')
    exefile = gmt_bash
    CommandString = exefile + ' '+ OutputGrd_NaN_file + ' '+str(width)+' '+ str(height) +' '+Out_ps_file\
                    + ' '+ Out_jpg_file + ' '+str(max_value)
    basic.outputlogMessage(CommandString)
    (status, result) = subprocess.getstatusoutput(CommandString)
    basic.outputlogMessage(result)

    if os.path.isfile(Out_ps_file) is False:
        return False

    return Out_ps_file

def get_isce_geo_with_height(isce_geo):
    width = 0
    height =0

    CommandString = 'gdalinfo -json ' + isce_geo
    imginfo = basic.exec_command_string_output_string(CommandString)
    if imginfo is False:
        return False
    imginfo_obj = json.loads(imginfo)
    # print imginfo_obj
    # print type(imginfo_obj)
    # print imginfo_obj.keys()
    try:
        size_info = imginfo_obj['size']
        width = size_info[0]
        height = size_info[1]
    except KeyError:
        basic.outputlogMessage(str(KeyError))
        pass

    return (width,height)

def define_ref_points(intput_img,ref_lat,ref_lon):
    ref_phase_value = RSImage.get_image_location_value(intput_img, ref_lon, ref_lat, 'lon_lat_wgs84', 1)
    basic.outputlogMessage('reference point, lon: %s  lat: %s phase value: %s'%(str(ref_lat),str(ref_lon),str(ref_phase_value)))

    out_img = io_function.get_name_by_adding_tail(intput_img,'ref')
    expression = "A-"+str(ref_phase_value)
    return basic.exec_command_args_list_one_file(['gdal_calc.py','-A',intput_img,'--outfile='+out_img,'--calc='+expression],out_img)


def save_aoi_region_phase(isce_geo_unw):
    ulx = 93.972996
    uly = 35.743013
    lrx = 94.073745
    lry = 35.642603
    io_function.mkdir('merged')
    basic.exec_command_args_list(['isce2gis.py','envi', '-i', isce_geo_unw])
    isce_geo_unw_envi_hdr = isce_geo_unw+'.hdr'
    basic.exec_command_args_list(['mv','merged/filt_topophase.unw.geo.hdr',isce_geo_unw_envi_hdr])
    out_tif = isce_geo_unw+'.pha_sub.tif'
    basic.exec_command_args_list(['gdal_translate','-of', 'GTiff','-b',str(2),\
                                  '-projwin',str(ulx),str(uly),str(lrx),str(lry), \
                                  isce_geo_unw,out_tif])
    #define reference points
    # lat = 35.7159472222
    # lon = 94.0355972222
    lat = 35.70226388888889
    lon = 94.03267499999998
    out_tif = define_ref_points(out_tif, lat, lon)

    #draw aoi area by gmt
    if os.path.isfile(out_tif):
        result = draw_raster_data_by_gmt('plot_unwrap_phase.sh',out_tif, 10)

        # result = draw_raster_data_by_gmt('/home/hlc/bin/plot_unwrap_phase_icon.sh', out_tif, 20)
        # # output to kml
        # outkml = os.path.splitext(os.path.basename(out_tif))[0] +'.kml'
        # outicon = os.path.splitext(os.path.basename(out_tif))[0] +'.png'
        # f = open(outkml, 'w')
        # f.write('<?xml version="1.0" encoding="UTF-8"?>' + "\n")
        # f.write('<kml xmlns="http://earth.google.com/kml/2.2">' + "\n")
        # f.write('<GroundOverlay>' + "\n")
        # f.write('    <name>Scene Title Here</name>' + "\n")
        # f.write('    <description>Sentinel-1/Sentinel-1</description>' + "\n")
        # f.write('    <Icon>' + "\n")
        # f.write('          <href>' + outicon + '</href>' + "\n")
        # f.write('    </Icon>' + "\n")
        # f.write('    <LatLonBox>' + "\n")
        # f.write('        <north> ' + str(uly) + ' </north>' + "\n")
        # f.write('        <south> ' + str(lry) + ' </south>' + "\n")
        # f.write('        <east> ' + str(lrx) + ' </east>' + "\n")
        # f.write('        <west> ' + str(ulx) + ' </west>' + "\n")
        # f.write('    </LatLonBox>' + "\n")
        # f.write('</GroundOverlay>' + "\n")
        # f.write('</kml>' + "\n")
        # f.close()



def convert_isce_geo_to_kml(isce_geo):
    if io_function.is_file_exist(isce_geo) is False:
        return False
    outkml = isce_geo+'.kml'
    basic.exec_command_args_list(['mdx.py',isce_geo,'-kml',outkml])

    out_png = isce_geo+'.png'
    out_ppm = 'out.ppm'

    (width,height) = get_isce_geo_with_height(isce_geo)
    if isce_geo.find('unw.geo')>0:
        rmg2mag_phs = '/home/hlc/programs/ROI_PAC_3_0_1/bin/rmg2mag_phs'
        amp_band = isce_geo + '.amp'
        pha_band = isce_geo+'.pha'
        basic.exec_command_args_list([rmg2mag_phs,isce_geo,amp_band,pha_band,str(width)])
        basic.exec_command_args_list(['mdx', '-CW','-P', '-cols', str(width), '-rows', str(height), '-cmap', 'cmy', pha_band])

        # save_aoi_region_phase(isce_geo)

    elif isce_geo.find('cor.geo')>0:
        return True
    else:
        basic.exec_command_args_list(['mdx', '-P', '-c8pha ','-cols',str(width),'-rows',str(height),'-cmap','cmy',isce_geo])


    basic.exec_command_args_list(['convert',out_ppm,out_png])
    # basic.exec_command_args_list(['rm',out_ppm])

if __name__=='__main__':

    isce_geo = []
    if len(sys.argv) > 1:
        isce_geo.append(sys.argv[1])
        print(isce_geo)
    else:
        isce_geo = os.popen('ls  *.unw.geo').readlines()
        print (isce_geo)
    count = len(isce_geo)


    count = len(isce_geo)
    for i in range(0,count):
        geo_file = isce_geo[i].split()[0]
        basic.outputlogMessage('convert %s'%geo_file)
        convert_isce_geo_to_kml(geo_file)


    # for i in range(0, count):
    #     geo_file = isce_geo[i].split()[0]
    #     basic.outputlogMessage('save aoi to gmt %s' % geo_file)
    #     save_aoi_region_phase(geo_file)



