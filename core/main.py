from os import name
from fastapi import FastAPI

app = FastAPI()
name_list =[
    {"id" :1, "name" : "ali"},
    {"id" :2, "name" : "hosein"},
    {"id" :3, "name" : "hasan"},
    {"id" :1, "name" : "reza"},
    {"id" :1, "name" : "roozbeh"},
]

@app.get("/names")
def retrive_name_list() :
    return name_list

@app.get("/names/{name_id}")
def retrive_name_detail(name_id:int):
    for name in name_list:
        if name[id]== name_id:
         return name
    return {"object not found"}
    # print(name_id)
    # return()
@app.get("/")
def root():
    return {"message": "Hello World"}
