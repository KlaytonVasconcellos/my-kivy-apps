from other import *
import other


class Primeira():
	def decorar(funcao):
		def decor():
			print("Antes da funcão da outra class")
			funcao()
			print("Depois da função da outra class\n")
		return decor
	@decorar
	def outra():
		name = Primeira.__name__
		print('Outra função da mesma class. class {}'.format(name))

	#funcao_decor = decorar(outra)
	#funcao_decor()

class Outra():
	def agir(a, b):
		print(a, b)
	@Primeira.decorar
	def outra():
		name = Outra.__name__
		print('Função de outra class. nome da class {}'.format(name))


class Import():
	@Primeira.decorar
	def import_other():
		oclass = other.Other
		oclass.other()


class App():
	def options():
		try:
			exemplo = input(r"""1. Chamar Função de Mesma class
2. Chamar Função de Outra class
3. Chamar Função de outra class em outro file.py
> """)

			if exemplo == "1":
				print("\n------- Função chama Função da mesma classe -------\n")
				Primeira.outra()
			elif exemplo == "2":
				print("------- Função chama Função de outra class ---------\n")
				Outra.outra()
			elif exemplo == "3":
				print("------ Função chama Função de outra class em outro arquivo importado ----------\n")
				Import.import_other()
			else:
				print("Opção Invalida")
		except Exception as a:
			print(a)

	options()
App()
