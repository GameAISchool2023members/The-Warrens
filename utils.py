from enum import Enum

def in_nested_list(elem, nested_list):
    for sublist in nested_list:
        for item in sublist:
            if elem == item:
                return True
    return False


def fetch_face_expression():
    pass