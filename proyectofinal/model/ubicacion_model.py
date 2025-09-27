from sqlmodel import SQLModel, Field

class UbicacionLocal(SQLModel, table=True):
    id: int = Field(default=1, primary_key=True)
    lat: float
    lng: float