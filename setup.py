from os import system
from sys import argv
from matchProject.settings import DEBUG

from matchProject.settings import DEBUG

"""
0 - error
1 - done
2 - already satisfied
"""


def setup(seed):
    result = 0

    # try to init and migrate database
    try:
        system("python3 manage.py makemigrations")
        system("python3 manage.py makemigrations core")
        system("python3 manage.py migrate")

        if seed == "seed":
            system("python3 manage.py loaddata auxiliary_tables.json")
            system("python3 manage.py loaddata admin.json")
            system("python3 manage.py loaddata startups_advisors.json")
            system("python3 manage.py loaddata matchpointskeys.json")

        result = 1

        if not DEBUG:
            system("service apache2 start")
        else:
            system("python3 manage.py runserver 0.0.0.0:8000")

    except Exception as e:
        result = 0

    return result


if __name__ == "__main__":

    result = setup(argv[-1])
