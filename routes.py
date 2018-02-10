import flask
import socket
import os
import cassandra.cluster as cluster
import pprint

pp = pprint.PrettyPrinter(indent=4)

app = flask.Flask("graphenespike")

def cassandra_hosts(app):
    """
    cassandra_host returns the cassandra host from the apps config or 127.0.0.1
    as a default.
    """
    return app.config.get("cassandra_hosts", ["127.0.0.1"])

with app.app_context():
    config_file = os.getenv("CONFIG_PATH", "config.json")
    app.config.from_json(config_file)
    pp.pprint(app.config)
    # disable deprecation warning when unit test is run.
    app.config.update(JSONIFY_PRETTYPRINT_REGULAR=False)

PING_QUERY = 'SELECT uuid() FROM system.local;'
def ping_cql(sess):
    rs = sess.execute(PING_QUERY)
    if len(rs.current_rows) != 1:
        # TODO: Replace with throwing an exception.
        print("len = ", len(rs.current_rows))

def cql_session():
    """
    data_session returns the Cassandra connection.
    """
    c = getattr(flask.g, "cluster", None)
    if c is None:
        flask.g.cluster = cluster.Cluster(cassandra_hosts(app))

    s = getattr(flask.g, "cassandra_session", None)
    if s is None:
        # TODO: this will likely need adjustment for a multiprocess setup.
        flask.g.cassandra_session = flask.g.cluster.connect()

    return flask.g.cassandra_session

@app.route("/")
def root():
    return "Go away!"

@app.route("/graphql")
def graphql():
    return "Mount schema here..."

@app.route("/healthz")
def healthz():
    """
    healthz is a monitoring end-point used to verify the node is available to
    serve traffic.

    :return: 200 OK if all dependencies are reachable, otherwise status is 500.
    """
    try:
        ping_cql(cql_session())
    except cluster.NoHostAvailable:
        abort(500)

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
    try:
        ping_cql(cql_session())
    except cluster.NoHostAvailable as err:
        errors.append("CQL Ping: {0}".format(err))

    return flask.jsonify(hostname=socket.gethostname(), metadata={"cassandra_hosts": cassandra_hosts(app)}, errors=errors)

@app.route("/healthz/ready")
def isready():
    """
    isready is a monitoring end-point used to verify that the node is ready to 
    be placed in balance after start-up.

    :return: 200 OK if all dependencies are reachable, otherwise status is 500.
    """
    try:
        ping_cql(cql_session())
    except cluster.NoHostAvailable:
        abort(500)

    return "OK"


