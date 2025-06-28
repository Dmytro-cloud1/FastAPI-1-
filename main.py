from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from random import choices
from string import ascii_letters
from typing import List
from fastapi import Body
from abc import ABC, abstractmethod


app = FastAPI()

#ALIENS AND PLANETS
class SpaceObject(ABC):
    @abstractmethod
    def to_dict() -> dict:
        pass


class Planet(SpaceObject):
    def __init__(self, name:str, distance_to_Eath: str, is_legal: bool):
        self.name = name
        self.distance_to_Eath = distance_to_Eath
        self.is_legal = is_legal
    
    def to_dict(self):
        return {
            "name": self.name,
            "distance_to_earth": self.distance_to_earth,
            "is_legal": self.is_legal
        }


class Alien(SpaceObject):
    def __init__(self, name:str, age:int, visited_planets: List[Planet], registered_date: int):
        self.name = name
        self.age = age
        self.registered_date = registered_date
        self.visited_planets = visited_planets

    def to_dict(self):
        return{
            "name": self.name,
            "age": self.age,
            "registered_date": self.registered_date,
            "visited_planet": [planet.name for planet in self.visited_planets]
        }


planet_jupiter = Planet("Jupiter", "365 million miles", True)
planet_saturn = Planet("Saturn", "746 million miles", False)
planet_mercury = Planet("Mercury", "48 million miles", True)

all_planets = [planet_jupiter, planet_saturn, planet_mercury]

aliens = [
    Alien('Krellax-9', 110, [planet_jupiter, planet_mercury], 1900),
    Alien('Veluna Shikari', 200, [planet_jupiter, planet_mercury, planet_saturn], 1800),
    Alien('Zorvak Treen', 400,  [planet_mercury, planet_saturn], 1600)
]

class UnknownAlien(BaseModel):
    name:str
    age: int
    registered_date: int
    visited_planet: List[str]

#ALIENS AND PLANETS
@app.get("/get-all-aliens/")
def get_all_aliens():
    return [alien.to_dict() for alien in aliens]

@app.get("/get-alien/{alien_name}")
def get_alien(alien_name:str):
    for alien in aliens:
        if alien.name == alien_name:
            return alien.to_dict()
        
    raise HTTPException(status_code=404, detail="This Post not found")


def get_planet(planet):
    for all_planet in all_planets:
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

    aliens.append(new_alien)

    return {
        "message": "New alien are created",
        "New alien": new_alien.to_dict()
    }


