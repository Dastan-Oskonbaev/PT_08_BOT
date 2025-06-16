CREATE TABLE IF NOT EXISTS users (
    "id" SERIAL PRIMARY KEY,
    "tg_id" BIGINT,
    "username" TEXT NOT NULL UNIQUE,
    "gender" VARCHAR(50),
    "age" INT,
    "profession" VARCHAR(75)
);
