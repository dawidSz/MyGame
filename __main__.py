import time, cv2, random, threading, socket, sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial
from game_package import map, player


class Game(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.dirplace = os.path.abspath(__file__).strip('__main__.py')
        self.height = height
        self.width = width

        self.world = map.Map()
        self.players = []
        self.player_icns = []

        self.initWindow()

    def initWindow(self):
        self.initScene()

        Exitbtn = QPushButton('Exit', self)
        Exitbtn.setFixedSize(180, 20)
        Exitbtn.move(self.width - 190, self.height - 30)
        Exitbtn.clicked.connect(self.close)

        self.showFullScreen()

    def initScene(self):
        self.scene = QGraphicsScene()
        self.scene_width = 0.85 * self.width
        self.scene_height = self.height

        self.cut_start_X = 1500
        self.cut_start_Y = 1500
        self.map = QPixmap(self.dirplace + 'map_graphics/map.jpg')
        self.map_to_show = self.map.copy(self.cut_start_X, self.cut_start_Y, self.scene_width, self.height)
        self.map_to_show = self.scene.addPixmap(self.map_to_show)

        self.players.append(player.Player())
        self.players[0].x = int(self.scene_width / 2) + self.cut_start_X
        self.players[0].y = int(self.scene_height / 2) + self.cut_start_Y

        player_icn = QPixmap(self.dirplace + 'players_icons/left3.png')
        self.player_icns.append(player_icn.copy())
        self.player_icns[0] = self.scene.addPixmap(self.player_icns[0])
        self.player_icns[0].setPos(self.scene_width / 2, self.scene_height / 2)

        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setGeometry(0, 0, self.scene_width, self.scene_height)

        self.mainTimer = QTimer(self)
        self.mainTimer.start()
        self.mainTimer.setInterval(10)
        self.mainTimer.timeout.connect(self.worldCycle)

    def worldCycle(self):
        self.set_orientation(self.players[0], self.player_icns[0])
        self.cut_map()

    def keyPressEvent(self, event):
        temp_pos_y = self.players[0].y
        temp_pos_x = self.players[0].x

        if event.key() == Qt.Key_W:
            temp_pos_y -= 10
            if self.mov_possible(temp_pos_x, temp_pos_y):
                self.cut_start_Y -= 10
                self.players[0].y -= 10
                self.players[0].orient = 'up'
                self.players[0].mov_counter += 1
        elif event.key() == Qt.Key_S:
            temp_pos_y += 10
            if self.mov_possible(temp_pos_x, temp_pos_y):
                self.cut_start_Y += 10
                self.players[0].y += 10
                self.players[0].orient = 'down'
                self.players[0].mov_counter += 1
        elif event.key() == Qt.Key_A:
            temp_pos_x -= 10
            if self.mov_possible(temp_pos_x, temp_pos_y):
                self.cut_start_X -= 10
                self.players[0].x -= 10
                self.players[0].orient = 'left'
                self.players[0].mov_counter += 1
        elif event.key() == Qt.Key_D:
            temp_pos_x += 10
            if self.mov_possible(temp_pos_x, temp_pos_y):
                self.cut_start_X += 10
                self.players[0].x += 10
                self.players[0].orient = 'right'
                self.players[0].mov_counter += 1

    def cut_map(self):
        decenter_x_up = False
        decenter_y_up = False
        decenter_x_down = False
        decenter_y_down = False
        if self.players[0].x <= self.scene_width / 2:
            cut_X = 0
            decenter_x_up = True
        elif self.players[0].x >= 4800 - self.scene_width / 2:
            cut_X = 4800 - self.scene_width
            decenter_x_down = True
        else:
            cut_X = self.cut_start_X

        if self.players[0].y <= self.height / 2:
            cut_Y = 0
            decenter_y_up = True
        elif self.players[0].y >= 3408 - self.height / 2:
            cut_Y = 3408 - self.height
            decenter_y_down = True
        else:
            cut_Y = self.cut_start_Y

        temp = self.map.copy(cut_X, cut_Y, self.scene_width, self.scene_height)
        self.map_to_show.setPixmap(temp)

        if decenter_x_up and decenter_y_up:
            self.player_icns[0].setPos(self.players[0].x, self.players[0].y)
        elif decenter_x_down and decenter_y_up:
            self.player_icns[0].setPos(self.players[0].x - cut_X, self.players[0].y)
        elif decenter_x_up and decenter_y_down:
            self.player_icns[0].setPos(self.players[0].x, self.players[0].y - cut_Y)
        elif decenter_x_down and decenter_y_down:
            self.player_icns[0].setPos(self.players[0].x - cut_X, self.players[0].y - cut_Y)
        elif decenter_x_up:
            self.player_icns[0].setPos(self.players[0].x, self.scene_height / 2)
        elif decenter_y_up:
            self.player_icns[0].setPos(self.scene_width / 2, self.players[0].y)
        elif decenter_x_down:
            self.player_icns[0].setPos(self.players[0].x - cut_X, self.scene_height / 2)
        elif decenter_y_down:
            self.player_icns[0].setPos(self.scene_width / 2, self.players[0].y - cut_Y)

        self.cut_start_X = cut_X
        self.cut_start_Y = cut_Y

    def set_orientation(self, obj, obj_icn):
        if obj.mov_counter > 3: obj.mov_counter = 1
        if obj.orient == 'up':
            obj_icn.setPixmap(QPixmap(self.dirplace + 'players_icons/up{}.png'.format(obj.mov_counter)))
        elif obj.orient == 'down':
            obj_icn.setPixmap(QPixmap(self.dirplace + 'players_icons/down{}.png'.format(obj.mov_counter)))
        elif obj.orient == 'right':
            obj_icn.setPixmap(QPixmap(self.dirplace + 'players_icons/right{}.png'.format(obj.mov_counter)))
        elif obj.orient == 'left':
            obj_icn.setPixmap(QPixmap(self.dirplace + 'players_icons/left{}.png'.format(obj.mov_counter)))

    def mov_possible(self, x, y):
        if self.world.boolean[y][x] and self.world.boolean[y+30][x+20] and self.world.boolean[y+30][x] and self.world.boolean[y][x+20] :
            return True
        else:
            return False

    def phone_control(self):
        self.host = '192.168.8.100'
        self.port = 50001
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind((self.host, self.port))
        self.reciv_thread = threading.Thread(target=self.imu_reciv)
        self.reciv_thread.start()

    def imu_reciv(self):
        while True:
            try:
                message, address = self.s.recvfrom(8192)
                message = str(message)[106:128]
                self.horiz = float(message[0:6])
                self.vert = float(message[7:13])
                self.phone_steering_wheel()
            except:
                pass
            else:
                continue

    def phone_steering_wheel(self):
        temp_pos_y = self.players[0].y
        temp_pos_x = self.players[0].x

        if abs(self.vert) > 5 and self.vert < 0:
            temp_pos_y -= 5
            if self.mov_possible(temp_pos_x, temp_pos_y):
                self.cut_start_Y -= 10
                self.players[0].y -=10
                self.players[0].mov_counter += 1
                self.players[0].orient = 'up'
        elif abs(self.vert) > 5 and self.vert > 0:
            temp_pos_y += 5
            if self.mov_possible(temp_pos_x, temp_pos_y):
                self.cut_start_Y += 10
                self.players[0].y +=10
                self.players[0].mov_counter += 1
                self.players[0].orient = 'down'

        if abs(self.horiz) > 5 and self.horiz > 0:
            temp_pos_x -=5
            if self.mov_possible(temp_pos_x, temp_pos_y):
                self.cut_start_X -= 10
                self.players[0].x -=10
                self.players[0].mov_counter += 1
                self.players[0].orient = 'left'
        elif abs(self.horiz) > 5 and self.horiz < 0:
            temp_pos_x += 5
            if self.mov_possible(temp_pos_x, temp_pos_y):
                self.cut_start_X += 10
                self.players[0].x +=10
                self.players[0].mov_counter += 1
                self.players[0].orient = 'right'



if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    window = Game(width, height)
    sys.exit(app.exec())
