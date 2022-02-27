from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel



class Vehicle_Listing(BaseModel):
    dealership_id: str
    vin: str
    mileage: Optional[int] = 0
    is_new: Optional[bool] = True
    stock_number: Optional[str]
    dealer_year: Optional[int]    
    dealer_make: Optional[str]
    dealer_model: Optional[str]
    dealer_trim: Optional[str]
    dealer_model_number: Optional[str]
    dealer_msrp: Optional[int]  
    dealer_invoice: Optional[int]  
    dealer_body: Optional[str]
    dealer_inventory_entry_date: Optional[datetime]
    dealer_exterior_color_description: Optional[str]
    dealer_interior_color_description: Optional[str]
    dealer_exterior_color_code: Optional[str]
    dealer_interior_color_code: Optional[str]
    dealer_transmission_name: Optional[str]
    dealer_installed_option_codes: List[str]
    dealer_installed_option_descriptions: List[str]
    dealer_additional_specs: Optional[str]
    dealer_doors: Optional[str]
    dealer_drive_type: Optional[str]
    dealer_images: List[str]
    dealer_certified: Optional[bool]

    