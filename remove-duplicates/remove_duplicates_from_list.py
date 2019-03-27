# -*- coding: utf-8 -*-

list_with_duplicates = [
    {"foo": 42, "bar": "bacon", "age": 100, "need_food": True},
    {"foo": 42, "bar": "bacon", "age": 100, "need_food": True},
    {"foo": 20, "bar": "bacon", "age": 50, "need_food": True}
]


def form1_basic(items):
    """
    Removes duplicate items using a more basic method.
    :return: list with unique items.
    """
    unique_list = list()
    for i in range(len(items)):
        if items[i] not in items[i + 1:]:
            unique_list.append(items[i])

    return unique_list


def form2_list_comprehension(items):
    """
    Remove duplicates using list comprehension.
    :return: list with unique items.
    """
    return [i for n, i in enumerate(items) if i not in items[n + 1:]]


if __name__ == '__main__':
    print("#### Method 1.")
    unique_1 = form1_basic(list_with_duplicates)
    for u1 in unique_1:
        print(u1)

    print("#"*100)

    print("#### Method 2.")
    unique_2 = form2_list_comprehension(list_with_duplicates)
    for u2 in unique_2:
        print(u2)
