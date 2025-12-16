CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    date DATE,
    amount DECIMAL(10, 2),
    description VARCHAR(255),
    balance DECIMAL(10, 2)
);