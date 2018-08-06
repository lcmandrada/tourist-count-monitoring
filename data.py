""" data layer for tourist monitoring """

import sqlite3
import csv

class Tools():
    """ data aux class """
    def __init__(self):
        self.database = sqlite3.connect("data/count.db")
        # self.table = 'count'
        self.cursor = self.database.cursor()

        self.create_table()

    def create_table(self):
        """ create database """
        try:
            with self.database:
                self.cursor.execute("""CREATE TABLE IF NOT EXISTS count(
                                    date TEXT PRIMARY KEY,
                                    fort INTEGER NOT NULL,
                                    casa INTEGER NOT NULL,
                                    total INTEGER NOT NULL
                                    )""")
        except sqlite3.IntegrityError:
            print('Error: create database')

    def select_all(self):
        """ select * from count """
        self.cursor.execute("SELECT * FROM count")
        try:
            return self.cursor.fetchall()
        except sqlite3.Error:
            return self.cursor.fetchone()

    def add_entry(self, date, fort, casa, total):
        """ insert into count """
        try:
            with self.database:
                self.cursor.execute("""INSERT INTO count(date, fort, casa, total)
                                    VALUES (?, ?, ?, ?)
                                    """, (date, fort, casa, total))
        except sqlite3.IntegrityError:
            print('Error: add entry')

    def edit_entry(self, date, fort, casa, total):
        """ update count """
        try:
            with self.database:
                self.cursor.execute("""UPDATE count SET fort = ?, casa = ?, total = ?
                                    WHERE date = ?
                """, ( fort, casa, total, date))
        except sqlite3.IntegrityError:
            print('Error: edit entry')

    def check_entry(self, date):
        """ select entry from count """
        try:
            with self.database:
                self.cursor.execute("SELECT date FROM count WHERE date = ?", (date,))
        except sqlite3.IntegrityError:
            print('Error: check entry')

        return self.cursor.fetchone()

    def export_log(self):
        """ export log """
        table = self.select_all()
        with open('log/log.csv', 'w', newline='') as file:
            out = csv.writer(file)
            # out.writerow([d[0] for d in self.cursor.description])
            out.writerow(['Date', 'Fort', 'Casa', 'Total'])
            for entry in table:
                out.writerow(entry)

    def __del__(self):
        self.database.close()
