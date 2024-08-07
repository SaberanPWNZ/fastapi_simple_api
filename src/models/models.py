# import datetime
#
#
# from sqlalchemy import MetaData, Column, String, Integer, ForeignKey, Table, Float, TIMESTAMP, Boolean
#
# from src.auth.database import Base
#
# metadata_models = MetaData()
#
# #
# users = Table(
#     'user',
#     metadata_models,
#     Column('id', Integer, primary_key=True),
#     Column('username', String, nullable=False),
#     Column('registered_at', TIMESTAMP, default=datetime.datetime.utcnow()),
#     Column('email', String, unique=True, index=True, nullable=False),
#     Column('hashed_password', String, nullable=False),
#     Column('is_active', Boolean, default=True, nullable=False),
#     Column('is_superuser', Boolean, default=False, nullable=False),
#     Column('is_verified', Boolean, default=False, nullable=False),
# )

# class User(Base):
#     __tablename__ = 'user'
#
#     id = Column(Integer, primary_key=True)
#     username = Column(String, nullable=False)
#     registered_at = Column(TIMESTAMP,
#                            default=datetime.datetime.utcnow)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, default=True, nullable=False)
#     is_superuser = Column(Boolean, default=False, nullable=False)
#     is_verified = Column(Boolean, default=False, nullable=False)