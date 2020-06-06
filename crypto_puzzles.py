#!/usr/bin/env python3

# crypto puzzles
# pseudo encryption, never use for anything serious!
# Copyright 2020 Arnim Rupp


#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


from __future__ import unicode_literals
import sys
import codecs
import pyqrcode
import random
import argparse
import upsidedown
import re
import roman
import base64
from string import ascii_lowercase
from collections import defaultdict

number_words={}
# number words have to be in the right order and start with 0
number_words['de'] = ['null', 'eins','zwei','drei','vier','fünf','sechs','sieben','acht','neun','zehn', 'elf', 'zwölf']
number_words['en'] = ['zero', 'one','two','three','four','five','six','seven','eight','nine','ten', 'eleven', 'twelve']

animals = {}
animals['en'] = [
        'ape',
        'bird',
        'lion',
        'elephant',
        'beaver',
        'bunny',
        'tiger',
        'squirrel',
        'stegosaurus',
        'shark',
        'carp',
        'swallow',
        'parrot',
        'swan',
        'snake',
        'wasp',
        'dolphin',
        'leopard',
        'hippo',
        'raven',
        'frog',
        'butterfly',
        ]
animals['de'] = [
        'affe',
        'vogel',
        'löwe',
        'elefant',
        'biber',
        'hase',
        'tiger',
        'eichhörnchen',
        'stegosaurus',
        'hai',
        'karpfen',
        'schwalbe',
        'papagei',
        'schwan',
        'kreuzotter',
        'biene',
        'delfin',
        'leopard',
        'nilpferd',
        'rabe',
        'frosch',
        'schmetterling',
        ]

alphabet_words = {}
alphabet_words['en'] = [
        'antelop',
        'bug',
        'computer',
        'dolphin',
        'empire',
        'fish',
        'goose',
        'hobbit',
        'internet',
        'jogger',
        'kangaroo',
        'lumber',
        'mars',
        'nose',
        'orange',
        'perfect',
        'queen',
        'ring',
        'sabre',
        'tunnel',
        'under',
        'vampire',
        'wardrobe',
        'xylophon',
        'yellow',
        'zebra',
        ]

alphabet_words['de'] = [
        'ameise',
        'blödelt',
        'computer',
        'der',
        'ehrlich',
        'fällt',
        'gestern',
        'hatschi',
        'in',
        'jetzt',
        'kommt',
        'laut',
        'mindestens',
        'nase',
        'oder',
        'perfekt',
        'quatsch',
        'reichlich',
        'schön',
        'toll',
        'und',
        'verspielt',
        'weil',
        'xylophon',
        'yak',
        'zaubert',
        ]

def insert_noise(intext, language, grade=1, noise_type="", noise_chars=""):

    # e.g. top secret => tRÖNFoRÖNFpRÖNFsRÖNFeRÖNFcRÖNFrRÖNFeRÖNFtRÖNF
    outtext=""
    hint=""

    if grade > 2:
        # remove whitespace
        intext=intext.replace(' ', '')

    for char in intext:
        if char == ' ':
            outtext = outtext + ' '
        else:
            outtext = outtext + char + get_noise(language, grade, noise_type, noise_chars)

    return outtext, hint

def get_noise(language, grade, noise_type="", noise_chars=""):

    noise=''

    if noise_type == 'numberwords':
        noise = number_words[language][random.randrange(len(number_words[language])-1)]
    elif noise_type == 'numbers':
        noise = str(random.randrange(99))
    elif noise_type == 'specialchars':
        choice=';:_-,.+*#!%&/()[]=|<>'
        noise = choice[random.randrange(len(choice))]
    elif noise_type == 'currency_symbols':
        # chars which look very similar to normal chars
        choice='$€¥₳₩₰₮₪฿￡₱￠₣₲₭Ł₥₴'
        noise = choice[random.randrange(len(choice))]
    elif noise_type == 'animals':
        noise = animals[language][random.randrange(len(animals[language])-1)]
    elif noise_chars:
        noise = noise_chars
    else:
        # if neither noise_type nor noise_chars is defined, pick something according to grade
        if grade == 1:
            noise = get_noise(language,grade, 'specialchars')
        elif grade == 2:
            noise="RÖNF"
        elif grade == 3:
            noise = get_noise(language,grade, 'numbers')
        elif grade == 4 or grade == 5:
            noise="rönf"
        elif grade == 6:
            noise = get_noise(language,grade, 'animals')
        elif grade == 7:
            # numbe words are harder bec shorter
            noise = get_noise(language,grade, 'numberwords')
        elif grade == 8:
            # mix of animals and numbers
            if random.randrange(2) == 1:
                noise = get_noise(language,grade, 'numberwords')
            else:
                noise = get_noise(language,grade, 'animals')
        else:
            # mix of animals, numbers, ...
            dice = random.randrange(3)
            if dice == 0:
                noise = get_noise(language,grade, 'numberwords')
            elif dice == 1:
                noise = get_noise(language,grade, 'animals')
            else:
                noise = get_noise(language,grade, 'currency_symbols')

    return noise


def randomize_middle_of_words(intext, language, grade=1):

    # top secret => top screet, top sercet, ...
    outtext=""
    hint=""
    words=intext.split()
    for word in words:
        rword = randomize_middle_of_one_word(word, grade)
        outtext = outtext + rword + ' '

    return outtext.rstrip(' '), hint

def randomize_middle_of_one_word(word, grade):
    rword=""
    count=0
    # don't start for words with 3 chars because it won't change
    if len(word) > 3:
        # repeat if rword by random chance equals word 
        # have a maximum of count iterations to avoid endless loops on words with equal chars in the middle like "tool" or "wooooot"
        while (word == rword or not rword) and count < 10:
            count += 1
            chars=list(word)
            rword=chars.pop(0)

            # keep chars in beginning of word intact depending on word length and grade
            if grade < 4:
                rword += chars.pop(0)
            if len(chars) > 7:
                rword += chars.pop(0)
            if len(chars) > 9:
                rword += chars.pop(0)
            if len(chars) > 11:
                rword += chars.pop(0)
            # for German and Finnish :)
            if len(chars) > 12:
                rword += chars.pop(0)
            if grade < 8 and len(chars) > 8:
                rword += chars.pop(0)

            while len(chars) > 1:
                rword += chars.pop(random.randrange(len(chars)-1))
            rword = rword + chars[0]
        return rword
    else:
        return word

def upside_down(text, language, grade, upside_down_rate=0):

    # top secret => doʇ ʇǝɹɔǝs

    if grade == 1:
        upside_down_rate = 1
    else:
        upside_down_rate = 2

    #print(grade, upside_down_rate)

    # todo: fix upstream (but that might need some time, until it's in pypi)
    # workaround for chars not properly displayed on QR reader of iOS 13.4.1 (works also fine on android 8.1.0 patchlevel april 2020)
    text = text.replace('Ü', 'ü') # lowercase ü works (introduce orthographic errors!!! ;)
    # Q => Ꝺ doesn't work on iOS but didn't find a good replacement yet
    text = text.replace('Q', 'q') # lowercase q works (introduce orthographic errors!!! ;)

    words=text.split()
    count=0
    outtext=""
    hint=""
    for word in words:
        count += 1

        if grade > 2:
            word, hint = insert_noise(word, language, 1)

        if count/upside_down_rate == int(count/upside_down_rate):
            rword = upsidedown.transform(word)
        else:
            rword= word
        outtext = outtext + rword + " "
        #print(rword, end=" ")

    # todo: fix upstream (but that might need some time, until it's in pypi)
    # workaround for chars not properly displayed on QR reader of iOS 13.4.1
    outtext = outtext.replace('ꞁ', '|') # l
    outtext = outtext.replace('Ꞁ', '˥') # L
    return outtext, hint





def repl(x):
    replacements.append(x.group(1))
    return ''


def reichify(wort, grade):

    wort_org=wort

    # remove punctuation marks (and restore them later)
    #replacements = []
    wort_org = re.sub('([\.,:;])$', repl, wort_org)

    # aber => aba
    if len(wort_org) > 3:
        wort = re.sub('er$', 'a', wort)

    if 'tzt' in wort_org:
        wort = wort.replace('tzt','ts')
    elif 'tz' in wort_org:
        wort = wort.replace('tz','ts')

    # dehnungs-h raus
    if 'hm' in wort_org and not 'chm' in wort_org:
        wort = wort.replace('hm','m')
    if 'hn' in wort_org and not 'chn' in wort_org:
        wort = wort.replace('hn','n')
    if 'hr' in wort_org and not 'chr' in wort_org:
        wort = wort.replace('hr','r')
    if 'hl' in wort_org and not 'chl' in wort_org:
        wort = wort.replace('hl','l')
    if 'ht' in wort_org and not 'cht' in wort_org:
        wort = wort.replace('ht','t')

    if grade > 2:
        if 'sch' in wort_org:
            wort = wort.replace('sch','ch')
        elif 'ch' in wort_org:
            wort = wort.replace('ch','sch')

    if 'ie' in wort_org:
        wort = wort.replace('ie','i')

    if 'ei' in wort_org:
        wort = wort.replace('ei','ai')
    elif 'ai' in wort_org:
        wort = wort.replace('ai','ei')
    elif 'e' in wort_org:
        wort = wort.replace('e','ä', 1)

    if grade > 4:
        if 'äu' in wort_org:
            würfel=random.randint(1,6)
            if würfel < 3:
                wort = wort.replace('äu','oi')
            elif würfel > 4:
                wort = wort.replace('äu','eu')
            else:
                wort = wort.replace('äu','öj')
        elif 'ä' in wort_org:
            wort = wort.replace('ä','e')

    if grade > 2:
        # doppelte raus
        wort = re.sub('(.)\\1', '\\1', wort)

    if 'ck' in wort_org:
        wort = wort.replace('ck','k')

    if grade > 5:
        if 'b' in wort_org:
            wort = wort.replace('b','p')
        elif 'p' in wort_org:
            wort = wort.replace('p','b')

    if grade > 3:
        if 'st' in wort_org:
            wort = wort.replace('st','schd')
        elif 't' in wort_org:
            wort = wort.replace('t','d')
        # d in artikeln lassen
        elif 'd' in wort_org and (len(wort_org) > 3 or re.search('d$', wort_org)):
            wort = wort.replace('d','t', 1)


    if grade > 2:
        if 'g' in wort_org:
            wort = wort.replace('g','k')
        elif 'k' in wort_org:
            wort = wort.replace('k','g')
        if 'qu' in wort_org:
            wort = wort.replace('qu','kw')
        if 'v' in wort_org:
            wort = wort.replace('v','f')
        elif 'f' in wort_org:
            wort = wort.replace('f','v')


    if 'y' in wort_org:
        wort = wort.replace('y','i')

    wort = re.sub('x', 'ks', wort)

    # fvb spezial
    if wort_org == 'baby':
        wort = 'bebi'

    # großschreibung zufällig
    if random.randint(1,6) == 1:
        wort = wort.title()

    if replacements:
        wort = wort + replacements.pop()

    return wort

def lässn_tursch_chraipen(intext, language, grade):

    # special encryption, ignore if you're not from germany ;)
    # streng geheim => schdränk Kehaim

    # list for use in repl function in re.sub later
    global replacements 
    replacements = []

    wörter=intext.lower().split(' ')

    outtext=""
    hint=""
    for wort in wörter:
        reichen_wort = reichify(wort, grade)
        outtext = outtext + reichen_wort + ' '

    return outtext.rstrip(' '), hint

def leet(text, language, grade):
    hint=""
    text = text.replace('o','0')
    text = text.replace('O','0')
    text = text.replace('s','$')
    text = text.replace('E','€')
    text = text.replace('i','1')

    if grade > 3:
        text = text.replace('f','ph')
        text = text.replace('a','@')
        text = text.replace('e','3')
    return text, hint
    
def wrong_whitespace(intext, language, grade):
    # top secret => to pse cret

    if grade > 5:
        # make it harder by mirroring the words (at grade 1)
        intext, hint = mirror_words(intext, language, 1)

    words=intext.split()
    outtext=""
    hint=""
    for word in words:
        if grade == 1:
            # uppercase original first char to make it easier
            word=word.title()

        if grade == 1:
            # just remove spaces, don't insert wrong ones
            # top secret => topsecret
            outtext += word
        else:
            if len(word) == 1:
                outtext += word
            elif len(word) == 2:
                outtext += word[0] + ' ' + word[1]
            else:
                cut = 1 + random.randrange(len(word)-1)
                outtext += word[:cut]
                outtext +=' '
                if grade > 4:
                    # uppsercase wrong first chars of words for additional confusion
                    # top secret => to Pse Cret
                    outtext += word[cut:].title()
                else:
                    outtext += word[cut:]

    return outtext, hint
            
def mirror_words(intext, language, grade):
    # top secret => pot terces


    words=intext.split()
    outtext=""
    hint=""
    for word in words:
        outtext += word[::-1] + ' '

    if grade > 5:
        # insert noise with reduced grade
        outtext, hint = insert_noise(outtext, language, grade -5)

    return outtext.rstrip(' '), hint

def shift_words(intext, language, grade):
    # top secret => pto ecrets
    words=intext.split()
    outtext=""
    hint=""

    # list for use in repl function in re.sub later
    global replacements
    replacements = []

    for word in words:
        word = re.sub('([\.,:;!?])$', repl, word)
        if grade < 3:
            outtext += word[1:] + word[0]
        else:
            outtext += word[2:] + word[0:2]

        if replacements:
            outtext += replacements.pop()
        outtext += ' '

    outtext = outtext.rstrip(' ')

    # make harder
    if grade > 3:
        outtext, hint_dummy = camelcase(outtext, language, 1)
    if grade > 5:
        # insert noise with reduced grade
        outtext, hint = insert_noise(outtext, language, grade -4 )

    return outtext, hint

def camelcase(intext, language, grade):
    # top secret => tOp sEcReT
    outtext=""
    hint=""
    up=0
    for char in intext:
        if up == 1:
            up=0
            outtext += char.upper()
        else:
            up=1
            outtext += char.lower()
    return outtext.rstrip(' '), hint

def rot13(intext, language, grade):
    # top secret => gbc frperg
    hint=""
    if grade < 5:
        hint="a=n, b=o, c=p, d=q, e=r, f=s, g=t, h=u, i=v, j=w, k=x, l=y, m=z, n=a, o=b, p=c, q=d, r=e, s=f, t=g, u=h, v=i, w=j, x=k, y=l, z=m"
    elif grade < 7:
        hint="a=n, b=o, c=p, d=q, ..."
    elif grade < 9:
        hint="a=n, b=o, ..."
    else:
        hint="Caesar, rot13, geocaching"

    return (codecs.encode(intext, "rot-13")), hint

def char_to_num(intext, language, grade):
    # top secret => 20,15,16, 19,5,3,18,5,20
    # a=> 1 , b=> 2, c=>3, ...

    # make all lowercase
    intext=intext.lower()
    outtext=""
    hint=""
    count = 4-grade
    for char in intext:
        if char == ' ':
            outtext += ' '
        else:
            count += 1
            if grade < 4:
                hint = "a=1, b=2, c=3, ..."
                char_num = ord(char)-96
                # only convert every nth char to num
                if count/(5-grade) == int(count/(5-grade)) and (char_num >= 0 and char_num < 27 ):
                    outtext += str(char_num) + ',' 
                else:
                    outtext += char + ',' 

            elif grade < 7:
                hint = "a=1"
                # all chars to num
                char_num = ord(char)-96
                if char_num >= 0 and char_num < 27:
                    outtext += str(char_num) + ',' 
                else:
                    outtext += char + ',' 
            else:
                # use roman numbers
                # top secret => XX,XV,XVI, XIX,V,III,XVIII,V,XX
                if language == 'de':
                    hint = "Rom"
                elif language == 'en':
                    hint = "Rome"
                char_num = ord(char)-96
                if char_num >= 0 and char_num < 27:
                    outtext += roman.toRoman(ord(char)-96) + ',' 
                else:
                    outtext += char + ',' 


    return outtext.rstrip(','), hint

def ip_to_roman(ip):
    # for https://192.168.1.123/puzzle.py => https://CXCII.CLXVIII.I.CXXIII/puzzle.py
    tuples = ip.split('.')
    outtext=""
    hint=""
    for tuple in tuples:
        outtext += roman.toRoman(int(tuple)) + '.' 
    return outtext.rstrip('.')

def char_to_word(intext, language, grade):
    # top secret => Toll Oder Perfekt  Schön Ehrlich Computer Reichlich Ehrlich Toll
    intext=intext.lower()
    outtext=""

    if language == 'en':
        hint="Ape = A, Bear = B, Clown = C, ..."
    elif language == 'de':
        hint="Affe = A, Baum = B, Clown = C, ..."

    for char in intext:
        char_num = ord(char)-97
        if char_num >= 0 and char_num < 27:
            if grade < 4:
                # top secret => T-oll O-der P-erfekt  S-chön E-hrlich C-omputer R-eichlich E-hrlich T-oll
                outtext += alphabet_words[language][char_num][0]  + '-' + alphabet_words[language][char_num][1:]  + ' '
            elif grade < 6:
                # uppercase 1st chars to emphasize them
                outtext += alphabet_words[language][char_num].title() + ' '
            elif grade < 7:
                outtext += alphabet_words[language][char_num] + ' '
            elif grade < 9:
                # without spaces between replaced words, but between real words
                outtext += alphabet_words[language][char_num] 
            else:
                outtext += alphabet_words[language][char_num] + ' '
                outtext, hint_dummy = camelcase(outtext, language, 1)
        else:
            if grade < 7:
                outtext += char
            else:
                outtext += char + ' '

    return outtext.rstrip(' '), hint

def substitute_partly_solved_frequency_analysis(intext, language, grade=1):

    # top secret => every character is substituted by a random number
    outtext=""
    hint=""

    worktext=intext.lower()
    num_for_letter = {}
    num_to_letter = {}
    count_letters = defaultdict(int)


    # get random number fpr each letter of the alphabet
    for letter in ascii_lowercase:

        while True:
            # use numbers > 30 to avoid confusion with a=1, b=2, c=3, ... (maybe leave that for higher grades?)
            num = random.randrange(69) + 30
            if num not in num_for_letter.values():
                num_for_letter[letter] = num
                num_to_letter[str(num)] = letter
                break

    for letter in worktext:
        if letter in ascii_lowercase:
            outtext += str(num_for_letter[letter]) + ','
            count_letters[letter] += 1
        else:
            outtext += letter + ','

    if language == 'en':
        hint = 'This message was encrypted using a random assignment of letters to numbers, an example would be a=421, b=178, c=288, ... . It would far too long to try every possible combination but we can use the knowledge, that for example E, N and S appear more often in the English language than Q or X. Some of the common letters have been pre filled by the frequency of the respective numbers. You should be able to fill in the rest ;) (Btw, in cryptography this method to break a code is called "frequency analysis")'
    elif language == 'de':
        hint = 'Diese Botschaft ist durch eine zufällige Zuordnung von Buchstaben zu Zahlen verschlüsselt worden, ein Beispiel wäre a=421, b=178, c=288, ... . Alle Möglichkeiten durchzuprobieren würde viel zu lange dauern aber man kann ausnutzen, dass einige Buchstaben wie beispielsweise E und N viel häufiger vorkommen, als Q und Y. Die häufigsten Buchstaben im Deutschen sind in absteigender Reihenfolge E N S I R A T. Einige davon haben wir bereits nach der Häufigkeit der Zahlen eingetragen. Den Rest kriegt man alleine hin ;) (Übrigens, dieses Verfahren nennt man Häufigkeitsanalyse in der Kryptographie.)'

    return outtext, hint, count_letters, num_for_letter, num_to_letter


def null_cipher(intext, language, grade):
    # no encryption, just return intext
    return intext, ''


def convert_num_to_number_words(intext, language):

    outtext = ''
    # 123 => one two three
    for char in intext:
        if char in "0123456789":
            value = int(char)
            outtext += number_words[language][value] + ' '
        else:
            outtext += char

    return outtext

def qr_code(intext, language, filename):

    # size or qr code
    # don't make it too small because some cheap kids smartphones with fix focus lenses aren't good at macro mode.
    # too big uses more ink
    scale = 4

    # set maximum error correction for better reading if parts of the QR code are crumbled or missing
    qr = pyqrcode.create(intext, encoding='utf-8', mode='binary', error='H')

    # set color to grey to save ink at printing
    qr.png(filename, scale=scale, module_color=(100, 100, 100))

    return filename


#def join_puzzle(intext, language, grade, player_names=['Alice', 'Bob', 'Carol'], noise=''):
def join_puzzle(intext, language, grade, player_names=['Alice', 'Bob'], noise=''):

    # top secret for real => ['top:for:', 'secret:real:']
    # split intext into several outtexts which need to be combined by the players
    # useful to get all players on the same stage
    # todo: this code is very euli specific at the moment, mainly here for easier debugging

    # create list of noise words to avoid being abe to guess the right place by a lucky shot
    if language == 'en':
        continue_at = ' // continue at player '
        line_word = ' in line number '
        if not noise: noise ='spoon fork knive kitchen bathroom under bed handle toothbrush garden door couch computer table chair sink tap window carpet drawer'
    if language == 'de': 
        continue_at = ' // Weiter bei Spieler '
        line_word = ' in Zeilenummer '
        if not noise: noise ='Löffel Gabel Messer Küche Badezimmer unter Bett Griff Zahnbürste Garten Tür Couch Computer Tisch Stuhl Waschbecken Wasserhahn Fenster Teppich Schublade'

    noise_words=noise.split()

    number_of_players= len(player_names)
    #outtexts = [""] * number_of_players
    outtexts = defaultdict(str)
    hint=""

    player_num=0
    # init all players positions with 1
    positions=[1] * number_of_players

    words=intext.split()
    for word in words:

        next_player = (player_num + 1) % number_of_players
        next_player_of_next_player = (next_player + 1) % number_of_players

        # fill in some noise for next player
        for lola in range(random.randrange(1,4)):
            outtexts[player_names[next_player]] += str(positions[next_player]) + ' ' + noise_words[random.randrange(len(noise_words)-1)] + continue_at + player_names[next_player_of_next_player] + line_word + str(positions[next_player] + random.randrange(0,3)) + '\n'
            #outtexts[next_player] += str(positions[next_player]) + ' ' + noise_words[random.randrange(len(noise_words)-1)] + continue_at + player_names[next_player_of_next_player] + line_word + str(positions[next_player] + random.randrange(0,3)) + '\n'
            positions[next_player] += 1 

        outtexts[player_names[player_num]] += str(positions[player_num]) + ' ' + word + continue_at + player_names[next_player] + line_word + str(positions[next_player]) + '\n'

        # count up own position and switch to next player
        positions[player_num] += 1 
        player_num = next_player

    return outtexts


def generate_crackme_python(intext, language, grade, crackme_num):

    outtext = ''

    crackme_template = {}

    if crackme_num == 1 or grade <6:

        # define template for crackme, anything with TEMPL_ will be replaced with beef
        # todo!!! this sucks, seperate code from text 
        crackme_template['de'] = """#!/usr/bin/env python3

# Dieses kleine Programm kennt das Geheimnis, das Du suchst, wird es Dir aber erst in 9582790 Billionen Jahren verraten, harhar :) Wenn Du nicht so viel Zeit hast, musst Du einen anderen Weg suchen ...

import base64
import time

print('Das ', end='', flush=True)
time.sleep(1)
print('Geh', end='', flush=True)
time.sleep(2)
print('heim', end='', flush=True)
time.sleep(4)
print('nis ', end='', flush=True)
time.sleep(8)
print('ist ', end='', flush=True)
time.sleep(16)
print('echt ', end='', flush=True)
time.sleep(16)
print('sehr ', end='', flush=True)
time.sleep(16)
print('geheim ', end='', flush=True)
time.sleep(16)
print('und ', end='', flush=True)
time.sleep(16)
print('ich werd es Dir in 9582790 Billionen Jahren verraten: ', end='', flush=True)
time.sleep(65536133708153272784892092746726238958271672343782738923972138217189789897890)

print (base64.b64decode('TEMPL_BASE64_SECRET').decode('utf8'))
"""

        crackme_template['en'] = """#!/usr/bin/env python3

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

print (base64.b64decode('TEMPL_BASE64_SECRET').decode('utf8'))
"""
        secret = str(base64.b64encode(intext.encode('utf-8')), 'utf-8')

        outtext = crackme_template[language]
        outtext = outtext.replace('TEMPL_BASE64_SECRET', secret)

    elif crackme_num == 2 or grade >= 6:

        # define template for crackme, anything with TEMPL_ will be replaced with beef
        crackme_template['de'] = """#!/usr/bin/env python3

# Dieses kleine Programm kennt das Geheimnis, das Du suchst, wird es Dir aber auf gar keinstem Fall überhaupt nicht verraten. Außer die zwingst es dazu ;)

import base64
import hashlib
import time

passwort=input('Wie lautet das Passwort? ')

hashitem=hashlib.new('sha256')
hashitem.update(passwort.encode('utf8'))
hexdigest_passwort=hashitem.hexdigest

if hexdigest_passwort == '9f86d081884c7d659a2feaa0c55ad015a3bf4fb12b0b822cd15d6c15b00f0a08' and passwort[:4:] == 'F' and hexdigest_passwort[1:2:] == 'XR' and False:
    print('Das Geheimnis ist: ', end='')
    secret1 = 'TEMPL_BASE64_SECRET1'
    secret3 = 'TEMPL_BASE64_SECRET3'
    secret2 = 'TEMPL_BASE64_SECRET2'
    secret = secret1 + secret2 + secret3
    print (base64.b64decode(secret).decode('utf-8'))

else:
    print('Falsches Passwort!')

"""

        crackme_template['en'] = """#!/usr/bin/env python3

# This little script knows the secret you are looking for, but will never tell it to you, unless you force it to ;)

import base64
import hashlib
import time

passwort=input('What it the password? ')

hashitem=hashlib.new('sha256')
hashitem.update(passwort.encode('utf8'))
hexdigest_passwort=hashitem.hexdigest

if hexdigest_passwort == '9f86d081884c7d659a2feaa0c55ad015a3bf4fb12b0b822cd15d6c15b00f0a08' and passwort[:4:] == 'F' and hexdigest_passwort[1:2:] == 'XR' and False:
    print('The secret is: ', end='')
    secret1 = 'TEMPL_BASE64_SECRET1'
    secret3 = 'TEMPL_BASE64_SECRET3'
    secret2 = 'TEMPL_BASE64_SECRET2'
    secret = secret1 + secret2 + secret3
    print (base64.b64decode(secret).decode('utf-8'))

else:
    print('Wrong password!')

"""
        secret = str(base64.b64encode(intext.encode('utf-8')), 'utf-8')

        # split secret into 2 strings to make copy&paste into cyberchef a bit harder
        # don't pick a slice dividable by 3 or it will work
        secret1 = secret[:4]
        secret2 = secret[4:8]
        secret3 = secret[8:]

        outtext = crackme_template[language]
        outtext = outtext.replace('TEMPL_BASE64_SECRET1', secret1)
        outtext = outtext.replace('TEMPL_BASE64_SECRET2', secret2)
        outtext = outtext.replace('TEMPL_BASE64_SECRET3', secret3)

    return outtext


def get_crypto_functions(type='all'):

    # encryption of flags has to be 100% reversible and not e.g. randomize the order of the numbers
    if type == 'reversible':
        crypto_functions_text="""insert_noise
upside_down
wrong_whitespace
mirror_words
shift_words
char_to_word
"""
# char_to_num not reversible if the message contains numbers ;)


    else:
        # all
        crypto_functions_text="""insert_noise
upside_down
leet
wrong_whitespace
mirror_words
shift_words
char_to_num
char_to_word
"""
# leave out, boring:
#randomize_middle_of_words

    crypto_functions=[]
    for line in crypto_functions_text.splitlines():
        crypto_functions.append(line)
    return crypto_functions

def main():

    # parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("plaintext", help="Plain text to be \"encrypted\"")
    parser.add_argument("--technique", "-T", help="Techniques used to \"encrypt\". Such argument is a string composed by any combination of NUMLlWmSC13Asnc characters where each letter stands for a different technique. Be careful in combining them, it get's incomprehensible quickly ;) Start with e.g. \"top secret\" and tell it the recipient to enable a known plaintext attack.", required=True)
    parser.add_argument("--noise_type", help="Type of noise. Can be numbers,numberwords, animals")
    parser.add_argument("--noise_chars", help="Character(s) for noise")
    parser.add_argument("--upside_down_rate", help="Turn every nth word", default=2)
    parser.add_argument("--grade", "-g", help="Adjust difficulty by school grade aka years of school experience.", default=1)
    parser.add_argument("--language", help="Language for hints", default='en')
    parser.add_argument("--crackme_num", help="Number of crackme", default=1)
    parser.add_argument("--num_parts", help="Number of parts for join_puzzle", default=2)
    parser.add_argument("--seed", help="Random seed (only set to static number to always get the same randomness for debugging!)")
    parser.add_argument("--show_function_name",action='store_true', help="Shows the python function name below the encrypted text (for internal use)")
    args = parser.parse_args()
    noise_type = args.noise_type
    language = args.language
    noise_chars = args.noise_chars
    grade = int(args.grade)
    upside_down_rate = int(args.upside_down_rate)
    crackme_num = int(args.crackme_num)
    seed = args.seed
    show_function_name = args.show_function_name
    num_parts = int(args.num_parts)

    outtext = ""
    function_name = ""
    worktext = args.plaintext
    worktexts = []

    if seed:
        random.seed(a=seed)

    for technique in args.technique:

        if technique == "N":
            worktext, hint = insert_noise(worktext, language, grade, noise_type, noise_chars)
            function_name = "insert_noise"
        elif technique == "U":
            worktext, hint = upside_down(worktext, language, grade, upside_down_rate)
            function_name = "upside_down"
        elif technique == "M":
            worktext, hint= randomize_middle_of_words(worktext, language, grade)
            function_name = "randomize_middle_of_words"
        elif technique == "L":
            worktext, hint= lässn_tursch_chraipen(worktext, language, grade)
            function_name = "lässn_tursch_chraipen"
        elif technique == "l":
            worktext, hint= leet(worktext, language, grade)
            function_name = "leet"
        elif technique == "W":
            worktext, hint= wrong_whitespace(worktext, language, grade)
            function_name = "wrong_whitespace"
        elif technique == "m":
            worktext, hint= mirror_words(worktext, language, grade)
            function_name = "mirror_words"
        elif technique == "S":
            worktext, hint= shift_words(worktext, language, grade)
            function_name = "shift_words"
        elif technique == "C":
            worktext, hint= camelcase(worktext, language, grade)
            function_name = "camelcase"
        elif technique == "1":
            worktext, hint= char_to_num(worktext, language, grade)
            function_name = "char_to_num"
        elif technique == "3":
            worktext, hint= rot13(worktext, language, grade)
            function_name = "rot13"
        elif technique == "A":
            worktext, hint= char_to_word(worktext, language, grade)
            function_name = "char_to_word"
        # not really useful on command line yet:
        elif technique == "s":
            worktext, hint, count_letters = substitute_partly_solved_frequency_analysis(worktext, language, grade)
            function_name = "substitute_partly_solved_frequency_analysis"
        elif technique == "n":
            worktext = convert_num_to_number_words(worktext, language)
            function_name = "convert_num_to_number_words"
        elif technique == "c":
            worktext = generate_crackme_python(worktext, language, grade, crackme_num)
            function_name = "generate_crackme_python"
        elif technique == "j":
            worktexts = join_puzzle(worktext, language, grade)
            function_name = "join_puzzle"
         
    if show_function_name:
        print(function_name)

    if worktexts:
        #print(worktexts)
        for worktext in worktexts:
            print(worktext, worktexts[worktext])
    else:
        print(worktext)

if __name__ == "__main__":
    main()

