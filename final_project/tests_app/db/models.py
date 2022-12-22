from sqlalchemy import Column, Integer, VARCHAR, SmallInteger, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'test_users'
    __table_args__ = (
        UniqueConstraint('email', name='email'),
        UniqueConstraint('username', name='ix_test_users_username'),
        {'mysql_charset': 'utf8'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(VARCHAR(255), nullable=False)
    surname = Column(VARCHAR(255), nullable=False)
    middle_name = Column(VARCHAR(255), nullable=True)
    username = Column(VARCHAR(16), nullable=True)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(64), nullable=False)
    access = Column(SmallInteger, nullable=True)
    active = Column(SmallInteger, nullable=True)
    start_active_time = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"id:{self.id} - name:{self.name} - surname:{self.surname} - " \
               f"middle_name:{self.middle_name} - username:{self.username} - " \
               f"email:{self.email} - access:{self.access} - active:{self.active} - " \
               f"start_active_time:{self.start_active_time}"
