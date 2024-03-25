CREATE TABLE IF NOT EXISTS Calculations
(
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description TEXT         NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS Parameters
(
    id             SERIAL PRIMARY KEY,
    calculation_id INTEGER      NOT NULL,
    name           TEXT         NOT NULL DEFAULT '',
    title          VARCHAR(255) NOT NULL,
    description    TEXT         NOT NULL DEFAULT '',
    data_type      VARCHAR(255) NOT NULL,
    data_shape     VARCHAR(255) NOT NULL,
    default_value  INT          NOT NULL,
    FOREIGN KEY (calculation_id) REFERENCES Calculations (id)
);

CREATE TABLE IF NOT EXISTS Outputs
(
    id             SERIAL PRIMARY KEY,
    calculation_id INTEGER      NOT NULL,
    name           VARCHAR(255) NOT NULL,
    title          VARCHAR(255) NOT NULL,
    description    TEXT         NOT NULL DEFAULT '',
    data_type      VARCHAR(255) NOT NULL,
    data_shape     VARCHAR(255) NOT NULL,
    default_value  INT          NOT NULL,
    FOREIGN KEY (calculation_id) REFERENCES Calculations (id)
);