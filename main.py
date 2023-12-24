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
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Such ID")
    
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