CREATE TABLE IF NOT EXISTS bronze_breweries_simulation (
    id VARCHAR(36) PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    brewery_type VARCHAR(50) NOT NULL,
    address_1 VARCHAR(255),
    address_2 VARCHAR(255),
    address_3 VARCHAR(255),
    street VARCHAR(255),
    city VARCHAR(100),
    state_province VARCHAR(100),
    state VARCHAR(50), 
    postal_code VARCHAR(20),
    country VARCHAR(100) NOT NULL,
    longitude VARCHAR(50),
    latitude VARCHAR(50),
    phone VARCHAR(50),
    website_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bronze_breweries (
    id VARCHAR(36) PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    brewery_type VARCHAR(50) NOT NULL,
    address_1 VARCHAR(255),
    address_2 VARCHAR(255),
    address_3 VARCHAR(255),
    street VARCHAR(255),
    city VARCHAR(100),
    state_province VARCHAR(100),
    state VARCHAR(50), 
    postal_code VARCHAR(20),
    country VARCHAR(100) NOT NULL,
    longitude VARCHAR(50),
    latitude VARCHAR(50),
    phone VARCHAR(50),
    website_url VARCHAR(255),
    batch_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bronze_monitor (
    total_amount_breweries INTEGER NOT NULL,
    source_endpoint VARCHAR(500) NOT NULL,
    source_query VARCHAR(500) NOT NULL,
    creation_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    batch_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS silver_breweries (
    name VARCHAR(255) NOT NULL,
    brewery_type VARCHAR(50) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(50), 
    country VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gold_breweries (
    country VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL, 
    city VARCHAR(100) NOT NULL,
    brewery_type VARCHAR(50) NOT NULL,
    brewery_count INTEGER NOT NULL
);