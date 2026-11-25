# BIP-39 and BIP-32 Key Derivation

Companion notebooks for [BIP-39 and BIP-32: Understanding Key Derivation](https://weisser-zwerg.dev/posts/bip39-bip32-key-derivation/).

| Notebook | Approach | Preview |
| --- | --- | --- |
| [bip39-bip32-key-derivation-by-foot.ipynb](bip39-bip32-key-derivation-by-foot.ipynb) | Intermediate steps using basic cryptographic primitives | [View with nbviewer](https://nbviewer.jupyter.org/github/cs224/bip39-bip32-key-derivation/blob/main/bip39-bip32-key-derivation-by-foot.ipynb?flush_cache=true) |
| [bip39-bip32-key-derivation-bip-utils.ipynb](bip39-bip32-key-derivation-bip-utils.ipynb) | Concise derivation using `bip_utils` | [View with nbviewer](https://nbviewer.jupyter.org/github/cs224/bip39-bip32-key-derivation/blob/main/bip39-bip32-key-derivation-bip-utils.ipynb?flush_cache=true) |

The by-foot notebook covers BIP-39 word indices, entropy and checksums, recovery-phrase validation, and seed derivation.
It continues through BIP-32 master and child derivation, following a BIP-84 Bitcoin path and a BIP-44 Ethereum path, with checks against published BIP-39, BIP-32, and BIP-84 vectors.
BIP-32's HMAC and scalar arithmetic are implemented directly; `coincurve` supplies the secp256k1 public-key primitive.
The `bip_utils` notebook performs the same derivations through the library's BIP-39 and BIP-32 APIs and checks the same published reference values.

Use the nbviewer links to read the notebooks with their saved example outputs, or follow the local setup below to run the cells yourself.

## Run locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python 3.12 or newer, then clone the repository and set up the environment:

```bash
git clone https://github.com/cs224/bip39-bip32-key-derivation.git
cd bip39-bip32-key-derivation
uv sync --locked
uv run jupyter nbclassic
```

For the Notebook 7 interface:

```bash
uv run jupyter notebook
```

JupyterLab is also installed with Notebook 7:

```bash
uv run jupyter lab
```

Open either notebook and run its cells in order using the Python 3 kernel.
Each notebook starts with a watermark showing the Python and package versions, followed by 70% width settings for nbclassic and Notebook 7.

## Public example recovery phrases

The notebooks use two standard public [BIP-39 test vectors](https://github.com/trezor/python-mnemonic/blob/master/vectors.json):

- 12 words: `abandon` repeated 11 times, followed by `about`.
- 24 words: `abandon` repeated 23 times, followed by `art`.

These encode all-zero entropy and are deliberately predictable.
Use them only for learning, never for real funds.
The default BIP-39 passphrase is empty.
In either notebook, select `ENTROPY_BITS = 128` or `256` and rerun from the beginning.

## Local word list

[`english.txt`](english.txt) is an unmodified copy of the English BIP-39 word list from [Trezor's reference implementation at commit `f5697ffc7554`](https://github.com/trezor/python-mnemonic/blob/f5697ffc75547e0f2982b4f43dbd7f8810d09abd/src/mnemonic/wordlist/english.txt).
Its original MIT license and copyright notice are retained in [LICENSE-bip39-wordlist](LICENSE-bip39-wordlist).
The by-foot notebook reads this local file and embeds the two reference seeds it checks, so it needs no network access after environment setup.

## Compare Zcash wallet paths

[`verify_zec_derivation.py`](verify_zec_derivation.py) uses a separate public test phrase to reproduce the different transparent Zcash addresses selected by Brave and Guarda:

```bash
uv run python verify_zec_derivation.py
```
