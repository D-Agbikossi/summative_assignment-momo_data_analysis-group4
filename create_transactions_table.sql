CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,  -- Unique transaction ID (auto-incremented)
    category VARCHAR(255) NOT NULL,     -- Category of the transaction
    transaction_date DATE NOT NULL,     -- Date of the transaction
    transaction_time TIME NOT NULL,     -- Time of the transaction
    amount INTEGER NOT NULL,            -- Amount in the transaction (with decimal precision)
    sms_transaction_id VARCHAR(255),    -- Transaction ID from SMS (if available)
    sms_body TEXT,                      -- Raw SMS body
    UNIQUE (sms_transaction_id)         -- Prevent duplicate SMS transaction IDs
);
