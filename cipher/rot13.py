import string


class Rot13:
    __cipher: dict[str, str]

    def __init__(self) -> None:
        self.__cipher = self.__build_cipher(
            letter_sets=[
                string.ascii_lowercase,
                string.ascii_uppercase,
            ]
        )

    def __build_cipher(self, letter_sets: list[str]) -> dict[str, str]:

        cipher = {}

        for letters in letter_sets:
            rot_letters = letters[13:] + letters[0:13]
            for i in range(len(letters)):
                cipher[letters[i]] = rot_letters[i]

        return cipher

    def __run_cipher(self, message):
        str = ""

        for letter in message:
            if letter.isalpha():
                str += self.__cipher[letter]
            else:
                str += letter

        return str

    def encrypt(self, message: str) -> str:
        """
        Encrypts a message using the ROT13 cipher
        """

        return self.__run_cipher(message)

    def decrypt(self, encrypted: str) -> str:
        """
        Decrypts a ROT13 encrypted string.
        """

        return self.__run_cipher(encrypted)
