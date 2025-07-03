from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List


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


class UnknownAlien(BaseModel):
    name:str
    age: int
    registered_date: int
    visited_planet: List[str]

class PlanetModel(BaseModel):
    name : str
    distance_to_Eath: str
    is_legal : bool

class PlanetLegalModel(BaseModel):
    name: str
    distance_to_Eath: str