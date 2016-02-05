# ArcpyDAMapBookRiverMileListRotatedJPG.py
#
# Generate a River MapBook based on Start and End River Miles
# User supplies a CSV file that has two values in each row: Start, End
# 
#
# Tom Gushue
# June 11, 2014
#
# 
#                   Parameter Properties
# Program Name                Display Name  Data type       Type      Direction
# arcpy.GetParameterAsText(0) outFolder     Folder          Required  Input
# arcpy.GetParameterAsText(1) chkCreateMAPS Boolean         Required  Input
# arcpy.GetParameterAsText(2) startMile     Text            Required  Input
# arcpy.GetParameterAsText(3) stopMile       Text            Required  Input

import re
import sys
import string
import os
import time
import csv
import arcpy
from arcpy import env

# Turn on history logging so that a history log file is written
arcpy.LogHistory = True
env.overwriteOutput = True

# Toggle Map Production ON or OFF
inFile = arcpy.GetParameterAsText(0)
outFolder = arcpy.GetParameterAsText(1)
chkCreateMAPS = arcpy.GetParameterAsText(2)
#startMile = arcpy.GetParameterAsText(2)
#stopMile = arcpy.GetParameterAsText(3)

# FUTURE WORK:  Allow user to select from list of standard river map scales (1:2000, 1:2500, 1:3000, 1:4000, 
1:5000)
# The selected value (2000, 2500, 3000) is then passed to a variable and used to select the appropriate, 
pre-made MXD that is set to that scale.
# The MXD also has a particular river mile increment already used for Data Driven Pages (i.e. 0.2 mile, 0.3 
mile).
# selectScale = 

#tmpFile = str(inFile.replace("\\","/")) + str("/")
#rmFile = str(os.path.split(tmpFile)[1])

#arcpy.AddMessage(" ")
#arcpy.AddMessage("Map Output Folder Path is: " + tmpFile)
#arcpy.AddMessage(" ")

# Correct the Path to the Workspace
outWS = str(outFolder.replace("\\","/")) + str("/")
arcpy.AddMessage(" ")
arcpy.AddMessage("Map Output Folder Path is: " + outWS)
arcpy.AddMessage(" ")

# Reference the current map document
# Define the map document
mxd = arcpy.mapping.MapDocument("CURRENT")
arcpy.AddMessage("Got current map")
arcpy.AddMessage(" ")

# Reference data frames
# Define the data frames
MainMap = arcpy.mapping.ListDataFrames(mxd, "Main Map Frame")[0]
LocalIndicator = arcpy.mapping.ListDataFrames(mxd, "Local Indicator")[0]
arcpy.AddMessage("Got data frames")
arcpy.AddMessage(" ")

#Reference the River Miles to print based on Input File provided
# PLACEHOLDER FOR INPUTTING RIVER MILE GEODATABASE AND FEATURE CLASS, MAY NOT BE NECESSARY
#inGDB =
with open(inFile, 'rb') as f:
    rmCSV = csv.reader(f)
    for row in rmCSV:
        startMile = row[0]
        stopMile = row[1]
        arcpy.AddMessage("startMile = " + str(startMile))
        arcpy.AddMessage("stopMile = " + str(stopMile))
        arcpy.AddMessage(" ")

        fltStartMile = float(startMile)
        fltStopMile = float(stopMile)
        arcpy.AddMessage("fltStartMile = " + str(fltStartMile))
        arcpy.AddMessage("fltStopMile = " + str(fltStopMile))
        arcpy.AddMessage(" ")

        if (fltStartMile >= fltStopMile or startMile == "" or stopMile == ""):
            arcpy.AddMessage("No Miles selected. All points will be processed")
            arcpy.AddMessage(" ")  
            sys.exit()
        
        for layer in arcpy.mapping.ListLayers(mxd, "", MainMap):
            if (layer.name == "RiverMileThreeTenths_RotateAngle"):
                arcpy.AddMessage("Found RiverMileThreeTenths_RotateAngle!")
                arcpy.AddMessage(" ")
                rmPoints = layer
                rmSearch = arcpy.da.SearchCursor(rmPoints, ["TENTH_MILE"])
                fltSearch = float(rmSearch)
                for rmRow in fltSearch:
                    #exp = " \"TENTH_MILE\" >= " + (fltStartMile) AND " \"TENTH_MILE\" <= " +  (fltStopMile)
                    #exp = fltSearch >= fltStartMile) AND fltSearch <= fltStopMile)
                    exp = '"TENTH_MILE" >= ' + fltStartMile + ' AND "TENTH_MILE" <= ' + fltStopMile #Updated exp 
by TCJ 20150727
                    arcpy.AddMessage(" ")
                    arcpy.AddMessage("expression = " + str(exp))
                    arcpy.AddMessage(" ")
                               
                #searchRows = arcpy.SearchCursor(rmPoints, "", "", "", "TENTH_MILE A")

                    mapMiles = arcpy.SelectLayerByAttribute_management(rmPoints, "NEW_SELECTION", exp)
                    for rmMap in mapMiles:
                        try:
                            
                            #Export each of the data driven pages
                            for pgNum in range(1, mxd.dataDrivenPages.pageCount + 1):
                                mxd.dataDrivenPages.currentPageID = pgNum
                                maxDDPages = mxd.dataDrivenPages.pageCount
                                #searchRow = searchRows.next()
                                firstTenth = str(rmMap)
                                fltTenth = float(firstTenth)
                        
                                if ((fltTenth >= fltStartMile) and (fltTenth <= fltStopMile)):
                                    theRotation = MainMap.rotation
                                    LocalIndicator.rotation = theRotation
                              
                                    if (chkCreateMAPS == "true"):
                                        OutJPG = str(outWS) + str(firstTenth) + ".jpg"
                                        arcpy.AddMessage("Out JPG location = " + str(outWS))
                                        arcpy.mapping.ExportToJPEG(mxd, OutJPG, resolution=300)
                                        #arcpy.mapping.ExportToJPEG(mxd, OutJPG)
                                        arcpy.AddMessage("Full Output JPG File Path = " + str(OutJPG))
                                        arcpy.AddMessage(" ")
                        
                                    else:
                                        time.sleep(2)
                                        # If an error occurred while running a tool, then print the messages.
                                        arcpy.GetMessages()
                        
                                elif (fltTenth > fltStopMile):
                                    #del fltStartMile
                                    #del fltStopMile
                                    #next(row)
                                    #arcpy.AddMessage("OVER HERE!!!!!!!!!!")
                                    #arcpy.AddMessage("GO TO NEXT START MILE:  " + str(startMile))
                                    #arcpy.AddMessage(" ")
                                    sys.exit()
                        except:
                            
        
del mxd

