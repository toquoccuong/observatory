"""
This pyton script sets up the sqlite database
"""


import sqlite3

conn = sqlite3.connect('benchmarks\\outputs\\benchmark_sqlite.sqlite')
cursor = conn.cursor()
conn.commit()
conn.close()

conn = sqlite3.connect('benchmarks\\outputs\\benchmark_sqlite.sqlite')
cursor1 = conn.cursor()

#Create Model Table
cursor1.execute(
    '''CREATE TABLE IF NOT EXISTS Model(
        name TEXT PRIMARY KEY NOT NULL,
        date TEXT NOT NULL
        );''')

#Create Version Table
cursor1.execute(
    '''CREATE TABLE IF NOT EXISTS Version(
        id INT PRIMARY KEY NOT NULL,
        date TEXT NOT NULL,
        model TEXT,
        FOREIGN KEY(model) REFERENCES Model(name)
        );''')

#Create Experiment Table
cursor1.execute(
    '''CREATE TABLE IF NOT EXISTS Experiment(
        name TEXT PRIMARY KEY NOT NULL,
        date TEXT NOT NULL,
        version INT,
        FOREIGN KEY(version) REFERENCES Version(id)
        );''')

#Create Run Table
cursor1.execute(
    '''CREATE TABLE IF NOT EXISTS Run(
        id INT PRIMARY KEY NOT NULL,
        date TEXT NOT NULL,
        experiment TEXT,
        FOREIGN KEY(experiment) REFERENCES Experiment(name)
        );''')

#Create Metric Table
cursor1.execute(
    '''CREATE TABLE IF NOT EXISTS Metric(
        name TEXT PRIMARY KEY NOT NULL,
        date TEXT NOT NULL,
        value TEXT NOT NULL,
        run INT,
        FOREIGN KEY(run) REFERENCES Run(id)        
        );''')

#Create Setting Table
cursor1.execute(
    '''CREATE TABLE IF NOT EXISTS Setting(
        id INT PRIMARY KEY NOT NULL,
        Date TEXT NOT NULL,
        run INT,
        FOREIGN KEY(run) REFERENCES Run(id)        
        );''')

#Create Output Table
cursor1.execute(
    '''CREATE TABLE IF NOT EXISTS Output(
        id INT PRIMARY KEY NOT NULL,
        Date TEXT NOT NULL,
        run INT,
        FOREIGN KEY(run) REFERENCES Run(id)        
        );''')



cursor1.close