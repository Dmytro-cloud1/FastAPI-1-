from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from random import choices
from string import ascii_letters
from typing import List
from fastapi import Body

app = FastAPI()

#ALIENS AND PLANETS

class Planet:
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


class Alien:
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


class Post(BaseModel):
    id: int
    title: str
    body: str

posts = [
    {'id':1, 'title':'News1', 'body': 'Test1'},
    {'id':2, 'title':'News2', 'body': 'Test2'},
    {'id':3, 'title':'News3', 'body': 'Test3'}
]


@app.get("/")
async def items() -> int:
    return 100

@app.get("/items")
async def items() -> list[Post]:
    return posts

@app.get("/items/{id}")
async def items(id:int) -> dict:
    for post in posts:
        if post["id"] == id:
            return post

    raise HTTPException(status_code=404, detail="This Post not found")


@app.post("/create_item/")
async def create_item(post:Post) -> int:
    print(post.title)
    return 200

@app.get("/password/{abc}")
def create_password(abc:int):
    passw = choices(ascii_letters, k=abc)
    if len(passw) >= 8:
        return "Password is longer than 8 items"
    
    return passw


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
    return[get_planet(aliens_planets) for aliens_planets in alien_query.visited_planet]

# Из unknownalien создать обычного alien без потери данных(если на сервер приходит новый запрос )