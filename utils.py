import re

from typing import List, Iterator


def get_data_from_file(file_name: str) -> Iterator[str]:
    with open(file_name, 'r', encoding='utf-8') as f:
        data_list: List[str] = f.readlines()
        for item in data_list:
            yield item
    #     data_list = list(map(lambda row: row.strip(), f))
    # return data_list


def filter_query(param: str, data_list: list) -> list:
    res = filter(lambda row: param in row, data_list)
    return list(res)


def map_query(param: str, data_list: list) -> list:
    column_number = int(param)
    res = map(lambda row: row.split(' ')[column_number], data_list)
    return list(res)


def unique_query(data_list: list, *args, **kwargs) -> list:
    list_of_unique_rows = []
    unique_rows = set()

    for row in data_list:
        if row in unique_rows:
            continue
        else:
            list_of_unique_rows.append(row)
            unique_rows.add(row)

    return list_of_unique_rows


def sort_query(param: str, data_list: list) -> list:
    reverse = False if param == 'asc' else True
    res = sorted(data_list, reverse=reverse, key=lambda row: row)
    return list(res)


def limit_query(param: str, data_list: list) -> list:
    rows_count = int(param)
    return data_list[:rows_count]


def regex_query(param: str, data_list: list) -> list:
    res_list = []
    for item in data_list:
        regex = re.compile(param)
        m = regex.findall(item)
        if m:
            res_list.append(item)
    return res_list
