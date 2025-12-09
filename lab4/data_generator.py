import random
from datetime import date, timedelta
from typing import List
from models import Order

def generate_orders(n: int = 150) -> List[Order]:
    customers = [f"Client_{i}" for i in range(1, 21)]
    products = [f"Item_{i}" for i in range(1, 31)]
    statuses = ["completed", "pending", "shipped", "cancelled"]

    start_date = date(2020, 1, 1)
    end_date = date(2025, 12, 9)
    delta_days = (end_date - start_date).days

    orders = []

    # 1. Генерируем основную массу — случайные даты
    main_count = n - 20 
    for i in range(main_count):
        customer = random.choice(customers)
        product = random.choice(products)
        quantity = random.randint(1, 100)
        price = round(random.uniform(10.0, 1000.0), 2)
        random_days = random.randint(0, delta_days)
        order_date = start_date + timedelta(days=random_days)
        status = random.choice(statuses)
        orders.append(
            Order(
                customer_name=customer,
                product=product,
                quantity=quantity,
                price_per_unit=price,
                order_date=order_date,
                status=status
            )
        )

    # 2. Гарантированно добавляем 20 'completed' заказов в последние 30 дней
    recent_start = date(2025, 11, 9)
    recent_end = date(2025, 12, 9)
    for i in range(20):
        customer = random.choice(customers)
        product = random.choice(products)
        quantity = random.randint(50, 200)
        price = round(random.uniform(50.0, 500.0), 2)
        days_offset = random.randint(0, (recent_end - recent_start).days)
        order_date = recent_start + timedelta(days=days_offset)
        orders.append(
            Order(
                customer_name=customer,
                product=product,
                quantity=quantity,
                price_per_unit=price,
                order_date=order_date,
                status="completed"
            )
        )

    return orders