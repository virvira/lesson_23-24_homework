import os
from typing import Union, Dict, Optional, Any, Iterator, List

from utils import get_data_from_file, filter_query, map_query, unique_query, sort_query, limit_query, regex_query

from flask import Flask, request, jsonify, Response

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=["POST"])
def perform_query() -> Union[Response, str]:
    req_json: Union[Dict[str, str], Any] = request.json
    valid_commands: Dict[str, Any] = {
        'filter': filter_query,
        'map': map_query,
        'unique': unique_query,
        'sort': sort_query,
        'limit': limit_query,
        'regex': regex_query
    }
    try:
        file_name: Optional[str] = req_json['file_name']
        cmd1: Optional[str] = req_json['cmd1']
        value1: Optional[str] = req_json['value1']
        cmd2: Optional[str] = req_json['cmd2']
        value2: Optional[str] = req_json['value2']
    except Exception as e:
        return Response(f"Поле {e} не найдено", status=400)

    file_path: str = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return Response(f"Файл {file_name} не найден", status=400)

    data: Iterator[str] = get_data_from_file(file_path)
    res: List[str] = []

    if cmd1 and cmd2 in valid_commands:
        res_cmd1 = valid_commands[cmd1](param=value1, data_list=data)
        res = valid_commands[cmd2](param=value2, data_list=res_cmd1)

    if res is not None:
        return jsonify(res)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
