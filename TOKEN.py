
try :
    with open("C://PyCharmProject//pythonProject/.env", "r") as f:
        TOKEN = f.readline().split("=")
        TOKEN = TOKEN[1]
except FileNotFoundError:
    with open(".env", "r") as f:
        # /home/pavel/Documents/.env"
        TOKEN = f.readline().split("=")
        TOKEN = TOKEN[0]
