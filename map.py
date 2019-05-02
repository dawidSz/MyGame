import numpy, cv2, os


class Map:
    def __init__(self):
        self.dirplace = os.path.abspath(__file__).strip('map.py')
        self.boolean, self.array = self.read_img()

    def read_img(self):
        map = cv2.imread(self.dirplace + 'map_graphics\white_mov_map.jpg')
        map = cv2.resize(map, (4800, 3408))
        map = cv2.cvtColor(map, cv2.COLOR_BGR2GRAY)
        map_array = numpy.asarray(map)
        map = map_array < 250
        return map, map_array


if __name__ == '__main__':
    map = Map()
    dup = map.boolean[100][100]
    print(dup)