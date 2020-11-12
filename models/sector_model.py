from sqlalchemy import Column, Integer, String


from sqlalchemy.orm import relationship

from core.database import db, ma


class Sector(db.Model):

    fields = ('name',)

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    # Creates a pseudo column in the Collaborator table
    collaborators = relationship('Collaborator', cascade='all,delete', backref='sector')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Database id: {Sector.id}, Sector name: {self.name}'

    @staticmethod
    def get_types():
        """
        Returns a dictionary that maps an attribute to its type
        (Used by the validator)
        """
        from validators import type_validator
        return {'name': type_validator.is_string}


class SectorSchema(ma.Schema):
    class Meta:
        fields = Sector.fields


sector_schema = SectorSchema()
sectors_schema = SectorSchema(many=True)
