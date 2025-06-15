import pyxel

WINDOW_WIDTH = 160
WINDOW_HEIGHT = 120
RESOURCE_PATH = "/Users/macbook/goldenpotato/python/TerrainGeneration/v1.1/my_resource.pyxres"
APP_TITLE = "TerrainGeneration"
VERSION = "v1.1"
TERRAIN_SEED = 0

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

class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title = APP_TITLE)
        pyxel.load(RESOURCE_PATH)
        self.terrain = Terrain(TERRAIN_SEED)
        self.parameters_visible = None
        pyxel.run(self.update, self.draw)
    def update(self):
        self.parameters_visible = pyxel.btn(pyxel.KEY_P)
    def draw(self):
        pyxel.cls(0)
        self.draw_map()
        if(self.parameters_visible):self.show_parameters()
    def draw_map(self):
        for i in range(WINDOW_HEIGHT):
            for j in range(WINDOW_WIDTH):
                height = self.terrain.get_height(i, j)
                is_waterfront = False
                for d in range(4):
                    if(self.terrain.get_height(i + dy[d], j + dx[d]) < -0.2):is_waterfront = True
                if(height < -0.4):pyxel.pset(j, i, 5)
                elif(height < -0.2):pyxel.pset(j, i, 12)
                elif(is_waterfront):pyxel.pset(j, i, 15)
                elif(height < 0):pyxel.pset(j, i, 11)
                elif(height < 0.6):pyxel.pset(j, i, 3)
                else:pyxel.pset(j, i, 13)
    def show_parameters(self):
        pyxel.text(140, 110, VERSION, 0)

App()