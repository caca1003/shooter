from kivy.uix.image import Image
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy import platform
from kivy.clock import Clock
from kivy.metrics import sp, dp
DIR_UP=1
DIP_DOWN=-1
FPS=60
SPEED=dp(5)
class MainScreen(MDScreen):
    ...




class Ship(Image):
    def __init__(self,direction=DIR_UP, **kwargs):
        super().__init__(**kwargs)
        self.direction=direction
    def move_left(self):
        self.pos[0]-=SPEED

    def move_right(self):
        self.pos[0]+=SPEED

    def update(self,keys):
        for key in keys:
            if keys[key]:
                if key=="left"and self.center_x>0:
                    self.move_left()
                elif key=="right"and self.center_x < Window.width:
                    self.move_right()


class GameScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ship=self.ids.ship
        self.eventkeys={}
    def on_enter(self):
        self.updateEvent=Clock.schedule_interval(self.update,1.0/FPS)

    def press_key(self,key):
        self.eventkeys[key]=True
    
    def release_key(self,key):
        self.eventkeys[key]=False

    def update(self,dt):
        self.ship.update(self.eventkeys)

        
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






















