from flask import jsonify, Response, abort, request, send_file
import json, os

from PIL import image

from apiapp import app



class Menu:
    def __init__(self, id: int, name: str, price: int, image_source: str):
        self.id = id
        self.name = name
        self.price = price
        self.image_source = image_source

    def to_dict(self):
        return {'id': self.id, 'name': self.name,
                'price': self.price, 'image_source': self.image_source}


menus = {}

menu_chococone = Menu(0, '초코콘', 900, 'menu_chococone.png')
menus[0] = menu_chococone

menu_burger = Menu(90, '시그니처 버거', 7500, 'menu_burger.png')
menus[90] = menu_burger

menu_chicken = Menu(77, '치킨', 6000, 'menu_chicken.png')
menus[77] = menu_chicken

menu_softcone = Menu(721, '소프트콘', 600, 'menu_softcone.png')
menus[721] = menu_softcone


@app.route('/')
@app.route('/menus')
def end_index():
    menu_dicts = []
    for menu in menus.values():
        menu_dicts.append(menu.to_dict())

    response_content = json.dumps(menu_dicts, ensure_ascii=False)
    response = Response(response=response_content,
                        status=200,
                        mimetype="application/json")
    return response
    # return jsonify(menu_dicts)


# 메뉴 정보 가져와서 뿌리기
@app.route('/menus/<int:menu_id>')
def end_info(menu_id: int):
    if menu_id not in menus:
        return abort(404)

    response_content = json.dumps(menus[menu_id].to_dict(), ensure_ascii=False)
    response = Response(response=response_content,
                        status=200,
                        mimetype="application/json")

    return response


@app.route('/menu_info', methods=['POST'])
def end_info_post():
    post_dict = request.form.to_dict()

    if 'menu_id' not in post_dict:
        return abort(400)

    menu_id: str = post_dict['menu_id']

    if not menu_id.isnumeric():
        return abort(400)
    menu_id = int(menu_id)

    if menu_id not in menus:
        return abort(404)

    response_content = json.dumps(menus[menu_id].to_dict(), ensure_ascii=False)
    response = Response(response=response_content,
                        status=200,
                        mimetype="application/json")

    return response

@app.route('/menu_add', methods=['POST'])
def end_menu_add():
    post_dict = request.form.to_dict()

    try:
        menu_id = int(post_dict['id'])
        menu_name = post_dict['name']
        menu_price = int(post_dict['price'])

        new_menu = Menu(menu_id, menu_name, menu_price, 'menu_chococone.png')
        menus[menu_id] = new_menu

        return 'ok'

    except Exception:
        return 'something wrong...'


@app.route('/image/<filename>')
def end_image(filename: str):
    current_dirname = os.path.dirname(__file__)
    image_path = os.path.join(current_dirname,'menu_images', filename)

    if os.path.exists(image_path):
        return send_file(image_path)
    else:
        return abort(404)