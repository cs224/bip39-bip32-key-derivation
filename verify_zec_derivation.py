"""Verify Brave and Guarda transparent ZEC addresses from public test data.

Run with: uv run python verify_zec_derivation.py
"""

import hashlib
import unicodedata

from bip_utils import Base58Encoder, Bip32Secp256k1, Bip39MnemonicDecoder, Hash160


MNEMONIC = "firm bring recipe cook inflict science casino athlete army faint exhaust aisle"
BIP39_PASSPHRASE = ""  # Optional text in addition to the 12 words.
ZCASH_MAINNET_P2PKH = bytes.fromhex("1cb8")

WALLET_CASES = (
    ("Brave (BIP-44)", "m/44'/133'/0'/0/0", "t1YwmDXZJi2V1LQA6viggxbFUXkAhfRJtZC"),
    ("Guarda (web adapter, account 0)", "m/0'/0/0", "t1WqdzwtvDM65H2tjpZiXWM8kE8mBMJcCbU"),
)


def bip39_seed(mnemonic: str, passphrase: str) -> bytes:
    password = unicodedata.normalize("NFKD", mnemonic).encode("utf-8")
    salt = unicodedata.normalize("NFKD", "mnemonic" + passphrase).encode("utf-8")
    return hashlib.pbkdf2_hmac("sha512", password, salt, 2048, dklen=64)


def zcash_address(compressed_public_key: bytes) -> str:
    # HASH160 is RIPEMD-160(SHA-256(pubkey)). Base58Check adds its own checksum.
    pubkey_hash = Hash160.QuickDigest(compressed_public_key)
    return Base58Encoder.CheckEncode(ZCASH_MAINNET_P2PKH + pubkey_hash)


def main() -> int:
    # Decode the English word list indices and validate the mnemonic checksum.
    entropy = Bip39MnemonicDecoder().Decode(MNEMONIC)
    checksum_length = len(entropy) * 8 // 32
    checksum_bits = f"{hashlib.sha256(entropy).digest()[0]:08b}"[:checksum_length]
    print(f"BIP-39 entropy:   {entropy.hex()}")
    print(f"BIP-39 checksum:  {checksum_bits}")

    # The same seed is the input to BIP-32 for both wallets.
    seed = bip39_seed(MNEMONIC, BIP39_PASSPHRASE)
    master = Bip32Secp256k1.FromSeed(seed)
    print(f"BIP-39 seed size: {len(seed) * 8} bits")

    all_match = True
    for wallet, path, expected in WALLET_CASES:
        child = master.DerivePath(path)
        public_key = child.PublicKey().RawCompressed().ToBytes()
        address = zcash_address(public_key)
        match = address == expected
        all_match = all_match and match

        print(f"\n{wallet}")
        print(f"  Path:       {path}")
        print(f"  Public key: {public_key.hex()}")
        print(f"  Derived:    {address}")
        print(f"  Expected:   {expected}")
        print(f"  Result:     {'MATCH' if match else 'MISMATCH'}")

    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
