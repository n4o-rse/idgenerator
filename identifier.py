import random
import string
import csv
import hashlib
import os

# ---------------------------------------------
# Konfiguration
# ---------------------------------------------
code_length = 6
number_of_codes = 5000

generation_seed = 12345           # Seed für reproduzierbare Code-Erzeugung
shuffle_seed = 42                 # Seed für reproduzierbares Mischen
salt_string = "SECRET_SALT"    # Salt für Hex-Code-Erzeugung

# ---------------------------------------------
# Output-Pfad = gleicher Ordner wie das Skript
# ---------------------------------------------
try:
    # wenn als .py-Datei ausgeführt
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # wenn in Notebook oder interaktiv
    script_dir = os.getcwd()

output_file = os.path.join(script_dir, "unique_codes.csv")

# ---------------------------------------------
# Zeichenvorrat
# ---------------------------------------------
first_characters = string.ascii_uppercase
other_characters = string.ascii_uppercase + string.digits

# ---------------------------------------------
# Funktionen
# ---------------------------------------------
def generate_hex_code(code: str, salt: str) -> str:
    return hashlib.sha256((salt + code).encode('utf-8')).hexdigest()

def verify_code(code: str, given_hex: str, salt: str = salt_string) -> bool:
    return generate_hex_code(code, salt) == given_hex

# ---------------------------------------------
# Codes erzeugen (reproduzierbar)
# ---------------------------------------------
gen_rng = random.Random(generation_seed)

unique_codes = set()
while len(unique_codes) < number_of_codes:
    first = gen_rng.choice(first_characters)
    rest = ''.join(gen_rng.choices(other_characters, k=code_length - 1))
    code = first + rest
    unique_codes.add(code)

sorted_codes = sorted(unique_codes)

# Hex-Codes berechnen
entries = [(code, generate_hex_code(code, salt_string)) for code in sorted_codes]

# Mischen (reproduzierbar)
shuffle_rng = random.Random(shuffle_seed)
shuffle_rng.shuffle(entries)

# ---------------------------------------------
# CSV schreiben
# ---------------------------------------------
with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['index', 'code', 'hex_code'])
    for i, (code, hex_code) in enumerate(entries, 1):
        writer.writerow([i, code, hex_code])

# ---------------------------------------------
# Beispielausgabe
# ---------------------------------------------
example_code, example_hex = entries[0]
print(f"Beispielcode: {example_code}")
print(f"Hex-Code:    {example_hex}")
print("Verifikation:", verify_code(example_code, example_hex))

# ---------------------------------------------
# Infos
# ---------------------------------------------
print(f"\nSalt-String:      '{salt_string}'")
print(f"Generation-Seed:  {generation_seed}")
print(f"Shuffle-Seed:     {shuffle_seed}")
print(f"{number_of_codes} eindeutige Codes wurden in '{output_file}' gespeichert.")
