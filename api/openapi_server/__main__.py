#!/usr/bin/env python3

import os
import json
import pickle

import connexion
from flask_cors import CORS
from flask import request, g

from openapi_server import encoder
from openapi_server.db import get_db

def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'pathoLogic'},
                pythonic_params=True)

    # Serve results under /v1/result/PATH
    app.app.config['STATIC_URL_PATH'] = os.path.abspath(os.getenv('BASE_DIR', os.getcwd()))
    CORS(app.app) # enable CORS everywhere

    # Use dictionary as DB
    with app.app.app_context():
        get_db()

    @app.app.teardown_appcontext
    def close_db(e=None):
        db = g.pop('db', None)

        if db is not None:
            pickle.dump(db, open(os.path.join(os.getenv('BASE_DIR', os.getcwd()), 'pathoLogic.db'), 'wb'))
    
    # Create route for nextflow weblog (assembly)
    @app.app.route('/v1/nf_assembly/<runid>', methods=['POST'])
    def nf_assembly(runid):
        req_data = request.get_json()
        print(req_data)
        db = get_db()
        db['status_assembly'][runid] = req_data
        print(json.dumps(db['status'][runid]))
        if req_data['event'] == 'process_completed':
            for sID in db['runs'][runid]:
                db['samples'][sID]['status'] = 'finished'
        return 'NF Request received'

    # Create route for nextflow weblog (plasmident)
    @app.app.route('/v1/nf_plasmident/<runid>', methods=['POST'])
    def nf_plasmident(runid):
        req_data = request.get_json()
        print(req_data)
        db = get_db()
        db['status_plasmident'][runid] = req_data
        print(json.dumps(db['status'][runid]))
        if req_data['event'] == 'process_completed':
            for sID in db['runs'][runid]:
                db['samples'][sID]['status'] = 'finished'
        return 'NF Request received'

    production = os.getenv('PRODUCTION', False)
    app.run(port=os.getenv('HTTP_PORT', 8080), debug=not production, use_debugger=not production, use_reloader=not production, passthrough_errors=not production)

if __name__ == '__main__':
    main()
