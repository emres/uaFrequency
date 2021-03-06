import sqlite3

conn = sqlite3.connect('frequency.db')
c = conn.cursor()

c.execute('CREATE TABLE mainFrequency (word TEXT PRIMARY KEY, frequency INTEGER)')
c.execute('CREATE TABLE urlTable (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT)')
c.execute('CREATE TABLE wordReverseIndex (wordReverseIndexID INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT, url INTEGER, context TEXT)')

c.execute('CREATE UNIQUE INDEX idx_mainFrequency ON mainFrequency (word)')

conn.commit()
conn.close()

