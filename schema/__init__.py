import graphene
import models
import cql
import loaders
import threading
from .html import HTML
from .fetch import *

__all__ = ["html"]

load = threading.local()

def span(info, args):
    tracer = info._tracer
    parent_span = info._parent
    if parent_span is None:
        parent_span = tracer.get_span()
    span = tracer._tracer.start_span(info._name, child_of=parent_span)
    span.set_tag("component", "resolver")
    span.log_kv(args)
    return span

def get_film(episode_id, info):
    with span(info, {'episode_id': episode_id}):
        ep = models.Films.objects(episode_id=episode_id).first()
        f = Film(
                ep.id,
                episode_id=ep.episode_id,
                title=ep.title,
                director=ep.director,
                producer=ep.producer,
                release_date=ep.release_date,
                opening_crawl=ep.opening_crawl,
                species=ep.species,
                characters=ep.characters,
                starships=ep.starships,
                planets=ep.planets,
                )
        return f

class Film(graphene.ObjectType):
    _parent_span = None
    id = graphene.ID()
    episode_id = graphene.Int()
    title = graphene.String()
    director = graphene.String()
    producer = graphene.String()
    release_date = graphene.String()
    opening_crawl = graphene.String()
    species = graphene.List(lambda: Specie)
    characters = graphene.List(lambda: Character)
    starships = graphene.List(lambda: Starship)
    planets = graphene.List(lambda: Planet)
    vehicles = graphene.List(lambda: Vehicle)

    def resolve_species(self, info):
        if self.species is None:
            return []
        return load.specie.load_many(self.species)

    def resolve_characters(self, info):
        if self.characters is None:
            return []
        return load.character.load_many(self.characters)
    
    def resolve_starships(self, info):
        if self.starships is None:
            return []
        return load.starship.load_many(self.starships)

    def resolve_planets(self, info):
        if self.planets is None:
            return []
        return load.planet.load_many(self.planets)

class Character(graphene.ObjectType):
    _parent_span = None
    id = graphene.ID()
    name = graphene.String()
    height = graphene.String()
    mass = graphene.String()
    skin_color = graphene.String()
    eye_color = graphene.String()
    birth_year = graphene.String()
    gender = graphene.String()
    films = graphene.List(lambda: Film)
    species = graphene.List(lambda: Specie)
    starships = graphene.List(lambda: Starship)
    vehicles = graphene.List(lambda: Vehicle)

    def resolve_films(self, info):
        if self.films is None:
            return []
        return load.film.load_many(self.films)

    def resolve_species(self, info):
        if self.species is None:
            return []
        return load.specie.load_many(self.species)
    
    def resolve_starships(self, info):
        if self.starships is None:
            return []
        return load.starship.load_many(self.starships)

    def resolve_vehicles(self, info):
        if self.vehicles is None:
            return []
        return load.vehicle.load_many(self.vehicles)

class Starship(graphene.ObjectType):
    _parent_span = None
    id = graphene.ID()
    name = graphene.String()
    cargo_capacity = graphene.String()
    consumables = graphene.String()
    cost_in_credits = graphene.String()
    crew = graphene.String()
    hyperdrive_rating = graphene.String()
    length = graphene.String()
    manufacturer = graphene.String()
    max_atmosphering_speed = graphene.String()
    mglt = graphene.String()
    model = graphene.String()
    name = graphene.String()
    passengers = graphene.String()
    starship_class = graphene.String()
    films = graphene.List(lambda: Film)
    pilots = graphene.List(lambda: Character)

    def resolve_films(self, info):
        if self.films is None:
            return []
        return load.film.load_many(self.films)

    def resolve_pilots(self, info):
        if self.pilots is None:
            return []
        return load.character.load_many(self.pilots)

class Vehicle(graphene.ObjectType):
    _parent_span = None
    id = graphene.ID()
    name = graphene.String()
    cargo_capacity = graphene.String()
    consumables = graphene.String()
    cost_in_credits = graphene.String()
    crew = graphene.String()
    length = graphene.String()
    manufacturer = graphene.String()
    max_atmosphering_speed = graphene.String()
    model = graphene.String()
    passengers = graphene.String()
    vehicle_class = graphene.String()
    pilots = graphene.List(lambda: Character)
    films = graphene.List(lambda: Film)

    def resolve_films(self, info):
        if self.films is None:
            return []
        return load.film.load_many(self.films)

    def resolve_pilots(self, info):
        if self.pilots is None:
            return []
        return load.character.load_many(self.pilots)

class Planet(graphene.ObjectType):
    _parent_span = None
    id = graphene.ID()
    name = graphene.String()
    diameter = graphene.String()
    rotation_period = graphene.String()
    orbital_period = graphene.String()
    gravity = graphene.String()
    population = graphene.String()
    climate = graphene.String()
    terrain = graphene.String()
    surface_water = graphene.String()
    residents = graphene.List(lambda: Character)
    films = graphene.List(lambda: Film)

    def resolve_films(self, info):
        if self.films is None:
            return []
        return load.film.load_many(self.films)
    
    def resolve_residents(self, info):
        if self.residents is None:
            return []
        return load.character.load_many(self.residents)

class Specie(graphene.ObjectType):
    _parent_span = None
    id = graphene.ID()
    name = graphene.String()
    classification = graphene.String()
    designation = graphene.String()
    average_height = graphene.String()
    average_lifespan = graphene.String()
    eye_colors = graphene.String()
    hair_colors = graphene.String()
    skin_colors = graphene.String()
    language = graphene.String()
    homeworld = graphene.List(lambda: Planet)
    people = graphene.List(lambda: Character)
    films = graphene.List(lambda: Film)
    
    def resolve_homeworld(self, info):
        ids = [self.homeworld]
        if self.homeworld is None:
            return []

        return load.planet.load_many(ids)

    def resolve_films(self, info):
        if self.films is None:
            return []
        return load.film.load_many(self.films)
    
    def resolve_people(self, info):
        if self.people is None:
            return []
        return load.character.load_many(self.people)

class Episode(graphene.Enum):
    PHANTOM = 1
    CLONES = 2
    SITH = 3 
    NEWHOPE = 4
    EMPIRE = 5
    JEDI = 6
    AWAKENS = 7

def init_loaders():
    global load
    load.character = loaders.Character()
    load.film = loaders.Film()
    load.planet = loaders.Planet()
    load.specie = loaders.Specie()
    load.starship = loaders.Starship()
    load.vehicle = loaders.Vehicle()

class Query(graphene.ObjectType):
    episode = graphene.Field(Film, episode_id=Episode())

    def resolve_episode(self, info, episode_id):
        init_loaders()
        return get_film(episode_id, info)

schema = graphene.Schema(query=Query)