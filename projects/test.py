from datetime import date, datetime, timedelta

def get_birthdays_per_week(users):
    today = date.today()
    current_weekday = today.weekday()
    days_in_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    birthdays_per_week = {day: [] for day in days_in_week}

    if not users or all(today > user["birthday"].replace(year=today.year) for user in users):
        return birthdays_per_week  # Повертаємо пустий словник, якщо список користувачів порожній або всі дні народження вже минули

    for user in users:
        user_name = user["name"]
        birthday = user["birthday"]

        # Розраховуємо наступний день народження
        next_birthday = datetime(today.year, birthday.month, birthday.day).date()
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, birthday.month, birthday.day).date()

        # Розраховуємо дні до наступного дня народження
        days_until_birthday = (next_birthday - today).days
        if days_until_birthday < 0:
            next_birthday = datetime(today.year + 1, birthday.month, birthday.day).date()
            days_until_birthday = (next_birthday - today).days

        # Виправлення для врахування вихідних
        next_birthday_weekday = (current_weekday + days_until_birthday) % 7

        if next_birthday_weekday >= 5:
            next_birthday_weekday = 0  # Переносимо на понеділок

        # Виправлення для врахування того, що день народження може вже минутий у цьому році
        if days_until_birthday < 0:
            continue

        # Перевіряємо, що день народження не виходить за межі поточного тижня
        if days_until_birthday < 7:
            birthdays_per_week[days_in_week[next_birthday_weekday]].append(user_name)

    return birthdays_per_week

if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
        {"name": "Bill Gates", "birthday": datetime(1955, 10, 28).date()},
        {"name": "Kim Kardashian", "birthday": datetime(1980, 10, 21).date()},
        {"name": "Jik", "birthday": datetime(2000, 12, 3).date()},
        {"name": "Niml", "birthday": datetime(2023, 12, 7).date()},
    ]

    result = get_birthdays_per_week(users)

    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
