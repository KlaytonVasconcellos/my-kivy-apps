from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.core.audio import SoundLoader
from os.path import join, dirname
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.slider import Slider
from kivy.properties import StringProperty
from kivy.properties import DictProperty
from functools import partial
import sys
import threading
import time

var_ids = []

class Janela(BoxLayout):
	pass

class Gerenciador_Tela(ScreenManager):
	pass

class Tocar(Screen):
	id_dinamico = []
	def __init__(self, **kwargs):
		super(Tocar, self).__init__(**kwargs)
		Clock.schedule_once(self.on_enter, 0)

	def on_enter(self, dt=0):
		self.botoes = GridLayout(cols=4, id="pads_box")
		self.generate_buttons(self.botoes)
		try:
			self.ids.box_pads.add_widget(self.botoes)
		except Exception as a:
			print("Erro em On_Enter:", a)

	def playsound(self, instance):
		banco = self.ids.banco_atual.text
		filename = join(dirname(__file__), '{}/{}.wav'.format(banco, instance.id))
		self.sound = SoundLoader.load(filename)
		self.pitch_slider(self.ids.slid1.value)
		self.volume(int(self.ids.slid2.value))
		self.rid = instance.id
		self.estado = instance.state
		self.padrepeat = self.ids.ef2.ids.noterepeat
		indexs = int(int(self.rid) - 1)
		event_repetir = Clock.schedule_interval(partial(self.repetidor, indexs), 0.5)
		self.id_dinamico[indexs].bind(on_press=event_repetir, on_release = event_repetir.cancel)
		if self.sound:
			self.sound.play()
			#threading.Thread(target=self.repetidor(indexs)).start()
			#self.repetidor(indexs)

	"""def playsound_repet(self, instance):
		while True:
			banco = self.ids.banco_atual.text
			filename = join(dirname(__file__), '{}/{}.wav'.format(banco, instance.id))
			self.sound = SoundLoader.load(filename)
			self.pitch_slider(self.ids.slid1.value)
			self.volume(int(self.ids.slid2.value))
			self.rid = instance.id
			self.estado = instance.state
			self.padrepeat = self.ids.ef2.ids.noterepeat
			indexs = int(int(self.rid) - 1)
			if self.sound:
				self.sound.play()
		else:
			self.id_dinamico[indexs].bind(on_press=self.playsound(instance))"""

	def repetidor(self, enfeite, sendid):
		while (self.ids.ef2.ids.noterepeat.text != 'Disabled' and self.id_dinamico[sendid].state == 'down'): #and self.ids.ef2.ids.noterepeat.state == 'down':
			self.sound.play()
			time.sleep(0.5)
		else:
			pass

	def stopsound(self):
		self.sound.stop()

	def pitch_reset(self):
		self.ids.slid1.value = 1

	def pitch_slider(self, valor):
		slider1 = self.ids.slid1.value
		self.sound.pitch = slider1

	def volume(self, vol):
		volu = self.ids.slid2.value
		self.sound.volume = vol

	def generate_buttons(self, layout):
		for counter in range(1, 17):
			# device = str(counter)
			new_button = Button(id="{0}".format(counter))
			new_button.bind(on_press=self.playsound)
			layout.add_widget(new_button)
			self.id_dinamico.append(new_button)
			pos_index = counter
			id_index = int(int("{}".format(counter)) - 1)
			print(pos_index, id_index, self.id_dinamico[id_index].state)


	def BancoA(self):
		self.ids.banco_atual.text = "BancoA"

	def BancoB(self):
		self.ids.banco_atual.text = "BancoB"

	def BancoC(self):
		self.ids.banco_atual.text = "BancoC"

	def BancoD(self):
		self.ids.banco_atual.text = "BancoD"

class Pad(Button):
	pass

class PadBanco(Button):
	pass

class Infos(BoxLayout):
	pass

class Slid(Slider):
	pass

class Efeitos(BoxLayout):
	pass

class Efeitos2(BoxLayout):
	pass

class Drumpad(App):
    def build(self):
        return Gerenciador_Tela()

if __name__=="__main__":
    Drumpad().run()
