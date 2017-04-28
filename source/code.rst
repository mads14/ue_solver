Documentation for the UE Solver
**************************

.. automodule:: ue_solver


Conversions
=========================

.. automodule:: ue_solver.conversions
   
.. py:function:: networkx_to_geojson(graph_f, geojson_outf, simple_geom=False)

 Converts graph_f (a networkx graph) into a pandas DataFrame, then converts the DataFrame into a geoJSON file

 :param networkx graph_f: Input road network
 :param str geojson_outf: File path of out file
 :param bool simple_geom: set to True if user wants to use less memory by only saving straight-line paths between 
      origin and destination, rather than actual shape of path

.. py:function:: df_to_geoJson(df, geojson_fileout, with_flow=False)

 Converts a pandas DataFrame to a geoJSON file

 :param DataFrame df: Input DataFrame
 :param str geojson_outf: File path of out file

.. py:function:: graph_to_network_file(graph, filepath)

 Writes networkx traffic graph to a text file according to the FW program requirements.
    Format is '~ Init/Term/Cap/Length/FreeFlowTime/B=0.15/Power=4/Speed limit/Toll/Type;' 
    tab delineated, with meta-data.

 :param networkx g: Input road network
 :param str filepath: Filepath where graph will be saved



Modify network
=========================

.. automodule:: ue_solver.modify_network
	
.. py:function:: label_road_network(input_shp, road_network_geojson, attributes, geojson_outf, rename_attributes = None)

 Generalized function of append_city_names. Allows user to specify which attributes to keep from the input shape file. Spatial join shape file with network, so that network file now has identifying labels

 :param str input_shp: filepath for generalized shapefile for cities, neighborhoods, from any state
 :param str road_network_geojson: filepath for input geoJSON network file 
 :param [str] attributes: either string or array of strings, selected attributes that will be joined
 :param str geojson_outf: filepath for output file with identifying labels 
 :param [str] rename_attributes: either string or array of strings (should match attributes), can be used if user would like to rename the attributes to more user-friendly names

.. py:function:: update_capacity(attr_dict, percent_cap, geojson_inf, geojson_outf, graph_f=None)

 :param dict attr_dict: list of values that will be changed, example: {'county': ['Alameda', 'Berkeley', 'Emeryville']}
 :param float percent_cap: percent of existing capacity roads will now have 
 :param str geojson_in: filepath network geoJSON file
 :param str geojson_out: filepath save locations of modified network geoJSON file
 :param str graph_f: path of updated networkx or None if don't want to save networkx graph

.. py:function:: cut_links(geojson_inf, links_f, geojson_outf, graph_outf)
 
 Removes links in the road network to simulate roads being closed off or inaccessible. 

 :param str geojson_inf: filepath network geoJSON file
 :param str links_f: filepath CSV file of links to delete
 :param str geojson_outf: filepath network geoJSON file, to save modified network geojson
 :param str graph_outf: filepath networkx file, reconstructed graph file from geoJSON outfile


Process results
=========================
.. automodule:: ue_solver.process_results

.. py:function:: results_to_geojson(results_f, geojson_inf, geojson_outf)
 
 Results file is merged with the network geojson file based on the init and term ids of each link. Saves geojson with merged results.

 :param str results_f: filepath of results from solver
 :param str geojson_inf: filepath to input network geoJSON
 :param str geojson_outf: filepath to save geoJSON results

.. py:function:: geoj_vmt_vht_delay(results_geoj, cities_aggregate_output_file, output_summary, totalODflow = 0, min_speed = 0, save_path = 0)

 Calculates VMT, VHT, and delay from results_geoj 

 :param str results_geoj: filepath for results geoJSON
 :param str cities_aggregate_output_file: placeholder
 :param str output_summary: placeholder  
 :param float totalODflow: total demand (number of passengers)
 :param float min_speed: force speed to min_speed if link speed < min_speed
 :param str save_path: filepath to save plot to 


   

   
