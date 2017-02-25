import networkx as nx
from networkx.readwrite import json_graph
# from haversine import haversine
from sklearn.neighbors import KNeighborsClassifier
from ue_solver.conversions import *
from geopandas.tools import sjoin
import json
import geopandas as gpd
import pandas as pd
import numpy as np
import math as math
import os


#####################add_virtual_nodes#####################
def haversinefunction(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 * 10**6 # m

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c * radius

    return d

def add_virtual_nodes(networkx_f, taz_shpf, n_neighbors):#, taz_dict_outf, graph_name):
    with open (networkx_f) as f:
        data = json.load(f)
    G = json_graph.node_link_graph(data)

    nodes = np.array(G.nodes(data=True))
    tazs = gpd.read_file(taz_shpf)
    taz_centroids = [[i.xy[j][0] for j in [1,0]] for i in tazs.centroid] 
    neighbors = get_nearest_neighbors(taz_centroids, nodes, n_neighbors)

    nid = max([nd[1]['nid'] for nd in nodes]) +1

    taz_dict = {}

    for i in range(len(tazs)):
        # add node to graph
        virtual_nd_coords = taz_centroids[i][::-1]

        nd_out_id = 'virtual' +str(2*i)
        nd_in_id = 'virtual' +str(2*i+1)
        G.add_node(nd_out_id, {u'coords': virtual_nd_coords, u'nid': nid, u'virtual_node': True})
        G.add_node(nd_in_id, {u'coords': virtual_nd_coords, u'nid': nid, u'virtual_node': True})

        for neighbor,data in nodes[neighbors[i]]:

            distance = haversinefunction(tuple(virtual_nd_coords[::-1]), 
                                         tuple(data['coords'][::-1]))
            travel_speed = 6.7 #m/s = 15mph

            # add edges from virtual node to k nearests neighbors
            props = {u'B': 0.15, u'capacity': 100000, u'fftt': distance/travel_speed, 
                     u'freeflow_speed': travel_speed, u'geom': [virtual_nd_coords,data['coords']], 
                     u'init': nid, u'lanes': 0, u'length': distance, u'osm_init': nd_out_id,
                     u'osm_term': neighbor, u'power': 4, u'term': data['nid'], u'toll': 0,
                     u'type': u'virtual;'}
            G.add_edge(nd_out_id, neighbor, attr_dict=props)


            # add edges to virtual node from k nearests neighbors
            props = {u'B': 0.15, u'capacity': 100000, u'fftt': distance/travel_speed, 
                     u'freeflow_speed': travel_speed, u'geom': [data['coords'], virtual_nd_coords],
                     u'init': data['nid'], u'lanes': 0, u'length': distance, u'osm_init': neighbor, 
                     u'osm_term': nd_in_id, u'power': 4, u'term': nid+1, u'toll': 0, u'city': 'None', 
                     u'type': u'virtual;'}

            G.add_edge(neighbor, nd_in_id, attr_dict=props)
        taz_dict[tazs['TAZ1454'][i]] = {'origin': nid, 'destination': nid+1}
        nid += 2

    return G, taz_dict


def get_nearest_neighbors(taz_coords, nodes, n_neighbors):
    
    lons = [pt['coords'][0] for pt in nodes[:,1]]
    lats = [pt['coords'][1] for pt in nodes[:,1]]
    nids = [pt['nid'] for pt in nodes[:,1]]
    node_coords = np.vstack([lats, lons]).T

    knn = KNeighborsClassifier(n_neighbors,metric='haversine')
    knn.fit(node_coords, nids)
    return knn.kneighbors(taz_coords, n_neighbors, False)

#####################append_city_names#####################
def append_city_names(ca_cities_shp, geojson_f, geojson_outf):
    # read links geojson
    links = gpd.GeoDataFrame.from_file(geojson_f)
    if 'city' in links.columns:
        print('network already has city labels')
        return None

    # read city shapefile
    ca_cities = gpd.GeoDataFrame.from_file(ca_cities_shp)
    ca_cities = ca_cities[['CityType','County','NAME','geometry']]
    ca_cities = ca_cities.rename(columns={'NAME':'city','County':'county',
                                          'CityType':'city_type'})
    # spatial join
    links_w_city=sjoin(links, ca_cities, 'left')

    # if link in more than one city, then will be doubled in table, drop duplicates
    links_w_city = links_w_city.reset_index().drop_duplicates(subset='index').set_index('index')
    links_w_city = links_w_city.drop('index_right',1)
    with open(geojson_outf, 'w') as f:
        f.write(links_w_city.to_json())

###########alternative_append_city_names############
def label_road_network(input_shp, road_network_geojson, attributes, geojson_outf, rename_attributes = None):
    #####################append_city_names#####################
    # read links geojson
    links = gpd.GeoDataFrame.from_file(road_network_geojson)

    # read input shapefile
    network = gpd.GeoDataFrame.from_file(input_shp)

    # if only one attribute  
    if type(attributes) == str:
        if attributes in network.columns:
            network = network[[attributes, 'geometry']]
            if rename_attributes is not None:
                network = network.rename(columns={attributes:rename_attributes})
        else:
            raise ValueError("Column name is not in input_shp")

    # if multiple attributes
    elif type(attributes) is list:
        # check if column name in input_shp
        for x in attributes:
            if x not in network.columns:
                raise ValueError("Column name is not in input_shp")
        if 'geometry' in network.columns:
            attributes.append('geometry')
        network = network[[attributes]]
        if len(attributes) != len(rename_attributes):
            raise ValueError("Number of attributes different from number of rename attributes.")
        rename_columns = {}
        for i in range(len(attributes)):
            rename_columns.update({attributes[i]:rename_attributes[i]})
        network = network.rename(columns = rename_columns)
    # spatial join
    links_w_city = sjoin(links, network, 'left')

    # if link in more than one city, then will be doubled in table, drop duplicates
    links_w_city = links_w_city.reset_index().drop_duplicates(subset='index').set_index('index')
    links_w_city = links_w_city.drop('index_right',1)
    with open(geojson_outf, 'w') as f:
        f.write(links_w_city.to_json())

#####################update_cap#####################
def update_capacity(attr_dict, percent_cap, geojson_inf, 
                    geojson_outf, graph_f=None):
    
    '''
    update a network file by changing the capacity according to the fields in attr_dict
    
    inputs
    attr_dict = {key: [list of values that will be changed]}
    precent_cap = type decimal, percent of existing capacity roads will now have
    geojson_in = type str, filepath network geojson file
    geojson_out = type str, filepath save locations of modified network geojson file
    graph_f = path of updated networkx or None if don't want to save networkx graph
    '''
    if not os.path.exists(os.path.dirname(geojson_outf)):
        try:
            os.makedirs(os.path.dirname(geojson_outf))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    # if directory exists            
    else: 
        # ask if user wants to rewrite
        rewrite = input("This file already exists. Would you like to write over it? (y/n)")
        if rewrite == 'n':
            return None
    links = gpd.read_file(geojson_inf)

    roads_to_update = 1
    for k,v in attr_dict.items():
        if k == 'type':
            v = [r+';' for r in v]
        roads_to_update = roads_to_update & links[k].isin(v)

        
    # Change capacity of city Arterials and save to dataframe
    links['capacity'] = np.where(roads_to_update,
                                 links['capacity']*percent_cap,
                                 links['capacity'])

    with open(geojson_outf, 'w') as f:
        f.write(links.to_json())

    if graph_f != None:
        geojson_to_networkx(geojson_outf, graph_f)

#####################cut_links#####################
def cut_links(geojson_inf, links_f, geojson_outf, graph_outf):
    '''

    '''
    if not os.path.exists(os.path.dirname(geojson_outf)):
        try:
            os.makedirs(os.path.dirname(geojson_outf))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    # if directory exists            
    else: 
        # ask if user wants to rewrite
        rewrite = input("This file already exists. Would you like to write over it? (y/n)")
        if rewrite == 'n':
            return None
    geojson_f = gpd.GeoDataFrame.from_file(geojson_inf)
    geojson_f[['osm_init','osm_term']] = geojson_f[['osm_init','osm_term']].apply(pd.to_numeric)
    
    # Read csv to df
    cut_links_df = pd.read_csv(links_f)
    
    # Add a label column
    cut_links_df.columns=['osm_init','osm_term']
    cut_links_df['cut_links'] = [1]*len(cut_links_df['osm_init'])

    result = pd.merge(geojson_f, cut_links_df, how = 'left', on=['osm_init', 'osm_term'])
    result = result[result['cut_links'] != float(1)]
    result.drop(labels = ['cut_links'], axis = 1, inplace = True)
    

    # save network geojson
    with open(geojson_outf, 'w') as f:
        f.write(result.to_json())

    G = geojson_to_networkx(geojson_outf)
    G = remove_non_accessible_nodes(G)
    G = reassign_node_ids(G)    

    save_graph(G, graph_outf)

def remove_non_accessible_nodes(G, start_node = None):
    '''
    remove all nodes in graph G that are not accessible from the start node.
    If start_node = None, then set start node to middle node.
    '''
    l = G.number_of_nodes()
    start_node = G.nodes()[l//2]

    # filter for path from center node
    node_list = G.nodes()
    to_keep = list(set(sum(list(nx.algorithms.bfs_tree(G, start_node).edges()), ())))
    to_remove = set(node_list) - set(to_keep)
    for n in to_remove:
         G.remove_node(n)

    # filter for path to center node
    node_list = G.nodes()
    to_keep = list(set(sum(list(nx.algorithms.bfs_tree(G, start_node, reverse=True).edges()), ())))
    to_remove = set(node_list) - set(to_keep)
    for n in to_remove:
         G.remove_node(n)
    return G
    

def reassign_node_ids(G):
    '''
    assign node ids 1,...,number_of_nodes, to the nodes in the graph
    assign init and term properties to the corresponding links.
    '''
    #assign nids to nodes
    k = 1
    osmId_2_nId = {}
    for n in G.nodes_iter():
        osmId_2_nId[n] = k # osmId_2_gId[int(osmId)] = gId
        k+=1
    nx.set_node_attributes(G, 'nid', osmId_2_nId)

    #assign init and term to appropriate links
    st_ids ={}
    end_ids = {}
    for e in G.edges_iter(keys=True):
        st_ids[e] = osmId_2_nId[e[0]]
        end_ids[e] = osmId_2_nId[e[1]]

    nx.set_edge_attributes(G, 'init', st_ids)
    nx.set_edge_attributes(G, 'term', end_ids)

    return G

def remove_duplicate_links(geojson_inf, geojson_outf):
    networkdf = gpd.GeoDataFrame.from_file(geojson_inf)
    networkdf = networkdf.sort_values(by = ['init', 'term', 'capacity'])
    df = networkdf.drop_duplicates(subset = ['init', 'term'], keep = 'last')
    df = df.reset_index(level=['osm_init', 'osm_term'])
    df['key'] = 0
    if not os.path.exists(os.path.dirname(geojson_outf)):
        try:
            os.makedirs(os.path.dirname(geojson_outf))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    # if directory exists            
    else: 
        # ask if user wants to rewrite
        rewrite = input("This file already exists. Would you like to write over it? (y/n)")
        if rewrite == 'n':
            return None
    with open(geojson_outf, 'w') as f:
        f.write(df.to_json())

