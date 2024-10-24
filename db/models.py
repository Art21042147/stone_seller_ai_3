from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class Brand(Base):
    __tablename__ = 'manufacture'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(500))

    colors: Mapped[list["Color"]] = relationship(back_populates="brand")
    orders: Mapped[list["Order"]] = relationship(back_populates="brand")


class Color(Base):
    __tablename__ = 'color'

    id: Mapped[int] = mapped_column(primary_key=True)
    color: Mapped[str] = mapped_column(String(30))
    price: Mapped[int] = mapped_column()
    brand_id: Mapped[int] = mapped_column(ForeignKey('manufacture.id'))

    brand: Mapped["Brand"] = relationship(back_populates="colors")
    orders: Mapped[list["Order"]] = relationship(back_populates="color")


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(30))
    phone: Mapped[int] = mapped_column()
    address: Mapped[str] = mapped_column(String(100))
    length: Mapped[int] = mapped_column()
    width: Mapped[int] = mapped_column()
    cost: Mapped[int] = mapped_column()
    brand_id: Mapped[int] = mapped_column(ForeignKey('manufacture.id'))
    color_id: Mapped[int] = mapped_column(ForeignKey('color.id'))

    brand: Mapped["Brand"] = relationship(back_populates="orders")
    color: Mapped["Color"] = relationship(back_populates="orders")


async def async_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
