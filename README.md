# pyccwc

A Python reimplementation of `wc` (word count), built as part of the [Coding Challenges](https://codingchallenges.fyi/challenges/challenge-wc) series.

## Why

The standard `wc` command seems simple — count lines, words, bytes. But under the hood, there are interesting problems: UTF-8 characters split across read buffers, locale-dependent whitespace, stdin that can only be read once. This project rebuilds `wc` from scratch to understand how it actually works.

## Features

- `-c` — byte count
- `-l` — line count
- `-w` — word count
- `-m` — character count (UTF-8 aware)
- Default (no flag) — lines, words, and bytes
- File input and stdin (piping)
- Output matches `wc`

## Usage

```bash
# make it executable
chmod +x pyccwc

# count bytes
./pyccwc -c test.txt

# count lines
./pyccwc -l test.txt

# count words
./pyccwc -w test.txt

# count characters (UTF-8)
./pyccwc -m test.txt

# default: lines + words + bytes
./pyccwc test.txt

# read from stdin
cat test.txt | ./pyccwc -l
cat test.txt | ./pyccwc -w
cat test.txt | ./pyccwc -c
cat test.txt | ./pyccwc
```

## How It Works

**Streaming with chunks** — Files are read in 4096-byte chunks, not loaded entirely into memory. This handles large files without running out of RAM.

**UTF-8 boundary handling** — A multi-byte character (like `é` or `—`) can be split across two chunks. The character counter carries incomplete bytes between chunks and decodes them on the next read.

**Word boundary correction** — Words counted via `split()` can be double-counted at chunk boundaries. The tool detects when both the end of one chunk and the start of the next are non-whitespace, and corrects the count.

**File vs stdin** — The `open_source` abstraction handles both transparently. For stdin, data is read once and passed to all counting functions to avoid exhausting the stream.

## Requirements

- Python 3.8+ (uses walrus operator `:=`)

## What I Learned

1. **Byte vs character** — `wc -c` counts raw bytes; `wc -m` counts Unicode codepoints. In UTF-8, they're different. Python's text mode silently converts `\r\n` to `\n`, which skews character counts.
2. **Chunk boundaries** — Splitting a read buffer can break multi-byte characters and split words across chunks. Both need explicit handling.
3. **Stdin is a stream** — It can only be read once. If multiple functions need the same input, read it once and pass the data around.
4. **Locale matters** — What counts as whitespace depends on locale settings. The real `wc` uses `isspace()` which varies by system.
