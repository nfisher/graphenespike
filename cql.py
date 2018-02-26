import cassandra.cluster as cluster
import cassandra.policies as policies
import cassandra.query as query
import models

people_stmt = None
film_by_episode_stmt = None
films_stmt = None
planets_stmt = None
species_stmt = None
starships_stmt = None
vehicles_stmt = None
sess = None

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

def select(sess, stmt, ids):
    a = []
    if ids is None or len(ids) < 1:
        return a

    rs = sess.execute(stmt, parameters=[query.ValueSequence(ids)])
    for f in rs:
        a.append(f)

    return a

SELECT_FILM_BY_EPISODE = """SELECT * FROM swapi.films WHERE episode_id = ?;"""
def film_by_episode(sess, episode_id):
    return select(sess, film_by_episode_stmt, episode_id)

SELECT_FILMS = """SELECT * FROM swapi.films WHERE id IN ?;"""
def films(sess, ids):
    return select(sess, films_stmt, ids)

SELECT_PEOPLE = """SELECT * FROM swapi.people WHERE id IN ?;"""
def people(sess, ids):
    return select(sess, people_stmt, ids)

SELECT_PLANETS = """SELECT * FROM swapi.planets WHERE id in ?;"""
def planets(sess, ids):
    return select(sess, planets_stmt, ids)

SELECT_SPECIES = """SELECT * FROM swapi.species WHERE id in ?;"""
def species(sess, ids):
    return select(sess, species_stmt, ids)

SELECT_STARSHIPS = """SELECT * FROM swapi.starships WHERE id in ?;"""
def starships(sess, ids):
    return select(sess, starships_stmt, ids)

SELECT_VEHICLES = """SELECT * FROM swapi.vehicles WHERE id in ?;"""
def vehicles(sess, ids):
    return select(sess, vehicles_stmt, ids)
    
def session(hosts = ["127.0.0.1"]):
    """
    session returns the Cassandra connection.
    """
    global sess, film_by_episode_stmt, films_stmt, people_stmt, planets_stmt, species_stmt, starships_stmt, vehicles_stmt
    if sess is None:
        # TODO (NF 2018-02-13): Use connection pool.
        lbp = policies.RoundRobinPolicy()
        sess = cluster.Cluster(hosts, load_balancing_policy=lbp).connect()
        models.init(sess)
        film_by_episode_stmt = sess.prepare(SELECT_FILM_BY_EPISODE)
        films_stmt = sess.prepare(SELECT_FILMS)
        people_stmt = sess.prepare(SELECT_PEOPLE)
        planets_stmt = sess.prepare(SELECT_PLANETS)
        species_stmt = sess.prepare(SELECT_SPECIES)
        starships_stmt = sess.prepare(SELECT_STARSHIPS)
        vehicles_stmt = sess.prepare(SELECT_VEHICLES)

    return sess

def hosts(app):
    """
    host returns the cassandra host from the apps config or 127.0.0.1
    as a default.
    """
    if app is None:
        return ["127.0.0.1"]
    return app.config.get("cassandra_hosts", ["127.0.0.1"])