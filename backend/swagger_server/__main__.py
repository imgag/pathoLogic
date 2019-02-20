#!/usr/bin/env python3

import os
import connexion

from swagger_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'pathoLogic'})
    app.run(port=os.getenv('HTTP_PORT', 8080))


if __name__ == '__main__':
    main()
