# Cipwei

Cipwei is a custom cipher method I developed for educational purposes. It uses hashes to encrypt text, with a random seed of up to 64 bits (which can be extended in the future). The encryption process is initialized with a key, and then the content of the file itself is used to further encrypt the data. **Please note that the security of this encryption method has not been thoroughly tested, and I do not recommend using it for commercial or sensitive information.** This project was created purely for learning purposes and is not designed to be highly secure.

The project consists of four Python files and an executable:

- **`cipweiCore`**: This is the core of the project. It contains the main logic for encrypting and decrypting text. The core functionality is implemented in just 9 lines of code. You need to call the appropriate functions to use it.
- **`cipweiEncripter`**: This is the encryption module. It provides a user-friendly terminal interface (TTY) for encrypting files. It essentially performs the same function as the encryption feature in `cipweiCore`, but with a more polished UI.
- **`cipweiDecripter`**: This module is used for decrypting files. Like the encrypter, it operates in the terminal and offers a more user-friendly interface compared to the core decryption function.
- **`cipweiUI`**: This file has been compiled into an executable, so you should use the executable instead of running this Python file directly.
- **`cipweiV2`**: In testing mode, not implemented on the other python files, this encriptation has a better format and performance also adding more security on it.

## Disclaimer:
**Do not use this tool for sensitive information such as passwords or secret messages. It may not be secure enough for such purposes.**

## No further changes will be made for now!