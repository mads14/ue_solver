# coding: utf-8

"""
created on Mon Jun 13
@author: msheehan
"""
import pandas as pd
import geopandas as gpd
import numpy as np
import json
from sklearn.neighbors import KNeighborsClassifier


def demand_to_virtual_node(taz_demand_csv, taz_node_dict, scale, demand_outf):
    # taz_dict_f = 'resources/input_files/demand/taz_dict.txt'
    taz_demand_df = pd.read_csv(taz_demand_csv)
    taz_node_dict = pd.DataFrame.from_dict(taz_node_dict).T
    # taz_node_dict = pd.read_json(taz_dict_f, dtype='int').T

    taz_demand_df['origin_node'] = taz_demand_df['tazi'].map(taz_node_dict['origin'], 'ignore')
    taz_demand_df['dest_node'] = taz_demand_df['tazj'].map(taz_node_dict['destination'], 'ignore')
    taz_demand_df.dropna(inplace=True)
    node_demand_df = taz_demand_df[['origin_node','dest_node']].astype(int)
    node_demand_df['flow (whole morning commute)'] = taz_demand_df['flow (whole morning commute)']
    node_demand_scaled = scale_demand(node_demand_df, scale)

    write_output(node_demand_scaled.as_matrix(), demand_outf)


def scale_demand(node_demand_df, scale):
    scaled_demand = node_demand_df[['origin_node','dest_node']].astype(int)
    scaled_demand['demand'] = node_demand_df['flow (whole morning commute)']/float(scale)
    return scaled_demand

def write_output(ODS_nodes, fname):
    ODs_sorted = sort_ODs_by_flow(ODS_nodes)
    write_OD_textfile_in_cpp_format(ODs_sorted, fname)
    
def sort_ODs_by_flow(ODs_unsorted):
    def Get_key(item):
        return item[2]
    ODs_sorted = np.asarray(sorted(ODs_unsorted, key = Get_key))
    return ODs_sorted


def write_OD_textfile_in_cpp_format(clean_ODs, filename):
    n_zones = count_total_origins_or_dests(clean_ODs)
    total_flow = np.sum(clean_ODs[:,2])
    def Get_key(item): return item[0] #sort by the origin
    ODs_sorted = np.asarray(sorted(clean_ODs, key = Get_key))
    
    def write_new_origin_as_string(i):
        current_origin = ODs_sorted[i][0]
        text_file.write('Origin '+str(int(current_origin))+'\n')
        return current_origin    
    text_file = open(filename, "w")
    text_file.write('<NUMBER OF ZONES> '+str(n_zones)+'\n')
    text_file.write('<TOTAL OD FLOW> '+str(total_flow)+'\n')
    text_file.write('<END OF METADATA>\n')
    text_file.write('\n')
    i, current_origin = 0, -1
    list_of_ODs_per_origin_as_string = ''
    while(i < len(clean_ODs)):
        od = ODs_sorted[i]
        if od[0] != current_origin:
            if i != 0: 
                text_file.write(list_of_ODs_per_origin_as_string+'\n')
            current_origin = write_new_origin_as_string(i)
            list_of_ODs_per_origin_as_string = '\t'+str(int(od[1]))+' :\t'+str(od[2])+';'
        else: 
            list_of_ODs_per_origin_as_string += '\t'+str(int(od[1]))+' :\t'+str(od[2])+';'
        if i == len(clean_ODs) - 1:
            text_file.write(list_of_ODs_per_origin_as_string)
        i += 1   
    return n_zones

def count_total_origins_or_dests(ODs_list):
    dict = {}
    for od in ODs_list:
        if not dict.has_key(od[0]):
            dict[od[0]] = 1
        if not dict.has_key(od[1]):
            dict[od[1]] = 1
    return len(dict.items())



