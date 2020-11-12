from sqlalchemy import Column, Integer, String


from sqlalchemy.orm import relationship

from core.database import db, ma

from marshmallow import fields


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


class SectorSchema(ma.Schema):

    name = fields.Str(required=True)

    class Meta:
        fields = Sector.fields


sector_schema = SectorSchema()
sectors_schema = SectorSchema(many=True)
