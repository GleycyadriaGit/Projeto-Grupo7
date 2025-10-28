import tkinter as tk
from ttkbootstrap import Style, ttk
from PIL import Image, ImageTk

class Onibus:
    def __init__(self, placa, modelo):
        self.placa = placa
        self.modelo = modelo
        self.motorista = None

    def atribuir_motorista(self, motorista):
        self.motorista = motorista
        motorista.onibus = self

class Motorista:
    def __init__(self, nome):
        self.nome = nome
        self.onibus = None

class SistemaTransporte:
    def __init__(self):
        self.lista_onibus = []
        self.lista_motoristas = []

    def cadastrar_onibus(self, onibus):
        self.lista_onibus.append(onibus)

    def cadastrar_motorista(self, motorista):
        self.lista_motoristas.append(motorista)

    def vincular_onibus_motorista(self, onibus, motorista):
        onibus.atribuir_motorista(motorista)

class Aluno:
    def __init__(self, nome: str, idade: int, escola: str, ponto_de_embarque):
        self.nome_aluno = nome
        self.idade_aluno = idade
        self.escola_do_aluno = escola
        self.ponto_de_embarque = ponto_de_embarque

class PontoDeEmbarque:
    def __init__(self, endereco, tempo_ate_escola):
        self.endereco = endereco
        self.tempo_ate_escola = tempo_ate_escola
        self.alunos = []

    def adicionar_aluno(self, nome, idade, escola):
        novo_aluno = Aluno(nome, idade, escola, self)
        self.alunos.append(novo_aluno)

class Turno:
    def __init__(self, nome_turno, escola):
        self.nome_turno = nome_turno
        self.escola = escola
        self.pontos = []

    def adicionar_ponto(self, ponto: PontoDeEmbarque):
        self.pontos.append(ponto)

def criar_dados_predefinidos():
    manha = Turno("MANHA", "Escola Iracema")
    ponto_a = PontoDeEmbarque("A", 10)
    ponto_a.adicionar_aluno("João", 14, manha.escola)
    ponto_a.adicionar_aluno("Beatriz", 13, manha.escola)
    ponto_b = PontoDeEmbarque("B", 4)
    ponto_b.adicionar_aluno("Marina", 15, manha.escola)
    ponto_b.adicionar_aluno("Kaio", 14, manha.escola)
    manha.adicionar_ponto(ponto_a)
    manha.adicionar_ponto(ponto_b)

    tarde = Turno("TARDE", "Escola Samago")
    ponto_c = PontoDeEmbarque("C", 9)
    ponto_c.adicionar_aluno("Roberto", 12, tarde.escola)
    ponto_c.adicionar_aluno("Pedro", 16, tarde.escola)
    ponto_d = PontoDeEmbarque("D", 4)
    ponto_d.adicionar_aluno("Joana", 14, tarde.escola)
    ponto_d.adicionar_aluno("Maya", 13, tarde.escola)
    tarde.adicionar_ponto(ponto_c)
    tarde.adicionar_ponto(ponto_d)

    return [manha, tarde]

'''funções horario'''

saida_escola = {"MANHA": "11:00", "TARDE": "17:00"}

def horaPassagem(horaSaida, minutos):
    h, m = map(int, horaSaida.split(":"))
    m += minutos
    h += m // 60
    m = m % 60
    h = h % 24
    return f"{h:02d}:{m:02d}"

'''interface'''

turnos = criar_dados_predefinidos()

sistema = SistemaTransporte()
onibus1 = Onibus(placa="CDF-2345", modelo="Mercedes-Benz OF-1723")
sistema.cadastrar_onibus(onibus1)
motorista1 = Motorista(nome="Rodrigo Cardoso")
sistema.cadastrar_motorista(motorista1)
sistema.vincular_onibus_motorista(onibus1, motorista1)

onibus_nome = onibus1.modelo
motorista_nome = motorista1.nome

style = Style(theme="cyborg")
janela = style.master
janela.title("Rotas de Ônibus")
janela.geometry("800x450")
janela.resizable(False, False)

'''frames'''
frame_imagem = tk.Frame(janela, bg="white")
frame_imagem.place(relx=0, rely=0, relwidth=0.4, relheight=1)
frame_interface = tk.Frame(janela, bg="white")
frame_interface.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)

'''imagem'''
imagem_pil = Image.open(r"C:\Users\gleyc\Downloads\minha.foto.jpg")
altura_nova = 450
largura_original, altura_original = imagem_pil.size
largura_nova = int((altura_nova / altura_original) * largura_original)
imagem_pil = imagem_pil.resize((largura_nova, altura_nova), Image.LANCZOS)
frame_largura = int(0.4 * 800)
if largura_nova > frame_largura:
    excesso = largura_nova - frame_largura
    left = excesso // 2
    right = left + frame_largura
    imagem_pil = imagem_pil.crop((left, 0, right, altura_nova))
imagem = ImageTk.PhotoImage(imagem_pil)
label_imagem = tk.Label(frame_imagem, image=imagem, bg="white")
label_imagem.image = imagem
label_imagem.place(relx=0.5, rely=0.5, anchor="center")

'''funções interface'''

def atualizar_pontos(event=None):
    turno_selecionado = combo_turno.get()
    pontos_disponiveis = []
    if turno_selecionado in ["MANHA", "TARDE"]:
        for t in turnos:
            if t.nome_turno == turno_selecionado:
                pontos_disponiveis = [p.endereco for p in t.pontos]
                texto_pontos = "; ".join([f"{p.endereco} ({', '.join([a.nome_aluno for a in p.alunos])})" for p in t.pontos])
                label_pontos.config(text=f"Pontos disponíveis neste turno: {texto_pontos}", foreground="black")
                break
    combo_ponto['values'] = pontos_disponiveis
    combo_ponto.set('')

def mostrar_informacoes():
    turno_selecionado = combo_turno.get()
    ponto_selecionado = combo_ponto.get().upper()

    if not turno_selecionado:
        label_resultado.config(text="Escolha o turno primeiro!", foreground="red")
        return
    if not ponto_selecionado:
        label_resultado.config(text="Escolha o ponto!", foreground="red")
        return

    encontrou = False
    for t in turnos:
        if t.nome_turno == turno_selecionado:
            for p in t.pontos:
                if p.endereco == ponto_selecionado:
                    chegada = horaPassagem(saida_escola[turno_selecionado], p.tempo_ate_escola)
                    alunos_com_idade = [f"{aluno.nome_aluno} ({aluno.idade_aluno} anos)" for aluno in p.alunos]
                    texto = (f"Escola: {t.escola}\n"
                             f"Motorista: {motorista_nome}\nÔnibus: {onibus_nome}\n"
                             f"Turno: {turno_selecionado}\n"
                             f"Ponto: {p.endereco}\n"
                             f"Alunos neste ponto: {', '.join(alunos_com_idade)}\n"
                             f"A Chegada aproximada do seu filho(a) é: {chegada}h")
                    label_resultado.config(text=texto, foreground="black")
                    encontrou = True
                    break
    if not encontrou:
        label_resultado.config(text="Ponto inválido para este turno.", foreground="red")

'''interface geral'''

ttk.Label(frame_interface, text="Qual turno seu filho(a) estuda?", font=("Helvetica", 14), foreground="white").pack(pady=10)
combo_turno = ttk.Combobox(frame_interface, values=["MANHA", "TARDE"], state="readonly")
combo_turno.pack(pady=5)
combo_turno.bind("<<ComboboxSelected>>", atualizar_pontos)

label_pontos = ttk.Label(frame_interface, text="", font=("Helvetica", 12), background="#f0f0f0", justify="left")
label_pontos.pack(pady=5)

ttk.Label(frame_interface, text="Escolha o ponto:", font=("Helvetica", 14), foreground="white").pack(pady=10)
combo_ponto = ttk.Combobox(frame_interface, state="readonly")
combo_ponto.pack(pady=5)

ttk.Button(frame_interface, text="Verificar Rota", bootstyle="primary", command=mostrar_informacoes).pack(pady=15)

label_resultado = ttk.Label(frame_interface, text="", font=("Helvetica", 12), justify="left", background="#f0f0f0")
label_resultado.pack(pady=10)

janela.mainloop()
