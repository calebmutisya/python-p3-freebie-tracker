#!/usr/bin/env python3
from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie, Base

fake = Faker()
# Script goes here!
if __name__ == '__main__':
    
    engine = create_engine('sqlite:///freebies.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # # Create some companies, devs, and freebies
    # company1 = Company(name="Company1", founding_year=2000)
    # company2 = Company(name="Company2", founding_year=2010)
    # session.add_all([company1, company2])
    # session.commit()

    # dev1 = Dev(name="Dev1")
    # dev2 = Dev(name="Dev2")
    # session.add_all([dev1, dev2])
    # session.commit()

    # freebie1 = Freebie(item_name="Item1", value=100, dev=dev1, company=company1)
    # freebie2 = Freebie(item_name="Item2", value=200, dev=dev1, company=company2)
    # freebie3 = Freebie(item_name="Item3", value=150, dev=dev2, company=company1)
    # session.add_all([freebie1, freebie2, freebie3])
    # session.commit()

    # # Relationships and methods
    # print(f"Dev1's Freebies: {dev1.freebies}")
    # print(f"Dev1's Companies: {dev1.companies}")

    # print(f"Company1's Freebies: {company1.freebies}")
    # print(f"Company1's Devs: {company1.devs}")

    company = Company(name='Company1', founding_year=1990)
    dev = Dev(name='Dev1')
    freebie = Freebie(item_name='Item1', value=50, dev=dev, company=company)

    # Print details of the freebie
    print(freebie.print_details())

    # Give a freebie from a company to a dev
    new_dev = Dev(name='Dev2')
    company.give_freebie(new_dev, 'Item2', 100)

    # Find the oldest company
    oldest_company = Company.oldest_company(session)
    print(f'Oldest Company: {oldest_company.name}')
