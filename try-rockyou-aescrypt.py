#!/usr/bin/env python3
"""
Try to decrypt an AES-Crypt .aes file using passwords from a wordlist.
Uses pyAesCrypt (pure Python wrapper for AES-Crypt).
Usage:
    python3 try-rockyou-aescrypt.py -f web_20250806_120723.zip.aes -w /path/to/rockyou.txt
"""

import pyAesCrypt
import argparse
import os
import sys
from tqdm import tqdm
import tempfile

BUFFER_SIZE = 64 * 1024  # 64KB (pyAesCrypt recommended chunk size)

def try_password(aesfile, outdir, password):
    """
    Attempt to decrypt aesfile with password, writing to a temp file in outdir.
    Returns (True, outpath) on success, (False, None) on failure.
    """
    basename = os.path.basename(aesfile)
    # Name output file with password-safe suffix
    safe_pw = password.strip().replace(" ", "_")[:80]
    outname = f"{basename}.decrypted_{safe_pw}"
    outpath = os.path.join(outdir, outname)

    # Ensure no stale partial file
    if os.path.exists(outpath):
        os.remove(outpath)

    try:
        # pyAesCrypt.decryptFile will raise ValueError if password is wrong or integrity fails
        pyAesCrypt.decryptFile(aesfile, outpath, password, BUFFER_SIZE)
    except ValueError:
        # Wrong password / integrity error; remove partial file
        if os.path.exists(outpath):
            try:
                os.remove(outpath)
            except Exception:
                pass
        return False, None
    except Exception as e:
        # Other I/O errors: bubble up
        if os.path.exists(outpath):
            try:
                os.remove(outpath)
            except Exception:
                pass
        raise
    # If we reach here, decryptFile didn't raise -> likely success
    return True, outpath

def main():
    p = argparse.ArgumentParser(description="Brute-force AES-Crypt .aes with a wordlist (rockyou).")
    p.add_argument("-f", "--file", required=True, help="Path to the .aes file")
    p.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist (e.g., rockyou.txt)")
    p.add_argument("-o", "--outdir", default=".", help="Directory to write decrypted file(s) (default: current dir)")
    p.add_argument("--start-line", type=int, default=1, help="Resume from a specific wordlist line number (1-based)")
    p.add_argument("--verbose", action="store_true", help="Print every attempt (no tqdm)")
    args = p.parse_args()

    aesfile = args.file
    wordlist = args.wordlist
    outdir = args.outdir
    start_line = args.start_line

    if not os.path.exists(aesfile):
        print("AES file not found:", aesfile); sys.exit(2)
    if not os.path.exists(wordlist):
        print("Wordlist not found:", wordlist); sys.exit(2)
    if not os.path.isdir(outdir):
        os.makedirs(outdir, exist_ok=True)

    total_lines = None
    try:
        # Try to get total lines for tqdm
        with open(wordlist, "rb") as f:
            total_lines = sum(1 for _ in f)
    except Exception:
        total_lines = None

    print(f"Trying to decrypt {aesfile} using passwords from {wordlist}")
    if start_line > 1:
        print(f"Resuming from line {start_line}")

    with open(wordlist, "r", errors="ignore") as wl:
        # Skip lines if resuming
        for _ in range(start_line - 1):
            next(wl, None)

        iterable = wl
        if not args.verbose:
            iterable = tqdm(wl, total=(total_lines - start_line + 1) if total_lines else None, unit="pw")

        for i, line in enumerate(iterable, start=start_line):
            pw = line.rstrip("\n\r")
            if pw == "":
                continue
            try:
                ok, outpath = try_password(aesfile, outdir, pw)
            except Exception as e:
                print("Error attempting password (I/O/other):", e)
                # If you want to abort on I/O errors, uncomment next line
                # sys.exit(1)
                continue

            if ok:
                print("\n=== SUCCESS ===")
                print("Password found (line {}): {}".format(i, pw))
                print("Decrypted file written to:", outpath)
                return 0

    print("Done: no password from wordlist succeeded (or file uses a different format).")
    return 1

if __name__ == "__main__":
    sys.exit(main())
