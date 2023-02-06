from datetime import datetime
import os

from flask import abort, redirect, render_template, jsonify
from menuapp import app


class Menu:
    def __init__(self, id: int, name: str, price: int, image_source: str):
        self.id = id
        self.name = name
        self.price = price
        self.image_source = image_source


menus = {}

menu_chococone = Menu(0, '초코콘', 900, 'menu_chococone.png')
menus[0] = menu_chococone

menu_burger = Menu(90, '시그니처 버거', 7500, 'menu_burger.png')
menus[90] = menu_burger

menu_chicken = Menu(77, '치킨', 6000, 'menu_chicken.png')
menus[77] = menu_chicken

menu_softcone = Menu(721, '소프트콘', 600, 'menu_softcone.png')
menus[721] = menu_softcone


def write_log(url):
    now_str = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
    new_line = f'{now_str}\t{url}\n'

    current_filepath = __file__
    current_directory = os.path.dirname(current_filepath)
    runpy_directory = os.path.join(current_directory, '..')
    log_path = os.path.join(runpy_directory, 'log.txt')

    # with open(log_path, 'a') as f:
    #     f.write(new_line)

    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            current_log = f.read()
            new_log = current_log + new_line
    else:
        new_log = new_line

    with open(log_path, 'w') as f:
        f.write(new_log)


@app.route('/')
def endpoint_index():
    write_log('/')
    return redirect('/menus')


@app.route('/menus')
def endpoint_menus():
    write_log('/menus')
    # TODO : 메뉴 리스트 가져와서 뿌리기
    # menulist_html = ''
    #
    # for menu_key in menus.keys():
    #     menu_name = menus[menu_key].name
    #     menulist_html += f'<a href="/menus/{menu_key}">{menu_name}</a><BR/>'
    #
    # return render_template('menu_list.html', menulist_html=menulist_html)

    return render_template('menu_list.html', menus=menus.values())
    return jsonify()


# 메뉴 정보 가져와서 뿌리기
@app.route('/menus/<int:menu_id>')
def endpoint_info(menu_id: int):
    write_log(f'/menus/{menu_id}')
    if menu_id not in menus:
        return abort(404)

    return render_template('menu_info.html', menu=menus[menu_id])


# 새 메뉴 등록
@app.route('/menus/add/<int:menu_id>/<menu_name>/<int:menu_price>')
def endpoint_add_menu(menu_id: int, menu_name: str, menu_price: int):
    write_log(f'/menus/add/{menu_id}/{menu_name}/{menu_price}')

    if menu_id in menus:
        return '중복된 메뉴입니다'

    new_menu = Menu(menu_id, menu_name, menu_price, 'menu_burger.png')
    menus[menu_id] = new_menu

    return redirect('/menus')
