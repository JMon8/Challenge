import logging
import pandas as pd
import numpy as np
from database import db
from listing_model import Vehicle_Listing as VL_Obj
from db_models import Vehicle_Listing as VL_Record

logger = logging.getLogger(__name__)

mapping_filepath = './pybe/mappings/mappings.xlsx'

def import_listings(provider, filename):
    import_file = f'./pybe/provider_feeds/provider{provider}/{filename}'
    try:
        df_listings = pd.read_csv(import_file)
    
    except Exception as e:
        msg = f"Could not open csv {import_file}"
        logger.exception(msg)
        return {"success":False,"message":f"Could not open {filename} for provider {provider}"}
        
    logger.info("Listings:")
    logger.info(df_listings)

    return {"success":True}

    
def vehicle_listing_to_db_record(listing_obj:VL_Obj):
    """Convert listing_obj to a Vehicle Listing record"""
    record = VL_Record(listing_obj.dealership_id,listing_obj.vin,listing_obj.mileage,listing_obj.is_new,
                listing_obj.stock_number,listing_obj.dealer_transmission_name,listing_obj.dealer_installed_option_codes,
                listing_obj.dealer_installed_option_descriptions, listing_obj.dealer_additional_specs,
                listing_obj.dealer_doors, listing_obj.dealer_drive_type, listing_obj.dealer_images,
                listing_obj.dealer_certified)

    try:
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        logger.info("There was an error adding vehicle listing to database")
        logger.exception(e)
        db.session.rollback

def generate_vehicle_listing_obj(listing_json):
    """Generate a vehicle listing object from json"""
    # Attempt to create a new vl object from the listing_json
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