def in_nested_list(elem, nested_list):
    for sublist in nested_list:
        for item in sublist:
            if elem == item:
                return True
    return False