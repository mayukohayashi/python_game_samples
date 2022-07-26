from kivy.metrics import sp
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy import properties as kp
from kivy.lang import Builder

## Windowsサイズ
SPRITE_SIZE = sp(40)
WIDTH = int(Window.width / SPRITE_SIZE)
HEIGHT = int(Window.height / SPRITE_SIZE)

## SNAKE自体の長さやスピード
LENGTH = 4
SPEED = .1

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

## Snake
class Snake(App):

  head = kp.ListProperty([0, 0])
  snake =  kp.ListProperty()

  food = kp.ListProperty([0, 0])

  direction = kp.StringProperty(RIGHT, options = (UP, DOWN, RIGHT, LEFT))

  def on_start(self):
    Clock.schedule_interval(self.move, MOVESPEED)

  def on_head(self, *args):
    self.snake.append(self.head)

    def move(self, *args):
      new_head = [sum(x) for x in zip(self.head, direction_values[self.direction])]
      self.head = new_head


if __name__ == '__main__':
  Snake().run()
