from flask import render_template, abort

import json
import requests

from webapp import app

API_HOST = 'http://0.0.0.0:1026'


class Menu:
    def __init__(self, menu_dict):
        self.id = menu_dict['id']
        self.name = menu_dict['name']
        self.price = menu_dict['price']
        self.image_source = menu_dict['image_source']


@app.route('/')
@app.route('/menus')
def end_menus():
    api_call_url = f'{API_HOST}/menus'

    response = requests.get(api_call_url)
    assert response.status_code // 100 == 2

    menu_dicts = json.loads(response.content)

    menus = {}
    for menu_dict in menu_dicts:
        menu = Menu(menu_dict)
        menus[menu.id] = menu

    return render_template('menu_list.html', menus=menus.values())


# 메뉴 정보 가져와서 뿌리기
@app.route('/menus/<int:menu_id>')
def end_info(menu_id: int):
    api_call_url = f'{API_HOST}/menus/{menu_id}'

    response = requests.get(api_call_url)

    if response.status_code // 100 != 2:
        return '그런 메뉴 없음'

    menu_info = json.loads(response.content)
    return render_template('menu_info.html', menu=menu_info)
