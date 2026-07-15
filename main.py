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
from random import randint
DIR_UP=1
DIR_DOWN=-1
FPS=60
SPEED=dp(5)
class MainScreen(MDScreen):
    ...

class GameOverScreen(MDScreen):
    ...


class Ship(Image):
    def __init__(self,direction=DIR_UP, **kwargs):
        super().__init__(**kwargs)
        self.direction=direction
    def move_left(self):
        self.pos[0]-=SPEED

    def move_right(self):
        self.pos[0]+=SPEED


class PlayerShip(Ship):
    def update(self,keys):
        for key in keys:
            if keys[key]:
                if key=="left"and self.center_x>0:
                    self.move_left()
                elif key=="right"and self.center_x < Window.width:
                    self.move_right()


class EnemyShip(Ship):
    def __init__(self,  **kwargs):
        super().__init__(direction=DIR_DOWN, **kwargs)
        self.frame=0

    def update(self):
        self.pos[1]-=dp(3)
        self.frame+=1

class GameScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ship=self.ids.ship
        self.eventkeys={}
        self.enemy_ship=[]
        self.time_last_spawn=0
        self.delay_spawn=2

    def spawn_enemy(self):
        enemy=EnemyShip()
        enemy.pos=(randint(0,int(Window.size[0]-enemy.size[0])),Window.size[1])
        self.enemy_ship.append(enemy)
        self.ids.front.add_widget(enemy)

    def on_enter(self):
        self.updateEvent=Clock.schedule_interval(self.update,1.0/FPS)
        self.spawn_enemy()

    def press_key(self,key):
        self.eventkeys[key]=True
    
    def release_key(self,key):
        self.eventkeys[key]=False

    def update(self,dt):
        self.ship.update(self.eventkeys)
        self.time_last_spawn+=dt
        if self.time_last_spawn>self.delay_spawn:
            self.spawn_enemy()
            self.time_last_spawn=0
    
        for enemy in self.enemy_ship:
            enemy.update()
            if enemy.top<0:
                self.enemy_ship.remove(enemy)
                self.ids.front.remove_widget(enemy)
            if enemy.collide_widget(self.ship):
                self.game_over()

    def game_over(self):
        self.updateEvent.cancel()
        for enemy in self.enemy_ship[:]:
            self.enemy_ship.remove(enemy)
            self.ids.front.remove_widget(enemy) 
        self.manager.current='gameover'
        
class ShooterApp(MDApp):
     def build(self):
        Builder.load_file("shooter.kv")
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="Purple"
        sm=MDScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(GameOverScreen(name='gameover'))
        return sm
if platform!="android":
    Window.size = (400,750)
    Window.top=50
    Window.left=900

     

ShooterApp().run()






















