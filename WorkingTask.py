import random

def create_orders(data):
    volume = data['volume']
    number = data['number']
    amount_dif = data['amountDif']
    side = data['side']
    price_min = data['priceMin']
    price_max = data['priceMax']

    # Рассчитываем объем каждого ордера
    order_volume = volume / number

    # Создаем ордеры
    for i in range(number):
        # Генерируем случайную цену в диапазоне от price_min до price_max
        price = random.uniform(price_min, price_max)

        # Генерируем случайный разброс объема в пределах amount_dif
        volume_dif = random.uniform(-amount_dif, amount_dif)

        # Вычисляем итоговый объем ордера
        final_volume = order_volume + volume_dif

        # Округляем объем до шага, допустимого на бирже Binance
        step_size = get_step_size(price)
        final_volume = round(final_volume / step_size) * step_size

        # Выводим информацию о создаваемых ордерах
        print(f"Created order {i+1}/{number}: Side: {side}, Price: {price}, Volume: {final_volume}")

def get_step_size(price):
    # Здесь можно добавить логику получения шага объема для конкретной пары торгов
    # В данном примере, для упрощения, просто возвращаем шаг в размере 0.01
    return 0.01

# Пример использования
data = {
    "volume": 10000.0,
    "number": 5,
    "amountDif": 50.0,
    "side": "SELL",
    "priceMin": 200.0,
    "priceMax": 300.0
}

create_orders(data)
