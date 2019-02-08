from flask import Flask, request, jsonify
from jsonschema import validate
from response_utils import *
from web_constants import *

from plot_data_listing import plot_data_listing

from plot_clustering import plot_clustering

from scale_samples import scale_samples

from plot_exposures import plot_exposures
from scale_exposures import scale_exposures

from plot_counts import plot_counts
from scale_counts import scale_counts

from plot_samples_meta import plot_samples_meta

from plot_gene_event_track import plot_gene_event_track, autocomplete_gene, plot_pathways_listing
from plot_clinical import plot_clinical, plot_clinical_variables, plot_clinical_scale_types
from scale_clinical import scale_clinical
from plot_survival import plot_survival

# Reconstruction plots
from plot_counts_per_category import plot_counts_per_category
from plot_reconstruction import plot_reconstruction
from plot_reconstruction_error import plot_reconstruction_error
# Reconstruction scales
from scale_counts_per_category import scale_counts_per_category
from scale_reconstruction import scale_reconstruction
from scale_reconstruction_error import scale_reconstruction_error

from scale_contexts import scale_contexts
from plot_signature import plot_signature
from plot_reconstruction_cosine_similarity import plot_reconstruction_cosine_similarity
# Sharing
from sharing_state import get_sharing_state, set_sharing_state, plot_featured_listing
# Authentication
from auth import NotAuthenticated, login, logout, check_token


app = Flask(__name__)

""" 
Authentication helpers 
"""
@app.errorhandler(NotAuthenticated)
def handle_not_authenticated(error):
    return response_json_error(app, error.to_dict(), error.status_code)

def check_req(request, schema=None):
  req = request.get_json(force=True)
  check_token(req)
  if schema != None:
    validate(req, schema)
  return req

"""
Reusable JSON schema
"""
string_array_schema = {
  "type": "array",
  "items": {
    "type": "string"
  }
}
projects_schema = string_array_schema
signatures_schema = {
  "type" : "object",
  "properties": dict([(mut_type, string_array_schema) for mut_type in MUT_TYPES])
}


"""
Data listing
"""
@app.route('/data-listing', methods=['POST'])
def route_data_listing():
  req = check_req(request)
  output = plot_data_listing()
  return response_json(app, output)

# TODO: combine the below listing requests into the one data listing request
@app.route('/pathways-listing', methods=['POST'])
def route_pathways_listing():
  req = check_req(request)
  output = plot_pathways_listing()
  return response_json(app, output)

@app.route('/featured-listing', methods=['POST'])
def route_featured_listing():
  req = check_req(request)
  output = plot_featured_listing()
  return response_json(app, output)

@app.route('/clinical-variable-list', methods=['POST'])
def route_clinical_variable_list():
  req = check_req(request)
  output = plot_clinical_scale_types()
  return response_json(app, output) 


"""
Signatures
"""
schema_signature = {
  "type": "object",
  "properties": {
    "signature": {"type": "string"},
    "mut_type": {"type": "string"}
  }
}
@app.route('/plot-signature', methods=['POST'])
def route_plot_signature():
  req = check_req(request, schema=schema_signature)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_signature(signature=req["signature"], mut_type=req["mut_type"])
  return response_json(app, output)

"""
Samples-by-project
"""
schema_samples_meta = {
  "type": "object",
  "properties": {
    "projects": projects_schema
  }
}
@app.route('/plot-samples-meta', methods=['POST'])
def route_plot_samples_meta():
  req = check_req(request, schema=schema_counts)

  output = plot_samples_meta(req["projects"])
  return response_json(app, output)

"""
Counts
"""
schema_counts = {
  "type": "object",
  "properties": {
    "projects": projects_schema
  }
}
@app.route('/plot-counts', methods=['POST'])
def route_plot_counts():
  req = check_req(request, schema=schema_counts)

  output = plot_counts(req["projects"])
  return response_json(app, output)

# TODO: delegate as many "scale" requests to client as possible
@app.route('/scale-counts', methods=['POST'])
def route_scale_counts():
  req = check_req(request, schema=schema_counts)

  output = scale_counts(req["projects"])
  return response_json(app, output)

@app.route('/scale-counts-sum', methods=['POST'])
def route_scale_counts_sum():
  req = check_req(request)
  validate(req, schema_counts)

  output = scale_counts(req["projects"], count_sum=True)
  return response_json(app, output)

"""
Exposures
"""
schema_exposures = {
  "type": "object",
  "properties": {
    "signatures": string_array_schema,
    "projects": projects_schema,
    "mut_type": {"type": "string"}
  }
}
@app.route('/plot-exposures', methods=['POST'])
def route_plot_exposures():
  req = check_req(request, schema=schema_exposures)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_exposures(req["signatures"], req["projects"], req["mut_type"])
  return response_json(app, output)

@app.route('/plot-exposures-normalized', methods=['POST'])
def route_plot_exposures_normalized():
  req = check_req(request, schema=schema_exposures)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_exposures(req["signatures"], req["projects"], req["mut_type"], normalize=True)
  return response_json(app, output)

@app.route('/scale-exposures', methods=['POST'])
def route_scale_exposures():
  req = check_req(request, schema=schema_exposures)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_exposures(req["signatures"], req["projects"], req["mut_type"], exp_sum=False)
  return response_json(app, output)

@app.route('/scale-exposures-normalized', methods=['POST'])
def route_scale_exposures_normalized():
  req = check_req(request, schema=schema_exposures)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_exposures(req["signatures"], req["projects"], req["mut_type"], exp_sum=False, exp_normalize=True)
  return response_json(app, output)


@app.route('/scale-exposures-sum', methods=['POST'])
def route_scale_exposures_sum():
  req = check_req(request, schema=schema_exposures)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_exposures(req["signatures"], req["projects"], req["mut_type"], exp_sum=True)
  return response_json(app, output)

schema_exposures_single_sample = {
  "type": "object",
  "properties": {
    "signatures": string_array_schema,
    "projects": projects_schema,
    "mut_type": {"type": "string"},
    "sample_id": {"type": "string"}
  }
}
@app.route('/plot-exposures-single-sample', methods=['POST'])
def route_plot_exposures_single_sample():
  req = check_req(request, schema=schema_exposures_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_exposures(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)

@app.route('/scale-exposures-single-sample', methods=['POST'])
def route_scale_exposures_single_sample():
  req = check_req(request, schema=schema_exposures_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_exposures(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], exp_sum=False, exp_normalize=False)
  return response_json(app, output)


"""
Reconstruction error
"""
@app.route('/plot-counts-per-category-single-sample', methods=['POST'])
def route_plot_counts_per_category_single_sample():
  req = check_req(request, schema=schema_exposures_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_counts_per_category(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)

@app.route('/plot-reconstruction-single-sample', methods=['POST'])
def route_plot_reconstruction_single_sample():
  req = check_req(request, schema=schema_exposures_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_reconstruction(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)

@app.route('/plot-reconstruction-error-single-sample', methods=['POST'])
def route_plot_reconstruction_error_single_sample():
  req = check_req(request, schema=schema_exposures_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_reconstruction_error(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)

@app.route('/plot-reconstruction-cosine-similarity', methods=['POST'])
def route_plot_reconstruction_cosine_similarity():
  req = check_req(request, schema=schema_exposures_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_reconstruction_cosine_similarity(req["signatures"], req["projects"], req["mut_type"])
  return response_json(app, output)

@app.route('/plot-reconstruction-cosine-similarity-single-sample', methods=['POST'])
def route_plot_reconstruction_cosine_similarity_single_sample():
  req = check_req(request, schema=schema_exposures_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = plot_reconstruction_cosine_similarity(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"])
  return response_json(app, output)


@app.route('/scale-counts-per-category-single-sample', methods=['POST'])
def route_scale_counts_per_category_single_sample():
  req = check_req(request, schema=schema_exposures_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_counts_per_category(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)

@app.route('/scale-reconstruction-single-sample', methods=['POST'])
def route_scale_reconstruction_single_sample():
  req = check_req(request, schema=schema_exposures_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_reconstruction(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)

@app.route('/scale-reconstruction-error-single-sample', methods=['POST'])
def route_scale_reconstruction_error_single_sample():
  req = check_req(request, schema=schema_exposures_single_sample)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_reconstruction_error(req["signatures"], req["projects"], req["mut_type"], single_sample_id=req["sample_id"], normalize=False)
  return response_json(app, output)


schema_contexts = {
  "type": "object",
  "properties": {
    "signatures": string_array_schema,
    "mut_type": {"type": "string"}
  }
}
@app.route('/scale-contexts', methods=['POST'])
def route_scale_contexts():
  req = check_req(request, schema=schema_contexts)

  assert(req["mut_type"] in MUT_TYPES)

  output = scale_contexts(req["signatures"], req["mut_type"])
  return response_json(app, output)


"""
Hierarchical clustering plot
"""
schema_clustering = {
  "type": "object",
  "properties": {
    "signatures": signatures_schema,
    "projects": projects_schema
  }
}
@app.route('/clustering', methods=['POST'])
def route_clustering():
  req = check_req(request, schema=schema_clustering)

  output = plot_clustering(req["signatures"], req["projects"])
  return response_json(app, output)


"""
Genome Event Tracks
"""
schema_gene_event_track = {
  "type": "object",
  "properties": {
    "gene_id": {"type": "string"},
    "projects": projects_schema
  }
}
@app.route('/plot-gene-event-track', methods=['POST'])
def route_gene_event_track():
  req = check_req(request, schema=schema_gene_event_track)

  output = plot_gene_event_track(req["gene_id"], req["projects"])
  return response_json(app, output) 


"""
Autocomplete gene ID
"""
schema_autocomplete_gene = {
  "type": "object",
  "properties": {
    "projects": projects_schema,
    "gene_id_partial": {"type": "string"}
  }
}
@app.route('/autocomplete-gene', methods=['POST'])
def route_autocomplete_gene():
  req = check_req(request, schema=schema_autocomplete_gene)

  output = autocomplete_gene(req["gene_id_partial"], req["projects"])
  return response_json(app, output)

"""
Clinical Variable Tracks
"""
schema_clinical = {
  "type": "object",
  "properties": {
    "clinical_variable": {"type": "string"},
    "projects": projects_schema
  }
}
@app.route('/plot-clinical', methods=['POST'])
def route_plot_clinical():
  req = check_req(request, schema=schema_clinical)

  output = plot_clinical(req["projects"])
  return response_json(app, output)

@app.route('/scale-clinical', methods=['POST'])
def route_scale_clinical():
  req = check_req(request, schema=schema_clinical)

  output = scale_clinical(req["projects"])
  return response_json(app, output)

schema_survival = {
  "type": "object",
  "properties": {
    "projects": projects_schema
  }
}
@app.route('/plot-survival', methods=['POST'])
def route_plot_survival():
  req = check_req(request, schema=schema_survival)

  output = plot_survival(req["projects"])
  return response_json(app, output)

"""
Samples listing
"""
schema_samples = {
  "type": "object",
  "properties": {
    "projects": projects_schema
  }
}
@app.route('/scale-samples', methods=['POST'])
def route_scale_samples():
  req = check_req(request, schema=schema_samples)

  output = scale_samples(req["projects"])
  if len(output) != len(set(output)):
    print("WARNING: Duplicate sample IDs")
  return response_json(app, output)



"""
Gene alteration scale
"""
@app.route('/scale-gene-alterations', methods=['POST'])
def route_scale_gene_alterations():
  req = check_req(request)
  output = [e.value for e in MUT_CLASS_VALS] + ["None"]
  return response_json(app, output) 

"""
Sharing: get state
"""
schema_sharing_get = {
  "type": "object",
  "properties": {
    "slug": {"type": "string"}
  }
}
@app.route('/sharing-get', methods=['POST'])
def route_sharing_get():
  req = check_req(request, schema=schema_sharing_get)
  try:
    output = get_sharing_state(req['slug'])
    return response_json(app, output)
  except:
    return response_json_error(app, {"message": "An error has occurred."}, 500)

"""
Sharing: set state
"""
schema_sharing_set = {
  "type": "object",
  "properties": {
    "state": {"type": "string"}
  }
}
@app.route('/sharing-set', methods=['POST'])
def route_sharing_set():
  req = check_req(request, schema=schema_sharing_set)
  try:
    output = set_sharing_state(req['state'])
    return response_json(app, output)
  except:
    return response_json_error(app, {"message": "An error has occurred."}, 500)

""" 
Authentication routes 
"""
schema_login = {
  "type": "object",
  "properties": {
    "password": {"type": "string"}
  }
}
@app.route('/login', methods=['POST'])
def route_login():
  req = request.get_json(force=True)
  validate(req, schema_login)
  output = login(req['password'])
  return response_json(app, output)

@app.route('/check-token', methods=['POST'])
def route_check_token():
  check_req(request)
  output = {'message': 'Authentication successful.'}
  return response_json(app, output)

@app.route('/logout', methods=['POST'])
def route_logout():
  req = check_req(request)
  logout(req['token'])
  output = {'message': 'Logout successful.'}
  return response_json(app, output)
  


if __name__ == '__main__':
  app.run(
      host='0.0.0.0',
      debug=bool(os.environ.get('DEBUG', '')), 
      port=int(os.environ.get('PORT', 8000)),
      use_reloader=True
  )
