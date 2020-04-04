import numpy as np


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


def get_data_augmentation(array: np.ndarray, operation=lambda a: a):
    """
    获取数据扩充。
    Get data augmentation.
    :param array: 要扩充的数据。 the data to augment.
    :param operation: 数据扩充后要执行的操作。 What to do after data augmentation.
    :return: 已扩充的数据。 Augmented data.
    """

    # 单个数。 A single number.
    if array.shape == ():
        return np.zeros(8) + array

    return [operation(array),
            operation(np.rot90(array, 1)),
            operation(np.rot90(array, 2)),
            operation(np.rot90(array, 3)),
            operation(np.fliplr(array)),
            operation(np.rot90(np.fliplr(array), 1)),
            operation(np.rot90(np.fliplr(array), 2)),
            operation(np.rot90(np.fliplr(array), 3))]
