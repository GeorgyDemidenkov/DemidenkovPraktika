import getpass
import pyperclip

#Словарь для хранения паролей
passwords = {}

def generate_password(length=8):
    """Генерация случайного пароля"""
    #Используется случайная строка
    import random #Модуль random предоставляет функции для работы со случайными числами
    import string #Модуль string содержит строковые константы, такие как буквы алфавита, цифры и символы пунктуации
    chars = string.ascii_letters + string.digits + string.punctuation #В переменную chars записываются все буквы, цифры и знаки пунктуации
    return ''.join(random.choice(chars) for _ in range(length)) #Цикл for _ in range(length) length раз, в каждой итерации цикла выбирается случайный символ из переменной chars с помощью функции random.choice, и эти символы соединяются в одну строку с помощью метода join.

def encrypt_password(password):
    """Шифрование пароля"""

    #Используется простая замена символов
    encrypted_password = ''
    key = 3  #Сдвиг на 3 символа вправо
    for char in password:
        if char.isalpha(): #Внутри цикла проверяется, является ли символ буквой
            ascii_code = ord(char) #Если да, то с помощью ascii-код все буквы сдвигаются на 3 символа вправо
            encrypted_ascii_code = (ascii_code - ord('a') + key) % 26 + ord('a')
            encrypted_password += chr(encrypted_ascii_code)
        else:
            encrypted_password += char
    return encrypted_password

def decrypt_password(encrypted_password):
    """Дешифрование пароля"""
    decrypted_password = ''
    key = 3  #Сдвиг на 3 символа влево
    for char in encrypted_password:
        if char.isalpha():
            ascii_code = ord(char)
            decrypted_ascii_code = (ascii_code - ord('a') - key) % 26 + ord('a')
            decrypted_password += chr(decrypted_ascii_code)
        else:
            decrypted_password += char
    return decrypted_password

def search_passwords(keyword):
    """Поиск паролей по ключевому слову в имени или метках"""
    found_passwords = []
    for username, password_info in passwords.items():
        if keyword.lower() in username.lower() or keyword.lower() in password_info.get('tags', '').lower():
            found_passwords.append((username, password_info['password']))
    return found_passwords

def write(name):
    """Автокопирование пароля"""
    pyperclip.copy(name) #Копирует в буфер обмена информацию
    pyperclip.paste()

def copy_password(username):
    try:
        password_info = passwords[username]
        password = password_info['password']
        text = password
        #Автоматическое копирование пароля в буфер обмена
        write(text)
        print(f'Пароль для пользователя {username} скопирован в буфер обмена.')
    except KeyError:
        print(f'Пользователь {username} не найден.')

def add_password():
    """Добавление нового пароля"""
    username = input('Введите имя пользователя: ')
    password = getpass.getpass('Введите пароль: ')
    tags = input('Введите метки через запятую (необязательно): ')
    passwords[username] = {
        'password': password,
        'tags': tags
    }
    print(f'Пароль для пользователя {username} успешно добавлен.')


while True:
    print('1. Сгенерировать новый пароль')
    print('2. Добавить новый пароль')
    print('3. Поиск паролей по ключевому слову')
    print('4. Автокопирование пароля')
    print('5. Выход')
    choice = input('Выберите действие: ')
    if choice == '1':
        generated_password = generate_password()
        print(f'Случайно сгенерированный пароль: {generated_password}')
    elif choice == '2':
        add_password()
    elif choice == '3':
        keyword = input('Введите ключевое слово для поиска: ')
        found_passwords = search_passwords(keyword)
        if found_passwords:
            print('Найдены следующие пароли:')
            for username, password in found_passwords:
                print(f'Пользователь: {username}\tПароль: {password}')
        else:
            print('Пароли не найдены.')
    elif choice == '4':
        username = input('Введите имя пользователя, для которого нужно скопировать пароль: ')
        copy_password(username)
    elif choice == '5':
        break
    else:
        print('Некорректный выбор. Пожалуйста, выберите действие снова.')
