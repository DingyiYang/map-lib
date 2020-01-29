# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 09:14:34 2019

@author: DYYang
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 16:10:39 2019

@author: DYYang
"""
import csv
import os
import json
import xlrd
from pypinyin import pinyin, lazy_pinyin

def loadFont(filename):
    if(os.path.exists(filename)==False):
        return "False";
    f = open(filename, encoding="utf-8")  #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
    setting = json.load(f)
    #family = setting['BaseSettings']['size']   #注意多重结构的读取语法
    #size = setting['fontSize']   
    return setting;

#读取xlsx表
data = xlrd.open_workbook('china_swine_flu_v8.xlsx')

break_num={}
first_break={}
first_break_date={}
#table = data.sheet_by_name(u'猪瘟爆发时间表')#通过名称获取
table = data.sheets()[0]

ids=table.col_values(0)
break_date=table.col_values(1)
province=table.col_values(4)

#num_range=[1,4,7,11,21,30]
num_range=[20180800,20180900,20181000,20181100,20181200,20190200]

temp_colume=0
for pro in province:
    if(temp_colume==0):
        temp_colume+=1
        continue
    if(pro in break_num):
        break_num[pro]+=1
    else:
        break_num[pro]=1
        temp_date=break_date[temp_colume].split("年")
        temp_year=temp_date[0]
        temp_str=temp_date[1].split("月")
        temp_month=temp_str[0]
        temp_day=temp_str[1].split("日")[0]
        if(len(temp_month)==1):
            temp_month="0"+temp_month
        if(len(temp_day)==1):
            temp_day="0"+temp_day
        first_break[pro]=int(temp_year+temp_month+temp_day)
        first_break_date[pro]=temp_year+"."+temp_month+"."+temp_day
    temp_colume+=1


china_data=loadFont("china_countries.json")
country_id=0

for country in china_data["features"]:
    temp_name=country["properties"]["name"]
    if(temp_name[0]=='黑' or temp_name[0]=='内'):
        temp_name=temp_name[0]+temp_name[1]+temp_name[2]
    else:
        temp_name=temp_name[0]+temp_name[1]
    china_data["features"][country_id]["properties"]["chinese_name"]=temp_name
    name_loc=-1  
    china_data["features"][country_id]["properties"]["name"]=''.join(lazy_pinyin(temp_name)).capitalize()
    if(temp_name in break_num):
        china_data["features"][country_id]["properties"]["main_data"]=first_break[temp_name]
        china_data["features"][country_id]["properties"]["hasData"]=1
        for i in range(len(num_range)-1):
            if(first_break[temp_name]>=num_range[i] and first_break[temp_name]<num_range[i+1]):
                china_data["features"][country_id]["properties"]["stage"]=i
                break
    else:
        china_data["features"][country_id]["properties"]["main_data"]=0
        china_data["features"][country_id]["properties"]["hasData"]=0
        china_data["features"][country_id]["properties"]["stage"]="null"
    china_data["features"][country_id]["properties"]["dx"]=0
    china_data["features"][country_id]["properties"]["dy"]=0
    country_id=country_id+1

with open("china_provinces_bilingual.json","w",encoding="utf-8") as fout:
    json.dump(china_data,fout,ensure_ascii=False)