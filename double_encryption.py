import sys
from cryptography.fernet import Fernet

# Функция для генерации ключа и сохранения его в файл
def generate_key():
    key = Fernet.generate_key()
    return key

# Функция для шифрования файла
def encrypt_file(file_name, key):
    f = Fernet(key)
    with open(file_name, "rb") as file:
        original = file.read()
    encrypted = f.encrypt(original)
    with open(file_name + ".enc", "wb") as file:
        file.write(encrypted)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python double_encryption.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    # Генерация первого ключа и его сохранение
    key1 = generate_key()
    with open("key1.key", "wb") as key_file:
        key_file.write(key1)

    # Шифрование файла первым ключом
    encrypt_file(filename, key1)

    # Генерация второго ключа и его сохранение
    key2 = generate_key()
    with open("key2.key", "wb") as key_file:
        key_file.write(key2)

    # Шифрование уже зашифрованного файла
    encrypt_file(filename + ".enc", key2)

    print("Файл был успешно зашифрован дважды.")
