DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  streak INTEGER,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

