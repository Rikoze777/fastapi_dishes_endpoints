from app.tasks.excel_utils import read_and_parse


filepath = "admin/menu.xlsx"


async def db_patch():
    menus, submenus, dishes = read_and_parse(filepath)
    menus
    submenus["submenus"] = submenus
    dishes["dishes"] = dishes
