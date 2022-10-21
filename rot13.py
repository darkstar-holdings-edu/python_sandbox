from cipher import Rot13


def main() -> int:
    cipher = Rot13()

    s = "cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_hyLicInt}"

    decrypted = cipher.decrypt(s)

    print(decrypted)

    encrypted = cipher.encrypt(message=decrypted)
    print(encrypted)

    return 0


if __name__ == "__main__":
    exit(main())
