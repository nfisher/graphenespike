import flask
import flask_graphql as graphql
import socket
import os
import cql
import models
import schema

app = flask.Flask("graphenespike")

config_file = os.getenv("CONFIG_PATH", "config.json")
# TODO: Replace this so there's no IO on import
app.config.from_json(config_file)
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=False)

@app.route("/")
def root():
    return "Go away!"

view = graphql.GraphQLView.as_view('graphql', schema=schema.schema, graphiql=True, graphiql_template=schema.HTML)
app.add_url_rule("/graphql", view_func=view)

@app.route("/healthz")
def healthz():
    """
    healthz is a monitoring end-point used to verify the node is available to
    serve traffic.

    :return: 200 OK if all dependencies are reachable, otherwise status is 500.
    """    
    error = cql.ping(cql.session())
    if error is not None:
        flask.abort(500)

    return "OK"

@app.route("/healthz/info")
def info():
    """
    info is a monitoring end-point that outputs JSON including the hostname,
    connection errors, and any relevant metadata. metadata MUST NOT include
    secrets or credentials.

    :returns: JSON data for this services configuration details and errors.
    """
    errors = []
    metadata = {
        "cassandra_hosts": cql.hosts(app)
    }

    ping_error = cql.ping(cql.session())
    if ping_error is not None:
        errors.append(ping_error)

    return flask.jsonify(hostname=socket.gethostname(),
                        metadata=metadata,
                        errors=errors)

@app.route("/healthz/ready")
def isready():
    """
    isready is a monitoring end-point used to verify that the node is ready to 
    be placed in balance after start-up.

    :return: 200 OK if all dependencies are reachable, otherwise status is 500.
    """
    error = cql.ping(cql.session())
    if error is not None:
        flask.abort(500)

    return "OK"