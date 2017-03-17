import networkx as nx
from networkx.readwrite import json_graph
import geopandas as gpd
import pandas as pd
import numpy as np
import json
import csv


########################Networkx_to_geojson########################
def networkx_to_geojson(graph_f, geojson_outf, simple_geom=False):
    '''
    converts a networkx file to a geojson
    '''
    df = networkx_to_df(graph_f, simple_geom)
    df_to_geoJson(df, geojson_outf)

def networkx_to_df(graph, simple_geom = False):
    if type(graph) == str:
        with open (graph) as f:
            data = json.load(f)
        network_g = json_graph.node_link_graph(data)

    else:
        network_g = graph

    # with open (networkx_f) as f:
    #     network_g = json.load(f)

    # create links and nodes dataframes
    n_links = len(network_g.edges())
    links = {}
    for key in network_g.edges(data=True)[0][-1].keys():
        attr = list(network_g.edges_iter(data=key, default=None))
        links[key] = [i[-1] for i in attr]
        #New fix because was getting an error here:
        # links[key] = [network_g.edges(data=True)[i][2][key] 
        #               if key in network_g.edges(data=True)[i][2].keys() 
        #               else 'None' for i in range(n_links)]
    
    links_df = pd.DataFrame.from_dict(links)
    
    if simple_geom:
        links_df = links_df.apply(simple_geom_fn, axis = 1)
   
    return links_df

def simple_geom_fn(row):
    row['geom'] = [row['geom'][0], row['geom'][-1]]
    return row


########################DF_to_geojson########################
def begin_feature(type):
    string = '    "type": "Feature",\n    "geometry": {\n'
    begin_coord = '        "coordinates": [\n'
    return string + '        "type": "{}",\n'.format(type) + begin_coord

def coord(lat,lon,type):
    if type == "LineString": return '            [{}, {}],\n'.format(lon,lat)
    if type == "Point": return '            [{}, {}]'.format(lon,lat)

def linestr(linestr,type):

    if type == "LineString": return '            {},\n'.format(linestr)
    # if type == "Point": return '            [{}, {}]'.format(lon,lat)


def end_prop(next):
    if next: return '    }},{\n'
    return '    }}]\n'

def prop(name, value):
    # try:
    #deleted unicode because unicode was replaced by str in python3
    if type(value) in [str]: return '        "{}": "{}",\n'.format(name, value)
    return '        "{}": {},\n'.format(name, value)
    # except(UnicodeEncodeError):
        # if type(value) in [str, unicode]: return '        "{}": "{}",\n'.format(name, 'NA')
        
def df_to_geoJson(df, geojson_fileout, with_flow=False):
    '''
    df is a regular pandas dataframe (rather than a geopandas df), 
    but it must have a geom column containing a list of coordinates 
    for the line or linestring: [[lon0, lat0],[lon1,lat1],...]
    all other columns in the dataframe will be converted to properties
    in the geojson file.
    '''
    begin = ' {"type": "FeatureCollection",\n  "features": [{ \n'
    begin_prop = '            ]},\n    "properties": {\n'


    type = 'LineString'
    out = begin
    for i in df.index.tolist(): #(len(df)):
        out += begin_feature(type)
        geom = df.loc[i]['geom']
        for g in geom:
            out += coord(g[1], g[0], type)
        out += begin_prop
        property_list = list(df.columns)
        property_list.remove('geom')
        for p in property_list:
            out += prop(p, df.loc[i][p])

        if i < df.index.tolist()[-1]:
            out += end_prop(next = True)
        else:
            out += end_prop(next = False)
    out += '\n'
    out+= '}'
    with open(geojson_fileout, 'w') as f:
        f.write(out)

########################Geojson_to_networkx########################
def geojson_to_networkx(geojson_f, graph_f=None):
    geof = gpd.GeoDataFrame.from_file(geojson_f)
    edge_tuples = [tuple(edge) for edge in geof[['osm_init','osm_term']].values]
    geof['key'] = 0
    geof = geof.set_index(['osm_init','osm_term','key'])
    geo_dict = geof.to_dict()

    # construct networkx graph from geojson
    G=nx.MultiDiGraph()
    G.add_edges_from(edge_tuples)

    # create a node dict from osm_id to network node id:
    node_dict={k[0]: {'nid': v} for (k, v) in geo_dict['init'].items()}
    node_dict2={k[1]: {'nid': v} for (k, v) in geo_dict['term'].items()}
    node_dict.update(node_dict2)

    geo_dict['osm_init'] = {}
    geo_dict['osm_term'] = {}

    for link in list(geo_dict.values())[0].keys():
        geo_dict['osm_init'][link] = link[0]
        geo_dict['osm_term'][link] = link[1]

    for key0 in geo_dict.keys():
        for key,value in geo_dict[key0].items():
            if value is None:
                geo_dict[key0][key] = "None"

    for key in geo_dict.keys():
        if key != 'geometry':
            nx.set_edge_attributes(G, key, geo_dict[key])
        else:
            geoms = {}
            for e in geo_dict['geometry'].keys():
                geoms[e] = np.vstack(geo_dict['geometry'][e].xy).T.tolist()                
                node_dict[e[0]]['coords'] = geoms[e][0]
                node_dict[e[1]]['coords'] = geoms[e][-1]
            nx.set_edge_attributes(G, 'geom', geoms)


    for node in G.nodes_iter():
        G.node[node] = node_dict[node]

    if graph_f != None:
        save_graph(G, graph_f)
    return G
    


########################Save_graph_and_network_files########################
#custom encoder from http://stackoverflow.com/questions/27050108/convert-numpy-type-to-python/27050186#27050186
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

def save_graph(G, filepath):
    data =  json_graph.node_link_data(G)
    # dump json to a file

    with open(filepath, 'w') as outfile:
        json.dump(data, fp = outfile, cls = MyEncoder)


def graph_to_network_file(graph, filepath):
    '''
    Writes networkx traffic graph to a text file according to the FW program requirements.
    Format is '~ Init/Term/Cap/Length/FreeFlowTime/B=0.15/Power=4/Speed limit/Toll/Type;' 
    tab delineated, with meta-data.
    :param G = networkx graph
    :param filename is a sting, path of the place where the graph file should be saved
    '''
    if type(graph) == str:
        with open (graph) as f:
            data = json.load(f)
        G = json_graph.node_link_graph(data)

    else:
        G = graph

    with open(filepath, 'w') as outfile:
        f = csv.writer(outfile, delimiter='\t')
        f.writerow(['<NUMBER OF ZONES> 1'])
        f.writerow(['<NUMBER OF NODES> ' + str(len(G.nodes()))])
        f.writerow(['<FIRST THRU NODE> 1'])
        f.writerow(['<NUMBER OF LINKS> ' + str(len(G.edges()))])
        f.writerow(['<END OF METADATA>'])
        f.writerow(['~ Init/Term/Cap/Length/FreeFlowTime/B=0.15/Power=4/Speed limit/Toll/Type'])
        
        #for i,j in G.edges_iter():
        for i,j,data in sorted(G.edges(data=True), key = lambda x: (x[2]['init'], x[2]['term'])):
            f.writerow([G.edge[i][j][0][x] for x in ['init', 'term', 'capacity', 'length', 'fftt',
                                                     'B', 'power', 'freeflow_speed', 'toll', 'type']])




