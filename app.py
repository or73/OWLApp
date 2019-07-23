"""
File Path: app.py
Description: Application Init
Copyright (c) 2019. This Application has been developed by OR73.
"""
import os
import sys

from application import create_app

ROOT_PATH = os.path.dirname(os.path.relpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

# Create a logger object to log in the info and debug

# Host variable
HOST = os.environ.get('MONGODB_HOST')
# Port variable to run the server on
PORT = os.environ.get('APP_PORT')

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=int(PORT),
            debug=True,
            FLASK_DEBUG=True)  # runt the app

# import os
# import sys

# from application import (create_app, logger)
# from .application import create_app

# ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
# os.environ.update({'ROOT_PATH': ROOT_PATH})
# sys.path.append(os.path.join(ROOT_PATH, 'modules'))

# Create a logger object to log the info and debug
# LOG = logger.get_root_logger(os.environ.get('ROOT_LOGGER', 'root'),
#                             filename=os.path.join(ROOT_PATH, 'output.log'))
# Port variable to run the server on
# PORT = os.environ.get('APP_PORT')

# app = create_app()

# if __name__ == '__main__':
    # LOG.info('running environment: %s', os.environ.get('APP_ENV'))   # Debug mode if development env
#     app.run(host='0.0.0.0',
#             port=int(PORT))   # run the app
