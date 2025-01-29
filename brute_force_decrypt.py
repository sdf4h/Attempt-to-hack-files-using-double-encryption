import sys
from cryptography.fernet import Fernet, InvalidToken
import itertools
import string
import threading

# Считываем зашифрованный файл
def load_encrypted_file(file_name):
    with open(file_name, "rb") as file:
        return file.read()

# Попытка расшифровки данных с конкретным ключом
def try_decrypt(key, encrypted_data):
    f = Fernet(key)
    try:
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data
    except InvalidToken:
        return None

# Перебор ключей
def brute_force(key_length, alphabet, encrypted_data):
    for key_tuple in itertools.product(alphabet, repeat=key_length):
        possible_key = b''.join(key_tuple)
        decrypted_data = try_decrypt(possible_key, encrypted_data)
        if decrypted_data is not None:
            print(f'Найден ключ: {possible_key.decode()}')
            print(f'Расшифрованные данные:\n{decrypted_data.decode()}')
            break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python brute_force_decrypt.py <encrypted_filename>")
        sys.exit(1)

    encrypted_filename = sys.argv[1]
    
    # Считываем зашифрованный файл
    encrypted_data = load_encrypted_file(encrypted_filename)

    # Определяем параметры
    alphabet = string.ascii_letters + string.digits
    key_length = 32  # Пример длины ключа (можете увеличить)

    # Запускаем многопоточную атаку на ключи
    threads = []
    for i in range(4):  # Количество потоков
        thread = threading.Thread(target=brute_force, args=(key_length, alphabet, encrypted_data))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
