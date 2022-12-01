import os
from utils import get_data_from_file, filter_query, map_query, unique_query, sort_query, limit_query

from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=["POST"])
def perform_query():
    req_json = request.json
    valid_commands = {
        'filter': filter_query,
        'map': map_query,
        'unique': unique_query,
        'sort': sort_query,
        'limit': limit_query
    }
    try:
        file_name = req_json['file_name']
        cmd1 = req_json['cmd1']
        value1 = req_json['value1']
        cmd2 = req_json['cmd2']
        value2 = req_json['value2']
    except Exception as e:
        return {"error": f"Поле {e} не найдено"}, 400

    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return {"error": f"Файл {file_name} не найден"}, 400

    data = get_data_from_file(file_path)
    res = []

    if cmd1 and cmd2 in valid_commands:
        res_cmd1 = valid_commands[cmd1](value1, data)
        res = valid_commands[cmd2](value2, res_cmd1)

    if res is not None:
        return jsonify(res)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
