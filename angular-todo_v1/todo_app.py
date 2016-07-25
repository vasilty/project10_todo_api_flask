import json
import requests
from flask import Flask, g, jsonify, render_template, redirect

from auth import auth
import models
from resources.todos import todos_api
from resources.users import users_api


app = Flask(__name__)
app.register_blueprint(todos_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')
app.secret_key = 'AHD%#274%dfna2$!l95fDBkrgnkr873^%@fk'


@app.route('/')
def my_todos():
    # return app.send_static_file('index.html')
    return render_template('index.html')


@app.route('/api/v1/users/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
    models.initialize()
    app.run(debug=True, port=8080)
