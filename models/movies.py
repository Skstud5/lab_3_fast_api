from sqlalchemy import Column, String, Integer, Identity, Sequence, Float, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Director(Base):
    __tablename__ = "directors"
    id = Column(Integer, Sequence("director_sequence"), primary_key=True)
    name = Column(String, index=True, nullable=False)
    birth_date = Column(String)
    country = Column(String)

    # Добавляем отношение к фильмам
    movies = relationship("Movie", back_populates="director")

    class Movie(Base):
        __tablename__ = "movies"
        id = Column(Integer, Sequence("movie_sequence"), primary_key=True)
        title = Column(String, index=True, nullable=False)
        release_year = Column(Integer)
        genre = Column(String)
        rating = Column(Float)
        is_published = Column(Boolean, default=True)
        director_id = Column(Integer, ForeignKey("directors.id"))

        # Добавляем отношение к режиссеру
        director = relationship("Director", back_populates="movies")
