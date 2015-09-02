__author__ = 'arthur'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

# DATABASE URI
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database/rate_parser.db')
# SQLALCHEMY_DATABASE_URI = 'mysql://<username>:<password>@<host>/<schema>?charset=utf8'

# LOGGING
APPLICATION_LOG_FILE = os.path.join(basedir, 'logs/application.log')
PARSER_LOG_FILE = os.path.join(basedir, 'logs/parser.log')

# APP SETTINGS
PARSING_INTERVAL_SECONDS = 3600  # 60min
OUTPUT_FILE = os.path.join(basedir, 'out.html')

# CACHE
CACHE_TIMEOUT = 1800  # 30min
# CACHE_TYPE = 'simple'
CACHE_TYPE = 'memcached'