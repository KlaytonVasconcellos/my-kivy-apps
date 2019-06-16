from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.graphics import Canvas
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy import Config
Config.set('graphics', 'multisamples', '0')
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.recycleview import RecycleView
import socket
import threading
import json
import MySQLdb

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 4000
name = 'Usuario'
last_name = 'Windows'
email = "rafaela@socialapp.com"
db_host = "sql10.freemysqlhosting.net"
db_name = "sql10292541"
db_user = "sql10292541"
db_pass = "cDtJHUVljT"

class Telas(ScreenManager):
	pass

class Tela(Screen):
	rv = ObjectProperty()
	def __init__(self, **kwargs):
		super(Tela, self).__init__(**kwargs)
		
	def on_enter(self):
		try:
			s.connect((host, port))
			welcome = s.recv(512)
			msg_text = (welcome + b'\n').decode()
			newmsg = TextMsg(text = '{}'.format(msg_text))
			client = (name + " " + last_name)
			temp_name = {"name": client}
			s.sendall(json.dumps(temp_name).encode('utf-8'))
			thread = threading.Thread(target=self.receive_messages)
			thread.daemon = True
			thread.start()
		except Exception as e:
			print("Error in on_enter:", e)	

	def receive_messages(self):
		while True:
			try:
				entrada = CaixaMensagem()
				data = json.loads(s.recv(1024).decode())
				newmsg = (data["from"] + " " + data["lastname"] + "\n" + data["msg"])
				user = (data["from"] + " " + data["lastname"])
				user_encod = (data["from"] + " " + data["lastname"]).encode()
				email_user = (data["email"] + "")
				user_text = TextMsg(text = newmsg)
				user_item = NameConversa(nametext = user, nameid = user)
				my_text = SelfTextMsg(text = newmsg)
				item = ItemConversa()
				nconversa = {'conversa': user}
				if data["msg_type"] == "broadcast" and data["email"] == email:
					self.manager.get_screen("tela_conversa").ids.msg_show.add_widget(my_text)
				else:
					if user == self.rv.data[0]['conversa']:
						self.manager.get_screen("tela_conversa").ids.msg_show.add_widget(user_text)
						print("Mensagem Recebida")
					elif user != self.rv.data[0]['conversa']:	
						self.rv.data.insert(0, nconversa)
						self.manager.get_screen("tela_conversa").ids.msg_show.add_widget(user_text)
						self.manager.get_screen("tela_conversa").ids.title_actionbar.text = user
						self.ids.box_msg.add_widget(user_item)
						print("Mensagem Recebida")

			except Exception as e:
				print("Error in receive_messages:",e)


	def add_conversa(self):
		d = ItemConversa()
		self.ids.box_msg.add_widget(d)

	def add_status(self):
		status = Button(text='Status', size_hint_y=0.2, height=self.parent.height * 0.15)
		self.ids.box_status.add_widget(status)

	def abrir_menu(self):
		self.parent.ids.menu_lateral.height = self.parent.height
		self.parent.ids.menu_lateral.opacity = 1

	def fechar_menu(self):
		self.parent.ids.menu_lateral.height = self.parent.height * 0
		self.parent.ids.menu_lateral.opacity = 0
		
class TelaConversa(Screen):
	global s

	def on_enter(self):
		try:
			"""s.connect((host, port))
			welcome = s.recv(512)
			msg_text = (welcome + b'\n').decode()
			newmsg = TextMsg(text = '{}'.format(msg_text))
			thread = threading.Thread(target=self.receive_messages)
			thread._stop()
			thread.start()"""
			pass
		except Exception as e:
			print("Error in on_enter:", e)	

	def send_message(self, to_send_out):
		try:
			"""logged = self.manager.get_screen('login')
			logged.infos()"""
			if self.ids.title_actionbar.text != "Grupo":
				type_msg = "private_message"
				pvt_receiver = self.ids.title_actionbar.text
			else:
				type_msg = "broadcast"
				pvt_receiver = ""

			template = {}
			template["msg_type"] = type_msg
			template["from"] = name
			template["lastname"] = last_name
			template["email"] = email
			template["msg"] = to_send_out
			template["pvt_receiver"] = pvt_receiver
			msend = json.dumps(template).encode('utf-8')
			s.sendall(msend)
			print("Mensagem Enviada:", to_send_out)
			self.ids.message.text = ''
		except Exception as e:
			print("Error in send_message:",e)

	"""def receive_messages(self):
		while True:
			try:
				data = json.loads(s.recv(1024).decode())
				newmsg = (data["from"] + " " + data["lastname"] + "\n" + data["msg"])
				user = (data["from"] + "")
				email_user = (data["email"] + "")
				mytext = SelfTextMsg(text = newmsg, id=email_user)
				mtext = TextMsg(text = newmsg, email_id=user)
				if data["msg_type"] == "broadcast" and data["email"] == email:
					self.ids.msg_show.add_widget(mytext)
				else:
					self.ids.msg_show.add_widget(mtext)
					print("Mensagem Recebida")
			except Exception as e:
				print("Error in receive_messages:",e)"""
class Login(Screen):
	def login_database(self):
		sql = MySQLdb
		db = MySQLdb.connect(db_host, db_user, db_pass, db_name)
		cursor = db.cursor()

		login_email = self.ids.form_email.text
		login_pass = self.ids.form_pass.text
		consulta = ("SELECT * FROM users WHERE email = '{}' AND senha = '{}'".format(login_email, login_pass))
		try_enter = ("SELECT senha FROM users WHERE email = {}".format(login_email))
		if cursor.execute(consulta):
			db.commit()
			email = login_email
			name = cursor.execute("SELECT nome FROM users WHERE email = '{}'".format(email))
			last_name = cursor.execute("SELECT sobrenome FROM users WHERE email = '{}'".format(email))
			self.manager.current = 'tela'
		else:
			self.ids.login_log.text = "Error: Email ou Senha incorreto!"
			print("Error: Usuario ou Senha Incorreta!")
	
	def infos(self):
		"""sql = MySQLdb
		db = MySQLdb.connect(db_host, db_user, db_pass, db_name)
		cursor = db.cursor()
		login_email = self.ids.form_email.text
		email = login_email"""
		name = name
		last_name = last_name

class Register(Screen):
	def register_database(self):
		sql = MySQLdb
		db = MySQLdb.connect(db_host, db_user, db_pass, db_name)
		cursor = db.cursor()

		reg_email = self.ids.register_email.text
		reg_confirm = self.ids.confirm_email.text
		reg_pass = self.ids.register_pass.text
		reg_nome = self.ids.register_nome.text
		reg_sobrenome = self.ids.register_sobrenome.text
		register = ("INSERT INTO users (id, email, senha, nome, sobrenome) VALUES (NULL, '{}', '{}', '{}', '{}')".format(reg_email, reg_pass, reg_nome, reg_sobrenome))
		if reg_confirm == reg_email and reg_pass != '' or reg_email != '' or reg_nome != '' or reg_sobrenome != '':
			if cursor.execute(register):
				db.commit()
				self.manager.current = 'login'
			else:
				self.ids.register_log.text = 'Não foi possivel realizar o registro!'
				print("Error: Não foi possivel realizar o registro!")
		else:
			self.ids.register_log.text = 'Error: Email não corresponde ou Campo Vazio!'

class Config(Screen):
	pass

class Jogos(Screen):
	pass

class AmigosPerto(Screen):
	pass

class Chamada(Screen):
	pass

class LayoutMsg(BoxLayout):
	pass

class TextMsg(Label):
	pass

class SelfTextMsg(Label):
	pass

class BarAction(BoxLayout):
	pass

class ItemConversa(Button):
	pass

class CaixaMensagem(RecycleView):
	def __init__(self, **kwargs):
		super(CaixaMensagem, self).__init__(**kwargs)
	pass
		
class NameConversa(Button):
	nameide = StringProperty('')
	nametext = StringProperty('')
	pass

class BotaoMenu(Button):
	pass

class MenuLateral(BoxLayout):
	pass

class TabPanel(TabbedPanel):
	pass	

class KApp(App):
	def build(self):
		self.title = 'SocialApp Messenger'
		return Telas()
	
if __name__ == "__main__":
	KApp().run()