CREATE TABLE dealer_data (
    hash text PRIMARY KEY,
    dealership_id text NOT NULL,
    vin text NOT NULL,
    mileage integer,
    is_new boolean,
    stock_number text,
    dealer_year integer,
    dealer_make text,
    dealer_model text,
    dealer_trim text,
    dealer_model_number text,
    dealer_msrp integer,
    dealer_invoice integer,
    dealer_body text,
    dealer_inventory_entry_date date,
    dealer_exterior_color_description text,
    dealer_interior_color_description text,
    dealer_exterior_color_code text,
    dealer_interior_color_code text,
    dealer_transmission_name text,
    dealer_installed_option_codes text[],
    dealer_installed_option_descriptions text[],
    dealer_additional_specs text,
    dealer_doors text,
    dealer_drive_type text,
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    dealer_images text[],
    dealer_certified boolean
);

CREATE TABLE validation_data (
    id SERIAL PRIMARY KEY,
    provider text NOT NULL,
    record jsonb NOT NULL,
    errors jsonb NOT NULL
);
