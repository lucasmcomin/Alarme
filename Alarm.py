from datetime import *
from tkinter import messagebox
from TimeInterval import*
import pygame

class Alarm:

    lista_alarmes = []

    def __init__(self, cod,hora, minutos, flags, rotulo, som):
        self.codigo = cod

        if minutos >=60:
            self.minutos = minutos - 60
            self.hora = hora + 1
        else:
            self.hora  = hora
            self.minutos = minutos

        self.hora_alarme = f"{self.hora:02}"+ ":"  + f"{self.minutos:02}" + ":"  +  "00"
        self.flags = flags
        self.frequencia = self.frequencia_alarme()
        self.rotulo = rotulo
        self.som = som


    def frequencia_alarme(self):
        if self.flags == "0":
            return "Diário"
        else:
            frequencia = ""
            if "1" in self.flags:
                frequencia += "Seg. "

            if "2" in self.flags:
                frequencia += "Ter. "

            if "3" in self.flags:
                frequencia += "Qua. "

            if "4" in self.flags:
                frequencia += "Qui. "

            if "5" in self.flags:
                frequencia += "Sex. "

            if "6" in self.flags:
                frequencia += "Sab. "

            if "7" in self.flags:
                frequencia += "Dom."

            return frequencia

    def tempo_faltante(self):
        tempo_atual = datetime.now()
        t1 = TimeInterval(tempo_atual.hour, tempo_atual.minute, tempo_atual.second, 0)
        d = 0

        if self.flags!="0":

            dia_semana = tempo_atual.weekday() + 1

            if str(dia_semana) in self.flags and self.hora >= tempo_atual.hour:
                if (self.hora > tempo_atual.hour):
                    d = 0
                elif (self.minutos > tempo_atual.minute):
                    d = 0
                else:
                    c = self.proximoDia(self.flags, dia_semana)
                    if (dia_semana >= c):
                        d = c + 7 - dia_semana
                    else:
                        d = c - dia_semana

            else:
                c = self.proximoDia(self.flags, dia_semana)
                if (dia_semana >= c):
                    d = c + 7 - dia_semana
                else:
                    d = c - dia_semana

        else:
            if self.hora <= tempo_atual.hour:
                if self.hora == tempo_atual.hour:
                    if self.minutos <= tempo_atual.minute:
                        d = 1

                else:
                    d = 1

        t2 = TimeInterval(self.hora, self.minutos, 0, d)
        return t2 - t1


    def proximoDia(self, st, n):
        anterior = 8
        resultado = 0
        for i in st:
            c = int(i)
            if c > n and c < anterior:
                resultado = c
                anterior = c
        if resultado == 0:
            if int(st[1]) != n:
                resultado = int(st[1])
            else:
                resultado = n
        return resultado

    @staticmethod
    def verifica_alarme(hora_atual):
            dia_semana = str(hora_atual.now().weekday() + 1)
            ha = hora_atual.now().strftime("%H:%M:%S")

            for i in Alarm.lista_alarmes:
                if ha == i.hora_alarme and i.flags == "0":
                    return True, i

                elif ha == i.hora_alarme and i.flags != "0":
                    if dia_semana in i.flags:
                        return True, i
            return False, None

    @ staticmethod
    def popula_alarme(c,r, h, f, s):

        hora = int(h[0] + h[1])
        minutos = int(h[3] + h[4])
        flags = Alarm.freq_to_flags(f)
        a = Alarm(c,hora, minutos, flags, r, s)
        Alarm.lista_alarmes.append(a)


    @staticmethod
    def freq_to_flags(f):
        flag = "0"

        if f != "Diário":
            if "Seg. " in f:
                flag += "1"

            if "Ter. " in f:
                flag += "2"

            if "Qua. " in f:
                flag += "3"

            if "Qui. " in f:
                flag += "4"

            if "Sex. " in f:
                flag += "5"

            if "Sab. " in f:
                flag += "6"

            if "Dom." in f:
                flag+= "7"

        return flag

