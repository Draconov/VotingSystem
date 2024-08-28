import random
from Crypto.Util.number import getPrime, inverse

class ZKP:
    def __init__(self):
        self.p = getPrime(256)  # Большое простое число
        self.g = 2  # Генератор группы
        self.q = (self.p - 1) // 2  # Порядок подгруппы
        self.x = random.randint(1, self.q - 1)  # Секретный ключ
        self.y = pow(self.g, self.x, self.p)  # Открытый ключ

    def generate_proof(self, message):
        k = random.randint(1, self.q - 1)
        r = pow(self.g, k, self.p)
        e = hash((message, r)) % self.q
        s = (k - self.x * e) % self.q
        return (r, s)

    def verify_proof(self, message, proof):
        r, s = proof
        if r < 1 or r > self.p - 1:
            return False
        e = hash((message, r)) % self.q
        return pow(self.g, s, self.p) * pow(self.y, e, self.p) % self.p == r

# Функция для хеширования сообщения
def hash(message):
    return int.from_bytes(str(message).encode(), 'big')

zkp = ZKP()