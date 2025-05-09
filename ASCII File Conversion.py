import arcpy
from datetime import datetime
import os

date= datetime.today().strftime('%Y-%m-%d')

#variables to change
wd = r"xxxxxx" #location you want output folder to be created in
ProjectName="xxxxxx"
asciifold= r"xxxxxx"#location of ascii files
cellsize=2 #if file size over 250mb re-run with cell size of 5

#Create output folder to be uploaded to sharepoint
outputname=f"{date}_{ProjectName}_EG_Surface_{cellsize}X{cellsize}.tif"
output_location = os.path.join(wd,f"{date}_{ProjectName}_EG_Surface_{cellsize}X{cellsize}")
if not os.path.exists(output_location):
    os.makedirs(output_location)

#create pixel type tuple to get tool input from property
pixel_types = {
    "U1": "1_BIT",
    "U2": "2_BIT",
    "U4": "4_BIT",
    "S8": "8_BIT_SIGNED",
    "U8": "8_BIT_UNSIGNED",
    "S16": "16_BIT_UNSIGNED",
    "U16": "16_BIT_SIGNED",
    "S32": "32_BIT_UNSIGNED",
    "U32": "32_BIT_SIGNED",
    "F32": "32_BIT_FLOAT",
    "F64": "64_BIT"
}

#iterate through acsii files in folder to set variables and make sure all files match
arcpy.env.workspace = asciifold
rasfile=arcpy.ListRasters()
checklist=[] #this is to hold values to be checked
for ras in rasfile:
    desc=arcpy.Describe(ras)
    spref=desc.spatialReference
    band= desc.bandCount
    pixel_type = pixel_types[desc.PixelType]
    ras_info=[spref.name,band,pixel_type]
    check=[spref.name,band,pixel_type]
    #check to make sure all files have properties
    if check != checklist:
        checklist.extend(check)
        print(checklist) #if more than one value for each property is printed then one file differs from others in ascii folder

#run mosaic to raster tool
arcpy.management.MosaicToNewRaster(rasfile, output_location,outputname, spref, pixel_type, cellsize, band)

#check output folder size (note:windows uses binary sizes so 1MB = 1048576 bytes ¯\\(ツ)/¯)
def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total/1048576

sizeMB=get_dir_size(output_location)

if sizeMB>250:
    print(f"file size {sizeMB}mb, rerun tool with increased cell size")
else:
    print ("file under 250 mb")