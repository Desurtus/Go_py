from datetime import date, datetime, timedelta


def get_birthdays_per_week(users):
    today = datetime.combine(date.today(), datetime.min.time())
    next_week = today + timedelta(days=7)
    birthday_days = {}

    for user in users:
        name = user['name']
        birthday = user['birthday']

        # Конвертуємо birthday в datetime для порівняння
        birthday_datetime = datetime(birthday.year, birthday.month, birthday.day)

        # Додаємо 1 рік, якщо день народження вже минув у цьому році
        if today > birthday_datetime:
            birthday_datetime = datetime(today.year + 1, birthday.month, birthday.day)

        date_obj = birthday_datetime

        while date_obj.weekday() >= 5:
            date_obj += timedelta(days=1)

        if today <= birthday_datetime < next_week:
            birthday_days.setdefault(date_obj.strftime('%A'), []).append(name)

    return birthday_days


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(2023, 1, 1).date()},
        {"name": "Bill Gates", "birthday": datetime(2023, 12, 28).date()},
        {"name": "Kim Kardashian", "birthday": datetime(2023, 10, 21).date()},
        {"name": "Jik", "birthday": datetime(2023, 12, 3).date()},
        {"name": "Niml", "birthday": datetime(2023, 12, 7).date()},
    ]

    result = get_birthdays_per_week(users)

    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
