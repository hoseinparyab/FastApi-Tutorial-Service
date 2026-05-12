from imaplib import IMAP4
from pathlib import Path
import random
from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

_STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(docs_url=None)
app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")

name_list = [
    {"id": 1, "name": "ali"},
    {"id": 2, "name": "hosein"},
    {"id": 3, "name": "hasan"},
    {"id": 1, "name": "reza"},
    {"id": 1, "name": "roozbeh"},
]


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html(request: Request) -> HTMLResponse:
    root = request.scope.get("root_path", "").rstrip("/")
    return get_swagger_ui_html(
        openapi_url=f"{root}/openapi.json",
        title=f"{app.title} - Swagger UI",
        swagger_js_url=f"{root}/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url=f"{root}/static/swagger-ui/swagger-ui.css",
    )


@app.get("/names")
def retrive_name_list():
    return name_list


@app.post("/names")
def create_name(name: str):
    name_obj = {"id": random.randint(6, 100), "name": name}
    name_list.append(name_obj)
    return name_obj


@app.get("/names/{name_id}")
def retrive_name_detail(name_id: int):
    for item in name_list:
        if item["id"] == name_id:
            return item
    return {"detail": "object not found"}


@app.put("/names/{name_id}")
def update_name_detail(name_id: int, name: str):
    for item in name_list:
        if item["id"] == name_id:
            item["id"] = name
            return item
    return {"detail": "object not found.."}


@app.delete("/names/{name_id}")
def delete_name(name_id: int):
    for item in name_list:
        if item["id"] == name_id:
            name_list.remove(item)
        return {"detail": "object deleted is done"}
    return {"detail": "object not found.."}


@app.get("/")
def root():
    return {"message": "Hello World"}
