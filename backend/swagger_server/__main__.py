#!/usr/bin/env python3

import os
import connexion
import json
from flask import g
from flask import request
from swagger_server import encoder
from swagger_server import db
#from .db import get_db, close_db

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'pathoLogic'})

    #Temporary fix: use dictionary as db

    # Create route for nextflow weblog (assembly)
    @app.app.route('/v1/nf_assembly/<runid>', methods=['POST'])
    def nf_assembly(runid):
        req_data = request.get_json()
        print(req_data)
        db['status_assembly'][runid] = req_data
        print(json.dumps(db['status'][runid]))
        return 'NF Request received'

    # Create route for nextflow weblog (plasmident)
    @app.app.route('/v1/nf_plasmident/<runid>', methods=['POST'])
    def nf_plasmident(runid):
        req_data = request.get_json()
        print(req_data)
        db['status_plasmident'][runid] = req_data
        print(json.dumps(db['status'][runid]))
        return 'NF Request received'

    app.run(port=os.getenv('HTTP_PORT', 8080))

if __name__ == '__main__':
    main()
