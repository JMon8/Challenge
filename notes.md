# Developer Notes:
## Update thoughts
* I decided to go with an ORM to manage the inserts, and not tie myself up with sql commands
* I would have liked to create a bit more separation between the provider mapping/validation/lookup parts and the insert into the database. I think it would be easier to manage the code base where each provider module would handle the standardization of the data, and leave the target module to not depend on any updateds to providers
    * This would help isolate issues a bit better
* I would have liked to added a file particular for field formatting. Think it would be easier to manage expected date formats there
* I wonder if we could expand the listing_models validation function to check for other issues
* I'd like to remove the db credentials from the code directly

## Data Observations
* For the New/Used lookup, specifically for provider 1, not sure what the default would be if data is not either of those values
* For integer fields (e.g. dealership2.invoice), should we default empty values to 0?
* A couple of the fields from the Provider 1 mapping document did not line up, so I updated the mapping file to use what looked to be the correct field
    * New/Used -> Type
    * Stock # -> Stock
* I implemented the hash function, but I'm unsure of if this database should be updating records or just creating new ones, so currently it just adds new records
    * If we see a vin twice but it has different data, should it be updated?

## Sample listing csv
* I added a sample csv to test some validation
* Can run using '1' as *provider* and 'sample_some_errors' as *csvname* 