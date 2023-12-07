import sys
import importlib

from pathlib import Path

def base():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} country")
        sys.exit(1)

    country = sys.argv[1]
    country = country.lower()

    countries_dir = Path("countries")
    if not countries_dir.is_dir():
        print("Error: no countries dir found")
        sys.exit(1)

    module_path = Path(country + ".py")
    full_module_path = countries_dir.joinpath(module_path)

    if full_module_path.is_file():
        full_module_path = str(full_module_path)

        module = importlib.import_module(
            full_module_path.replace('/', '.').removesuffix(".py")
        )

        module.get_weather()
    else:
        print("I don't know")
        sys.exit(1)


if __name__ == "__main__":
    base()