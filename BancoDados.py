import sqlite3
from Alarm import Alarm
class BancoAlarmes():

    def conecta_bd(self):
        self.conn = sqlite3.connect("alarmes.bd")
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()

    def montarTabelas(self):
        self.conecta_bd();

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alarmes (
                cod INTEGER PRIMARY KEY, 
                rotulo CHAR(40), 
                hora_alarme CHAR(8) NOT NULL, 
                frequencia CHAR(30) NOT NULL, 
                som CHAR(30) NOT NULL
            );
        """)
        self.conn.commit()
        self.desconecta_bd()

    def add_alarme(self, alarme):

        self.conecta_bd()
        self.cursor.execute(""" 
                INSERT INTO alarmes (rotulo, hora_alarme, frequencia, som)
                VALUES (?, ?, ?, ?)
        """,(alarme.rotulo, alarme.hora_alarme, alarme.frequencia, alarme.som))

        self.conn.commit()
        self.desconecta_bd()


    def carregar_lista(self):
        self.conecta_bd()

        lista = self.cursor.execute(""" SELECT cod, rotulo, hora_alarme, frequencia, som FROM alarmes""")
        self.conn.commit()

        return lista

    def get_som(self, codigo):
        self.conecta_bd()
        self.cursor.execute("""SELECT som FROM alarmes WHERE cod = ?""", [codigo])
        som = self.cursor.fetchone()[0]
        self.conn.commit()
        self.desconecta_bd()
        return som

    def deletar_alarme(self, codigo):
        self.conecta_bd()

        self.cursor.execute("""DELETE FROM alarmes WHERE cod = ?""", [codigo])

        self.conn.commit()
        self.desconecta_bd()

    def alterar_alarme(self, alarme):
        self.conecta_bd()
        print(alarme.som)
        self.cursor.execute(""" 
                        UPDATE alarmes SET rotulo = ?, hora_alarme = ?, frequencia = ?, som = ? WHERE cod = ? """, (alarme.rotulo, alarme.hora_alarme, alarme.frequencia, alarme.som, alarme.codigo))

        self.conn.commit()
        self.desconecta_bd()