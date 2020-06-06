# Crypto Puzzles

Crypto Puzzles is a tool and library to provide a bunch of functions for encryption or pseudo encryption as puzzles or brain teasers. 

Puzzles come in three different categories:
1. Ciphers with zero knowledge needed

These puzzles can be "cracked" without any boring explanation, tables or tools. It should be sufficient to know that the the first words are always the same, e.g. "Top secret" to find the pattern and figure out how the secret code works. This makes it possible to decrypt the rest of the message. (Cryptographers would call it a known plaintext attack.) 

Example sentence:

  opT ecret!s heT ookiesc rea iddenh ni het edr owl!b

By searching for "Top secret" in the first two words, you can recognize, that the first letter was moved to the last position. Using that knowledge, the rest of the sentence can be decrypted.

 Top secret! The cookies are hidden in the red bowl!

2. Ciphers with knowledge needed

To solve these puzzles the players need to know (or guess, if you want to make it harder for experienced players) the cipher, which was used for the encryption. Common examples are the Caesar Cipher or translating each character to the number of it's alphabet position: a => 1, b => 2, c => 3, ...

3. Crackme programms
 
A crackme is a small (python) program that contains a secret message, but won't show it until the player has understood the code, found the obstacle and removed it. 

The following example simply waits gazillions years before decoding and printing it's secret message. It can be easily solved by either removing all the sleep statements, moving the print above them or decoding the base64-string with another tool.

```python
# This little script knows the secret you are looking for, but will only tell it in 890601 billion years, harhar :) If you don't have this much time, find a quicker way ...

import base64
import time

print('The ', end='', flush=True)
time.sleep(1)
print('sec', end='', flush=True)
time.sleep(2)
print('cr', end='', flush=True)
time.sleep(4)
print('et ', end='', flush=True)
time.sleep(8)
print('is ', end='', flush=True)
time.sleep(16)
print('really ', end='', flush=True)
time.sleep(16)
print('very ', end='', flush=True)
time.sleep(16)
print('secret ', end='', flush=True)
time.sleep(16)
print('and ', end='', flush=True)
time.sleep(16)
print('I wil tell it to you in 890601 million years: ', end='', flush=True)
time.sleep(65536133708153272784892092746726238958271672343782738923972138217189789897890)

print (base64.b64decode('VGhlIG5leHQgRFZEIGlzIGhpZGRlbiB1bmRlciB0aGUga2l0Y2hlbiBzaW5rLg==').decode('utf8'))
```
 
So far the crackmes are only in python, as this is the most popular programming language among kids at the moment. But they can be written in any programming language (Scratch or even Scratch Jr. would be interessing ;)

## Examples 

More examples created with Crypto Puzzles can be found [here](Examples.md)

## Purpose

The simplest use of Crypto Puzzles: Hide some sweets as a treasure and encrypt the location with Crypto Puzzles, print it out and give it to your kids. To make it more interesting, you could also hide that printout and create another puzzle which points to it. Hide this note again and use an ultraviolet marker to draw a trail of arrows through your whole house which point to it. Give your kids some ultraviolet lamps and enjoy the show. If you want to automate all of this, use Euli Treasure Hunt (<https://github.com/2d4d/euli_treasure_hunt>), which was the initial reason to write Crypto Puzzles ;)

## Other uses of Crypto Puzzles:
* Create puzzles for treasure hunts, mystery geocaches or escape rooms at home
* It's especially useful for groups with different age or skill sets. Normally treasure hunts end up in the way, that the oldest kids solve all the puzzles and the youngest don't even understand, what's going on. With Crypto Puzzles it's easy to create individual puzzles with specific difficulty for each player.
* Mystery geocaches can be created multiple levels of difficulty at the same time for the players to choose from.

Most functions have varying difficulty measured in school grades. That's a rough estimate which kids should be able to tackle which level. Of course this also depends on your national school system and puzzling experience of the kids. There isn't a minimum age or grade but kids should be able to read fluently to enjoy the puzzles and not get frustrated.

Functions which are language dependent are supported in English and German so far.

Contributions are always welcome! If you want to contribute another crypto function, the easiest way is to copy an existing similar one and change it.

# Usage
```
usage: kids_crypto.py [-h] --technique TECHNIQUE [--verbose]
                      [--noise_type NOISE_TYPE] [--noise_chars NOISE_CHARS]
                      [--upside_down_rate UPSIDE_DOWN_RATE] [--grade GRADE]
                      [--language LANGUAGE] [--crackme_num CRACKME_NUM]
                      [--seed SEED] [--show_function_name]
                      plaintext

positional arguments:
  plaintext             Plain text to be "encrypted"

optional arguments:
  -h, --help            show this help message and exit
  --technique TECHNIQUE, -T TECHNIQUE
                        Techniques used to "encrypt". Such argument is a
                        string composed by any combination of NUMLlWmSC13Asnc
                        characters where each letter stands for a different
                        technique. Be careful in combining them, it get's
                        incomprehensible quickly ;) Start with e.g. "top
                        secret" and tell it the recipient to enable a known
                        plaintext attack.
  --verbose, -v         print out verbose information
  --noise_type NOISE_TYPE
                        Type of noise. Can be numbers,numberwords, animals
  --noise_chars NOISE_CHARS
                        Character(s) for noise
  --upside_down_rate UPSIDE_DOWN_RATE
                        Turn every nth word
  --grade GRADE, -g GRADE
                        Adjust difficulty by school grade aka years of school
                        experience.
  --language LANGUAGE   Language for hints
  --crackme_num CRACKME_NUM
                        Number of crackme
  --seed SEED           Random seed (only set to static number to always get
                        the same randomness for debugging!)
  --show_function_name  Shows the python function name below the encrypted
                        text (for internal use)
```

## Example

```
./crypto_puzzles.py -T U --grade 2 "Top secret! The cookies are hidden in the red bowl!"
Top ¡ʇǝɹɔǝs The sǝᴉʞooɔ are uǝppᴉɥ in ǝɥʇ red ¡ꞁʍoq
```

[More examples](Examples.md)

