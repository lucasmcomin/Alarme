import time


class TimeInterval:

    def __init__(self, h, m, s, d):
        if (s == 60):
            m += 1

        if (m == 60):
            h += 1

        if (h >= 24):
            h = (h % 24)

        if not isinstance(h, int) or not isinstance(h, int) or not isinstance(s, int):
            raise TypeError("Hours, minutes, and seconds must be integers.")

        elif (s < 60) and (m < 60):
            self.dias = d
            self.horas = h
            self.minutos = m
            self.segundos = s
        else:
            raise TypeError("Digite um horário válido.")

    def secondTransform(self):
        if self.dias ==0:
            return (self.horas * 3600) + (self.minutos * 60) + self.segundos
        else:
            return ((self.dias * 24 + self.horas) * 3600) + (self.minutos * 60) + self.segundos

    def secondToTime(s):
        h, rest = divmod(s, 3600)
        d = h//24
        m,s = divmod(rest,60)
        return TimeInterval(h,m,s,d)


    def __add__(self,other):
         total_segundos = self.secondTransform() + other.secondTransform()
         return TimeInterval.secondToTime(total_segundos)



    def __sub__(self,other):
        total_segundos = self.secondTransform() - other.secondTransform()
        return TimeInterval.secondToTime(total_segundos)



    def __mul__(self,other):
            total_segundos = self.secondTransform() * other.secondTransform()
            return TimeInterval.secondToTime(total_segundos)

    def __str__(self):
        s = f"{self.horas:02d} horas  {self.minutos:02d} minutos e {self.segundos:02d} segundos"
        if  self.dias > 0:
            s = f"{self.dias} dias " + s

        return s

    @staticmethod
    def counter(x):
        for i in range (x):
            time.sleep(1)




