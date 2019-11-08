from models.base_model import BaseModel
import peewee as pw


class User_(BaseModel):
    username = pw.CharField(unique=False, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)
