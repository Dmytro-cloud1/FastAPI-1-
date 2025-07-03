from fastapi import FastAPI, HTTPException, Body
from models import Planet, Alien, UnknownAlien, PlanetModel, PlanetLegalModel

app = FastAPI()

class MigrationService:

    all_planets = []
    aliens = []

    @classmethod
    def get_info(cls):
        planet_jupiter = Planet("Jupiter", "365 million miles", True)
        planet_saturn = Planet("Saturn", "746 million miles", False)
        planet_mercury = Planet("Mercury", "48 million miles", True)

        cls.all_planets = [planet_jupiter, planet_saturn, planet_mercury]

        cls.aliens = [
            Alien('Krellax-9', 110, [planet_jupiter, planet_mercury], 1900),
            Alien('Veluna Shikari', 200, [planet_jupiter, planet_mercury, planet_saturn], 1800),
            Alien('Zorvak Treen', 400,  [planet_mercury, planet_saturn], 1600)
        ]

        return cls.all_planets, cls.aliens
    
    @classmethod
    def add_planet(cls, planet_model: PlanetLegalModel):
        search_planet = list(filter(lambda p: p.name == planet_model.name, cls.all_planets))

        if not search_planet:  
            new_planet = Planet(
                name = planet_model.name,
                distance_to_Eath = planet_model.distance_to_Eath,
                is_legal= False
            )

            cls.all_planets.append(new_planet)
            return new_planet
        

        return True

#ALIENS AND PLANETS
@app.get("/get-all-aliens/")
def get_all_aliens():
    return [alien.to_dict() for alien in MigrationService.aliens]

@app.get("/get-alien/{alien_name}")
def get_alien(alien_name:str):
    for alien in MigrationService.aliens:
        if alien.name == alien_name:
            return alien.to_dict()
        
    raise HTTPException(status_code=404, detail="This Post not found")

def get_planet(planet):
    for all_planet in MigrationService.all_planets:
        if all_planet.name == planet:
            return all_planet
        
@app.post("/get-unknown-alien/")
def get_unknown_alien(alien_query: UnknownAlien = Body(...)):
    visited_planets = [get_planet(aliens_planets) for aliens_planets in alien_query.visited_planet]

    new_alien = Alien(
        name = alien_query.name,
        age = alien_query.age,
        visited_planets= visited_planets,
        registered_date= alien_query.registered_date
    )

    MigrationService.aliens.append(new_alien)

    return {
        "message": "New alien are created",
        "New alien": new_alien.to_dict()
    }

@app.post("/register-planet/")
def register_new_planet(planet_model: PlanetLegalModel = Body(...)):
    return MigrationService.add_planet(planet_model)

# @app.on_event("startup")
# def startup_event():
#     MigrationService.get_info()

if __name__ == '__main__':
    MigrationService.get_info()