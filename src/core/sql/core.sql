DROP TABLE IF EXISTS credentials;
DROP TABLE IF EXISTS routes;

CREATE TABLE credentials (
    id_credential INTEGER PRIMARY KEY AUTOINCREMENT,
    title_credential  TEXT NOT NULL,
    username  TEXT NOT NULL,
    passwrd   TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    deleted_at DATETIME
);

CREATE TABLE routes (
    id_route INTEGER PRIMARY KEY AUTOINCREMENT,
    project   TEXT NOT NULL,
    title_route  TEXT NOT NULL,
    path_route TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    deleted_at DATETIME
);