from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import os


# Create data folder
os.makedirs("data", exist_ok=True)


# Database
DATABASE_URL = "sqlite:///data/lost_found.db"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)


# --------------------------------------------------
# ITEM TABLE
# --------------------------------------------------

class Item(Base):

    __tablename__ = "items"

    id = Column(
        Integer,
        primary_key=True
    )

    item_type = Column(
        String(20)
    )

    name = Column(
        String(100)
    )

    description = Column(
        Text
    )

    location = Column(
        String(200)
    )

    image_path = Column(
        String(300)
    )

    contact = Column(
        String(100)
    )


# Create table
Base.metadata.create_all(engine)


# --------------------------------------------------
# ADD ITEM
# --------------------------------------------------

def add_item(
    item_type,
    name,
    description,
    location,
    image_path,
    contact
):

    db = SessionLocal()

    item = Item(

        item_type=item_type,

        name=name,

        description=description,

        location=location,

        image_path=image_path,

        contact=contact
    )

    db.add(item)

    db.commit()

    db.close()


# --------------------------------------------------
# GET ITEMS
# --------------------------------------------------

def get_items(item_type=None):

    db = SessionLocal()

    if item_type:

        items = db.query(Item).filter(
            Item.item_type == item_type
        ).all()

    else:

        items = db.query(Item).all()

    db.close()

    return items