from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey

from core.database import db, ma


class Collaborator(db.Model):

    fields = ('collab_number', 'full_name', 'birth_date', 'current_salary', 'active', 'sector_name')

    id = Column(Integer, primary_key=True)

    collab_number = Column(Integer, nullable=False)
    full_name = Column(String(100), nullable=False)
    birth_date = Column(String, nullable=False)  # Change to DateTime
    current_salary = Column(Float, nullable=False)
    active = Column(Boolean, nullable=False)
    sector_id = Column(Integer, ForeignKey('sector.id'), nullable=False)

    def __init__(self, collab_number, full_name, birth_date, current_salary, active, sector_name):

        # Used to find a single collaborator in the database
        # Analogy: like someone's social security number or a student number in a school
        self.collab_number = collab_number

        self.full_name = full_name
        self.birth_date = birth_date
        self.current_salary = current_salary
        self.active = active
        self.sector_name = sector_name

    def __repr__(self):
        status = 'Active' if self.active else 'Inactive'
        return f'Database id: {Collaborator.id}, Collab number: {self.collab_number}, ' \
               f'Full name: {self.full_name}, Date of Birth: {self.birth_date},' \
               f' Current Salary: {self.current_salary}, Status: {status}, Sector name: {self.sector_name}'

    @staticmethod
    def get_types():
        """
        Returns a dictionary that maps an attribute to its type
        (Used by the validator)
        """
        from validators import type_validator
        return {
            'collab_number': type_validator.is_int,
            'full_name': type_validator.is_string,
            'birth_date': type_validator.is_string,
            'current_salary': type_validator.is_float,
            'active': type_validator.is_bool,
            'sector_name': type_validator.is_string
        }


class CollaboratorSchema(ma.Schema):
    class Meta:
        # We set this to True in order to keep the JSON response ordered
        ordered = True
        fields = Collaborator.fields


collaborator_schema = CollaboratorSchema()
collaborators_schema = CollaboratorSchema(many=True)
