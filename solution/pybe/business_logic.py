import logging
import pandas as pd
import numpy as np
import datetime
import json
from math import isnan
from database import db
from listing_model import Vehicle_Listing as VL_Obj
from db_models import Validation_Errors as VE_Record,Vehicle_Listing as VL_Record
from pydantic import ValidationError
from lookups import apply_lookups

logger = logging.getLogger(__name__)

mapping_filepath = './pybe/mappings/mappings.xlsx'

def import_listings(provider, filename):

    # Check if provider mapping exists
    try:
        pd.read_excel(mapping_filepath,f"Provider{provider}")
    except Exception as e:
        logger.info("Issue opening file")
        logger.exception(e)
        return {"success":False,"message":f"Mapping does not exist for provider {provider}"}

    logger.info("Generating Vehicle Listings")
    listings = generate_vehicle_listings(provider,filename)
    if listings is None:
        return {"success":False,"message":f"Could not open {filename} for provider {provider}"}
    
    logger.info("Validating and Creating records")
    total = len(listings)
    inserts = 0
    for vl in listings:
        # Apply lookups
        prepped_listing = apply_lookups(provider,vl)
        if prepped_listing is None:
            logger.warning("Cannot apply lookup")
            continue

        # Convert listing to VL_Obj
        vl_obj = generate_vehicle_listing_obj(filename,vl)
        if vl_obj is None:
            continue

        result = vehicle_listing_to_db_record(vl_obj)

        if result['success'] == True:
            inserts += 1


    
    return {"success":True,"message":f"{inserts} of {total} listings added"}

def generate_vehicle_listings(provider, filename):
    import_file = f'./pybe/provider_feeds/provider{provider}/{filename}'
    # Attempt to open the local listing file
    try:
        df_listings = pd.read_csv(import_file,  keep_default_na=False)
    
    except Exception as e:
        msg = f"Could not open csv {import_file}"
        logger.exception(msg)
        return

    """logger.info("Listings:")
    logger.info(df_listings)"""

    # Create the mappings for lookup
    df_mapping = generate_field_mappings()[provider-1]

    listings = []
    # Map the fields
    for i, listing in df_listings.iterrows():
        
        listing_json={}
        # 
        for j, r in df_mapping.iterrows():
            target = r['Target']
            source = r['Source']
            delim = r['Delimiter']
            logger.info(f'Target: {target} | Source: {source} | Delimiter: {delim}')

            # Check if mapping is N/A
            if isinstance(source,str) == False and isnan(source):
                continue
            
            # Check for delimiter
            if isinstance(delim,str) == False and isnan(delim):
                # Set to none if empty string
                if listing.get(source)=='':
                    listing_json[target] = None
                else:
                    listing_json[target] = listing.get(source)
            else:
                # If source is blank just make it an empty array
                if listing.get(source) is None or listing.get(source)=='':
                    listing_json[target] = []
                else:
                    listing_json[target] = listing.get(source).split(delim)



        logger.info(f'Result {i}: ')
        logger.info(listing_json)
        listings.append(listing_json)


    return listings
    


def vehicle_listing_to_db_record(listing_obj:VL_Obj):
    """Add listing to Vehicle Listing table"""

    record = VL_Record(dealership_id=listing_obj.dealership_id,
                vin=listing_obj.vin,
                mileage=listing_obj.mileage,
                is_new=listing_obj.is_new,                
                stock_number=listing_obj.stock_number,
                dealer_year=listing_obj.dealer_year,
                dealer_make=listing_obj.dealer_make,
                dealer_trim=listing_obj.dealer_trim,
                dealer_model_number=listing_obj.dealer_model_number,
                dealer_msrp=listing_obj.dealer_msrp,
                dealer_invoice=listing_obj.dealer_invoice,
                dealer_body=listing_obj.dealer_body,
                dealer_inventory_entry_date=listing_obj.dealer_inventory_entry_date,
                dealer_exterior_color_description=listing_obj.dealer_exterior_color_description,
                dealer_interior_color_description=listing_obj.dealer_interior_color_description,
                dealer_exterior_color_code=listing_obj.dealer_exterior_color_code,
                dealer_interior_color_code=listing_obj.dealer_interior_color_code,
                dealer_transmission_name=listing_obj.dealer_transmission_name,
                dealer_installed_option_codes=listing_obj.dealer_installed_option_codes,
                dealer_installed_option_descriptions=listing_obj.dealer_installed_option_descriptions,
                dealer_additional_specs=listing_obj.dealer_additional_specs,
                dealer_doors=listing_obj.dealer_doors,
                dealer_drive_type=listing_obj.dealer_drive_type,
                dealer_images=listing_obj.dealer_images,
                dealer_certified=listing_obj.dealer_certified)

    try:
        db.session.add(record)
        db.session.commit()
        return {"success":True}
    except Exception as e:
        logger.info("There was an error adding vehicle listing to database")
        logger.exception(e)
        db.session.rollback
        return {"success":False,"message":"Database record error"}

def generate_vehicle_listing_obj(filename,listing_json):
    """Generate a vehicle listing object from json"""
    # Attempt to create a new vl object from the listing_json
    try:
        # Handle Entry Date conversion
        if listing_json.get('dealer_inventory_entry_date') is None:
            entry_date = None
        else:
            entry_date = datetime.datetime.strptime(listing_json.get('dealer_inventory_entry_date'),'%m/%d/%Y')

        listing_obj = VL_Obj(dealership_id=listing_json.get('dealership_id'),
            vin=listing_json.get('vin'),
            mileage=listing_json.get('mileage'),
            is_new=listing_json.get('is_new'),
            stock_number=listing_json.get('stock_number'),
            dealer_year=listing_json.get('dealer_year'),
            dealer_make=listing_json.get('dealer_make'),
            dealer_trim=listing_json.get('dealer_trim'),
            dealer_model_number=listing_json.get('dealer_model_number'),
            dealer_msrp=listing_json.get('dealer_msrp'),
            dealer_invoice=listing_json.get('dealer_invoice'),
            dealer_body=listing_json.get('dealer_body'),
            dealer_inventory_entry_date=entry_date,
            dealer_exterior_color_description=listing_json.get('dealer_exterior_color_description'),
            dealer_interior_color_description=listing_json.get('dealer_interior_color_description'),
            dealer_exterior_color_code=listing_json.get('dealer_exterior_color_code'),
            dealer_interior_color_code=listing_json.get('dealer_interior_color_code'),
            dealer_transmission_name=listing_json.get('dealer_transmission_name'),
            dealer_installed_option_codes=listing_json.get('dealer_installed_option_codes'),
            dealer_installed_option_descriptions=listing_json.get('dealer_installed_option_descriptions'),
            dealer_additional_specs=listing_json.get('dealer_additional_specs'),
            dealer_doors=listing_json.get('dealer_doors'),
            dealer_drive_type=listing_json.get('dealer_drive_type'),
            dealer_images=listing_json.get('dealer_images'),
            dealer_certified=listing_json.get('dealer_certified'))
        
        return listing_obj
    except ValidationError as e:
        # Record validation errors in database
        logger.info("Invalid Vehicle Listing. See issues below")
        logger.info(e.json())
        error_details = VE_Record(
            provider=filename,
            record = listing_json,
            errors = json.loads(e.json())
        )

        try:
            db.session.add(error_details)
            db.session.commit()
        except Exception as e:
            logger.info("There was an error adding error detail to database")
            logger.exception(e)
            db.session.rollback
        
        return
    except Exception as e:
        logger.info("Issue generating object")
        logger.exception(e)
        return
    # If valid return obj
    # If invalid return validation errors

def map_vehicle_listing(provider,filename):
    import_file = f'./pybe/provider_feeds/provider{provider}/{filename}'


def generate_field_mappings():
    providers = 2
    mappings = []
    for i in range(1,providers+1):
        df_mapping = pd.read_excel(mapping_filepath,f"Provider{i}")
        mappings.append(df_mapping)

    return mappings