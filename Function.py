
def coordinates_set(width, height):
    """
    根据宽和高生成一个坐标元组集合。
    Get a set of coordinate tuples with width and height.
    :param width: 宽度。 width.
    :param height: 高度。 height.
    :return: <set (x_axis, y_axis)>
    """
    s = set()
    for i in range(width):
        for j in range(height):
            s.add((i, j))
    return s
