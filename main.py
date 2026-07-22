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
from kivy.core.window import Keyboard
DIR_UP=1
DIR_DOWN=-1
FPS=60
SPEED=dp(5)
BULLET_SPEED=dp(10)
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
    def shot(self):
        bullet=Bullet(self.direction,owner=self)
        bullet.center_x=self.center_x
        bullet.y=self.top if self.direction==DIR_UP else self.y-bullet.height
        self.parent.add_widget(bullet)
        self.parent.parent.parent.parent.bullets.append(bullet)


class PlayerShip(Ship):
    def update(self,keys):
        for key in keys:
            if keys[key]:
                if key=="left"and self.center_x>0:
                    self.move_left()
                elif key=="right"and self.center_x < Window.width:
                    self.move_right()
                elif key == "shot":
                    self.shot()
                    keys[key]=False


class EnemyShip(Ship):
    def __init__(self,  **kwargs):
        super().__init__(direction=DIR_DOWN, **kwargs)
        self.frame=0

    def update(self):
        self.pos[1]-=dp(3)
        self.frame+=1


class Bullet(Image):
    def __init__(self,direction,owner, **kwargs):
        super().__init__(**kwargs)
        self.direction=direction
        self.owner = owner

class GameScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ship=self.ids.ship
        self.eventkeys={}
        self.enemy_ship=[]
        self.bullets=[]
        self.time_last_spawn=0
        self.delay_spawn=2


        Window.bind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)
        # Керування з клавіатури під час тестування з комп'ютера
    def _on_key_down(self, window, keycode, *args, **kwargs):
        key = key if (key := Keyboard.keycode_to_string(window, keycode)) != 'spacebar' else 'shot'
        self.eventkeys[key] = True

    def _on_key_up(self, window, keycode, *args, **kwargs):
        key = key if (key := Keyboard.keycode_to_string(window, keycode)) != 'spacebar' else 'shot'
        self.eventkeys[key] = False

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

        for bullet in self.bullets[:]:
            bullet.y += BULLET_SPEED* bullet.direction
            self.check_collision(bullet)
            if bullet .top<0 or bullet.y>Window.height:

                self.bullets.remove(bullet)
                self.ids.front.remove_widget(bullet)
    
        for enemy in self.enemy_ship:
            enemy.update()
            if enemy.top<0:
                self.enemy_ship.remove(enemy)
                self.ids.front.remove_widget(enemy)
            if enemy.collide_widget(self.ship):
                self.game_over()
    def check_collision(self, bullet):
        if bullet.owner== self.ship:
            for enemy in self.enemy_ship[:]:
                if bullet.collide_widget(enemy):
                    self.enemy_ship.remove(enemy)
                    self.ids.front.remove_widget(enemy)
                    self.bullets.remove(bullet)
                    self.ids.front.remove_widget(bullet)
                    break
        else:
            if bullet.collide_widget(self.ship):
                self.bullets.remove(bullet)
                self.ids.front.remove_widget(bullet)
                self.game_over
                

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






















