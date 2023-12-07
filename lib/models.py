from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    #Add the relationship to Freebie
    freebies = relationship("Freebie", backref='company')
    devs= relationship('Dev', secondary='freebies', back_populates='companies')

    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        return freebie
    
    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    #Add the relationship to Freebie
    freebies= relationship('Freebie', backref='dev')
    companies=relationship('Company', secondary='freebies', back_populates='devs')

    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)
    
    def give_away(self, other_dev, freebie):
        if freebie.dev == self:
            freebie.dev = other_dev
    
class Freebie(Base):
    __tablename__='freebies'

    id=Column(Integer(), primary_key=True)
    item_name= Column(String())
    value= Column(Integer())

    #foreign keys
    dev_id=Column(Integer,ForeignKey('devs.id'))
    dev= relationship('Dev', backref='freebies')
    #Assumes a one-to-many relationship with Dev

    company_id=Column(Integer, ForeignKey('companies.id'))
    company=relationship('Company',backref='freebies')
    #Assumes a one-to-many relationship with company

    def __repr__(self):
        return f'<Freebie id={self.id}, item_name={self.item_name}, value={self.value} >'
    
    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'


