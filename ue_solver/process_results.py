import geopandas as gpd
import pandas as pd
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib



def results_to_geojson(results_f, geojson_inf, geojson_outf):
	'''
<<<<<<< HEAD
	Results file is merged with the network geojson file based on the init and term ids
	of each link. Saves geojson with merged results.
=======
    results file is merged with the network geojson file based on the init and term ids
    of each link. Saves geojson with merged results.
>>>>>>> c07400fc6481c2e95f3dd8e183f5adeebae2b4fe

    results_f = string, path to results text file from solver
    geojson_inf = string, path to network geojson
    geojson_outf = string, path save location for results geojson
    '''
	geodf = create_results_df(results_f, geojson_inf)

	with open(geojson_outf, 'w') as f:
		f.write(geodf.to_json())


def create_results_df(results_f, network_geojson):
<<<<<<< HEAD
	'''
	Results file is merged with the network geojson file based on the init and term ids
	returns merged results dataframe

	- results_f = type string, path to results text file from solver
	- network_geoj = type string, path to network geojson
	'''
	links = gpd.read_file(network_geojson)
	for col in ['cost','flow','flow/capacity','tt/fftt']:
		if col in links.columns:
			links = links.drop(col, axis = 1)
	results = pd.read_csv(results_f, skiprows=[0,1,2,3,4,5], delimiter='\t', 
						  usecols=[1,2,4,5], names=['init','term','flow','cost'])
		
	links = pd.merge(links, results, left_on=['init','term'], right_on=['init','term'])
	links = gpd.GeoDataFrame(links)
	links['cost'] = links['cost'].astype('float')
	links['tt/fftt'] = links['cost']/links['fftt']
	links['flow/capacity'] = links['flow']/links['capacity']
	
	return links

	
def geoj_vmt_vht_delay(results_geoj, cities_aggregate_output_file, output_summary, totalODflow = 0, min_speed = 0, save_path = 0):
	'''
	Calculates VMT, VHT, and delay from results_geoj 

	- results_geoj: type str, filepath to results geoJSON 
	- cities_aggregate_output_file:
	- output_summary:
	- totalODflow: type int (float?), total demand (total number of passengers)
	- min_speed: type float, force speed to min_speed if link speed < minspeed 
	- save_path: type str, save plot to this filepath 
	'''
	results_df = gpd.read_file(results_geoj)
	results = df_vmt_vht_delay(results_df, output_summary, totalODflow, min_speed)
	# results.to_csv(processing_output)
	results = results.groupby(['city']).sum()
	results = results.ix[:,['vmt', 'vht', 'delay']]
	results.to_csv(cities_aggregate_output_file)
	if save_path != 0:
		save_plot(results, save_path)
=======
    '''
    results file is merged with the network geojson file based on the init and term ids
    returns merged results dataframe

    results_f = type string, path to results text file from solver
    network_geoj = type string, path to network geojson
    '''
    links = gpd.read_file(network_geojson)
    for col in ['cost','flow','flow/capacity','tt/fftt']:
        if col in links.columns:
            links = links.drop(col, axis = 1)
    results = pd.read_csv(results_f, skiprows=[0,1,2,3,4,5], delimiter='\t', 
                          usecols=[1,2,4,5], names=['init','term','flow','cost'])
        
    links = pd.merge(links, results, left_on=['init','term'], right_on=['init','term'])
    links = gpd.GeoDataFrame(links)
    links['cost'] = links['cost'].astype('float')
    links['tt/fftt'] = links['cost']/links['fftt']
    links['flow/capacity'] = links['flow']/links['capacity']
    
    return links

    
def geoj_vmt_vht_delay(results_geoj, cities_aggregate_output_file, output_summary, totalODflow = 0, min_speed = 0, save_path = 0):
    if type(results_geoj) == str:
        results_df = gpd.read_file(results_geoj)
    else:
        results_df = results_geoj
    results = df_vmt_vht_delay(results_df, output_summary, totalODflow, min_speed)
    # results.to_csv(processing_output)
    results = results.groupby(['city']).sum()
    results = results.ix[:,['vmt', 'vht', 'delay']]
    return results
    # results.to_csv(cities_aggregate_output_file)
    # if save_path != 0:
    #     save_plot(results, save_path)
>>>>>>> c07400fc6481c2e95f3dd8e183f5adeebae2b4fe


def df_vmt_vht_delay(df, output_summary, totalODflow = 0, min_speed = 0):
	'''
	df = results dataframe
	totalODflow = total demand (total number of passengers)
	min_speed = force speed to min_speed if link speed < minspeed
	'''
	#TODO updated names?
	df['vmt'] = df['flow'].astype(float)*df['length'].astype(float)/1609.34
	df['travel time'] = df['fftt'].astype(float)*df['tt/fftt'].astype(float)/3600
	
	if float(min_speed) == 0:
		df['vht'] = df['flow'].astype(float)*df['travel time'].astype(float)
		df['delay'] = df['flow'].astype(float)*(df['travel time'].astype(float)-df['fftt'].astype(float)/3600)
		df['speed'] = (df['length'].astype(float)/1609.34)/df['travel time'].astype(float)
	else:
		df['speed'] = (df['length'].astype(float)/1609.34)/df['travel time'].astype(float)
		df['travel time'] = np.where([df['speed'] > float(min_speed)], df['travel time'], df['length'].astype(float)/(1609.34*float(speed_limit)))[0]
		df['vht'] = df['flow'].astype(float)*df['travel time'].astype(float)
		df['delay'] = df['flow'].astype(float)*(df['travel time'].astype(float)-df['fftt'].astype(float)/3600)
		df['speed_new'] = (df['length'].astype(float)/1609.34)/df['travel time'].astype(float)
	totalvmt = np.sum(df['vmt'])
	totalvht = np.sum(df['vht'])
	totaldelay = np.sum(df['delay'])
	print(totalvmt, totalvht, totaldelay)
	if totalODflow != 0:
		d = {'vmt': [totalvmt, float(totalvmt/totalODflow)],
			 'vht': [totalvht, float(totalvht/totalODflow)],
			 'delay': [totaldelay, float(totaldelay/totalODflow)]}
		totaldf = pd.DataFrame(d, index = ['total','per passenger'])
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
		with open(output_summary,'w') as f:
			f.write(totaldf.to_csv())
		#print('totalvmt: ' + str(totalvmt))
		#print('totalvht: ' + str(totalvht))
		#print('totaldelay: ' + str(totaldelay))
		#print('vmt per traveler: ' + str(totalvmt/totalODflow))
		#print('vht per traveler: ' + str(totalvht/totalODflow))
		#print('delay per traveler: ' + str(totaldelay/totalODflow))
	return df


def save_plot(df, save_path):
    matplotlib.style.use('ggplot')
    pp = PdfPages(save_path)
    plt.figure(figsize=(20, 20), dpi=400)
    df.ix[:,'vmt'].plot.bar()
    plt.title('vmt')
    pp.savefig()
    plt.figure(figsize=(20, 20), dpi=400)
    df.ix[:,'vht'].plot.bar()
    plt.title('vht')
    pp.savefig()
    plt.figure(figsize=(20, 20), dpi=400)
    df.ix[:,'delay'].plot.bar()
    plt.title('delay')
    pp.savefig()
    pp.close()



def cities_vmt_vht_delay(ca_cities_f, links_geojson, output_file, totalODflow = 0, speed_limit = 0):
    df = merge_links_citieshp(ca_cities_f, links_geojson)
    df_vmt_vht_delay = vmt_vht_delay(df, totalODflow)
    df_vmt_vht_delay = df_vmt_vht_delay.groupby(['NAME']).sum()
    df_vmt_vht_delay.to_csv(output_file)

# Calculate the rms of specific parameter between two dataframe
# to compare the difference.
def rms(df1_vmt_vht_delay, df2_vmt_vht_delay, column):
    rms_result = np.sqrt(np.mean(np.square(df1_vmt_vht_delay[str(column)].astype(float)-df2_vmt_vht_delay[str(column)].astype(float))))
    return rms_result




