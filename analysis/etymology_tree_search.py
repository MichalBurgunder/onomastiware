import csv
from re import I
import pandas as pd
from os import system
import time
import numpy as np
import os

from file_management import write_into_one_csv

global ety_depth
global clean_name
global element_hash_map
global clean_name_pos

def header_hashmaps(headers):
    head_i_hm = {}
    i_head_hm = {}
    
    for i in range(0,len(headers)):
        i_head_hm[i] = headers[i]
        head_i_hm[headers[i]] = i
    return {"it": i_head_hm, "ti": head_i_hm}
      
def find_clean_name_position(headers):
    for i in range(0,len(headers)):
        if headers[i] == "Cleaned Name":
            return i
    raise "Cannot find 'Cleaned Name' column"


def get_headers(path):
    with open(path) as file:
            return next(file)

def merge_csv_headers(root, paths):
    headerss = []
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    # with open(f"{root}/temp.txt", "wt") as fw:
    #     writer = csv.writer(fw)
    #     for path in paths:
    #         with open(f"{root}/{path}") as file:
    #             info = csv.reader(file, delimiter=',')
                
    #             for row in info:
    #                 writer.writerow(row)
    # #                 break
    path = write_into_one_csv(root, paths, "headers", True)
    
    file = csv.reader(open(path, mode ='r'))
    for i in range(0, len(paths)):  
        headerss.append(next(file))
    
    os.remove(path)
    return headerss

def merge_csv_data(root, paths):
    lines = []
    path = write_into_one_csv(root, paths, "data")
    
    file = csv.reader(open(path, mode ='r'))
    for i in range(0,len(paths)):  
        lines.append(next(file))
    
    os.remove(path)
    return

def get_headers_hashmap(root, paths):
    headerss = merge_csv_headers(root, paths)

    # we verify: length
    num_headers = len(headerss[0])
    if False in [len(headers) == num_headers for headers in headerss]:
        raise "Length of the headers are not the same:\n" + str(headerss)
    print()
    # we verify: each entry
    for i in range(0, num_headers):
        for j in range(1, len(headerss)):
            if headerss[0][i] != headerss[j][i]:
                print(headerss[0][i])
                print(headerss[j][i])
                raise "Entries in headers are not the same"

    return header_hashmaps(headerss[0]), headerss[0]
    
def prepare_data(root, paths):
    all_elements = []
    element_hash_map = {}
    header_hashmap, headers = get_headers_hashmap(root, paths)
    clean_name_pos = find_clean_name_position(headers)
    
    path = write_into_one_csv(root, paths, "data")
    
    file = csv.reader(open(path, mode ='r'))
    all_elements = []
    for line in file:
        all_elements.append(line)

    os.remove(path)
    
    for i in range(0, len(all_elements)):
        element_hash_map[all_elements[i][clean_name_pos]] = i

    # add_virtual_columns(all_elements, )
    return all_elements, element_hash_map, headers, header_hashmap

def add_virtual_columns(dataa, names, default_values):
    # all_elements, element_hash_map, headers, header_hashmap = dataa[0], dataa[1], dataa[2], dataa[3]
    # print(dataa[2])
    # exit()
    
    for i in range(0,len(names)):
        dataa[2].append(names[i]) # add to headers
        dataa[3]["ti"][names[i]] = len(dataa[2])-1 # add to headers hashmap
        dataa[3]["it"][len(dataa[2])] = names[i] # add to headers hashmap
    
        for j in range(1, len(dataa[0])): # add the default value to each entry
            dataa[0][j].append(default_values[i])
    # 
    # exit()
 
    
# The function that computes the max depth of an entry
def populate_depth(word, previous_jargons=[]):
    previous_jargons.append(word)
    if word not in element_hash_map["ti"]:
        if word not in additives:
            additives.append(word)
        return -1
    
    entry = element_hash_map["ti"][word]
    
    max_depths = [0]
    for j in range(0, jargon_entries):
        if lines[entry][ety_depth] != "-1": # if the entry has already been computed
            return lines[entry][ety_depth]
        
        if lines[entry][j] == "": # if there is no jargon entry
            continue
        
        if lines[entry][j] in previous_jargons: # if the entry is recursive
            for i in range(len(previous_jargons), 0, -1):
                if previous_jargons[i] == word:
                    return len(previous_jargons)-i
        
        # jargon must be there, and uncomputed
        max_depth = populate_depth(lines[entry][j], previous_jargons)
        max_depths.append(max_depth)
        
    return np.max(max_depths)
    
# # computes the etymology depth of any given entry
def populate_ety_depths(dataa):
    for i in range(0, len(dataa[0])):
        populate_depth(dataa[0][i])


    
# def read_from_csv(root, descriptor):
# def get_data(root, title):
#     if exists(f"{root}/{title}"):
#         res = []
#         with open(f"{root}/temp_{descriptor}", "wt") as fw:
#             for row in fw:
#                 res.append(row)
#     else:
#         data = prepare_data(root, )
#         save_as_csv(root, data, title)
#         return data
    

def merge_csv_headers(root, paths):
    headerss = []
    # code originating from here: https://stackoverflow.com/questions/36698839/python-3-opening-multiple-csv-files
    # with open(f"{root}/temp.txt", "wt") as fw:
    #     writer = csv.writer(fw)
    #     for path in paths:
    #         with open(f"{root}/{path}") as file:
    #             info = csv.reader(file, delimiter=',')
                
    #             for row in info:
    #                 writer.writerow(row)
    # #                 break
    path = write_into_one_csv(root, paths, "headers", True)
    
    file = csv.reader(open(path, mode ='r'))
    for i in range(0, len(paths)):  
        headerss.append(next(file))
    
    os.remove(path)
    return headerss
            