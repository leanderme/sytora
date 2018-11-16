#!/bin/bash

# to make it simple we include the variables here instead of creating yet another file

# export type, supported are: "csv", "mongo", "sqlite"
# if run without setting a type will simply print to console
export EXPORT_TYPE=

# MongoDB parameters
export MONGO_HOST='localhost'
export MONGO_PORT=27017
export MONGO_USER=
export MONGO_PASS=
export MONGO_DB=
export MONGO_BUCKET='rxnorm'

# SQLite parameters
export SQLITE_FILE='databases/rxnorm.db'

# TODO: add a Couchbase version

# run the setup script with these environment variables
python3 rxnorm_link_run.py
