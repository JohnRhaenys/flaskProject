from sqlalchemy import Column, Integer, String


from sqlalchemy.orm import relationship

from core.database import db, ma


class Sector(db.Model):

    fields = ('name',)

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    # Creates a pseudo column in the Collaborator table
    collaborators = relationship('Collaborator', backref='sector')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'ID: {Sector.id}, NAME: {self.name}'

    @staticmethod
    def get_types():

        from validators import type_validator

        types = {
            'name': type_validator.is_string,
        }

        return types


class SectorSchema(ma.Schema):
    class Meta:
        fields = Sector.fields


# Init sector schema
sector_schema = SectorSchema()
sectors_schema = SectorSchema(many=True)
