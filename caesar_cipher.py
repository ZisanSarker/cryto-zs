def caesar_cipher(text, shift, mode):
    if mode == 'D':
        shift = -shift

    result = ""

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result += chr(base + shifted)
        else:
            result += char  # keep numbers, space, punctuation same

    return result


# --- Main program ---
mode = input("Enter mode (E for Encrypt, D for Decrypt): ").upper()

if mode not in ['E', 'D']:
    print("Invalid mode! Use 'E' or 'D'")
else:
    text = input("Enter your text: ")
    try:
        shift = int(input("Enter shift value (can be negative): "))
        result = caesar_cipher(text, shift, mode)
        print("Result:", result)
    except ValueError:
        print("Shift value must be a number.")
