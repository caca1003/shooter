from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy import platform
class MainScreen(MDScreen):
    ...


class GameScreen(MDScreen):
    ...


class ShooterApp(MDApp):
     def build(self):
        Builder.load_file("shooter.kv")
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="Purple"
        sm=MDScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(GameScreen(name="game"))
        return sm
if platform!="android":
    Window.size = (400,750)
    Window.top=50
    Window.left=900

     

ShooterApp().run()






















