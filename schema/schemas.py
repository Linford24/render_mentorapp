from pydantic import BaseModel, Field, EmailStr, computed_field, field_validator, ValidationInfo, RootModel
from typing import Optional, List, Any, Dict
from datetime import datetime
from enum import Enum
import uuid
import json


class Innovator(BaseModel):
    fullname: str
    email: EmailStr
    status: str
    language: str

class InnovatorCreate(Innovator):
    password: str

class InnovatorUpdate(InnovatorCreate):
    pass

class InnovatorResponse(Innovator):
    id: int
    date_joined: datetime

class DynamicCourseContent(RootModel[Dict[str, Any]]):
    pass

    class Config:
        from_attributes = True

class Innovation(BaseModel):
    course_name: str
    course_description: str
    content: Optional[DynamicCourseContent] = None
    course_duration: int
    course_price: str
    course_image_path: str
    course_domain: str
    created_at: datetime
    learners: List[Innovator] = []
    

    """
    Assuming we want just the fullnames of the learners

    @computed_field
    @property
    def learner_fullnames(self) -> List[str]:
        return [learner.fullname for learner in self.learners]
    """

    class Config:
        from_attributes = True

class ShowInnovator(BaseModel):
    id: int
    fullname: str
    email: EmailStr
    status: str
    language: str #make it into a list...so multiple languages can be entered
    date_joined: datetime
    registered_courses: List[Innovation] = []

    class Config:
        from_attributes = True

class InnovationCreate(Innovation):
    pass

class InnovationUpdate(InnovationCreate):
    pass

class InnovationResponse(Innovation):

    @computed_field
    @property
    def specific_innovation_data(self) -> List[Any]:
        return [self.course_name, 
                self.course_price, 
                self.course_duration, 
                self.course_image_path, 
                self.course_domain]

    class Config(Innovation.Config):
        from_attributes = True

class InnovationMaterial(Innovation):

    @computed_field
    @property
    def specific_innovation_material(self) -> List[Any]:
        return [
            self.content,
            self.learners
        ]
    
    class Config(Innovation.Config):
        from_attributes = True

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class RefreshRequest(BaseModel):
    refresh_token: str