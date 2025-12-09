from datetime import date, timedelta
from database import DatabaseManager
from data_generator import generate_orders
from models import Order

def main():
    DB_PATH = "company_data.db"
    DAYS_AGO = 30
    TOP_N = 5

    # Текущая дата по условию задачи
    current_date = date(2025, 12, 9)
    cutoff_date = current_date - timedelta(days=DAYS_AGO)

    db = DatabaseManager(DB_PATH)

    should_populate = False
    with db.session_scope() as session:
        if not db.table_exists("Orders"):
            should_populate = True
        else:
            count = session.query(Order).count()
            if count == 0:
                should_populate = True

    if should_populate:
        print("Таблица 'Orders' отсутствует или пуста. Генерация тестовых данных...")
        orders = generate_orders(150)
        try:
            db.insert_orders(orders)
            print("✅ База данных успешно заполнена 150 тестовыми заказами.")
        except Exception as e:
            print(f"❌ Ошибка при вставке данных: {e}")
            return
    else:
        print("✅ Таблица 'Orders' уже содержит данные. Пропуск генерации.")

    # Этап 2: бизнес-логика — агрегация за последние 30 дней
    try:
        top_customers = db.get_top_customers_last_30_days(cutoff_date, TOP_N)
        print(f"ТОП-{TOP_N} клиентов за период с {cutoff_date} по {current_date}:")
        for i, (name, total) in enumerate(top_customers, 1):
            print(f"  {i}. {name}: {total:.2f} руб.")

        # Этап 3: запись в целевую таблицу
        db.save_top_customers(top_customers)
        print("✅ Результаты записаны в таблицу 'top_customers'.")
    except Exception as e:
        print(f"❌ Ошибка обработки: {e}")

if __name__ == "__main__":
    main()