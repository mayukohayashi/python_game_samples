from hashlib import new
from kivy.metrics import sp
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy import properties as kp
from kivy.uix.widget import Widget
from collections import defaultdict
from kivy.animation import Animation
from random import randint
# from kivy.lang import Builder  # わざわざいらんかった

## Windowsサイズ
SPRITE_SIZE = sp(20)
WIDTH = int(Window.width / SPRITE_SIZE)
HEIGHT = int(Window.height / SPRITE_SIZE)

## SNAKE自体の長さやスピード（挙動）
LENGTH = 4
MOVESPEED = .1
ALPHA = .5
### SNAKEの方向指示
UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'

## 方向軸どこに行くか指示
direction_values = {UP: [0, 1],
                    DOWN: [0, -1],
                    RIGHT: [1, 0],
                    LEFT: [-1, 0]
                    }

## 横軸なのか縦軸なのか
direction_group = {UP: 'vertical',
                   DOWN: 'vertical',
                   RIGHT: 'horizontal',
                   LEFT: 'horizontal'}

## 方向対応キー
direction_keys = {'w': UP,
                  's': DOWN,
                  'd': RIGHT,
                  'a': LEFT}

## Sprite(画面)構築
class Sprite(Widget):
  coordinate = kp.ListProperty([0, 0])
  bgcolor = kp.ListProperty([0, 0, 0, 0])

SPRITES = defaultdict(lambda: Sprite())

class Food(Sprite):
  pass

## Snake
class Snake(App):
  sprite_size = kp.NumericProperty(SPRITE_SIZE)

  head = kp.ListProperty([0, 0])
  snake =  kp.ListProperty()
  length = kp.NumericProperty(LENGTH)

  ### snakeがたべる餌
  food = kp.ListProperty([0, 0])
  food_sprite = kp.ObjectProperty(Food)

  direction = kp.StringProperty(RIGHT, options = (UP, DOWN, RIGHT, LEFT))
  buffer_direction = kp.StringProperty(RIGHT, options=(UP, DOWN, RIGHT, LEFT, ''))
  block_input = kp.BooleanProperty(False)

  ###　死んだ時の挙動用（snake.kv）
  alpha = kp.NumericProperty(0)

  def on_start(self):
    self.food_sprite = Food()
    self.food = self.new_food_location
    self.head = self.new_head_location
    Clock.schedule_interval(self.move, MOVESPEED)
    Window.bind(on_keyboard = self.key_handler)

  ## いつも違う場所に餌を出す
  def on_food(self, *args):
    self.food_sprite.coordinate = self.food
    if not self.food_sprite.parent:
      self.root.add_widget(self.food_sprite)


  ### キーコードをとる
  def key_handler(self, _, __, ___, key, *____):
    try:
      self.try_change_direction(direction_keys[key])

      ## keyプリントして確認　： print(direction_keys[key])
    except KeyError:
      pass

  def try_change_direction(self, new_direction):
    if direction_group[new_direction] != direction_group[self.direction]:
      if self.block_input:
        self.buffer_direction = new_direction
      else:
        self.direction = new_direction
        self.block_input = True

  def on_head(self, *args):
    self.snake = self.snake[-self.length:] + [self.head]

  def on_snake(self, *args):
    for index, coordinate in enumerate(self.snake):
      sprite = SPRITES[index]
      sprite.coordinate = coordinate
      if not sprite.parent:
        self.root.add_widget(sprite)

  @property
  def new_head_location(self):
    return [randint(2, dim - 2) for dim in [WIDTH, HEIGHT]]

  @property
  def new_food_location(self):
    while True:
      food = [randint(0, dim) for dim in [WIDTH, HEIGHT]]
      if food not in self.snake and food != self.food:
        return food

  def move(self, *args):
    self.block_input =False
    new_head = [sum(x) for x in zip(self.head, direction_values[self.direction])]
    if not self.check_in_bounds(new_head) or new_head in self.snake:
      return self.die()

    ### 蛇が餌をたべたとき
    if new_head == self.food:
      self.length += 1
      self.food = self.new_food_location
    if self.buffer_direction:
      self.try_change_direction(self.buffer_direction)
      self.buffer_direction = ''

    self.head = new_head

  ## 端にあたったら死ぬ
  def check_in_bounds(self, pos):
    return all(0 <= pos[x] < dim for x, dim in enumerate([WIDTH, HEIGHT]))

  def die(self):
    self.root.clear_widgets() ### 最初にクリア

    self.alpha = ALPHA
    Animation(alpha = 0, duration = MOVESPEED).start(self)
    self.snake.clear()
    self.length = LENGTH ### 死んだらもとの大きさ

    self.food = self.new_food_location
    self.head = self.new_head_location


if __name__ == '__main__':
  Snake().run()
