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
    dealer_transmission_name = Column(Text)
    dealer_installed_option_codes = Column(ARRAY(Text()))
    dealer_installed_option_descriptions = Column(ARRAY(Text()))
    dealer_additional_specs = Column(Text)
    dealer_doors = Column(Text)
    dealer_drive_type = Column(Text)
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    dealer_images = Column(ARRAY(Text()))
    dealer_certified = Column(Boolean)

    def __init__(self,dealership_id=None,vin=None,mileage=0,is_new=True,stock_number="n/a",
                    dealer_transmission_name="n/a",dealer_installed_option_codes=[],dealer_installed_option_descriptions=[],
                    dealer_additional_specs="n/a",dealer_doors="n/a",dealer_drive_type="n/a",dealer_images=[],dealer_certified=False):
        self.dealership_id = dealership_id
        self.vin = vin
        self.mileage = mileage
        self.is_new = is_new
        self.stock_number = stock_number
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
        string_to_hash = f"{self.dealership_id}{self.vin}"
        self.hash = hashlib.md5(string_to_hash)
        
    def update_record(self,input):
        #TODO: update based on input

        self.update_hash()

    #def update_field_updated_at(self)