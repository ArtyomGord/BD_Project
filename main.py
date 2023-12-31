import model
import sessions
from fastapi import FastAPI, HTTPException, status
from fastapi import Query
from random import randint, uniform
from faker import Faker

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





# ------------------------------------------------------------------------------------
# Data generation script



fake = Faker()

@APP.post("/generate_transports", tags=["transport"])
async def generate_transports(n: int):
    index = 0
    while index != n:
        if SESSION.query(model.TransportType).filter(model.TransportType._id_==index).first() is not None:
            index += 1
            n += 1
            continue
        obj = model.TransportType(
            _id_=index,
            transport_name=fake.word(),
            car_count_in_park=randint(1, 100),
            average_speed=round(uniform(10, 70), 2),
            fuel_usage=round(uniform(5, 20), 2)
        )
        SESSION.add(obj)
        SESSION.commit()
        index += 1
    return 

@APP.post("/generate_ways", tags=["way"])
async def generate_ways(n: int):
    index = 0
    while index != n:
        if SESSION.query(model.Way).filter(model.Way._id_==index).first() is not None:
            index += 1
            n += 1
            continue
        obj = model.Way(
            _id_=index,
            start=fake.city(),
            destination=fake.city(),
            stops_count=randint(5, 50),
            distance=round(uniform(10, 500), 2)
        )
        SESSION.add(obj)
        SESSION.commit()
        index += 1
    return 

@APP.post("/generate_routes", tags=["route"])
async def generate_routes(n: int):
    index = 0
    while index != n:
        # (route.id == index) && (route.tr_id = transport.id) 
        if SESSION.query(model.TransportType, model.Route).filter(model.TransportType._id_==model.Route.transport_type_id and model.Route._id_==index).first() is not None:
            if SESSION.query(model.Way, model.Route).filter(model.Way._id_==model.Route.way_id and model.Route._id_==index).first() is not None:
                if SESSION.query(model.Route).filter(model.Route._id_==index).first() is not None:
                    index += 1
                    n += 1
                    continue
            else: return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Way ID limit reached")
        else: return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transport ID limit reached")
        
        generated_route = model.Route(
            _id_=index,
            transport_type_id=randint(1, 99),
            way_id=randint(1, 99), 
            route_number=randint(1, 100),
            passengers_count=randint(0, 50),
            car_count_on_route=randint(0, 200),
            travel_fee=round(uniform(100, 1000), 2)
        )
        SESSION.add(generated_route)
        SESSION.commit()
        index += 1
    return





# -------------------------------------------------------------------------
# REQUESTS


# JOIN
# table1.join(table2, table1.param == table2.param)

@APP.get("/transport_and_way_join", tags=["requests"])
async def get_transport_and_way():
    transport_and_way_query = SESSION.query(model.TransportType).join(model.Way, 
        model.TransportType._id_ == model.Way._id_)
    return transport_and_way_query.all()



# SELECT

@APP.get("/select_from_transports", tags=["requests"])
async def get_transports_where(speed: float = 0, fuel_usage: float = 10):
    transport_query = SESSION.query(model.TransportType).filter(
        (model.TransportType.average_speed > speed)
        & (model.TransportType.fuel_usage < fuel_usage)
    )
    return transport_query.all()



# UPDATE

@APP.put("/update_actors_rank", tags=["requests"])
async def update_way_distance(
        stops_count: int = Query(..., description="input stops_count"),
        distance: float = Query(..., description="input distance")
    ):
    way_query = SESSION.query(model.Way).filter(model.Way.stops_count > stops_count).update({"distance": distance})
    SESSION.commit()



# SORT
    
@APP.get("/sort_routes", tags=["requests"])
async def sort_routes_by_travel_fee():
    route_query = SESSION.query(model.Route).order_by(model.Route.travel_fee)
    return route_query.all()


# GROUP BY

@APP.get("/group_way_by_start_and_destination", tags=["requests"])
async def group_ways():
    way_query = SESSION.query(model.Way.start, model.Way.destination).group_by(
        model.Way.start, model.Way.destination).all()
    return [{"start": start, "destination": destination} for start, destination in way_query]