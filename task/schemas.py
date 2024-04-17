from typing import Optional
from pydantic import EmailStr, BaseModel


class getTask(BaseModel):
    id: int
    title: Optional[str]
    data: str
    owner: str
    model_config = {
            "json_schema_extra": {
                "examples": [
                    {
                        "id": 1,
                        "title": "Task title",
                        "data": "some data",
                        "owner": "who owner",
                    }
                ]
            }
        }

class addTask(BaseModel):
    title: Optional[str]
    data: str
    owner: str
    # model_config = {
    #         "json_schema_extra": {
    #             "examples": [
    #                 {
    #                     "title": "Task title",
    #                     "data": "some data",
    #                     "owner": "who owner",
    #                 }
    #             ]
    #         }
    #     }