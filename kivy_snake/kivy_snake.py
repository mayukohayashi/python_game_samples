from kivy.metrics import sp
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy import properties as kp
from kivy.uix.widget import Widget
from collections import defaultdict
# from kivy.lang import Builder  # .kv使うため

## Windowsサイズ
SPRITE_SIZE = sp(20)
WIDTH = int(Window.width / SPRITE_SIZE)
HEIGHT = int(Window.height / SPRITE_SIZE)

## SNAKE自体の長さやスピード
LENGTH = 4
MOVESPEED = .1

### SNAKEの方向指示
UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'

direction_values = {UP: [0, 1],
                    DOWN: [0, -1],
                    RIGHT: [1, 0],
                    LEFT: [-1, 0]
                    }

## Sprite(画面)構築
class Sprite(Widget):
  coordinate = kp.ListProperty([0, 0])
  bgcolor = kp.ListProperty([0, 0, 0, 0])

SPRITES = defaultdict(lambda: Sprite())

## Snake
class Snake(App):
  sprite_size = kp.NumericProperty(SPRITE_SIZE)

  head = kp.ListProperty([0, 0])
  snake =  kp.ListProperty()
  length = kp.NumericProperty(LENGTH)

  food = kp.ListProperty([0, 0])

  direction = kp.StringProperty(RIGHT, options = (UP, DOWN, RIGHT, LEFT))

  def on_start(self):
    Clock.schedule_interval(self.move, MOVESPEED)

  def on_head(self, *args):
    self.snake = self.snake[-self.length:] + [self.head]

  def on_snake(self, *args):
    for index, coordinate in enumerate(self.snake):
      sprite = SPRITES[index]
      sprite.coordinate = coordinate
      if not sprite.parent:
        self.root.add_widget(sprite)

  def move(self, *args):
    new_head = [sum(x) for x in zip(self.head, direction_values[self.direction])]
    if not self.check_in_bounds(new_head):
      return  self.die()

    self.head = new_head

  ## 端にあたったら死ぬ
  def check_in_bounds(self, pos):
    return all(0 <= pos[x] < dim for x, dim in enumerate([WIDTH, HEIGHT]))


if __name__ == '__main__':
  Snake().run()
