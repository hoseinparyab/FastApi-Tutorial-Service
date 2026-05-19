import random
from pathlib import Path as SystemPath  # برای مدیریت پوشه استاتیک
from typing import List, Optional

from fastapi import FastAPI, File, Request, status
from fastapi import Path as FastAPIPath  # <--- کلاس مورد نظر فاست‌آپی با نام اختصاصی
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .Schemas import PersonResponseSchema, PersonResponseUpdateSchema, PersonSchema

_STATIC_DIR = SystemPath(__file__).resolve().parent / "static"

app = FastAPI(docs_url=None)
app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")

names_list = [
    {"id": 1, "name": "ali"},
    {"id": 2, "name": "hosein"},
    {"id": 3, "name": "hasan"},
    {"id": 4, "name": "reza"},
    {"id": 5, "name": "reza"},
    {"id": 6, "name": "reza"},
    {"id": 7, "name": "roozbeh"},
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


@app.post("/upload/")
async def upload_file(file: bytes = File(...)):
    # طول داده‌های فایل را چاپ می‌کنیم
    return {"file_size": len(file)}


@app.get("/names", response_model=List[PersonResponseSchema])
def retrive_names_list(q: Optional[str] = None):
    if q:
        return [item for item in names_list if item["name"] == q]
    return names_list


@app.post(
    "/names", status_code=status.HTTP_201_CREATED, response_model=PersonResponseSchema
)
def create_name(person: PersonSchema):
    name_obj = {"id": random.randint(6, 100), "name": person.name}
    names_list.append(name_obj)
    return name_obj


@app.get("/names/{name_id}", response_model=PersonResponseSchema)
def retrive_name_detail(
    name_id: int = FastAPIPath(
        title="object id", description="the id of the name in names_list"
    ),
):
    for item in names_list:
        if item["id"] == name_id:
            return item
    return {"detail": "object not found"}


@app.put(
    "/names/{name_id}",
    status_code=status.HTTP_200_OK,
    response_model=PersonResponseSchema,
)
def update_name_detail(person: PersonResponseUpdateSchema, name_id: int = FastAPIPath):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = person.name
            return item
    return {"detail": "object not found.."}


@app.delete("/names/{name_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_name(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
        return {"detail": "object deleted is done"}
    return {"detail": "object not found.."}


@app.get("/")
def root():
    return {"message": "Hello World"}
