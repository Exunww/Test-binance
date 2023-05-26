def test_create_orders():
    data = {
        "volume": 10000.0,
        "number": 5,
        "amountDif": 50.0,
        "side": "SELL",
        "priceMin": 200.0,
        "priceMax": 300.0
    }

    # Проверяем успешное создание ордеров
    create_orders(data)

    # Проверяем создание ордеров с неверными данными
    invalid_data = [
        {"volume": -10000.0, "number": 5, "amountDif": 50.0, "side": "SELL", "priceMin": 200.0, "priceMax": 300.0},
        {"volume": 10000.0, "number": 0, "amountDif": 50.0, "side": "SELL", "priceMin": 200.0, "priceMax": 300.0},
        {"volume": 10000.0, "number": 5, "amountDif": -50.0, "side": "SELL", "priceMin": 200.0, "priceMax": 300.0},
        {"volume": 10000.0, "number": 5, "amountDif": 50.0, "side": "INVALID", "priceMin": 200.0, "priceMax": 300.0},
        {"volume": 10000.0, "number": 5, "amountDif": 50.0, "side": "SELL", "priceMin": "200.0", "priceMax": 300.0},
        {"volume": 10000.0, "number": 5, "amountDif": 50.0, "side": "SELL", "priceMin": 200.0, "priceMax": "300.0"}
    ]

    for invalid in invalid_data:
        try:
            create_orders(invalid)
        except ValueError as e:
            print(f"Тест провален: {str(e)}")
        else:
            print("Тест провален: Ожидалась ошибка, но ордеры были созданы.")

def run_tests():
    test_create_orders()

run_tests()
