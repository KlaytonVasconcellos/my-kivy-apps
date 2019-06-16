from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider


class Window(BoxLayout):
	pass

class GerenciadorTela(ScreenManager):
	pass

class Principal(Screen):
	pass

class Partida(Screen):
	pass

class MeuTime(Screen):
	pass

class Action_Bar(BoxLayout):
	pass

class Acionar_Paleta(Button):
	pass

class MainApp(App):
	def build(self):
		return Window()

MainApp().run()
