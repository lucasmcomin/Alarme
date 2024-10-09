import os
import tkinter
import tkinter.filedialog
from datetime import *
from tkinter import *
from tkinter import Radiobutton
from tkinter.ttk import Combobox, Treeview
from tkinter import messagebox

from PIL import ImageTk, Image

from TimeInterval import TimeInterval
import pygame
from requests import options
import threading
from Alarm import Alarm
from BancoDados import BancoAlarmes

DEFAULT_SOUND = "Sons/Trumpet Military Wake Up.mp3"

ftypes = [
            ('Arquivos Mp3', '*.mp3'),
            ('Arquivos Wave', '*.wav'),
            ('Arquivos WMA', '*.wma'),
            ('Arquivos AIFF', '*.aiff'),

        ]

class MainWindow:
    IS_TOP = False

    def __init__(self):
        self.janela = Tk()
        self.montar_tela()
        self.gerar_frame1(self.janela, True)

        #inciação de variáveis para carregar valores de Checkbuttons de dias de semana
        self.v1 = IntVar()
        self.v2 = IntVar()
        self.v3 = IntVar()
        self.v4 = IntVar()
        self.v5 = IntVar()
        self.v6 = IntVar()
        self.v7 = IntVar()
        self.diario.select()
        self.gerar_frame2(self.janela)

        self.banco = BancoAlarmes()
        self.banco.montarTabelas()
        self.popular_tabela()
        self.som = DEFAULT_SOUND

        self.janela.mainloop()

    #configuração da janela principal
    def montar_tela(self):
        self.janela.title("DESPERTADOR")
        self.janela.configure(background="#314035")
        self.janela.geometry("650x450")
        self.janela.iconbitmap("despertador.ico")
        self.janela.maxsize(width=800, height=600)
        self.janela.minsize(width=600, height=400)




    #adicionar widgets frame superior de inserção de alarme
    def gerar_frame1(self, root, t):
        self.frame1 = Frame(root, bd=4, highlightbackground="gray", highlightthickness=4)

        if t:
            self.frame1.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.46)

        else:
            self.frame1.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.9)


        self.textoInicial = Label(self.frame1, text="Horário Alarme:", font= ("Verdana", 16), background="#466270", bd = 3, foreground="white")
        self.textoInicial.place(relx=0.1, rely=0.03, relwidth=0.8, relheight=0.2)


        self.label_hora = Label(self.frame1, text="Hora:", font=("Verdana", 12))
        self.label_hora.place(relx=0.05, rely=0.3)

        self.escolher_hora = Combobox(self.frame1, width=3, font= ("Verdana", 12))
        self.escolher_hora['values'] = MainWindow.gerar_horas()
        self.escolher_hora.place(relx=0.17, rely=0.3)
        self.escolher_hora.current()

        self.label_minuto = Label(self.frame1, text="Minuto:", font= ("Verdana", 12))
        self.label_minuto.place(relx=0.3, rely=0.3)

        self.escolher_minuto = Combobox(self.frame1, width=3, font= ("Verdana", 12))
        self.escolher_minuto['values'] = MainWindow.gerar_minutos()
        self.escolher_minuto.place(relx=0.44, rely=0.3)
        self.escolher_minuto.current()

        self.diario = Radiobutton(self.frame1, text="diário", value=1 , command=self.ocultar_dias)
        self.diario.place(relx=0.6, rely=0.3)


        self.dias_da_semana = Radiobutton(self.frame1, text="dias da semana", value=2, command=self.mostrar_dias)
        self.dias_da_semana.place(relx=0.75, rely=0.3)

        self.label_rotulo = Label(self.frame1, text="Rótulo do Alarme:", font= ("Verdana", 10))
        self.label_rotulo.place(relx=0.05, rely=0.55)

        self.rotulo = Entry(self.frame1,font = ("Verdana", 8))
        self.rotulo.place(relx=0.05, rely=0.67, relwidth=0.2)

        self.label_som = Label(self.frame1, text="Toque do Alarme:", font=("Verdana", 10))
        self.label_som.place(relx=0.35, rely=0.55, relwidth=0.2)

        self.browse_som = Button(self.frame1, text="Browse", command=self.botao_browse_action, bd = 2, background='#42b9f5', font = ("Verdana", 10), foreground="white")
        self.browse_som.place(relx=0.56, rely=0.67, relwidth=0.1, relheight=0.1)

        self.som_alarme = Entry(self.frame1, font=("Verdana", 8))
        self.som_alarme.place(relx=0.35, rely=0.67, relwidth=0.2)


        if t:
            self.botao_ativar_alarme = Button(self.frame1, text="Ativar Alarme", command=self.botao_ativar_action, bd = 2, background='#42b9f5', font = ("Verdana", 12), foreground="white")
            self.botao_ativar_alarme.place(relx=0.42, rely=0.8)
            self.botao_ativar_alarme.focus_set()
            self.som_alarme.insert(END, DEFAULT_SOUND)


        else:
            self.botao_alterar_alarme = Button(self.frame1, text="Alterar Alarme", command=self.botao_alterar_action, bd=2,background='#42b9f5', font=("Verdana", 12), foreground="white")
            self.botao_alterar_alarme.place(relx=0.42, rely=0.8)
            self.botao_alterar_alarme.focus_set()



    def botao_browse_action(self):

        self.som = tkinter.filedialog.askopenfilename(parent=self.frame1, filetypes=ftypes, initialdir="Sons")
        self.som_alarme.delete(0, END)
        self.som_alarme.insert(END, os.path.basename(self.som))


    def botao_ativar_action(self):


        if self.escolher_hora.get() == "" or self.escolher_minuto.get() == "":
           messagebox.showerror(message="Horário de Alarme Incorreto!")
        else:
            self.flags = self.flaggin_days()
            self.hora_alarme = int(self.escolher_hora.get())
            self.minuto_alarme = int(self.escolher_minuto.get())
            alarme = Alarm(0,self.hora_alarme, self.minuto_alarme,self.flags, str(self.rotulo.get()), self.som)
            self.banco.add_alarme(alarme)
            s = alarme.tempo_faltante()
            messagebox.showinfo(message=f"Alarme setado para {s}")
            self.popular_tabela()
            self.limpar_formulario()


    def limpar_formulario(self):

        self.popular_tabela()
        self.escolher_hora.delete(0, END)
        self.escolher_minuto.delete(0, END)
        self.rotulo.delete(0, END)
        self.diario.select()
        self.ocultar_dias()
        self.som_alarme.delete(0, END)
        self.som_alarme.insert(END, DEFAULT_SOUND)

    def popular_tabela(self):
        self.tabela_alarmes.delete(*self.tabela_alarmes.get_children())
        lista = self.banco.carregar_lista()
        t = 0
        for i in lista:

            self.tabela_alarmes.insert("", END, values=i,  iid = t)
            self.tabela_alarmes.set(t,"#5",os.path.basename(i[4]))
            Alarm.popula_alarme(i[0], i[1], i[2], i[3], i[4])
            t+=1



    def ocultar_dias(self):
        try:
            self.c1.destroy()
            self.c2.destroy()
            self.c3.destroy()
            self.c4.destroy()
            self.c5.destroy()
            self.c6.destroy()
            self.c7.destroy()
            self.v1.set(0)
            self.v2.set(0)
            self.v3.set(0)
            self.v4.set(0)
            self.v5.set(0)
            self.v6.set(0)
            self.v7.set(0)
        except AttributeError:
            print("Erro mas continua")

    def mostrar_dias(self):
        self.c1 = Checkbutton(self.frame1, text="Segunda", font=("Calibri", 10), variable=self.v1)
        self.c2 = Checkbutton(self.frame1, text="Terça", font=("Calibri", 10), variable=self.v2)
        self.c3 = Checkbutton(self.frame1, text="Quarta", font=("Calibri", 10), variable=self.v3)
        self.c4 = Checkbutton(self.frame1, text="Quinta", font=("Calibri", 10), variable=self.v4)
        self.c5 = Checkbutton(self.frame1, text="Sexta", font=("Calibri", 10), variable=self.v5)
        self.c6 = Checkbutton(self.frame1, text="Sábado", font=("Calibri", 10), variable=self.v6)
        self.c7 = Checkbutton(self.frame1, text="Domingo", font=("Calibri", 10), variable=self.v7)
        self.c1.place(relx=0.75, rely=0.45)
        self.c2.place(relx=0.75, rely=0.55)
        self.c3.place(relx=0.75, rely=0.65)
        self.c4.place(relx=0.75, rely=0.75)
        self.c5.place(relx=0.75, rely=0.85)
        self.c6.place(relx=0.87, rely=0.45)
        self.c7.place(relx=0.87, rely=0.55)


    def flaggin_days(self):
        flags = "0"
        if self.v1.get() == 1:
            flags += "1"
        if self.v2.get() == 1:
            flags += "2"
        if self.v3.get() == 1:
            flags += "3"
        if self.v4.get() == 1:
            flags += "4"
        if self.v5.get() == 1:
            flags += "5"
        if self.v6.get() == 1:
            flags += "6"
        if self.v7.get() == 1:
            flags += "7"

        return flags

    def gerar_frame2(self, root):
        self.frame2 = Frame(root, bd=4, highlightbackground="gray", highlightthickness=4)
        self.frame2.place(relx=0.02, rely=0.6, relwidth=0.96, relheight=0.36)
        self.mostrador_horario_atual = Label(self.frame2, text="Horário Alarme:", font= ("Verdana", 16),  background="#466270", bd = 2, foreground="white")
        self.mostrador_horario_atual.place(relx=0.1, rely=0.03, relwidth=0.8, relheight=0.2)
        self.atualizar_relogio()

        self.tabela_alarmes = Treeview(self.frame2, height=3, columns=("col1","col2","col3", "col4", "col5"))
        self.tabela_alarmes.heading("#1", text="Código")
        self.tabela_alarmes.heading("#2", text="Rótulo")
        self.tabela_alarmes.heading("#3", text="Horário")
        self.tabela_alarmes.heading("#4", text="Frequência")
        self.tabela_alarmes.heading("#5", text="Som")

        self.tabela_alarmes.column("#0", width=1)
        self.tabela_alarmes.column("#1", width=30)
        self.tabela_alarmes.column("#2", width=100)
        self.tabela_alarmes.column("#3", width=50)
        self.tabela_alarmes.column("#4", width=120)
        self.tabela_alarmes.column("#5", width=120)


        self.tabela_alarmes.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.7)
        self.tabela_alarmes.bind("<Button-3>", self.menu_bot_direito_mouse)
        self.tabela_alarmes.bind("<Delete>", self.popup_deletar)
        self.tabela_alarmes.bind("<Double-Button-1>", self.double_click)

        scroll_tabela = Scrollbar(self.frame2, orient="vertical", command = self.tabela_alarmes.yview)
        self.tabela_alarmes.configure(yscroll=scroll_tabela.set)
        scroll_tabela.place(relx=0.96, rely=0.25, relwidth=0.03,relheight=0.7)


    def atualizar_relogio(self):
        self.hora_atual = datetime.now()
        hora_mostrador = self.hora_atual.strftime("%H:%M:%S")
        self.mostrador_horario_atual.config(text=hora_mostrador)
        d, self.a = Alarm.verifica_alarme(self.hora_atual)

        if d:
            self.t1 = threading.Thread(target=self.despertar, args = (self.a.som,))
            self.t1.start()


        self.frame2.after(1000, self.atualizar_relogio)


    def popup_deletar(self, event=None):
        try:
            self.destruir(self.janela_escolher)
        except:
            print("Janela Escolha não Criada ")

        if not MainWindow.IS_TOP:
            MainWindow.IS_TOP = True

            self.janela_deletar = Toplevel(self.janela)
            self.janela_deletar.title('Apagar Alarme')
            self.janela_deletar.iconbitmap("despertador.ico")
            self.janela_deletar.geometry("300x150")
            self.janela_deletar.lift(self.janela)


            labelDeletar = Label(self.janela_deletar, text="Tem certeza que deseja apagar este alarme?")
            labelDeletar.place(relx=0.1, rely=0.4)

            botao_apagar = Button(self.janela_deletar, text="Apagar", command=self.deletar_alarme, bd=2, bg="#42b9f5",
                                  foreground="white")
            botao_apagar.place(relx=0.2, rely=0.7, relwidth=0.3)

            botao_fechar = Button(self.janela_deletar, text="Fechar", bd=2,bg="#42b9f5", foreground="white", takefocus=0)
            botao_fechar["command"] = lambda: self.destruir(self.janela_deletar)
            botao_fechar.focus_set()
            botao_fechar.place(relx=0.6, rely=0.7, relwidth=0.3)

            self.janela_deletar.protocol('WM_DELETE_WINDOW', lambda: self.destruir(self.janela_deletar))
      #      botao_fechar.bind("<Return>", botao_fechar.)


    def deletar_alarme(self):

        cod = 0
        for n in self.tabela_alarmes.selection():
            cod, rotulo, hora, frequencia, som = self.tabela_alarmes.item(n, 'values')

        self.banco.deletar_alarme(cod)
        self.popular_tabela()
        self.destruir(self.janela_deletar)

    def alterar_alarme(self):

        try:
            self.destruir(self.janela_escolher)
        except AttributeError:
            print("O tributo ainda não foi criado")


        self.janela_alterar = Toplevel(self.janela)
        self.janela_alterar.title('Alterar Alarme')
        self.janela_alterar.geometry("630x250")
        self.janela_alterar.iconbitmap("despertador.ico")
        self.janela_alterar.configure(background="#314035")


        cod = 0
        rotulo = ""
        hora = ""

        frequencia = ""
        som = ""
        for n in self.tabela_alarmes.selection():
            cod, rotulo, hora, frequencia, som = self.tabela_alarmes.item(n, 'values')


        self.gerar_frame1(self.janela_alterar, False)
        self.selecionar_freq(frequencia)
        self.rotulo.insert(END, rotulo)
        self.escolher_hora.insert(END, hora[0] + hora[1])
        self.escolher_minuto.insert(END, hora[3] + hora[4])
        self.som = self.banco.get_som(cod)
        self.som_alarme.insert(END, os.path.basename(som))
        self.cod_alterar = cod

        self.janela_alterar.protocol('WM_DELETE_WINDOW', self.fechar_alterar)

    def fechar_alterar(self):
        self.frame1.destroy()
        self.janela_alterar.destroy()
        self.gerar_frame1(self.janela, True)
        self.diario.select()

    def botao_alterar_action(self):

        if self.escolher_hora.get() == "" or self.escolher_minuto.get() == "":
            messagebox.showerror(message="Horário de Alarme Incorreto!")
        else:
            self.flags = self.flaggin_days()
            self.hora_alarme = int(self.escolher_hora.get())
            self.minuto_alarme = int(self.escolher_minuto.get())

            alarme = Alarm(self.cod_alterar, self.hora_alarme, self.minuto_alarme, self.flags, str(self.rotulo.get()), self.som)
            self.banco.alterar_alarme(alarme)
            s = alarme.tempo_faltante()
            messagebox.showinfo(message=f"Alarme alterado para {s}")
            self.popular_tabela()


            self.janela_alterar.destroy()
            self.frame1.destroy()
            self.gerar_frame1(self.janela, True)
            self.diario.select()


    def double_click(self, event=None):
        if not MainWindow.IS_TOP:
            MainWindow.IS_TOP = True
            self.janela_escolher = Toplevel(self.janela)
            self.janela_escolher.title('O que fazer')
            self.janela_escolher.geometry("300x150")
            self.janela_escolher.iconbitmap("despertador.ico")
            self.janela_escolher.transient(self.janela)
            labelEscolha = Label(self.janela_escolher, text="O que deseja fazer com este alarme?")
            labelEscolha .place(relx=0.1, rely=0.4)

            botao_apagar = Button(self.janela_escolher, text="Apagar", command=self.popup_deletar, bd=2, bg="#42b9f5",foreground="white")
            botao_apagar.place(relx=0.1, rely=0.7, relwidth=0.2)

            botao_alterar = Button(self.janela_escolher, text="Alterar", command=self.alterar_alarme, bd=2, bg="#42b9f5", foreground="white")
            botao_alterar.place(relx=0.4, rely=0.7, relwidth=0.2)

            botao_fechar = Button(self.janela_escolher, text="Fechar", bd=2,   bg="#42b9f5", foreground="white")
            botao_fechar["command"] = lambda: self.destruir(self.janela_escolher)

            botao_fechar.focus_set()
            botao_fechar.place(relx=0.7, rely=0.7, relwidth=0.2)
            self.janela_escolher.protocol('WM_DELETE_WINDOW', lambda: self.destruir(self.janela_escolher))




    def destruir(self, toplevel):
        toplevel.destroy()
        MainWindow.IS_TOP = False

    def selecionar_freq(self, f):

        if f == "Diário":
            self.diario.select()

        else:
            self.dias_da_semana.select()
            self.mostrar_dias()
            if "Seg. " in f:
                self.c1.select()

            if "Ter. " in f:
                self.c2.select()

            if "Qua. " in f:
                self.c3.select()

            if "Qui. " in f:
                self.c4.select()

            if "Sex. " in f:
                self.c5.select()

            if "Sab. " in f:
                self.c6.select()

            if "Dom." in f:
                self.c7.select()




    @staticmethod
    def gerar_horas():
        lista_horas = []
        for i in range(24):
            if i < 10:
                lista_horas.append('0' + str(i))
            else:
                lista_horas.append(i)

        return lista_horas

    @staticmethod
    def gerar_minutos():
        lista_horas = []
        for i in range(60):
            if i < 10:
                lista_horas.append('0' + str(i))
            else:
                lista_horas.append(i)

        return lista_horas

    def despertar(self, s):
        pygame.mixer.init()
        pygame.mixer.music.load(s)
        pygame.mixer.music.play(-1)
        self.janela_alarme = Toplevel(self.janela)
        self.janela_alarme.title('Acordar')
        self.janela_alarme.geometry("300x150")
        self.janela_alarme.iconbitmap("despertador.ico")

        self.parar = False
        labelAlarme = Label(self.janela_alarme, text="Acorde!!!!!")
        labelAlarme.place(relx=0.1, rely=0.4)

        botao_parar = Button(self.janela_alarme, text="Parar", command = self.parar_alarme, bd=2, bg="#42b9f5", foreground="white")

        botao_parar.place(relx=0.2, rely=0.7, relwidth=0.3)

        botao_soneca = Button(self.janela_alarme, text="Soneca (10 min)", command =  lambda:self.soneca(s), bd=2, bg="#42b9f5", foreground="white")
        botao_soneca.place(relx=0.6, rely=0.7, relwidth=0.3)
        t2 = threading.Thread(target=TimeInterval.counter, args=(180,))
        t2.start()
        t2.join()

        if not self.parar:
            self.soneca(s)


    def soneca(self, s):
        self.janela_alarme.destroy()
        pygame.mixer.music.stop()
        alarme = Alarm(0, self.hora_atual.hour, self.hora_atual.minute + 10, "0", "", s)
        messagebox.showinfo(message=f"Alarme alterado para {alarme.hora_alarme}")
        Alarm.lista_alarmes.append(alarme)

    def parar_alarme(self):
        self.parar = True
        self.janela_alarme.destroy()
        pygame.mixer.music.stop()

    def menu_bot_direito_mouse(self, event):

        m = Menu(self.janela, tearoff=0)
        m.add_command(label="Alterar", command=self.alterar_alarme)
        m.add_command(label="Deletar", command=self.popup_deletar)

        try:
            m.tk_popup(event.x_root, event.y_root)
            MainWindow.IS_TOP = False
        finally:
            m.grab_release()

