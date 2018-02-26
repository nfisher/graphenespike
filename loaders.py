import cql
import schema
import promise
import promise.dataloader as dataloader
import tracer

def span(name, args):
    t = tracer.instance()
    parent_span = t.get_span()
    span = t._tracer.start_span(name, child_of=parent_span)
    span.set_tag("component", "python-driver")
    span.set_tag("db.type", "cassandra")
    span.log_kv(args)
    return span

def map2character(cur):
    return schema.Character(
                    cur['id'],
                    name=cur['name'],
                    height=cur['height'],
                    mass=cur['mass'],
                    skin_color=cur['skin_color'],
                    eye_color=cur['eye_color'],
                    birth_year=cur['birth_year'],
                    gender=cur['gender'],
                    films=cur['films'],
                    species=cur.get('species',[]),
                    vehicles=cur.get('vehicles',[]),
                    starships=cur.get('starships',[]),
                    )

class Character(dataloader.DataLoader):
    def batch_load_fn(self, keys): # pylint: disable=E0202
        with span('character', {'count': len(keys), 'ids': keys}):
            return promise.Promise.resolve([map2character(c) for c in cql.people(cql.session(), keys)])

def map2film(r):
    return schema.Film(
                    r['id'],
                    episode_id=r['episode_id'],
                    title=r['title'],
                    director=r['director'],
                    producer=r['producer'],
                    release_date=r['release_date'],
                    opening_crawl=r['opening_crawl'],
                    species=r['species'],
                    starships=r['starships'],
                    vehicles=r['vehicles'],
                    characters=r['characters'],
                    planets=r['planets'],
                    )

class Film(dataloader.DataLoader):
    def batch_load_fn(self, keys): # pylint: disable=E0202
        with span('film', {'count': len(keys), 'ids': keys}):
            return promise.Promise.resolve([map2film(m) for m in cql.films(cql.session(), keys)])

def map2planet(cur):
    return schema.Planet(
                    cur['id'],
                    name=cur['name'],
                    diameter=cur['diameter'],
                    rotation_period=cur['rotation_period'],
                    orbital_period=cur['orbital_period'],
                    gravity=cur['gravity'],
                    population=cur['population'],
                    climate=cur['climate'],
                    terrain=cur['terrain'],
                    surface_water=cur['surface_water'],
                    residents=cur['residents'],
                    films=cur['films'],
                    )

class Planet(dataloader.DataLoader):
    def batch_load_fn(self, keys): # pylint: disable=E0202
        with span('planet', {'count': len(keys), 'ids': keys}):
            return promise.Promise.resolve([map2planet(m) for m in cql.planets(cql.session(), keys)])

def map2specie(cur):
    return schema.Specie(
                    cur['id'],
                    name=cur['name'],
                    classification=cur['classification'],
                    designation=cur['designation'],
                    average_height=cur['average_height'],
                    average_lifespan=cur['average_lifespan'],
                    eye_colors=cur['eye_colors'],
                    hair_colors=cur['hair_colors'],
                    skin_colors=cur['skin_colors'],
                    homeworld=cur['homeworld'],
                    language=cur['language'],
                    people=cur['people'],
                    films=cur['films'],
                    )

class Specie(dataloader.DataLoader):
    def batch_load_fn(self, keys): # pylint: disable=E0202
        with span('specie', {'count': len(keys), 'ids': keys}):
            return promise.Promise.resolve([map2specie(m) for m in cql.species(cql.session(), keys)])

def map2starship(cur):
    return schema.Starship(
                    cur['id'],
                    cargo_capacity=cur['cargo_capacity'],
                    consumables=cur['consumables'],
                    cost_in_credits=cur['cost_in_credits'],
                    crew=cur['crew'],
                    films=cur.get('films', []),
                    hyperdrive_rating=cur['hyperdrive_rating'],
                    length=cur['length'],
                    manufacturer=cur['manufacturer'],
                    max_atmosphering_speed=cur['max_atmosphering_speed'],
                    mglt=cur['mglt'],
                    model=cur['model'],
                    name=cur['name'],
                    passengers=cur['passengers'],
                    pilots=cur.get('pilots', []),
                    starship_class=cur['starship_class'],
                    )

class Starship(dataloader.DataLoader):
    def batch_load_fn(self, keys): # pylint: disable=E0202
        with span('starship', {'count': len(keys), 'ids': keys}):
            return promise.Promise.resolve([map2starship(m) for m in cql.starships(cql.session(), keys)])

def map2vehicle(cur):
    return schema.Vehicle(
                    cur['id'],
                    name=cur['name'],
                    cargo_capacity=cur['cargo_capacity'],
                    cost_in_credits=cur['cost_in_credits'],
                    crew=cur['crew'],
                    length=cur['length'],
                    manufacturer=cur['manufacturer'],
                    max_atmosphering_speed=cur['max_atmosphering_speed'],
                    model=cur['model'],
                    passengers=cur['passengers'],
                    pilots=cur.get('pilots', []),
                    films=cur.get('films', []),
                    vehicle_class=cur['vehicle_class'],
                    )

class Vehicle(dataloader.DataLoader):
    def batch_load_fn(self, keys): # pylint: disable=E0202
        with span('vehicle', {'count': len(keys), 'ids': keys}):
            return promise.Promise.resolve([map2vehicle(m) for m in cql.vehicles(cql.session(), keys)])
