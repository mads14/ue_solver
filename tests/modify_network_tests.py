
from ue_solver.modify_network import *


# def add_virtual_nodes_test():
#     networkx_f = 'resources/network/sf_secondary/network_graph.txt'
#     taz_shpf = 'resources/shapefiles/bay_area_tazs'
#     n_neighbors = 5
#     G, taz_dict = add_virtual_nodes(networkx_f, taz_shpf, n_neighbors)
#     # add some tests here


# def append_city_names_test():
#     ca_cities_shp = 'resources/shapefiles/ca_cities_2014'
#     geojson_f = 'resources/network/sf_secondary_all_roads_0p8/network.geojson'
#     append_city_names(ca_cities_shp, geojson_f)

def update_capacity_test():
    attr_dict = {'county': ['Alameda']}
    percent_cap = .5
    geojson_inf = 'resources/network/sf_secondary/network.geojson'
    geojson_outf = 'resources/network/sf_secondary_alameda_0p5/network.geojson'
    graph_outf = 'resources/network/sf_secondary_alameda_0p5/network_graph.txt'
    update_capacity(attr_dict, percent_cap, geojson_inff, 
                    geojson_outf, graph_outf)


# def remove_duplicate_links_test():
    
#     geojson_inf = 'resources/network/sf_secondary_all/network.geojson'
#     geojson_outf = 'resources/network/sf_secondary_all/network.geojson'
#     remove_duplicate_links(geojson_in, geojson_out)

# def cut_links_test():
#     geojson_inf = 'resources/network/sf_secondary_all_roads_0p8/network.geojson'
#     links_f = 'resources/cut_links/SLR025_KT_cutlinks.csv'
#     geojson_outf = 'resources/network/sf_secondary_SLR025_KT_cutlinks/network.geojson'
#     graph_outf = 'resources/network/sf_secondary_SLR025_KT_cutlinks/network_graph.txt'
#     cut_links(geojson_infile, links_f, geojson_outf, graph_outf)