from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import CategoriesModel, UpdateCategoriesModel

router = APIRouter()


@router.get("/", response_description="List all categories")
async def list_categories(request: Request):
    categories = []
    for doc in await request.app.mongodb["categories"].find().to_list(length=100):
        categories.append(doc)
    return categories


@router.get("/{id}", response_description="Get a single task")
async def show_categories(id: str, request: Request):
    if (categories := await request.app.mongodb["categories"].find_one({"_id": id})) is not None:
        return categories

    raise HTTPException(status_code=404, detail=f"categories {id} not found")


@router.post("/", response_description="Add new categories")
async def create_categories(request: Request, cate: CategoriesModel = Body(...)):
    cate = jsonable_encoder(cate)
    new_cate = await request.app.mongodb["categories"].insert_one(cate)
    created_cate = await request.app.mongodb["categories"].find_one(
        {"_id": new_cate.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_cate)


@router.put("/{id}", response_description="Update a categories")
async def update_cate(id: str, request: Request, cate: UpdateCategoriesModel = Body(...)):
    cate = {k: v for k, v in cate.dict().items() if v is not None}

    if len(cate) >= 1:
        update_result = await request.app.mongodb["categories"].update_one(
            {"_id": id}, {"$set": cate}
        )

        if update_result.modified_count == 1:
            if (
                updated_cate := await request.app.mongodb["categories"].find_one({"_id": id})
            ) is not None:
                return updated_cate

    if (
        existing_categories := await request.app.mongodb["categories"].find_one({"_id": id})
    ) is not None:
        return existing_categories

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.delete("/{id}", response_description="Delete categories")
async def delete_categories(id: str, request: Request):
    delete_result = await request.app.mongodb["categories"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"categories {id} not found")