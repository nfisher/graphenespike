import cassandra.cqlengine.models as m
import cassandra.cqlengine.columns as col
import cassandra.cqlengine.management as mgmt
import cassandra.cqlengine.connection as conn

class Films(m.Model):
    __keyspace__    = "swapi"
    __connection__  = "swapi"

    id              = col.BigInt(primary_key=True)
    episode_id      = col.Integer(index=True)
    title           = col.Text(index=True)
    director        = col.Text(max_length=96)
    producer        = col.Text(max_length=96)
    release_date    = col.Date()
    opening_crawl   = col.Text()
    species         = col.Set(col.BigInt)
    starships       = col.Set(col.BigInt)
    vehicles        = col.Set(col.BigInt)
    characters      = col.Set(col.BigInt)
    planets         = col.Set(col.BigInt)
    created         = col.Date()
    edited          = col.Date()

class Species(m.Model):
    __keyspace__    = "swapi"
    __connection__  = "swapi"

    id              = col.BigInt(primary_key=True)
    name            = col.Text(max_length=96)
    classification  = col.Text(max_length=96)
    designation     = col.Text(max_length=96)
    average_height  = col.Text(max_length=16)
    average_lifespan = col.Text(max_length=16)
    eye_colors      = col.Text(max_length=96)
    hair_colors     = col.Text(max_length=96)
    skin_colors     = col.Text(max_length=96)
    language        = col.Text(max_length=96)
    homeworld       = col.BigInt()
    people          = col.Set(col.BigInt)
    films           = col.Set(col.BigInt)
    created         = col.Date()
    edited          = col.Date()

class Starships(m.Model):
    __keyspace__    = "swapi"
    __connection__  = "swapi"

    id              = col.BigInt(primary_key=True)
    cargo_capacity  = col.Text(max_length=32)
    consumables     = col.Text(max_length=96)
    cost_in_credits = col.Text(max_length=32)
    crew            = col.Text(max_length=32)
    hyperdrive_rating = col.Text(max_length=32)
    length          = col.Text(max_length=32)
    manufacturer    = col.Text(max_length=96)
    max_atmosphering_speed = col.Text(max_length=32)
    mglt            = col.Text(max_length=96)
    model           = col.Text(max_length=96)
    name            = col.Text(max_length=96)
    passengers      = col.Text(max_length=16)
    starship_class  = col.Text(max_length=96)
    films           = col.Set(col.BigInt)
    pilots          = col.Set(col.BigInt)
    created         = col.Date()
    edited          = col.Date()

class People(m.Model):
    __keyspace__    = "swapi"
    __connection__  = "swapi"

    id              = col.BigInt(primary_key=True)
    name            = col.Text(max_length=96)
    height          = col.Text(max_length=16)
    mass            = col.Text(max_length=16)
    skin_color      = col.Text(max_length=16)
    eye_color       = col.Text(max_length=16)
    birth_year      = col.Text(max_length=16)
    gender          = col.Text(max_length=16)
    homeworld       = col.BigInt()
    films           = col.Set(col.BigInt)
    species         = col.Set(col.BigInt)
    starships       = col.Set(col.BigInt)
    vehicles        = col.Set(col.BigInt)
    created         = col.Date()
    edited          = col.Date()

class Planets(m.Model):
    __keyspace__    = "swapi"
    __connection__  = "swapi"

    id              = col.BigInt(primary_key=True)
    name            = col.Text(max_length=96)
    diameter        = col.Text(max_length=16)
    rotation_period = col.Text(max_length=16)
    orbital_period  = col.Text(max_length=16)
    gravity         = col.Text(max_length=96)
    population      = col.Text(max_length=32)
    climate         = col.Text(max_length=96)
    terrain         = col.Text(max_length=96)
    surface_water   = col.Text(max_length=16)
    residents       = col.Set(col.BigInt)
    films           = col.Set(col.BigInt)
    created         = col.Date()
    edited          = col.Date()

class Vehicles(m.Model):
    __keyspace__    = "swapi"
    __connection__  = "swapi"

    id              = col.BigInt(primary_key=True)
    cargo_capacity  = col.Text(max_length=32)
    consumables     = col.Text(max_length=96)
    cost_in_credits = col.Text(max_length=96)
    crew            = col.Text(max_length=32)
    films           = col.Set(col.BigInt)
    length          = col.Text(max_length=32)
    manufacturer    = col.Text(max_length=96)
    max_atmosphering_speed = col.Text(max_length=32)
    model           = col.Text(max_length=96)
    name            = col.Text(max_length=96)
    passengers      = col.Text(max_length=16)
    pilots          = col.Set(col.BigInt)
    vehicle_class   = col.Text(max_length=96)

def teardown(sess):
    mgmt.drop_keyspace("swapi")

def init(sess):
    conn.register_connection("swapi", session=sess, default=True)
    mgmt.create_keyspace_simple("swapi", replication_factor=1, durable_writes=True)

    mgmt.sync_table(Films)
    mgmt.sync_table(People)
    mgmt.sync_table(Planets)
    mgmt.sync_table(Species)
    mgmt.sync_table(Starships)
    mgmt.sync_table(Vehicles)