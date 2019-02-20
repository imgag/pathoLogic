#!/usr/bin/env python3

import os
import connexion

from flask import g
from flask import request
from swagger_server import encoder
from swagger_server import db
#from .db import get_db, close_db

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'pathoLogic'})
    app.run(port=os.getenv('HTTP_PORT', 8080))
    #app.app.teardown_appcontext(close_db)

    #Temporary fix: use dictionary as db
    @app.app.route('/v1/nextflow/<runid>', methods=['POST'])
    def nextflow(runid):
        # TODO: Implement update from nextflow
        print(request)
        return 'Hello, World!'

#    with app.app.app_context():
#        get_db()

if __name__ == '__main__':
    main()
