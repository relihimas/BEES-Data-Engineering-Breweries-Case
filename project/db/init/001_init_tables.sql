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
    state VARCHAR(100), 
    postal_code VARCHAR(20),
    country VARCHAR(100),
    longitude VARCHAR(100),
    latitude VARCHAR(100),
    phone VARCHAR(100),
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
    state VARCHAR(100), 
    postal_code VARCHAR(20),
    country VARCHAR(100),
    longitude VARCHAR(100),
    latitude VARCHAR(100),
    phone VARCHAR(100),
    website_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
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