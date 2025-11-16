# 🔐 AES-Crypt Brute-Force Tool

Try passwords from a wordlist (e.g., **rockyou.txt**) to decrypt `.aes` files created with **AES-Crypt**.  
This tool uses **pyAesCrypt** and performs efficient, line-by-line password attempts with safe file handling, resume support, and progress bars.

---

## ✨ Features

- 🚀 **Brute-force AES-Crypt `.aes` files** using any wordlist  
- 📦 Uses **pyAesCrypt** (pure Python AES-Crypt implementation)  
- ▶️ **Resume from any line** using `--start-line`  
- 📂 Output decrypted files without overwriting existing data  
- 📊 **tqdm progress bar** for smooth wordlist iteration  
- 🔧 Verbose mode for manual debugging  
- 🗑️ Automatic cleanup of partial/wrong decrypted files  

---

## 📥 Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/aescrypt-bruteforce.git
cd aescrypt-bruteforce
```
### 2. Install requirements
```bash
pip install -r requirements.txt
```

### Or install manually:
```bash
pip install pyAesCrypt tqdm
```

## ▶️ Usage
### Basic example:
```bash
python3 try-rockyou-aescrypt.py \
    -f web_20250806_120723.zip.aes \
    -w /usr/share/wordlists/rockyou.txt \
    -o ./decrypted_out
```
### Flags
| Flag               | Description                                       |
| ------------------ | ------------------------------------------------- |
| `-f`, `--file`     | Path to the AES-Crypt `.aes` file                 |
| `-w`, `--wordlist` | Path to wordlist (e.g. rockyou.txt)               |
| `-o`, `--outdir`   | Directory to save decrypted output (default: `.`) |
| `--start-line`     | Start at line N of the wordlist (resume mode)     |
| `--verbose`        | Disable tqdm and print every password attempt     |

### Example with resume:
```bash
python3 try-rockyou-aescrypt.py \
    -f backup.aes \
    -w rockyou.txt \
    --start-line 2000000
```
### Example with verbose output:
```bash
python3 try-rockyou-aescrypt.py -f secret.aes -w rockyou.txt --verbose
```
## 📂 Output
If a password succeeds, the tool creates a file such as:
```bash
filename.aes.decrypted_<password>
```

Example:
```bash
web_20250806_120723.zip.aes.decrypted_supersecret123
```

## 🛠 How It Works
- Reads the wordlist line-by-line (memory-safe)
- For each password, attempts decryption using:
```bash
pyAesCrypt.decryptFile(...)
```
- Catches ValueError for incorrect passwords
- Deletes partial output files on failure
- On success → prints password and output file path
