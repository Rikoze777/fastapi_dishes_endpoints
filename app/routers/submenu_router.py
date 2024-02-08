from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from typing import List
from app.schemas import schemas
from fastapi.responses import JSONResponse
from pydantic import UUID4
from app.services.submenu_service import SubmenuService


router = APIRouter(
    tags=["submenu"],
    prefix="/api/v1/menus/{menu_id}",
)


@router.get(
    "/submenus",
    response_model=List[schemas.Submenu],
    name="Просмотр списка подменю",
)
async def get_submenu_list(menu_id: UUID4, service: SubmenuService = Depends()):
    list_sub = await service.get_submenu_list(menu_id)
    return list_sub

@router.post(
    "/submenus",
    response_model=schemas.Submenu,
    name='Создать подменю',
    status_code=201,
)
async def add_submenu(menu_id: UUID4, data: schemas.SubmenuCreate, background_tasks: BackgroundTasks, service: SubmenuService = Depends()):
    submenu = await service.create(menu_id, data, background_tasks)
    return submenu


@router.get(
    "/submenus/{submenu_id}/",
    response_model=schemas.Submenu,
    name="Просмотр подменю по id",
)
async def get_submenu(menu_id: UUID4, submenu_id: UUID4, service: SubmenuService = Depends()):
    try:
        submenu = await service.get(menu_id, submenu_id)
    except:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenu


@router.patch(
    "/submenus/{submenu_id}/",
    response_model=schemas.Submenu,
    name="Обновить подменю",
)
async def update_submenu(menu_id: UUID4, submenu_id: UUID4, data: schemas.SubmenuUpdate, background_tasks: BackgroundTasks, service: SubmenuService = Depends()):
    try:
        submenu = await service.get(menu_id, submenu_id)
    except:
        raise HTTPException(status_code=404, detail="submenu not found")
    update_submenu = await service.update(menu_id, submenu_id, data, background_tasks)
    return update_submenu


@router.delete(
    "/submenus/{submenu_id}/",
    name="Удаление подменю",
)
async def delete_submenu(menu_id: UUID4, submenu_id: UUID4, background_tasks: BackgroundTasks, service: SubmenuService = Depends()):
    await service.delete(menu_id, submenu_id, background_tasks)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "Submenu has been deleted"}
    )
