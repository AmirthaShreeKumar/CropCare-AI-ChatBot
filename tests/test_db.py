import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Dummy(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    yield s
    s.close()
    engine.dispose()

def test_crud_operations(session):
    obj = Dummy(name="test")
    session.add(obj)
    session.commit()
    fetched = session.query(Dummy).filter_by(name="test").first()
    assert fetched is not None
    assert fetched.name == "test"
    fetched.name = "updated"
    session.commit()
    assert session.query(Dummy).filter_by(name="updated").count() == 1
    session.delete(fetched)
    session.commit()
    assert session.query(Dummy).count() == 0
