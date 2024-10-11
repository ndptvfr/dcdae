import minecraft_launcher_lib
import requests
import os

# Настройки пользователя
minecraft_directory = "minecraft_folder"  # Папка для установки Minecraft
version = "1.20.1"  # Версия Minecraft, которую будем запускать

# Функция для аутентификации через Ely.by
def authenticate_ely_by(username, password):
    auth_url = "https://auth.ely.by/auth/login"
    data = {
        "username": username,
        "password": password,
        "client": "MinecraftLauncher"
    }

    response = requests.post(auth_url, data=data)
    
    if response.status_code == 200:
        auth_data = response.json()
        return auth_data["accessToken"], auth_data["profile"]["id"], auth_data["profile"]["name"]
    else:
        print(f"Ошибка аутентификации: {response.status_code} - {response.text}")
        return None, None, None

# Данные для аутентификации
username = input("Введите ваш Ely.by логин: ")
password = input("Введите ваш Ely.by пароль: ")

# Аутентификация
token, uuid, display_name = authenticate_ely_by(username, password)

if not token or not uuid:
    print("Не удалось авторизоваться через Ely.by")
    exit()

# Проверяем наличие и устанавливаем Fabric
fabric_version = minecraft_launcher_lib.fabric.get_latest_loader_version()
minecraft_launcher_lib.fabric.install_fabric(version, minecraft_directory)

# Настраиваем параметры запуска
options = {
    "username": display_name,
    "uuid": uuid,
    "token": token,
    "version": version,
    "gameDirectory": minecraft_directory
}

# Генерация команды для запуска
command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)

# Запуск игры
print("Запускаем Minecraft с командой:")
print(" ".join(command))

os.system(" ".join(command))
