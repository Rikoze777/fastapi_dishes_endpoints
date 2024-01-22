from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database import submenu_crud, schemas
from app.database.db import get_db
from fastapi.responses import JSONResponse
from pydantic import UUID4


router = APIRouter(
    tags=["submenu"],
    prefix="/api/v1/menus",
)


@router.get(
    "/{menu_id}/submenus",
    response_model=List[schemas.Submenu],
    name="Просмотр списка подменю",
)
def get_submenu_list(menu_id: UUID4, db: Session = Depends(get_db)):
    list_sub = submenu_crud.get_submenu_list(db, menu_id)
    return list_sub

@router.post(
    "/{menu_id}/submenus",
    response_model=schemas.Submenu,
    name='Создать подменю',
    status_code=201,
)
def add_submenu(menu_id: UUID4, data: schemas.SubmenuCreate, db: Session = Depends(get_db)):
    submenu = submenu_crud.create_submenu(db, menu_id, data)
    return submenu


@router.get(
    "/{menu_id}/submenus/{submenu_id}/",
    response_model=schemas.Submenu,
    name="Просмотр подменю по id",
)
def get_submenu(menu_id: UUID4, submenu_id: UUID4, db: Session = Depends(get_db)):
    try:
        submenu = submenu_crud.get_sub(db, menu_id, submenu_id)
    except:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenu


@router.patch(
    "/{menu_id}/submenus/{submenu_id}/",
    response_model=schemas.Submenu,
    name="Обновить подменю",
)
def update_submenu(menu_id: UUID4, submenu_id: UUID4, data: schemas.SubmenuUpdate, db: Session = Depends(get_db)):
    try:
        submenu = submenu_crud.get_sub(db, menu_id, submenu_id)
    except:
        raise HTTPException(status_code=404, detail="submenu not found")
    update_submenu = submenu_crud.update_submenu(db, menu_id, submenu_id, data)
    return update_submenu


@router.delete(
    "/{menu_id}/submenus/{submenu_id}/",
    name="Удаление подменю",
)
def delete_submenu(menu_id: UUID4, submenu_id: UUID4, db: Session = Depends(get_db)):
    submenu_crud.delete_submenu(db, menu_id, submenu_id)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "Submenu has been deleted"}
    )
