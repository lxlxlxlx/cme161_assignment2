import os, copy
from flask import Flask, jsonify, request, send_from_directory, make_response
import json, collections
app = Flask(__name__, static_url_path='')

# get root
@app.route("/")
def index():
    return app.make_response(open('app/index.html').read())

@app.route('/three/<path:path>')
def three_route(path):
    return send_from_directory('app/assets/html/', path)

# @app.route('/libs/<path:path>')
# def lib_route(path):
#     return send_from_directory('app/assets/js/libs', path)

# send assets (ex. assets/js/random_triangle_meshes/random_triangle_meshes.js)
# blocks other requests, so your directories won't get listed (ex. assets/js will return "not found")
@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('app/assets/', path)

# set debug=True if you want to have auto-reload on changes
# this is great for developing



@app.route('/trellis', methods=['GET'])
def get_trellis():
	# This method should return the entire data
	# Replace the following line with your own code
	with open('app/assets/data/trellis.json') as data_file:
		return json.dumps(json.load(data_file))
	# return None

@app.route('/trellis/limit/<path:n_entries>', methods=['GET'])
def get_trellis_limit(n_entries):
	# This method should return only the first 'n_entries' entries
	# Replace the following line with your own code
	with open('app/assets/data/trellis.json') as data_file:
		return json.dumps(json.load(data_file)[:int(n_entries)])
	# return None

def make_data_graph(data_list_in):
	# This method should convert the raw trellis data into the graph format
	# Replace the following line with your own code
	idx = 0
	names = collections.OrderedDict()
	for e in data_list_in:
		to = e['to'][:7] # truncate
		fr = e['from'][:7]
		if to not in names:
			names[to] = idx
			idx += 1
		if fr not in names:
			names[fr] = idx
			idx += 1
	edges = [{
				"source": names[e['to'][:7]], 
				"target": names[e['from'][:7]], 
				"value": e['n'], 
				"tags":  [d['tag'] for d in e['data']] 
			} for e in data_list_in
		]
	nodes = [{"name":n} for n in names.keys()]
	return { "nodes": nodes, "edges": edges }
	# return None

@app.route('/graph', methods=['GET'])
def get_graph():
	# This method should return the entire converted graph data
	# Replace the following line with your own code
	with open('app/assets/data/trellis.json') as data_file:
		return json.dumps(make_data_graph(json.load(data_file)))
	# return None

@app.route('/graph/limit/<path:n_entries>', methods=['GET'])
def get_graph_limit(n_entries):
	# This method should convert and return only the first 'n_entries' entries
	# Replace the following line with your own code
	with open('app/assets/data/trellis.json') as data_file:
		return json.dumps(make_data_graph(json.load(data_file)[:int(n_entries)]))
	# return None
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5050))
	app.run(host='0.0.0.0', port=port, debug=False)
