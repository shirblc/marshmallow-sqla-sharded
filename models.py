"""
Defines the SQLAlchemy models that are used to generate the Mashmallow schemas
"""
import sys
import os
from sqlalchemy.ext.horizontal_shard import ShardedSession, ShardedQuery
from sharded_session import shard_chooser, id_chooser, execute_chooser, shards
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
)
from marshmallow_sqlalchemy import (
    SQLAlchemyAutoSchema,
    fields,
)

# Engine
Session = sessionmaker(class_=ShardedSession)
Session.configure(
    shards=shards,
    shard_chooser=shard_chooser,
    id_chooser=id_chooser,
    execute_chooser=execute_chooser,
    query_cls=ShardedQuery,
)


# Models
# -----------------------------------------------------------------
BaseModel = declarative_base()


class Category(BaseModel):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    parent = relationship("Category", remote_side=[id])
    parent_id = Column(Integer, ForeignKey("categories.id"))



class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        include_relationships = True
        include_fk = True

    parent = fields.Nested("PCategorySchema")


class PCategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        include_relationships = True
        include_fk = True