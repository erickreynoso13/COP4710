import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('''
CREATE TABLE IF NOT EXISTS Gamers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    email TEXT NOT NULL,
    login_password TEXT NOT NULL
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS Games (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name_of_game TEXT NOT NULL,
    year INTEGER,
    genre TEXT,
    version INTEGER,
    age_restriction TEXT,
    price REAL,
    did INTEGER,
    rate REAL,
    FOREIGN KEY (user_id) REFERENCES Gamers (id)
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS Reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    entry_id INTEGER NOT NULL,
    review_text TEXT,
    stars INTEGER CHECK (stars >= 1 AND stars <= 5),
    FOREIGN KEY (user_id) REFERENCES Gamers (name_of_game),
    FOREIGN KEY (entry_id) REFERENCES Games (name)
)
''')

sample_reviews = [
    (1, 1, "This game was amazing! Worth every penny.", 5),
    (1, 2, "Solid combat but the ending was rushed.", 4),
    (3, 3, "A bit outdated but still fun to play!", 4),
    (4, 4, "One of the best adventures ever made!", 5),
    (5, 5, "Not for everyone, but the writing is superb.", 5),
    (6, 6, "Loved the time-travel theme.", 5),
    (7, 7, "Too long for my taste, but beautiful graphics.", 3),
    (8, 8, "it could be better", 3),
    (9, 9, "music tracks were amazing", 5),
    (10, 10, "it was missing something", 2),
    (11, 11, "My kid love this game", 5),
    (12, 12, "dont waste your money on this game", 1),
    (13, 13, "over hype", 5),
    (14, 14, "needs a part 2", 5),
    (15, 15, "I Love this game", 5),
    (16, 16, "its so sad ", 5),
    (17, 17, "really long", 3),
    (18, 18, "it a little boring", 2),
    (19, 19, "really good graphics", 5),
    (20, 20, "its to laggy", 1),
]
conn.executemany('''
    INSERT INTO Reviews (user_id, entry_id, review_text, stars)
    VALUES (?, ?, ?, ?)
''', sample_reviews)

users = [
    ("Erick", 23, "test1@gmail.com", "erickpass"),
    ("Alice", 30, "test2@gmail.com", "alicepass"),
    ("John", 40, "test3@gmail.com", "Johnpass"),
    ("Ben", 25, "test4@gmail.com", "Benpass"),
    ("Frankie", 13, "test5@gmail.com", "Frankiepass"),
    ("Brumick", 30, "test6@gmail.com", "Brumickpass"),
    ("Kenny", 22, "test7@gmail.com", "Kennypass"),
    ("Ricky", 10, "test8@gmail.com", "Rickypass"),
    ("Saul", 11, "test9@gmail.com", "Saulpass"),
    ("Christian", 18, "test10@gmail.com", "Christianpass"),
    ("Christopher", 23, "test11@gmail.com", "Christopherpass"),
    ("Ricardo", 80, "test12@gmail.com", "Ricardopass"),
    ("Luis", 29, "test13@gmail.com", "Luispass"),
    ("Maria", 25, "test14@gmail.com", "Mariapass"),
    ("stephanie", 22, "test15@gmail.com", "stephaniepass"),
    ("Kate", 17, "test16@gmail.com", "Katepass"),
    ("Anisa", 23, "test17@gmail.com", "Anisapass"),
    ("Nina", 22, "test18@gmail.com", "Ninapass"),
    ("Elizabeth", 38, "test19@gmail.com", "Elizabethpass"),
    ("Kimberly", 20, "test20@gmail.com", "Kimberlypass"),
]

conn.executemany('''
    INSERT INTO Gamers (name, age, email, login_password)
    VALUES (?, ?, ?, ?)
''', users)

game_entries = [
    (1, "Baldur's Gate 3", 2023, "Role-playing", 2024, "Mature", 59.99, 1, 4.9),
    (1, "Elden Ring", 2022, "Role-playing", 2024, "Mature", 39.99, 2, 4.8),
    (1, "Mass Effect Trilogy", 2012, "Shooter", 2025, "Mature", 59.99, 3, 4.7),
    (1, "The Legend of Zelda: Tears of the Kingdom", 2023, "Role-playing", 2023, "E10+", 69.99, 4, 4.9),
    (1, "Disco Elysium", 2019, "Role-playing", 2021, "Mature", 11.99, 5, 4.5),
    (1, "Steins;Gate", 2009, "Adventure", 2009, "Mature", 29.99, 6, 4.6),
    (1, "The Witcher 3: Wild Hunt", 2015, "Role-playing", 2023, "Mature", 39.99, 7, 4.8),
    (1, "Half-Life: Alyx", 2020, "Shooter", 2020, "Mature", 59.99, 8, 4.7),
    (1, "The Last of Us", 2013, "Shooter", 2025, "Mature", 69.99, 9, 4.9),
    (1, "Red Dead Redemption 2", 2018, "Shooter", 2024, "Mature", 19.99, 10, 4.8),
    (1, "Chrono Trigger", 1995, "Role-playing", 2023, "E10+", 9.99, 11, 4.9),
    (2, "Super Metroid", 1994, "Shooter", 2023, "E", 59.99, 4, 4.6),
    (2, "Persona 5", 2016, "Role-playing", 2024, "Mature", 20.99, 12, 4.7),
    (2, "The Legend of Zelda: Breath of the Wild", 2017, "Puzzle", 2017, "E10+", 69.99, 4, 4.9),
    (2, "God of War", 2018, "Role-playing", 2025, "Mature", 19.99, 13, 4.8),
    (2, "Metroid Prime", 2002, "Shooter", 2023, "Teen", 39.99, 14, 4.6),
    (2, "Paper Mario: The Thousand-Year Door", 2004, "Role-playing", 2024, "E", 49.99, 15, 4.7),
    (2, "The Legend of Zelda: A Link to the Past", 1991, "Puzzle", 2024, "E10+", 59.99, 4, 4.8),
    (2, "Super Mario World", 1990, "Adventure", 2025, "E", 19.99, 4, 4.9),
    (2, "Hollow Knight", 2017, "Adventure", 2021, "E10+", 14.99, 16, 4.8),
    (2, "Castlevania: Symphony of the Night", 1997, "Role-playing", 2023, "Mature", 59.99, 17, 4.9),
    (2, "Sid Meier's Civilization", 1990, "Strategy", 2023, "E10+", 39.99, 18, 4.7),
    (2, "Silent Hill 2", 2001, "Puzzle", 2024, "Mature", 69.99, 19, 4.5),
    (2, "Outer Wilds", 2019, "Puzzle", 2024, "E10+", 14.99, 20, 4.8),
    (2, "Hades", 2020, "Role-playing", 2022, "Teen", 24.99, 21, 4.9),
    (2, "Indiana Jones and the Fate of Atlantis", 1992, "Puzzle", 2018, "E", 5.99, 22, 4.4),
]

conn.executemany('''
    INSERT INTO Games (user_id, name_of_game, year, genre, version, age_restriction, price, did, rate)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', game_entries)

conn.commit()
conn.close()

print(" Database initialized successfully!")
