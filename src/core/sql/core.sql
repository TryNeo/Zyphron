DROP TABLE IF EXISTS connections;
DROP TABLE IF EXISTS servers;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS credentials;
DROP TABLE IF EXISTS routes;
DROP TABLE IF EXISTS notes;

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
    project TEXT NOT NULL,
    title_route  TEXT NOT NULL,
    path_route TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    deleted_at DATETIME
);

CREATE TABLE notes (
    id_note INTEGER PRIMARY KEY AUTOINCREMENT,
    title_note TEXT NOT NULL,
    content_note TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);


CREATE TABLE servers (
    id_server INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_server TEXT NOT NULL,
    port_server INTEGER NOT NULL,
    category_server TEXT CHECK (category_server IN ('QA','TEST','DESA','PROD','JBOSS')) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    deleted_at DATETIME
);

CREATE TABLE projects (
    id_project INTEGER PRIMARY KEY AUTOINCREMENT,
    name_project TEXT NOT NULL,
    description_project TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    deleted_at DATETIME
);

CREATE TABLE connections (
    id_connection INTEGER PRIMARY KEY AUTOINCREMENT,
    name_connection TEXT NOT NULL,
    username_connection TEXT NOT NULL,
    passwrd_connection TEXT NOT NULL,
    auto_command TEXT,
    type_connection TEXT CHECK (type_connection IN ('SSH','SFTP')) NOT NULL,
    id_server INTEGER NOT NULL,
    id_project INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    deleted_at DATETIME,
    FOREIGN KEY (id_server) REFERENCES servers(id_server) ON DELETE RESTRICT,
    FOREIGN KEY (id_project) REFERENCES projects(id_project) ON DELETE RESTRICT
);