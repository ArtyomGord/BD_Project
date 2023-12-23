from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
import sessions

BASE = declarative_base()

class TransportType(BASE):
    __tablename__ = "TransportTypes"
    _id_ = Column(Integer, primary_key=True, autoincrement=True)
    transport_name = Column(String(32), nullable=False)
    car_count_in_park = Column(Integer)
    average_speed = Column(Float)
    fuel_usage = Column(Float)

class Way(BASE):
    __tablename__ = "Ways"
    _id_ = Column(Integer, primary_key=True, autoincrement=True)
    start = Column(String(32), nullable=False)
    destination = Column(String(32), nullable=False)
    stops_count = Column(Integer)
    distance = Column(Float)

class Route(BASE):
    __tablename__ = "Routes"
    _id_ = Column(Integer, primary_key=True, autoincrement=True)
    transport_type_id = Column(Integer, ForeignKey(TransportType._id_), nullable=False)
    way_id = Column(Integer, ForeignKey(Way._id_), nullable=False)
    route_number = Column(Integer, nullable=False)
    passengers_count = Column(Integer)
    car_count_on_route = Column(Integer)
    travel_fee = Column(Float)