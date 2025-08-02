from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List
from dataclasses import dataclass


#ALIENS AND PLANETS
class SpaceObject(ABC):
    @abstractmethod
    def to_dict() -> dict:
        pass

@dataclass
class Planet(SpaceObject):
    name: str
    distance_to_Eath: str
    is_legal: bool
    
    def to_dict(self):
        return {
            "name": self.name,
            "distance_to_earth": self.distance_to_earth,
            "is_legal": self.is_legal
        }


@dataclass
class Alien(SpaceObject):
    name:str 
    age:int
    visited_planets: List[Planet] 
    registered_date: int

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

class PlanetLegalModel(BaseModel):
    name: str
    distance_to_Eath: str