import random
import psycopg2
from binance.client import Client

api_key = 'g5WzDVLGoeLnyOBB3Ju529pOfAybLo8OBvVfZx4biZc640NMqW7BUbc2okc7OlWl'
api_secret = '2tLHNBPqebsOTNiAwleerYX4FjySumyh95UlWRsu1tNpMxUcx6FJsFj6iqLWsQIP'
client = Client(api_key, api_secret)

# Функция для подключения к базе данных
def connect_to_database():
    try:
        connection = psycopg2.connect(
            host="хост_базы_данных",
            database="название_базы_данных",
            user="имя_пользователя",
            password="пароль"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при подключении к базе данных:", error)
        return None

# Функция для сохранения данных в базе данных
def save_data_to_database(data):
    connection = connect_to_database()
    if connection is None:
        return

    try:
        cursor = connection.cursor()

        # Создание таблицы, если она еще не существует
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            volume FLOAT NOT NULL,
            number INTEGER NOT NULL,
            amount_dif FLOAT NOT NULL,
            side VARCHAR(4) NOT NULL,
            price_min FLOAT NOT NULL,
            price_max FLOAT NOT NULL
        )
        '''
        cursor.execute(create_table_query)
        connection.commit()

        # Вставка данных в таблицу
        insert_query = '''
        INSERT INTO users (volume, number, amount_dif, side, price_min, price_max)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (
            data['volume'], data['number'], data['amountDif'], data['side'], data['priceMin'], data['priceMax']
        ))
        connection.commit()

        print("Данные успешно сохранены в базе данных.")
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при сохранении данных в базе данных:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

# Функция для создания ордеров
def create_orders(data):
    # Проверка и типизация входных данных
    if not isinstance(data, dict):
        raise ValueError("Неверный формат данных. Ожидается словарь.")
    # ...

    # Рассчитываем объем каждого ордера
    order_volume = volume / number

    # Создаем ордеры
    for i in range(number):
        # ...

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

    # Сохраняем данные в базе данных
    save_data_to_database(data)

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



#В данном примере, данные пользователей сохраняются в таблицу "users" с указанными 
#полями (volume, number, amount_dif, side, price_min, price_max). Перед сохранением данных, выполняется проверка наличия таблицы и создание ее, если она не существует. 
#Если возникают ошибки при подключении к базе данных или сохранении данных, соответствующие сообщения об ошибке выводятся на экран.
