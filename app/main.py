from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Station
from app.schemas import Status, StationCreate, StationOut, StationUpdate


@asynccontextmanager
async def lifespan(_: FastAPI):
    # La base est recréée (tables) à chaque lancement si elle n'existe pas.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Dock Control - Stations", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/stations", response_model=StationOut, status_code=201)
def create_station(payload: StationCreate, db: Session = Depends(get_db)):
    station = Station(**payload.model_dump())
    db.add(station)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Code de station déjà utilisé")
    db.refresh(station)
    return station


@app.get("/stations", response_model=list[StationOut])
def list_stations(
    status: Status | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(Station).order_by(Station.id)
    if status is not None:
        stmt = stmt.where(Station.status == status)
    return db.scalars(stmt).all()


@app.get("/stations/{station_id}", response_model=StationOut)
def get_station(station_id: int, db: Session = Depends(get_db)):
    station = db.get(Station, station_id)
    if station is None:
        raise HTTPException(status_code=404, detail="Station introuvable")
    return station


@app.patch("/stations/{station_id}", response_model=StationOut)
def update_station(
    station_id: int, payload: StationUpdate, db: Session = Depends(get_db)
):
    station = db.get(Station, station_id)
    if station is None:
        raise HTTPException(status_code=404, detail="Station introuvable")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(station, field, value)
    db.commit()
    db.refresh(station)
    return station
