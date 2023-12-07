from datetime import date, datetime, timedelta

def calculate_birthday_date(today, birthday):
    if birthday.month > today.month or (birthday.month == today.month and birthday.day >= today.day):
        return datetime(today.year, birthday.month, birthday.day)
    else:
        return datetime(today.year + 1, birthday.month, birthday.day)

def get_birthdays_per_week(users):
    today = date.today()
    next_week = today + timedelta(days=7)
    birthday_days = {}
    
    for user in users:
        name = user['name']
        birthday = user['birthday']
        
        date_obj = calculate_birthday_date(today, birthday)

        while date_obj.weekday() >= 5:  # 5 і 6 - це субота і неділя
            date_obj += timedelta(days=1)

        if today <= birthday < next_week:
            birthday_days.setdefault(date_obj.strftime('%A'), []).append(name)

    return birthday_days

if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
        {"name": "Bill Gates", "birthday": datetime(1955, 12, 28).date()},
        {"name": "Kim Kardashian", "birthday": datetime(1980, 10, 21).date()},
        {"name": "Jik", "birthday": datetime(2000, 12, 3).date()},
        {"name": "Niml", "birthday": datetime(2023, 12, 7).date()},
    ]

    result = get_birthdays_per_week(users)

    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
