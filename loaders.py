import schema
import promise
import promise.dataloader as dataloader

class CharacterLoader(dataloader.DataLoader):
    def batch_load_fn(self, keys): # pylint: disable=E0202
        return promise.Promise.resolve(schema.get_characters(keys))

class FilmLoader(dataloader.DataLoader):
    def batch_load_fn(self, keys): # pylint: disable=E0202
        return promise.Promise.resolve(schema.get_films(keys))

class PlanetLoader(dataloader.DataLoader):
    def batch_load_fn(self, keys): # pylint: disable=E0202
        return promise.Promise.resolve(schema.get_planets(keys))

class SpecieLoader(dataloader.DataLoader):
    def batch_load_fn(self, keys): # pylint: disable=E0202
        return promise.Promise.resolve(schema.get_planets(keys))

class StarshipLoader(dataloader.DataLoader):
    def batch_load_fn(self, keys): # pylint: disable=E0202
        return promise.Promise.resolve(schema.get_characters(keys))

class VehicleLoader(dataloader.DataLoader):
    def batch_load_fn(self, keys): # pylint: disable=E0202
        return promise.Promise.resolve(schema.get_vehicles(keys))
