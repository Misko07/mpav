DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS blogs;
DROP TABLE IF EXISTS papers;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    sdesc TEXT,
    ldesc TEXT,
    tools TEXT,
    period TEXT
);

CREATE TABLE blogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    created DATE NOT NULL,
    body TEXT
);

CREATE TABLE papers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ref_text TEXT NOT NULL,
  category TEXT NOT NULL,
  sdesc TEXT,
  url TEXT
);