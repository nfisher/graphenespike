import graphene
import models

def start_span(info):
    tracer = info._tracer
    parent_span = info._parent
    if parent_span is None:
        print("Parent span unavailable linking to root")
        parent_span = tracer.get_span()

    span = tracer._tracer.start_span(info._name, child_of=parent_span)
    return span

def get_films(ids, info):
    with start_span(info) as span:
        if ids is None:
            span.log_kv({"ids": ids})
            return []

        c = models.Films.objects.filter(id__in = ids)
        a = []
        for cur in c:
            f = Film(
                    cur.id,
                    episode_id=cur.episode_id,
                    title=cur.title,
                    director=cur.director,
                    producer=cur.producer,
                    release_date=cur.release_date,
                    opening_crawl=cur.opening_crawl,
                    species=cur.species,
                    starships=cur.starships,
                    vehicles=cur.vehicles,
                    characters=cur.characters,
                    planets=cur.planets,
                    )
            f._parent_span = span
            a.append(f)
        span.log_kv({"ids": ids})
        return a

def get_species(ids, info):
    span = start_span(info)
    if ids is None:
        span.log_kv({"ids": ids})
        span.finish()
        return []

    c = models.Species.objects.filter(id__in = ids)
    a = []
    for cur in c:
        s = Specie(
                cur.id,
                name=cur.name,
                classification=cur.classification,
                designation=cur.designation,
                average_height=cur.average_height,
                average_lifespan=cur.average_lifespan,
                eye_colors=cur.eye_colors,
                hair_colors=cur.hair_colors,
                skin_colors=cur.skin_colors,
                homeworld=cur.homeworld,
                language=cur.language,
                people=cur.people,
                films=cur.films,
                )
        s._parent_span = span
        a.append(s)
    span.log_kv({"ids": ids})
    span.finish()
    return a

def get_starships(ids, info):
    span = start_span(info)
    if ids is None:
        span.log_kv({"ids": ids})
        span.finish()
        return []

    c = models.Starships.objects.filter(id__in = ids)
    a = []
    for cur in c:
        s = Starship(
                cur.id,
                name=cur.name,
                cargo_capacity=cur.cargo_capacity,
                consumables=cur.consumables,
                cost_in_credits=cur.cost_in_credits,
                crew=cur.crew,
                hyperdrive_rating=cur.hyperdrive_rating,
                length=cur.length,
                manufacturer=cur.manufacturer,
                max_atmosphering_speed=cur.max_atmosphering_speed,
                mglt=cur.mglt,
                model=cur.model,
                passengers=cur.passengers,
                starship_class=cur.starship_class,
                films=cur.films,
                pilots=cur.pilots,
                )
        a.append(s)
    span.log_kv({"ids": ids})
    span.finish()
    return a

def get_characters(ids, info):
    span = start_span(info)
    if ids is None:
        span.log_kv({"ids": ids})
        span.finish()
        return []
    c = models.People.objects.filter(id__in = ids)
    a = []
    for cur in c:
        c = Character(
                cur.id,
                name=cur.name,
                height=cur.height,
                mass=cur.mass,
                skin_color=cur.skin_color,
                eye_color=cur.eye_color,
                birth_year=cur.birth_year,
                gender=cur.gender,
                films=cur.films,
                species=cur.species,
                starships=cur.starships,
                vehicles=cur.vehicles,
                )
        c._parent_span = span
        a.append(c)
    span.log_kv({"ids": ids})
    span.finish()
    return a

def get_planets(ids, info):
    span = start_span(info)
    if ids is None:
        span.log_kv({"ids": ids})
        span.finish()
        return []
    c = models.Planets.objects.filter(id__in = ids)
    a = []
    for cur in c:
        p = Planet(
                cur.id,
                name=cur.name,
                diameter=cur.diameter,
                rotation_period=cur.rotation_period,
                orbital_period=cur.orbital_period,
                gravity=cur.gravity,
                population=cur.population,
                climate=cur.climate,
                terrain=cur.terrain,
                surface_water=cur.surface_water,
                residents=cur.residents,
                films=cur.films,
                )
        p._parent_span = span
        a.append(p)
    span.log_kv({"ids": ids})
    span.finish()
    return a

def get_vehicles(ids, info):
    span = start_span(info)
    if ids is None:
        span.log_kv({"ids": ids})
        span.finish()
        return []
    c = models.Vehicles.objects.filter(id__in  = ids)
    a = []
    for cur in c:
        v = Vehicle(
                cur.id,
                name=cur.name,
                diameter=cur.diameter,
                rotation_period=cur.rotation_period,
                orbital_period=cur.orbital_period,
                gravity=cur.gravity,
                population=cur.population,
                climate=cur.climate,
                terrain=cur.terrain,
                surface_water=cur.surface_water,
                residents=cur.residents,
                films=cur.films,
                )
        v._parent_span = span
        a.append(v)
    span.log_kv({"ids": ids})
    span.finish()
    return a

def get_film(episode_id, info):
    span = start_span(info)
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
    span.log_kv({"ids": episode_id})
    span.finish()
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

    def resolve_species(self, info):
        info._parent = self._parent_span
        return get_species(list(self.species), info)

    def resolve_characters(self, info):
        info._parent = self._parent_span
        return get_characters(list(self.characters), info)
    
    def resolve_starships(self, info):
        info._parent = self._parent_span
        return get_starships(list(self.starships), info)

    def resolve_planets(self, info):
        info._parent = self._parent_span
        return get_planets(list(self.planets), info)

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
        info._parent = self._parent_span
        return get_films(list(self.films), info)

    def resolve_species(self, info):
        info._parent = self._parent_span
        return get_species(list(self.species), info)
    
    def resolve_starships(self, info):
        info._parent = self._parent_span
        return get_starships(list(self.starships), info)

    def resolve_vehicles(self, info):
        info._parent = self._parent_span
        return get_vehicles(list(self.vehicles), info)

class Starship(graphene.ObjectType):
    _parent_span = None
    id = graphene.ID()
    name = graphene.String()
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
        info._parent = self._parent_span
        return get_films(list(self.films), info)
    
    def resolve_pilots(self, info):
        info._parent = self._parent_span
        return get_characters(list(self.pilots), info)

class Vehicle(graphene.ObjectType):
    _parent_span = None
    id = graphene.ID()
    name = graphene.String()

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
        info._parent = self._parent_span
        return get_films(list(self.films), info)
    
    def resolve_residents(self, info):
        info._parent = self._parent_span
        return get_characters(list(self.residents), info)

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
        info._parent = self._parent_span
        ids = [self.homeworld]
        if self.homeworld is None:
            ids = []

        return get_planets(ids, info)

    def resolve_films(self, info):
        info._parent = self._parent_span
        return get_films(list(self.films), info)
    
    def resolve_people(self, info):
        info._parent = self._parent_span
        return get_characters(list(self.people), info)

class Episode(graphene.Enum):
    PHANTOM = 1
    CLONES = 2
    SITH = 3 
    NEWHOPE = 4
    EMPIRE = 5
    JEDI = 6
    AWAKENS = 7

class Query(graphene.ObjectType):
    episode = graphene.Field(Film, episode_id=Episode())

    def resolve_episode(self, info, episode_id):
        return get_film(episode_id, info)

schema = graphene.Schema(query=Query)

HTML = '''<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/graphiql/0.11.11/graphiql.min.css" integrity="sha256-gSgd+on4bTXigueyd/NSRNAy4cBY42RAVNaXnQDjOW8=" crossorigin="anonymous" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fetch/1.1.1/fetch.min.js" integrity="sha256-TQsP3yTWwfvm6Auy90oBeVhYhGZuKa1jRM3vpnQpX+8=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react/15.6.2/react.min.js" integrity="sha256-c/17te7UpABi7+wcIHAAiIMOrNMVcTIzoxtRTDoYB4s=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/15.6.2/react-dom.min.js" integrity="sha256-Xhtg7QJuNhwB5AzaUcgr0iqNtCitzN+c/6k5/SOtENU=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/graphiql/0.11.11/graphiql.min.js" integrity="sha256-oeWyQyKKUurcnbFRsfeSgrdOpXXiRYopnPjTVZ+6UmI=" crossorigin="anonymous"></script>
    <title>GraphiQL</title>
  </head>
  <body style="width: 100%; height: 100%; margin: 0; overflow: hidden;">
    <div id="graphiql" style="height: 100vh;">Loading...</div>
    <script>
      "use strict";
      var headers = new Headers();
      headers.set("Content-Type", "application/json");

      function graphQLFetcher(graphQLParams) {
        return fetch("graphql?raw", {
          method: "post",
          headers: headers,
          body: JSON.stringify(graphQLParams),
        }).then(function (response) {
          return response.text();
        }).then(function (responseBody) {
          try {
            return JSON.parse(responseBody);
          } catch (error) {
            return responseBody;
          }
        });
      }

      ReactDOM.render(
        React.createElement(GraphiQL, {fetcher: graphQLFetcher}),
        document.getElementById("graphiql")
      );
    </script>
  </body>
</html>'''