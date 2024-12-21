import sys
from datetime import date

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    create_engine,
    func,
    ForeignKey,
    text,
    extract,
)
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Satellite(Base):
    __tablename__ = "satellite"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    production_date = Column(Date)
    country = Column(String)


class Flight(Base):
    __tablename__ = "flight"

    id = Column(Integer, primary_key=True)
    satellite_id = Column(Integer, ForeignKey(Satellite.id))
    launch_date = Column(Date)
    launch_time = Column(Time)
    weekday = Column(String)
    type = Column(Integer)


# Using local database
# - host: localhost
# - port: 5432
# - name: postgres
# - user: postgres
# - password: postgres
DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def create_tables():
    Base.metadata.create_all(engine)
    print("Tables created successfully.")

    satellites = [
        Satellite(
            id=1, name="SIT-2086", production_date="2050-01-01", country="Россия"
        ),
        Satellite(
            id=2, name="Шинзян 16-02", production_date="2049-12-01", country="Китай"
        ),
    ]

    flights = [
        Flight(
            id=1,
            satellite_id=1,
            launch_date="2050-05-11",
            launch_time="09:00:00",
            weekday="Среда",
            type=1,
        ),
        Flight(
            id=2,
            satellite_id=1,
            launch_date="2051-06-14",
            launch_time="23:05:00",
            weekday="Среда",
            type=0,
        ),
        Flight(
            id=3,
            satellite_id=1,
            launch_date="2051-10-10",
            launch_time="23:50:00",
            weekday="Вторник",
            type=1,
        ),
        Flight(
            id=4,
            satellite_id=2,
            launch_date="2050-05-11",
            launch_time="15:15:00",
            weekday="Среда",
            type=1,
        ),
        Flight(
            id=5,
            satellite_id=1,
            launch_date="2052-01-01",
            launch_time="12:15:00",
            weekday="Понедельник",
            type=0,
        ),
    ]

    session.add_all(satellites)
    session.commit()

    session.add_all(flights)
    session.commit()

    print("Sample data inserted successfully.")


def find_countries_with_less_than_55_satellites_sql():
    result = session.execute(
        text(
            """
                SELECT country
                FROM satellite
                GROUP BY country
                HAVING COUNT(id) < 55;
            """
        )
    ).fetchall()
    return result


def find_countries_with_less_than_55_satellites():
    result = (
        session.query(Satellite.country)
        .group_by(Satellite.country)
        .having(func.count(Satellite.id) < 55)
        .all()
    )
    return result


def find_first_returned_satellite_this_year_sql():
    result = session.execute(
        text(
            """
                SELECT s.name
                FROM satellite s
                JOIN flight f ON s.id = f.satellite_id
                WHERE f.type = 0
                  AND EXTRACT(YEAR FROM f.launch_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                ORDER BY f.launch_date
                LIMIT 1;
            """
        )
    ).fetchone()
    return result


def find_first_returned_satellite_this_year():
    result = (
        session.query(Satellite.name)
        .join(Flight, Satellite.id == Flight.satellite_id)
        .filter(Flight.type == 0)
        .filter(extract("year", Flight.launch_date) == date.today().year)
        .order_by(Flight.launch_date.asc())
        .first()
    )
    return result


def find_russian_satellites_launching_before_september_2024_sql():
    result = session.execute(
        text(
            """
                SELECT s.name
                FROM satellite s
                JOIN flight f ON s.id = f.satellite_id
                WHERE s.country = 'Россия'
                  AND f.type = 1
                  AND EXTRACT(YEAR FROM f.launch_date) = 2024
                  AND f.launch_date <= '2024-09-01';
            """
        )
    ).fetchall()
    return result


def find_russian_satellites_launching_before_september_2024():
    result = (
        session.query(Satellite.name)
        .join(Flight, Satellite.id == Flight.satellite_id)
        .filter(Flight.type == 1)
        .filter(Satellite.country == "Россия")
        .filter(extract("year", Flight.launch_date) == 2024)
        .filter(Flight.launch_date <= "2024-09-01")
        .all()
    )
    return result


def execute_queries():
    print(
        f"find_countries_with_less_than_55_satellites_sql: {find_countries_with_less_than_55_satellites_sql()}"
    )
    print(
        f"find_countries_with_less_than_55_satellites: {find_countries_with_less_than_55_satellites()}"
    )

    print(
        f"find_first_returned_satellite_this_year_sql: {find_first_returned_satellite_this_year_sql()}"
    )
    print(
        f"find_first_returned_satellite_this_year: {find_first_returned_satellite_this_year()}"
    )

    print(
        f"find_russian_satellites_launching_before_september_2024_sql: {find_russian_satellites_launching_before_september_2024_sql()}"
    )
    print(
        f"find_russian_satellites_launching_before_september_2024: {find_russian_satellites_launching_before_september_2024()}"
    )


if __name__ == "__main__":
    if len(sys.argv) == 1:
        execute_queries()
    elif len(sys.argv) == 2 and sys.argv[1] == "--create-tables":
        create_tables()
    else:
        print("Usage: python main.py [--create-tables]")
        exit(1)
