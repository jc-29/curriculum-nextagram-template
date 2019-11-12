from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin


class User_(BaseModel, UserMixin):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)
    role = pw.CharField(default='User')
    profile_picture = pw.TextField(default='https://www.sackettwaconia.com/wp-content/uploads/default-profile.png')

    def validate(self):
        invalid_username = User_.get_or_none(User_.username == self.username)
        invalid_email = User_.get_or_none(User_.email == self.email)

        if invalid_username and invalid_username.id != self.id:
            self.errors.append('Error! Username is already taken!')
        if invalid_email and invalid_username.id != self.id:
            self.errors.append('Error! Email is already taken')
        # if len(self.password) < 8 or len(self.password) > 25:
        #     self.errors.append('Invalid password!')
        
    # def access_profile_picture(self):
    #     return 