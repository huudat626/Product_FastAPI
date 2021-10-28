from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import ProductsModel, UpdateProductsModel

router = APIRouter()


@router.get("/", response_description="List all products")
async def list_products(request: Request):
    products = []
    for doc in await request.app.mongodb["products"].find().to_list(length=100):
        products.append(doc)
    return products


@router.get("/{id}", response_description="Get a single task")
async def show_products(id: str, request: Request):
    if (products := await request.app.mongodb["products"].find_one({"_id": id})) is not None:
        return products

    raise HTTPException(status_code=404, detail=f"products {id} not found")


@router.post("/", response_description="Add new products")
async def create_products(request: Request, pro: ProductsModel = Body(...)):
    pro = jsonable_encoder(pro)
    new_pro = await request.app.mongodb["products"].insert_one(pro)
    created_pro = await request.app.mongodb["products"].find_one(
        {"_id": new_pro.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_pro)


@router.put("/{id}", response_description="Update a products")
async def update_pro(id: str, request: Request, pro: UpdateProductsModel = Body(...)):
    pro = {k: v for k, v in pro.dict().items() if v is not None}

    if len(pro) >= 1:
        update_result = await request.app.mongodb["products"].update_one(
            {"_id": id}, {"$set": pro}
        )

        if update_result.modified_count == 1:
            if (
                updated_pro := await request.app.mongodb["products"].find_one({"_id": id})
            ) is not None:
                return updated_pro

    if (
        existing_products := await request.app.mongodb["products"].find_one({"_id": id})
    ) is not None:
        return existing_products

    raise HTTPException(status_code=404, detail=f"products {id} not found")


@router.delete("/{id}", response_description="Delete products")
async def delete_products(id: str, request: Request):
    delete_result = await request.app.mongodb["products"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"products {id} not found")