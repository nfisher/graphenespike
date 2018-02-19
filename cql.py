import cassandra.cluster as cluster

PING_QUERY = 'SELECT uuid() FROM system.local;'
def ping(sess):
    """
    ping
    """
    try:
        sess.execute(PING_QUERY)
    except cluster.NoHostAvailable as err:
        return "Error CQL Ping: {0}".format(err)
    
    return None

def session(hosts = ["127.0.0.1"]):
    """
    session returns the Cassandra connection.
    """
    # TODO (NF 2018-02-13): Use connection pool.
    return cluster.Cluster(hosts).connect()

def hosts(app):
    """
    host returns the cassandra host from the apps config or 127.0.0.1
    as a default.
    """
    if app is None:
        return ["127.0.0.1"]
    return app.config.get("cassandra_hosts", ["127.0.0.1"])