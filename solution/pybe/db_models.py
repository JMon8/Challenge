import datetime
import hashlib
from database import db
from sqlalchemy import ARRAY, Boolean, Column, Date, DateTime, Integer, Text, text
from sqlalchemy.sql.elements import TextClause as text
from sqlalchemy.dialects.postgresql import JSONB

class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self,column.name)
            if not isinstance(
                getattr(self,column.name),(datetime.datetime,datetime.date)
            )
            else getattr(self,column.name).isoformat()
            for column in self.__table__.columns
        }

class AbstractModel(db.Model,DictMixIn):
    __abstract__ = True
    pass

class Vehicle_Listing(AbstractModel):
    __tablename__ = 'dealer_data'
    __table_args__ = {'schema': 'public'}

    hash = Column(Text, primary_key=True)
    dealership_id = Column(Text, nullable=False)
    vin = Column(Text, nullable=False)
    mileage = Column(Integer)
    is_new = Column(Boolean)
    stock_number = Column(Text)
    dealer_year = Column(Integer)
    dealer_make = Column(Text)
    dealer_model = Column(Text)
    dealer_trim = Column(Text)
    dealer_model_number = Column(Text)
    dealer_msrp = Column(Integer)
    dealer_invoice = Column(Integer)
    dealer_body = Column(Text)
    dealer_inventory_entry_date = Column(Date)
    dealer_exterior_color_description = Column(Text)
    dealer_interior_color_description = Column(Text)
    dealer_exterior_color_code = Column(Text)
    dealer_interior_color_code = Column(Text)
    dealer_transmission_name = Column(Text)
    dealer_installed_option_codes = Column(ARRAY(Text()))
    dealer_installed_option_descriptions = Column(ARRAY(Text()))
    dealer_additional_specs = Column(Text)
    dealer_doors = Column(Text)
    dealer_drive_type = Column(Text)
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    dealer_images = Column(ARRAY(Text()))
    dealer_certified = Column(Boolean)

    def __init__(self,dealership_id=None,vin=None,mileage=0,is_new=True,stock_number=None,dealer_year=None,dealer_make=None,
                    dealer_trim=None,dealer_model_number=None,dealer_msrp=None,dealer_invoice=None,dealer_body=None,dealer_inventory_entry_date=None,                    
                    dealer_exterior_color_description = None,dealer_interior_color_description = None,
                    dealer_exterior_color_code = None, dealer_interior_color_code = None,
                    dealer_transmission_name=None,dealer_installed_option_codes=[],dealer_installed_option_descriptions=[],
                    dealer_additional_specs=None,dealer_doors=None,dealer_drive_type=None,dealer_images=[],dealer_certified=False):
        self.dealership_id = dealership_id
        self.vin = vin
        self.mileage = mileage
        self.is_new = is_new
        self.stock_number = stock_number
        self.dealer_year=dealer_year
        self.dealer_make=dealer_make        
        self.dealer_trim=dealer_trim
        self.dealer_model_number=dealer_model_number
        self.dealer_msrp=dealer_msrp
        self.dealer_invoice=dealer_invoice
        self.dealer_body=dealer_body
        self.dealer_inventory_entry_date=dealer_inventory_entry_date                            
        self.dealer_exterior_color_description = dealer_exterior_color_description
        self.dealer_interior_color_description = dealer_interior_color_description        
        self.dealer_exterior_color_code = dealer_exterior_color_code
        self.dealer_interior_color_code = dealer_interior_color_code        
        self.dealer_transmission_name = dealer_transmission_name
        self.dealer_installed_option_codes = dealer_installed_option_codes
        self.dealer_installed_option_descriptions = dealer_installed_option_descriptions
        self.dealer_additional_specs = dealer_additional_specs
        self.dealer_doors = dealer_doors
        self.dealer_drive_type = dealer_drive_type
        self.dealer_images = dealer_images
        self.dealer_certified = dealer_certified

        self.update_hash()

    def update_hash(self):
        string_to_hash = f"{self.dealership_id}{self.vin}{self.mileage}{self.is_new}{self.stock_number}{self.dealer_transmission_name}{self.dealer_installed_option_codes}{self.dealer_installed_option_descriptions}{self.dealer_additional_specs}{self.dealer_doors}{self.dealer_drive_type}{self.dealer_images}{self.dealer_certified}"
        self.hash = hashlib.md5(string_to_hash.encode()).hexdigest()
        

class Validation_Errors(AbstractModel):
    __tablename__ = 'validation_data'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"public\".validation_data_id_seq'::regclass)"))
    provider = Column(Text, nullable=False)
    record = Column(JSONB(astext_type=Text()), nullable=False)
    errors = Column(JSONB(astext_type=Text()), nullable=False)

    def __init__(self,provider=None, record={},errors={}) -> None:
        self.provider=provider
        self.record=record
        self.errors=errors