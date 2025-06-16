import pyxel
import random

WINDOW_WIDTH = 160
WINDOW_HEIGHT = 120
RESOURCE_PATH = "/Users/macbook/goldenpotato/python/TerrainGeneration/v1.1/my_resource.pyxres"
APP_TITLE = "TerrainGeneration"
VERSION = "v1.1"
TERRAIN_SEED = random.randint(1, 1e6)

dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]

#pyxel edit "/Users/macbook/goldenpotato/python/TerrainGeneration/v1.1/my_resource.pyxres"

class Terrain:
    def __init__(self, seed:int):
        self.seed = seed
        pyxel.nseed(seed)
    def get_height(self, y:int, x:int):
        height = pyxel.noise(x / 32, y / 32)
        height += pyxel.noise(x / 32, y / 32) / 2
        height += pyxel.noise(x / 16, y / 16) / 4
        height += pyxel.noise(x / 8, y / 8) / 8
        return height
    def get_temperature(self, y:int, x:int):
        temperature = pyxel.noise(x / 128, y / 128, 1)
        temperature += pyxel.noise(x / 64, y / 64, 1) / 2
        temperature += pyxel.noise(x / 32, y / 32, 1) / 4
        temperature -= self.get_height(y, x) / 4
        return temperature
    def get_humidity(self, y:int, x:int):
        humidity = pyxel.noise(x / 128, y / 128, 2)
        humidity += pyxel.noise(x / 64, y / 64, 2) / 2
        humidity += pyxel.noise(x / 32, y / 32, 2) / 4
        return humidity

class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title = APP_TITLE)
        pyxel.load(RESOURCE_PATH)
        self.terrain = Terrain(TERRAIN_SEED)
        self.parameters_visible = False
        pyxel.run(self.update, self.draw)
    def update(self):
        if(pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)):self.parameters_visible = not self.parameters_visible
    def draw(self):
        pyxel.cls(0)
        self.draw_map()
        if(self.parameters_visible):self.show_parameters()
    def draw_map(self):
        for i in range(WINDOW_HEIGHT):
            for j in range(WINDOW_WIDTH):
                height = self.terrain.get_height(i, j)
                temperature = self.terrain.get_temperature(i, j)
                humidity = self.terrain.get_humidity(i, j)
                is_waterfront = False
                for d in range(4):
                    if(self.terrain.get_height(i + dy[d], j + dx[d]) < -0.2):is_waterfront = True
                if(height < -0.4):pyxel.pset(j, i, 5)
                elif(height < -0.2):pyxel.pset(j, i, 12)
                elif(is_waterfront):pyxel.pset(j, i, 15)
                elif(height < 0.6):
                    if(humidity < -0.4 and temperature > 0):pyxel.pset(j, i, 10) #砂漠
                    elif(temperature > 0.2 and humidity < 0):pyxel.pset(j, i, 9) #サバンナ
                    elif(temperature < -0.4 and humidity > 0):pyxel.pset(j, i, 6) #雪原
                    elif(height < 0):pyxel.pset(j, i, 11) #草原
                    else:pyxel.pset(j, i, 3) #森林
                else:
                    if(temperature < -0.4 and humidity > 0):pyxel.pset(j, i, 7) #雪山
                    elif(humidity < -0.4 and temperature > 0):pyxel.pset(j, i, 15) #砂山
                    else:pyxel.pset(j, i, 13) #岩山
    def show_parameters(self):
        pyxel.text(5, 5, str(TERRAIN_SEED), 0)
        pyxel.text(140, 110, VERSION, 0)

App()