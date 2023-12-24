import model
import sessions
from fastapi import FastAPI, HTTPException, status
from fastapi import Query


def create_BD():
    engine = sessions.connect_to_base()
    model.BASE.metadata.create_all(engine)

if __name__ == "__main__":
    create_BD()

APP = FastAPI()
SESSION = sessions.connect_to_session()



# CRUD for TransportType



@APP.post("/add_transport", tags=["transport"])
async def add_transport(
    _id_: int, 
    transport_name: str,
    car_count_in_park: int,
    average_speed: float,
    fuel_usage: float
):
    
    if SESSION.query(model.TransportType).filter(model.TransportType._id_==_id_).first() is None:
        obj = model.TransportType(
            _id_=_id_,
            transport_name=transport_name,
            car_count_in_park=car_count_in_park,
            average_speed=average_speed,
            fuel_usage=fuel_usage
        )
        SESSION.add(obj)
        SESSION.commit()
        return f"Transport added: {obj.transport_name}"
    
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID is already used")


@APP.get("/get_transport", tags=["transport"])
async def get_all_transports(skip: int = 0, limit: int = 100):
    transport_query = SESSION.query(model.TransportType).offset(skip).limit(limit)
    return transport_query.all()


@APP.put("/update/{transport_id}", tags=["transport"])
async def update_transport(
    transport_id: int,
    new_transport_name: str,
    new_car_count_in_park: int,
    new_average_speed: float,
    new_fuel_usage: float
):
    new_obj = SESSION.query(model.TransportType).filter(model.TransportType._id_==transport_id).first()
    
    if new_obj is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    
    if new_transport_name:
        new_obj.transport_name = new_transport_name
    if new_car_count_in_park:
        new_obj.car_count_in_park = new_car_count_in_park
    if new_average_speed:
        new_obj.average_speed = new_average_speed
    if new_fuel_usage:
        new_obj.fuel_usage = new_fuel_usage

    SESSION.add(new_obj)
    SESSION.commit()
    return f"Transport with ID '{new_obj._id_}' is updated"


@APP.delete("/delete/{transport_id}", tags=["transport"])
async def delete_transport(transport_id: int):
    obj = SESSION.query(model.TransportType).filter(model.TransportType._id_==transport_id).first()
    if obj is not None:
        if SESSION.query(model.Route).filter(model.Route.transport_type_id==transport_id).first() is None:
            SESSION.delete(obj)
            SESSION.commit()
            return f"Transport {obj.transport_name} deleted"
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")    
    



# -----------------------------------------------------------------------------------------------------
# CRUD for Way



@APP.post("/add_way", tags=["way"])
async def add_way(
    _id_: int, 
    start: str,
    destination: str,
    stops_count: int,
    distance: float
):
    
    if SESSION.query(model.Way).filter(model.Way._id_==_id_).first() is None:
        obj = model.Way(
            _id_=_id_,
            start=start,
            destination=destination,
            stops_count=stops_count,
            distance=distance
        )
        SESSION.add(obj)
        SESSION.commit()
        return f"Way added: {obj._id_}"
    
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID is already used")


@APP.get("/get_way", tags=["way"])
async def get_all_ways(skip: int = 0, limit: int = 100):
    way_query = SESSION.query(model.Way).offset(skip).limit(limit)
    return way_query.all()


@APP.put("/update/{way_id}", tags=["way"])
async def update_way(
    way_id: int,
    new_start: str,
    new_destination: str,
    new_stops_count: int,
    new_distance: float
):
    new_obj = SESSION.query(model.Way).filter(model.Way._id_==way_id).first()
    
    if new_obj is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    
    if new_start:
        new_obj.start = new_start
    if new_destination:
        new_obj.destination = new_destination
    if new_stops_count:
        new_obj.stops_count = new_stops_count
    if new_distance:
        new_obj.distance = new_distance

    SESSION.add(new_obj)
    SESSION.commit()
    return f"Way with ID '{new_obj._id_}' is updated"


@APP.delete("/delete/{way_id}", tags=["way"])
async def delete_way(way_id: int):
    obj = SESSION.query(model.Way).filter(model.Way._id_==way_id).first()
    if obj is not None:
        if SESSION.query(model.Route).filter(model.Route.way_id==way_id).first() is None:
            SESSION.delete(obj)
            SESSION.commit()
            return f"Way '{obj.start} - {obj.destination}' deleted"
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")



# -----------------------------------------------------------------------------------------------------
# CRUD for Routes



@APP.post("/add_route", tags=["route"])
async def add_route(
    _id_: int,
    transport_type_id: int,
    way_id: int,
    route_number: int,
    passengers_count: int,
    car_count_on_route: int,
    travel_fee: float
):
    
    if SESSION.query(model.Route).filter(model.Route._id_==_id_).first() is None:
        if SESSION.query(model.TransportType).filter(model.TransportType._id_==transport_type_id).first() is not None:
            if SESSION.query(model.Way).filter(model.Way._id_==way_id).first() is not None:
                obj = model.Route(
                    _id_=_id_,
                    transport_type_id=transport_type_id,
                    way_id=way_id,
                    route_number=route_number,
                    passengers_count=passengers_count,
                    car_count_on_route=car_count_on_route,
                    travel_fee=travel_fee
                )
                SESSION.add(obj)
                SESSION.commit()
                return f"Route added: {obj._id_}"
    
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID is already used")


@APP.get("/get_route", tags=["route"])
async def get_all_routes(skip: int = 0, limit: int = 100):
    route_query = SESSION.query(model.Route).offset(skip).limit(limit)
    return route_query.all()


@APP.put("/update/{route_id}", tags=["route"])
async def update_route(
    route_id: int,
    new_transport_type_id: int,
    new_way_id: int,
    new_route_number: int,
    new_passengers_count: int,
    new_car_count_on_route: int,
    new_travel_fee: float
):
    new_obj = SESSION.query(model.Route).filter(model.Route._id_==route_id).first()
    
    if new_obj is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    
    if new_transport_type_id:
        new_obj.transport_type_id = new_transport_type_id
    if new_way_id:
        new_obj.way_id = new_way_id
    if new_route_number:
        new_obj.route_number = new_route_number
    if new_passengers_count:
        new_obj.passengers_count = new_passengers_count
    if new_car_count_on_route:
        new_obj.car_count_on_route = new_car_count_on_route
    if new_travel_fee:
        new_obj.travel_fee = new_travel_fee

    SESSION.add(new_obj)
    SESSION.commit()
    return f"Route with ID '{new_obj._id_}' is updated"


@APP.delete("/delete/{route_id}", tags=["route"])
async def delete_route(route_id: int):
    obj = SESSION.query(model.Route).filter(model.Route._id_==route_id).first()
    if obj is not None:
        SESSION.delete(obj)
        SESSION.commit()
        return f"Route with ID {obj._id_} deleted"
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")