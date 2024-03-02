from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from tortoise import Model, fields
from passlib.hash import bcrypt
from tortoise.contrib.pydantic import pydantic_model_creator

class RankModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)

    class Meta:
        table = "ranks"
class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=255)
    email = fields.CharField(max_length=100, null=False, unique=True, default='default@example.com')
    name = fields.CharField(max_length=50)
    surname = fields.CharField(max_length=50)
    thirdname = fields.CharField(max_length=50, null=True)
    rank = fields.ForeignKeyField("models.RankModel", related_name="users")
    unit = fields.CharField(max_length=50)
    is_admin = fields.BooleanField(default=False)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    class Meta:
        table = "users"


User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)

class OrderModel(Model):
    id = fields.IntField(pk=True)
    number_order = fields.CharField(max_length=10, unique=True, null=True)
    customer = fields.ForeignKeyField("models.User", related_name="orders")
    technics = fields.JSONField(default=list, null=True)
    total_cost = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_active = fields.BooleanField(default=False)
    unit = fields.CharField(max_length=50)
    time_of_execution = fields.DatetimeField()

    class Meta:
        table = "orders"



class UserDTO(BaseModel):
    username: str
    password: str
    email: str
    name: str
    surname: str
    thirdname: str
    unit: str
    is_admin: Optional[bool] = False
    rank_id: int

class LoginDTO(BaseModel):
    email: str
    password: str

class OrderDTO(BaseModel):
    number_order: str
    technics: List[object]
    total_cost: float
    is_active: Optional[bool] = False
    time_of_execution: datetime
