CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS admins (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    id BIGSERIAL PRIMARY KEY,
    balance FLOAT DEFAULT 0.0,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    amount FLOAT NOT NULL,
    account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
    transaction_id VARCHAR NOT NULL
);

INSERT INTO users (email, password, full_name)
VALUES ('user@example.com', 'scrypt:32768:8:1$qLvqAoYNhKKoJVdm$65e9e1bc1d3b25d4a222eb41125a4da9eda5345a7f2e820f6c0d1e8ccf4cb200d72fe9f41ac9c933ac63c9c7f8281156b1dde55a46f6ff95f9db81f3b2af18cd', 'Test User')
ON CONFLICT (email) DO NOTHING;

INSERT INTO admins (email, password, full_name)
VALUES ('admin@example.com', 'scrypt:32768:8:1$qLvqAoYNhKKoJVdm$65e9e1bc1d3b25d4a222eb41125a4da9eda5345a7f2e820f6c0d1e8ccf4cb200d72fe9f41ac9c933ac63c9c7f8281156b1dde55a46f6ff95f9db81f3b2af18cd', 'Test Admin')
ON CONFLICT (email) DO NOTHING;

INSERT INTO accounts (balance, user_id)
VALUES (1000.0, (SELECT id FROM users WHERE email = 'user@example.com'))
ON CONFLICT DO NOTHING;

INSERT INTO payments (amount, account_id, transaction_id)
VALUES
    (100.0, (SELECT id FROM accounts WHERE user_id = (SELECT id FROM users WHERE email = 'user@example.com')), 'txn_001'),
    (200.0, (SELECT id FROM accounts WHERE user_id = (SELECT id FROM users WHERE email = 'user@example.com')), 'txn_002'),
    (700.0, (SELECT id FROM accounts WHERE user_id = (SELECT id FROM users WHERE email = 'user@example.com')), 'txn_003')
ON CONFLICT DO NOTHING;
