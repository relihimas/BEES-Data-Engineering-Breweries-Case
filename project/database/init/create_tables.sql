CREATE TABLE IF NOT EXISTS bronze_breweries_simulation (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    brewery_type TEXT NOT NULL,
    address_1 TEXT,
    address_2 TEXT,
    address_3 TEXT,
    street TEXT,
    city TEXT,
    state_province TEXT,
    state TEXT,
    postal_code TEXT,
    country TEXT NOT NULL,
    longitude NUMERIC(9,6),
    latitude NUMERIC(9,6),
    phone TEXT,
    website_url TEXT,
    ingestion_timestamp TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bronze_breweries (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    brewery_type TEXT NOT NULL,
    address_1 TEXT,
    address_2 TEXT,
    address_3 TEXT,
    street TEXT,
    city TEXT,
    state_province TEXT,
    state TEXT,
    postal_code TEXT,
    country TEXT NOT NULL,
    longitude NUMERIC(9,6),
    latitude NUMERIC(9,6),
    phone TEXT,
    website_url TEXT,
    batch_id UUID NOT NULL,
    ingestion_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (id, batch_id)
);

CREATE INDEX idx_bronze_batch_id ON bronze_breweries(batch_id);
CREATE INDEX idx_bronze_country ON bronze_breweries(country);
CREATE INDEX idx_bronze_state ON bronze_breweries(state);
CREATE INDEX idx_bronze_city ON bronze_breweries(city);

CREATE TABLE IF NOT EXISTS silver_breweries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    brewery_type TEXT NOT NULL,
    city TEXT,
    state TEXT,
    country TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT brewery_type_not_empty CHECK (length(brewery_type) > 0)
);

CREATE INDEX idx_silver_country_state ON silver_breweries(country, state);
CREATE INDEX idx_silver_city ON silver_breweries(city);

CREATE TABLE IF NOT EXISTS gold_breweries (
    country TEXT NOT NULL,
    state TEXT NOT NULL,
    city TEXT NOT NULL,
    brewery_type TEXT NOT NULL,
    brewery_count INTEGER NOT NULL CHECK (brewery_count >= 0),
    PRIMARY KEY (country, state, city, brewery_type)
);