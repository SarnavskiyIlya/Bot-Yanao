PRAGMA foreign_keys=on;

CREATE TABLE IF NOT EXISTS messages (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 number INTEGER NOT NULL UNIQUE,
 send_date_and_time TEXT NOT NULL,
 text TEXT NOT NULL,
 date_of_addition TEXT NOT NULL,
 activate INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS files (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 id_message INTEGER NOT NULL,
 name TEXT NOT NULL,
 file_id TEXT NOT NULL UNIQUE,
 CONSTRAINT fk_message FOREIGN KEY (id_message) REFERENCES messages(id) ON DELETE CASCADE,
 CONSTRAINT message_file_name UNIQUE (id_message, name)
);

CREATE TABLE IF NOT EXISTS chats_and_channels (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 id_message INTEGER NOT NULL,
 name TEXT NOT NULL,
 stamp TEXT NOT NULL,
 CONSTRAINT fk_message FOREIGN KEY (id_message) REFERENCES messages(id) ON DELETE CASCADE,
 CONSTRAINT message_stamp UNIQUE (id_message, stamp)
);