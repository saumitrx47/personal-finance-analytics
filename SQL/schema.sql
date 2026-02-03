CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    date DATE,
    amount DECIMAL(10, 2),
    description VARCHAR(255),
    balance DECIMAL(10, 2),
    category VARCHAR(100)
);

CREATE TABLE monthly_spending_summary (
    summary_id SERIAL PRIMARY KEY,
    year_month DATE,
    total_spending DECIMAL(10, 2),
    total_income DECIMAL(10, 2),
    net_spending DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE category_wise_spending (
    spending_id SERIAL PRIMARY KEY,
    year_month DATE,
    category VARCHAR(100),
    total_amount DECIMAL(10, 2),
    transaction_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);