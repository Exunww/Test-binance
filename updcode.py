import random
from binance.client import Client

api_key = 'g5WzDVLGoeLnyOBB3Ju529pOfAybLo8OBvVfZx4biZc640NMqW7BUbc2okc7OlWl'
api_secret = '2tLHNBPqebsOTNiAwleerYX4FjySumyh95UlWRsu1tNpMxUcx6FJsFj6iqLWsQIP'
client = Client(api_key, api_secret)


def create_orders(data):
    # Проверка и типизация входных данных
    if not isinstance(data, dict):
        raise ValueError("Неверный формат данных. Ожидается словарь.")
    required_keys = ['volume', 'number', 'amountDif', 'side', 'priceMin', 'priceMax']
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        raise ValueError(f"Отсутствуют обязательные ключи в данных: {', '.join(missing_keys)}")
    if not isinstance(data['volume'], float) or data['volume'] <= 0:
        raise ValueError("Неверный формат объема. Ожидается положительное число.")
    if not isinstance(data['number'], int) or data['number'] <= 0:
        raise ValueError("Неверный формат количества. Ожидается положительное целое число.")
    if not isinstance(data['amountDif'], float) or data['amountDif'] < 0:
        raise ValueError("Неверный формат разброса объема. Ожидается неотрицательное число.")
    if data['side'] not in ['BUY', 'SELL']:
        raise ValueError("Неверное значение стороны ордера. Ожидается 'BUY' или 'SELL'.")
    if not isinstance(data['priceMin'], float) or not isinstance(data['priceMax'], float):
        raise ValueError("Неверный формат минимальной или максимальной цены. Ожидается число.")

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

        try:
            # Создаем ордер
            order = client.create_order(
                symbol='BTCUSDT',
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=final_volume,
                price=str(price)
            )
            print(f"Создан ордер {i+1}/{number}: {order}")
        except Exception as e:
            print(f"Ошибка при создании ордера {i+1}/{number}: {str(e)}")


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

client.RECV_WINDOW = 60000  # Установите значение recvWindow в соответствии с вашими потребностями

create_orders(data)
