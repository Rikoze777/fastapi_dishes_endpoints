import os
import pandas as pd

filepath = os.path.join(os.getcwd(), "admin/Menu.xlsx")
print(filepath)


def parse_excel(frame):
    menu_data = []
    submenu_data = []
    dish_data = []

    for index, row in frame.iterrows():
        if not pd.isna(row[frame.columns[0]]):
            menu_data.append(
                {
                    "id": int(row[frame.columns[0]]),
                    "title": row[frame.columns[1]],
                    "description": row[frame.columns[2]],
                }
            )
            print(menu_data)
        if not pd.isna(row[frame.columns[1]]):
            submenu_data.append(
                {
                    "id": int(row[frame.columns[1]]),
                    "menu_id": menu_data["id"],
                    "title": row[frame.columns[2]],
                    "description": row[frame.columns[3]],
                    "menu_number": menu_data["id"],
                }
            )
            print(submenu_data)
        if not pd.isna(row[frame.columns[2]]):
            dish_data.append(
                {
                    "id": int(row[frame.columns[2]]),
                    "submenu_id": submenu_data["id"],
                    "menu_id": menu_data["id"],
                    "title": row[frame.columns[3]],
                    "description": row[frame.columns[4]],
                    "submenu_number": submenu_data["id"],
                    "price": row[frame.columns[5]],
                    "discount": row[frame.columns[6]],
                }
            )
            print(dish_data)
    return menu_data, submenu_data, dish_data


def read_and_parse(filepath):
    frame = pd.read_excel(filepath, header=None)
    menus, submenus, dishes = parse_excel(frame)
    return menus, submenus, dishes
