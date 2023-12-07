grades = {"A": 5, "B": 5, "C": 4, "D": 3, "E": 3, "FX": 2, "F": 1}

def formatted_grades(students):
    formatted_output = []
    for i, (name, grade) in enumerate(students.items(), start=1):
        points = grades.get(grade, 0)
        row = f"{i:>4}|{name:<10}| {grade:^5} |{points:^5}"
        formatted_output.append(row)

    return formatted_output

# Test with sample data
students = {"Nick": "A", "Olga": "B", "Boris": "FX", "Anna": "C"}

for el in formatted_grades(students):
    print(el)