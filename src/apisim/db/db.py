import sqlite3
from unit import response_unit

class query:
    def __init__(self) -> None:
        self.con = sqlite3.connect('responses.db')

    def setup(self):
        cur = self.con.cursor()
        cur.execute('''DROP TABLE IF EXISTS response_values''')
        cur.execute('''CREATE TABLE response_values
               (url text, value text, mode text, time float, status text, outcome text)''')
        self.con.commit()
        self.con.close()

    def write(self, res_unit: response_unit):
        self.con = sqlite3.connect('responses.db')
        cur = self.con.cursor()
        conv_vals = str(bytes(res_unit.value))
        vals = (res_unit.url, conv_vals, res_unit.mode, res_unit.time, res_unit.status, res_unit.outcome)
        qe = """INSERT INTO response_values (url, value, mode, time, status, outcome) VALUES (?, ?, ?, ?, ?, ?) """
        cur.execute(qe, vals)

        self.con.commit()
        self.con.close()

    def get(self):
        self.con = sqlite3.connect('responses.db')
        cur = self.con.cursor()
        cur.execute("SELECT * FROM response_values")
        records = cur.fetchall()
        self.con.close()
        return records
