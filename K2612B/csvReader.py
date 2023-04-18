# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 16:20:02 2018

@author: gsanca
"""

import csv

path            = ".\\results\\"
ext_fig         = ".png" 
ext_txt         = ".csv" 
dateString      = "1807311634"
text_name       = path + dateString + ext_txt
rState          = []
vState          = []
hslV            = 0.2

i = 0
j = 0
with open(text_name) as csvfile:
    reader      = csv.reader(csvfile, delimiter='\t')
    List        = list(reader)   
    for row in List:
        if i >= 15:
            if round(float(row[1]),1) == hslV:
                rState.append((row[3]))
                vState.append(List[j-1][1])
        j = j + 1        
        i = i + 1
#aux = round(aux,1)
#
#
#14

#"""
#Save function. Use this to save data in file. The file name is given by
#the day and hour, in format: yymmddhhmm. 
#Use this function to save V, I and R data (and meta data).
#"""
#[unused,completeDate,dateString] = date_time_now()
## For makin this cross platform, change the path name
#path          = ".\\results\\"
#ext_fig       = ".png" 
#ext_txt       = ".csv" 
#figure_name   = path + dateString + ext_fig
#text_name     = path + dateString + ext_txt
#"""
#Check if the folder exist. This is only Windows compatible (because of VISA)
#"""
#if not(os.path.exists(path)):
#    os.makedirs(path)
#File = open(text_name, 'w')
#
#"""
#Header:
#     - date:hour
#     - metaData:
#             - configuration
#"""    
#File.write("\n") 
#File.write(completeDate + "\n")
#for lines in metaData:
#    File.write(lines + "\n")
#File.write("\n")
#File.write("Time\tV\tI\tR\n")
#if len(readingsV) == len(readingsI) and len(readingsV) == len(calculatedR): 
#    for i in range(0,len(readingsV)):
#        line = str(times[i]) + '\t' + str(readingsV[i]) + '\t' + str(readingsI[i]) + '\t' + str(calculatedR[i]) +'\n' 
#        File.write(line)
#else:
#    File.write('R\n')
#    for i in range(0,len(calculatedR)):        
#            line = str(calculatedR[i]) + '\n'
#            File.write(line)
#File.close()
#if graph != 'NULL':
#    graph.savefig(figure_name, dpi=250, bbox_inches='tight')
#print("Saved as... ")
#print(path + dateString) + ".*"