from kivy.app import App
from kivy.uix.label import Label ## ボタンとかUI系のやつ


class IntroKivy(App):
    def build(self): ### buildクラスはアプリの初期化をしてくれる
        return Label(text="Hello, World!")

## このファイルがメインプログラムとして実行されたらRunしろ
if __name__ == "__main__":
    IntroKivy().run()
