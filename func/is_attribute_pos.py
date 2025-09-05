def is_attribute_pos(atr, attributes):
    pos = attributes.find(atr)
    index = pos + len(atr)
    while attributes[index] != "\0":
        if attributes[index] == "-":
            return False
        index += 1
    return True
