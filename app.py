from flask import Flask, jsonify, render_template, request

import guessers

app = Flask(__name__)
app.secret_key = '90f5bbad727de239db9ed3fc0bd633776ee6ca59e35e02c6'
user = guessers.User()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html",
                           user_history=user.history,
                           guessers=user.guessers_json,
                           guess_min=guessers.GUESS_MIN,
                           guess_max=guessers.GUESS_MAX,
                           )


@app.route('/start', methods=['GET'])
def start():
    return jsonify(user_history=user.history,
                   guessers=user.guessers_json,
                   )


@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        result = request.form.get('answer')
        user.set_selected_number(int(result))
        return jsonify(user_history=user.history,
                       guessers=user.guessers_json,
                       )


if __name__ == '__main__':
    app.run()
