#!/usr/bin/env python3

import os
import pickle
import json

import connexion
from flask import request, send_from_directory, g
from flask_cors import CORS

from swagger_server import encoder
from swagger_server.db import get_db

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'pathoLogic'})

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

    @app.app.route('/v1/result/<path:path>')
    def send_result(path):
        return send_from_directory('runs', path)
    
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

    app.run(port=os.getenv('HTTP_PORT', 8080))

if __name__ == '__main__':
    main()
