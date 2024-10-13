# Пример фиктивных данных, которые будут возвращаться от API
FAKE_USER_DATA = {"id": 123456}
FAKE_ITEMS_DATA = {
    "resources": [
        {"id": "1853257996", "title": "Продажа квартиры в центре города"},
        {"id": "1853257997", "title": "Аренда офиса на Лубянке"}
    ]
}
FAKE_CALL_STATS = {
                    "result": {
                        "items": [
                            {
                                "days": [
                                    {
                                        "answered": 5,
                                        "calls": 10,
                                        "date": "2023-09-01",
                                        "new": 4,
                                        "newAnswered": 2
                                    },
                                    {
                                        "answered": 3,
                                        "calls": 8,
                                        "date": "2023-09-02",
                                        "new": 5,
                                        "newAnswered": 1
                                    },
                                    {
                                        "answered": 4,
                                        "calls": 7,
                                        "date": "2023-09-03",
                                        "new": 3,
                                        "newAnswered": 2
                                    }
                                ],
                                "employeeId": 1,
                                "itemId": 1853257996,
                                "itemName": "Продажа квартиры в центре города"
                            },
                            {
                                "days": [
                                    {
                                        "answered": 2,
                                        "calls": 5,
                                        "date": "2023-09-01",
                                        "new": 1,
                                        "newAnswered": 0
                                    },
                                    {
                                        "answered": 6,
                                        "calls": 9,
                                        "date": "2023-09-02",
                                        "new": 3,
                                        "newAnswered": 1
                                    },
                                    {
                                        "answered": 4,
                                        "calls": 10,
                                        "date": "2023-09-03",
                                        "new": 2,
                                        "newAnswered": 2
                                    }
                                ],
                                "employeeId": 2,
                                "itemId": 1853257997,
                                "itemName": "Аренда офиса на Лубянке"
                            },
                            {
                                "days": [
                                    {
                                        "answered": 0,
                                        "calls": 0,
                                        "date": "2023-09-01",
                                        "new": 0,
                                        "newAnswered": 0
                                    },
                                    {
                                        "answered": 0,
                                        "calls": 0,
                                        "date": "2023-09-02",
                                        "new": 0,
                                        "newAnswered": 0
                                    },
                                    {
                                        "answered": 1,
                                        "calls": 3,
                                        "date": "2023-09-03",
                                        "new": 1,
                                        "newAnswered": 0
                                    }
                                ],
                                "employeeId": 3,
                                "itemId": 1853257998,
                                "itemName": "Продажа автомобиля"
                            }
                        ]
                    }
}