-- Create index if it does not exist

CREATE INDEX idx_name_first_score ON names (name(1), score);

