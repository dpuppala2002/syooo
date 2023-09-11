import socket
import json
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import algorithms, modes

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def generate_message():
  names = ["Alice", "Bob", "Charlie", "David", "Eve"]
  origins = ["London", "Paris", "Berlin", "Rome", "Tokyo"]
  destinations = ["New York", "Chicago", "Los Angeles", "Toronto", "Montreal"]

  name = random.choice(names)
  origin = random.choice(origins)
  destination = random.choice(destinations)

  message = {
    "name": name,
    "origin": origin,
    "destination": destination,
  }

  secret_key = hashlib.sha256(json.dumps(message).encode("utf-8")).hexdigest()

  message["secret_key"] = secret_key

  return message

def encrypt_message(message, password):
  cipher = algorithms.AES(password)
  mode = modes.CTR(cipher.nonce)
  backend = default_backend()
  encryptor = cipher.encryptor(mode, backend=backend)
  ciphertext = encryptor.update(json.dumps(message).encode("utf-8")) + encryptor.finalize()

  return ciphertext

def send_messages(messages):
  for message in messages:
    encrypted_message = encrypt_message(message, password)
    socket.sendall(encrypted_message + b"|")

def main():
  host = "localhost"
  port = 5000
  password = "secret"

  socket.connect((host, port))

  while True:
    messages = [generate_message() for _ in range(random.randint(49, 499))]
    send_messages(messages)
    time.sleep(10)

if __name__ == "__main__":
  main()
