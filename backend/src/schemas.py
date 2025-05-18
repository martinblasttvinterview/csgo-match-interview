from pydantic import BaseModel, ConfigDict


class _Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DataResponse[T: BaseModel](_Base):
    data: T
