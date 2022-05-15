from flask import Flask, jsonify, make_response, render_template, redirect, request
from algorithm.algorithm import *
from bot.bot import Database, DATABASE_PATH
import requests
from threading import Timer
import api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

GAME_START = False
game = Game('test.txt')
data = Database(DATABASE_PATH)
code = None
LEN_PINCODE = 6


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/")
def index():
    if GAME_START:
        redirect('/game')
    else:
        redirect('/waiting')


@app.route("/game")
def main_game():
    return render_template('*.html', game=game)


@app.route("/waiting", methods=['POST', 'GET'])
def waiting():
    global GAME_START
    # это окно ожидания и после нажатия кнопки старт игра начинается
    # есть проблема, она заключается в том, что кнопку старт может нажать кто угодно, если она в окне ожидания у всех
    # если она будет в другом месте то где????
    if GAME_START:
        redirect('/game')
    if request.method == 'GET':
        return render_template('*.html', game=game, pincode=code)
    elif request.method == 'POST':
        GAME_START = True
        redirect('/game')


@app.route("/pincode")
def pincode():
    return render_template('*.html', pincode=code)


def create_team(team_name):
    game.add_crew(team_name)


def generate_code():
    global code
    req = f'https://www.random.org/strings/?num=1&len={LEN_PINCODE}&digits=on&upperalpha=on&format=plain&rnd=new'
    code = requests.get(req).text.strip()
    timer = Timer(60 * 60, generate_code)  # раз в час будет меняться код
    timer.start()


def send_answer(team_name, task_category, task_number, answer):
    # Я не увидел у Димы функцию приема ответов, поэтому пока что оставлю это так
    # После токо, как человек дал ответ, Дима должен вызвать эту функцию
    pr = game.answer(team_name, task_category, task_number, answer)
    if pr == WRONG_ANSWER:
        return False
    return True


def main():
    global code, data
    app.register_blueprint(api.blueprint)
    generate_code()
    data.create_game(code)
    app.run()


if __name__ == '__main__':
    main()
