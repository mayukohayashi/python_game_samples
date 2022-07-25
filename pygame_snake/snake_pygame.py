from importlib.util import set_loader
import pygame
import sys
import random

# TODO: mainとゲームに分けた方がよいかも。

# Snakeクラス
class Snake():

  ## 初期化処理
  def __init__(self):
    self.length = 1
    self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
    self.direction = random.choice([up, down, left, right])
    self.color = (251, 212, 0) ###　TODO:4つめに暇だったらTransparencyいれたい
    self.score = 0

  ## 頭の位置を示す処理
  def get_head_position(self):
    return self.positions[0]

  ## 方向転換する処理
  def turn(self, point):
    if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
      return
    else:
      self.direction = point

  ## 動く処理
  def move(self):
    cur = self.get_head_position()
    x, y = self.direction
    new = (((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
    if len(self.positions) > 2 and new in self.positions[2:]:
      self.reset()
    else:
      self.positions.insert(0, new)
      if len(self.positions) > self.length:
        self.positions.pop()

  ## Gameover時蛇の大きさ（長さ）リセット
  def reset(self):
    self.length = 1
    self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
    self.direction = random.choice([up, down, left, right])
    self.score = 0

  ## 蛇の姿を描く処理
  def draw(self, surface):
    for p in self.positions:
      r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
      pygame.draw.rect(surface, self.color, r)
      pygame.draw.rect(surface, (93, 216, 218), r, 1)

  ## 上下左右キーとスネークの動きを結びつける処理
  def handle_keys(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_UP:
              self.turn(up)
          elif event.key == pygame.K_DOWN:
              self.turn(down)
          elif event.key == pygame.K_LEFT:
              self.turn(left)
          elif event.key == pygame.K_RIGHT:
              self.turn(right)

# Food(蛇が食べるブロック)クラス
class Food():

  ## 初期化処理
  def __init__(self):
    self.position = (0, 0)
    self.color = (44, 51, 51)
    self.randomize_position()


  ## 餌の位置をランダムスポーンさせる
  def randomize_position(self):
    self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE) ### drawGRIDで480指定

  ## 餌を描写する処理
  def draw(self, surface):
    r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
    pygame.draw.rect(surface, self.color, r) ### r = 餌が表示される範囲

## 盤面を描く処理
def drawGrid(surface):
    ### rとrr2種類のパターン⇒色の違うマス目が交互に描画される（みやすさのため）
    for y in range(0, int(GRID_HEIGHT)):
      for x in range(0, int(GRID_WIDTH)):
        if (x + y) % 2 == 0:
          r = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
          pygame.draw.rect(surface, (73, 148, 145), r)
        else:
          rr = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
          pygame.draw.rect(surface, (163, 222, 201), rr)


## MAIN処理

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRIDSIZE = 20
GRID_WIDTH = SCREEN_HEIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)


def main():
  pygame.init()
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
  surface = pygame.Surface(screen.get_size())
  surface = surface.convert()

  drawGrid(surface)
  snake = Snake()
  food = Food()

  myfont = pygame.font.SysFont("monospace", 16)
  while (True):
      clock.tick(10)
      snake.handle_keys()
      drawGrid(surface)
      snake.move()

      ### スネークの頭の位置が餌の位置に一致したとき（スネークが餌を食べたとき）体長＆スコア＋１ずつ
      if snake.get_head_position() == food.position:
          snake.length += 1
          snake.score += 1
          food.randomize_position()
      snake.draw(surface)
      food.draw(surface)
      screen.blit(surface, (0, 0))
      text = myfont.render("Score {0}".format(snake.score), 1, (0, 0, 0))
      screen.blit(text, (5, 10))
      pygame.display.update() ### 描画内容を画面に反映


main()
