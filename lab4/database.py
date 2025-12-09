from contextlib import contextmanager
from typing import List, Optional, Tuple
from datetime import date, timedelta
from sqlalchemy import create_engine, inspect, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Order, TopCustomer

class DatabaseManager:
    def __init__(self, db_path: str = "company_data.db"):
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.create_tables()

    def table_exists(self, table_name: str) -> bool:
        inspector = inspect(self.engine)
        return table_name in inspector.get_table_names()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def insert_orders(self, orders: List[Order]):
        with self.session_scope() as session:
            try:
                session.add_all(orders)
            except SQLAlchemyError as e:
                raise RuntimeError(f"Ошибка при вставке заказов: {e}")

    def get_top_customers_last_30_days(self, cutoff_date: date, limit: int = 5) -> List[Tuple[str, float]]:
        with self.session_scope() as session:
            try:
                results = (
                    session.query(
                        Order.customer_name,
                        func.sum(Order.quantity * Order.price_per_unit).label('total')
                    )
                    .filter(
                        Order.order_date >= cutoff_date,
                        Order.status == 'completed'
                    )
                    .group_by(Order.customer_name)
                    .order_by(func.sum(Order.quantity * Order.price_per_unit).desc())
                    .limit(limit)
                    .all()
                )
                return [(row[0], float(row[1])) for row in results]
            except SQLAlchemyError as e:
                raise RuntimeError(f"Ошибка при агрегации данных: {e}")

    def save_top_customers(self, top_customers: List[Tuple[str, float]]):
        with self.session_scope() as session:
            try:
                # Очистка предыдущих данных
                session.query(TopCustomer).delete()
                # Вставка новых
                for customer_name, total in top_customers:
                    session.add(TopCustomer(customer_name=customer_name, total_spent=total))
            except SQLAlchemyError as e:
                raise RuntimeError(f"Ошибка при сохранении топ-клиентов: {e}")