#!/usr/bin/env python3

# crypto puzzles
# encryption for fun, never use for anything serious!
# Use utf8 save editor/IDE because it contains emoji
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
from pyfiglet import Figlet
from string import ascii_lowercase
from collections import defaultdict
from PIL import Image
from math import sqrt

# Emoji alphabet
# Beware, emoji look different depending on the plattform so only choose ones, where the character can be 
# recognized everywhere
# seperate by comas because grapheme cluster support in python sucks, see https://hsivonen.fi/string-length/
# goal: have multiple options for common letters (ensirat) + don't use upside down because that's another function
# while editing, beware of the right to left characters ;)
emoji_letter={}
emoji_letter['a'] ='🅰️,ค,🃑,₳,ꬃ' # small ⎃ ?
emoji_letter['b'] ='🅱️,฿,𝔅,ᛒ,ℬ,ط'
emoji_letter['c'] ='©️,☪️,¢,℃,🂬,𝄴,ᆮ'
emoji_letter['d'] ='🌛,ԃ,Đ'
emoji_letter['e'] ='€,∈,📧,ℰ,モ' # 💶
emoji_letter['f'] ='℉,🎏,ƒ,₣,ᚩ'
emoji_letter['g'] ='Ⓖ,Ǥ,ﻮ,Ꮆ,₲'
emoji_letter['h'] ='♓,ℏ,ዙ,ᚺ'
emoji_letter['i'] ='ℹ️,🕕,𝔦,⌶,ï,༐'
emoji_letter['j'] ='⤴️,🕙,ɉ,ʝ,🃛,𝔧,ڸ'
emoji_letter['k'] ='Ⓚ,🃞,₭,㉿,ᛕ'
emoji_letter['l'] ='🕒,🛴,Ⱡ,£,ட' # 💷
emoji_letter['m'] ='♏,〽️,Ⓜ️,ℳ,₥,𝔐,ற,ᛖ'
emoji_letter['n'] ='♑,ℕ,И,🅽,ŋ,ᾗ,₦'
emoji_letter['o'] ='⭕,🍩,💍,𝔬'
emoji_letter['p'] ='🅿️,₱,🆊,₱,₽,𝔭,ᚹ'
emoji_letter['q'] ='Ǭ,Ɋ,🂭,𝔮'
emoji_letter['r'] ='®️,Ȑ,Ɽ,ℜ,ℛ,ᚱ'
emoji_letter['s'] ='⚡,💲,💰,⑀,ى' # small 💵?
emoji_letter['t'] ='✝️,ƫ,ȶ,🆃,Ṭ,₮,𝔱,⍑,ァ,ኘ,ፖ'
emoji_letter['u'] ='ᶙ,⛎'
emoji_letter['v'] ='♈,✌'
emoji_letter['w'] ='〰️,₩,௰' # not like w on some systems: 🔱
emoji_letter['x'] ='❌,❎,⚒,🛠,⚔️,✖,⤫,𝔛,྾,ᚸ' # 🙅‍♀️ is bad because sometimes displayed as '🙅‍♀️♀️' in ubuntu (broken grapheme clustering?)
emoji_letter['y'] ='¥,💴,Ŷ,⑂,ℽ,Ỿ,Ӳ'
emoji_letter['z'] ='Ƶ,ʑ,ɀ,💤,ᶽ'
emoji_letter['ä'] ='Ἂ,Ȁ'
emoji_letter['ö'] ='ő,⍥,ȫ,Ӫ,ة'
emoji_letter['ü'] ='ű,Ǚ,ت'
emoji_letter['ß'] ='ẞ'
emoji_letter['1'] ='🥇,❶' #1️⃣ boring ... dice 1 ⚀ hard to recognize, very small ♳♴♵ ?
emoji_letter['2'] ='🥈,➁,🂲,⚁,ᆯ,༢' #2️⃣
emoji_letter['3'] ='🥉,ᗱ,⚂,༣' #3️⃣
emoji_letter['4'] ='4️⃣,ᔰ,🂴,⚃'
emoji_letter['5'] ='5️⃣,Ƽ,🃅,⚄,༥'
emoji_letter['6'] ='6️⃣,➅,🃖,⚅'
emoji_letter['7'] ='7️⃣,⑦,🂷,ㇴ'
emoji_letter['8'] ='∞,🎱,𝟠'
emoji_letter['9'] ='9️⃣,⑨'
emoji_letter['0'] ='🅾️,Ѳ' # 0️⃣

# might be too confusing?
#emoji_letter['10'] ='🔟'
#emoji_letter['11'] ='⓫'
# ...
#emoji_letter_multiple['100'] ='💯'
# domino, mahjong numbers also confusing: http://xahlee.info/comp/unicode_games_cards.html ?? for higher grades?

emoji_letter['*'] ='*️⃣✳️'
emoji_letter['#'] ='#️⃣'
emoji_letter['+'] ='➕'
emoji_letter['-'] ='➖'
#emoji_letter[':'] ='' # ??? 
emoji_letter['/'] ='／'
emoji_letter['!'] ='❕,❗️'
emoji_letter['?'] ='❓,�'

emoji_letter_multiple={}
# boooooring
#emoji_letter_multiple['ii'] ='ⅱ'
#emoji_letter_multiple['iv'] ='ⅳ'
#emoji_letter_multiple['vi'] ='ⅵ'
#emoji_letter_multiple['ⅶ'] ='ⅶ'
#emoji_letter_multiple['ix'] ='ⅸ'
#emoji_letter_multiple['xi'] ='ⅺ'
emoji_letter_multiple['sm'] ='℠'
emoji_letter_multiple['tm'] ='™️'
emoji_letter_multiple['!?'] ='⁉️'
emoji_letter_multiple['!!'] ='‼️'
emoji_letter_multiple['ab'] ='🆎,ab'  # replace ab by ab = keep it to have some variety, the ab will then be processed like single letters
emoji_letter_multiple['ae'] ='ᴭ'
emoji_letter_multiple['fi'] ='ﬁ,fi'
emoji_letter_multiple['fl'] ='ﬂ,fl'
emoji_letter_multiple['cl'] ='🆑,cl'
emoji_letter_multiple['sos'] ='🆘,sos'
emoji_letter_multiple['vs'] ='🆚,vs'
emoji_letter_multiple['id'] ='🆔,id'
emoji_letter_multiple['ok'] ='🆗,ok'
emoji_letter_multiple['ng'] ='🆖,ng'
emoji_letter_multiple['abc'] ='🔤,abc'
emoji_letter_multiple['cool'] ='🆒,cool'
emoji_letter_multiple['free'] ='🆓,free'
emoji_letter_multiple['new'] ='🆕,new'
emoji_letter_multiple['atm'] ='🏧,atm'
emoji_letter_multiple['back'] ='🔙,back'
emoji_letter_multiple['end'] ='🔚,end'
emoji_letter_multiple['soon'] ='🔜,soon'
emoji_letter_multiple['top'] ='🔝,top'
emoji_letter_multiple['on'] ='🔛,on'
emoji_letter_multiple['tel'] ='℡,tel'
emoji_letter_multiple['ds'] ='𝄉,ds'
emoji_letter_multiple['dc'] ='𝄊,dc'
emoji_letter_multiple['tr'] ='𝆖,tr'
emoji_letter_multiple['aa'] ='⎂,aa'
emoji_letter_multiple['no'] ='№,no'
emoji_letter_multiple['rs'] ='₨,rs'
emoji_letter_multiple['ce'] ='₠,ce' # Œ
# booooring:
#emoji_letter_multiple['nm'] ='㎚'
#emoji_letter_multiple['mm'] ='㎜'
#emoji_letter_multiple['cm'] ='㎝'
#emoji_letter_multiple['km'] ='㎞' # ㏎
emoji_letter_multiple['ml'] ='㎖,ml'
emoji_letter_multiple['dl'] ='㎗,dl'
emoji_letter_multiple['kl'] ='㎘,kl'
#emoji_letter_multiple['cc'] ='㏄'
#emoji_letter_multiple['ps'] ='㎰'
#emoji_letter_multiple['ns'] ='㎱'
#emoji_letter_multiple['ms'] ='㎳'
#emoji_letter_multiple['mg'] ='㎎'
#emoji_letter_multiple['kg'] ='㎏'
#emoji_letter_multiple['kb'] ='㎅'
#emoji_letter_multiple['mb'] ='㎆' # ㏔ 
#emoji_letter_multiple['gb'] ='㎇'
#emoji_letter_multiple['hz'] ='㎐' # ㎑ ㎒ ㎓  shouldn't come up in normal words
emoji_letter_multiple['thz'] ='㎔'
#emoji_letter_multiple['pv'] ='㎴'
#emoji_letter_multiple['nv'] ='㎵'
#emoji_letter_multiple['mv'] ='㎷'
#emoji_letter_multiple['kv'] ='㎸'
#emoji_letter_multiple['mv'] ='㎹'
#emoji_letter_multiple['pw'] ='㎺'
#emoji_letter_multiple['nw'] ='㎻'
#emoji_letter_multiple['mw'] ='㎽' # ㎿
#emoji_letter_multiple['kw'] ='㎾'
#emoji_letter_multiple['pa'] ='㎀' # ㎩
#emoji_letter_multiple['na'] ='㎁'
#emoji_letter_multiple['ma'] ='㎃'
#emoji_letter_multiple['ka'] ='㎄'
emoji_letter_multiple['rad'] ='㎭'
emoji_letter_multiple['kpa'] ='㎪'
emoji_letter_multiple['mpa'] ='㎫'
emoji_letter_multiple['gpa'] ='㎬'
emoji_letter_multiple['cal'] ='㎈' # ㎉
#emoji_letter_multiple['dm'] ='dm'
emoji_letter_multiple['mil'] ='㏕'
#emoji_letter_multiple['fm'] ='㎙'
#emoji_letter_multiple['au'] ='㍳'
emoji_letter_multiple['db'] ='㏈'
#emoji_letter_multiple['ln'] ='㏑'
emoji_letter_multiple['log'] ='㏒'
emoji_letter_multiple['am'] ='㏂'
emoji_letter_multiple['pm'] ='㏘'
emoji_letter_multiple['hpa'] ='㍱'
#emoji_letter_multiple['da'] ='㍲'
emoji_letter_multiple['bar'] ='㍴'
#emoji_letter_multiple['ov'] ='㍵'
#emoji_letter_multiple['pc'] ='㍶'
#emoji_letter_multiple['IU'] ='㍺'
#emoji_letter_multiple['pf'] ='㎊'
#emoji_letter_multiple['nf'] ='㎋'
#emoji_letter_multiple['bq'] ='㏃'
#emoji_letter_multiple['cd'] ='㏅'
emoji_letter_multiple['co'] ='㏇'
#emoji_letter_multiple['gy'] ='㏉'
#emoji_letter_multiple['ha'] ='㏊'
emoji_letter_multiple['hp'] ='㏋'
emoji_letter_multiple['kk'] ='㏍'
#emoji_letter_multiple['kt'] ='㏏'
#emoji_letter_multiple['lm'] ='㏐'
#emoji_letter_multiple['lx'] ='㏓'
emoji_letter_multiple['mol'] ='㏖'
#emoji_letter_multiple['ph'] ='㏗'
#emoji_letter_multiple['pr'] ='㏚'
#emoji_letter_multiple['sr'] ='㏛'
#emoji_letter_multiple['sv'] ='㏜'
#emoji_letter_multiple['wb'] ='㏝'
emoji_letter_multiple['hu'] ='Ƕ'
#emoji_letter_multiple['dz'] ='Ǳ'
emoji_letter_multiple['oe'] ='œ'
emoji_letter_multiple['ts'] ='ʦ'
emoji_letter_multiple['dz'] ='ʥ'
emoji_letter_multiple['th'] ='ᵺ'
emoji_letter_multiple['ue'] ='ᵫ'
emoji_letter_multiple['ls'] ='ʪ'
emoji_letter_multiple['fn'] ='ʩ'
emoji_letter_multiple['lz'] ='ʫ'
emoji_letter_multiple['ww'] ='ʬ'
emoji_letter_multiple['le'] ='ᇉ' # korean
emoji_letter_multiple['lc'] ='ᇆ'
# too small: 𝆮 ?

############################################################
emoji_letter_xmas={}
emoji_letter_xmas['a'] ='🎄'
emoji_letter_xmas['b'] ='฿,𝔅,ᛒ,ℬ,ط'
emoji_letter_xmas['c'] ='¢,℃,𝄴'
emoji_letter_xmas['d'] ='🌛,ԃ,Đ'
emoji_letter_xmas['e'] ='€,∈,ℰ,モ' 
emoji_letter_xmas['f'] ='℉,ƒ,₣,ᚩ'
emoji_letter_xmas['g'] ='Ⓖ,Ǥ,ﻮ,Ꮆ,₲'
emoji_letter_xmas['h'] ='ℏ,ዙ,ᚺ'
emoji_letter_xmas['i'] ='🕯️'
emoji_letter_xmas['j'] ='ɉ,ʝ,𝔧,ڸ'
emoji_letter_xmas['k'] ='Ⓚ,₭,㉿,ᛕ'
emoji_letter_xmas['l'] ='🕒,🛴,Ⱡ,ட' 
emoji_letter_xmas['m'] ='ℳ,₥,𝔐,ற,ᛖ'
emoji_letter_xmas['n'] ='ℕ,И,🅽,ŋ,ᾗ,₦'
emoji_letter_xmas['o'] ='🍪,❄️ '
emoji_letter_xmas['p'] ='₱,₱,₽,𝔭,ᚹ'
emoji_letter_xmas['q'] ='Ǭ,Ɋ,𝔮'
emoji_letter_xmas['r'] ='Ȑ,Ɽ,ℜ,ℛ,ᚱ'
emoji_letter_xmas['s'] ='⑀,ى' # small 💵?
emoji_letter_xmas['t'] ='✝️'
emoji_letter_xmas['u'] ='ᶙ'
emoji_letter_xmas['v'] ='♈'
emoji_letter_xmas['w'] ='〰️,₩,௰' # not like w on some systems: 🔱
emoji_letter_xmas['x'] ='✖,⤫,𝔛,྾,ᚸ' # 🙅‍♀️ is bad because sometimes displayed as '🙅‍♀️♀️' in ubuntu (broken grapheme clustering?)
emoji_letter_xmas['y'] ='¥,Ŷ,⑂,ℽ,Ỿ,Ӳ'
emoji_letter_xmas['z'] ='Ƶ,ʑ,ɀ,💤,ᶽ'

############################################################

# Emoji animal alphabet, works in english and german 
# include the disputed in a hard version someday
# if you find animal emoji for the missing letters, please tell me on github (see also emoji_animals_sorted.txt)
emoji_animal={}
emoji_animal['a'] ='🐜'
emoji_animal['b'] ='🐻'
#emoji_animal['c'] ='©️,☪️,¢,℃,🂬,𝄴,ᆮ'
emoji_animal['d'] ='🐬,🐉'
emoji_animal['e'] ='🐘'
emoji_animal['f'] ='🐟,🦊'
emoji_animal['g'] ='🦒'
emoji_animal['h'] ='🐹'
#emoji_animal['i'] ='ℹ️,🕕,𝔦,⌶,ï,༐'
#emoji_animal['j'] ='⤴️,🕙,ɉ,ʝ,🃛,𝔧,ڸ'
emoji_animal['k'] ='🦘 ,🐨'
emoji_animal['l'] ='🦁'
# recognizable?
#🐆 Leopard
#🦙 Llama, everybody would say alpaka I guess :)
emoji_animal['m'] ='🐁'
#emoji_animal['n'] ='♑,ℕ,И,🅽,ŋ,ᾗ,₦'
emoji_animal['o'] ='🐙'
emoji_animal['p'] ='🦜 ,🦚 ,🐧,🐩'
#emoji_animal['q'] ='Ǭ,Ɋ,🂭,𝔮'
emoji_animal['r'] ='🐀'
# rat is hard to distinguish from a mouse but the rhino is also hard in german because most people say nashorn
# 🦏 Rhinoceros
emoji_animal['s'] ='🦂,🐌,🐍,🕷️,🦢'
emoji_animal['t'] ='🐅,🦖'
# is the T-Rex recognizable? or just a "dino"?
#emoji_animal['u'] ='ᶙ,⛎'
#emoji_animal['v'] ='♈,✌'
emoji_animal['w'] ='🐋,🐺'
# 🐃 Water Buffalo, nobody would get this in german
#emoji_animal['x'] ='❌,❎,⚒,🛠,⚔️,✖,⤫,𝔛,྾,ᚸ' # 🙅‍♀️ is bad because sometimes displayed as '🙅‍♀️♀️' in ubuntu (broken grapheme clustering?)
#emoji_animal['y'] ='¥,💴,Ŷ,⑂,ℽ,Ỿ,Ӳ'
emoji_animal['z'] ='🦓'


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

# todo: do the same with emoji (avoid emoji which might have 2+ fitting words)
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

    #if grade > 2:
        # remove whitespace
        #intext=intext.replace(' ', '')

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
        elif grade < 9:
            # number words are harder because they're shorter
            noise = get_noise(language,grade, 'numberwords')
        elif grade < 11 :
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

    # todo: keep punctuation marks in place? at the moment it's dOʇ ¡⊥ǝᴚɔƎs, would dOʇ ⊥ǝᴚɔƎs¡ be better/easier for lower grades? (code in shift_words)

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

        if grade > 4:
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
    outtext += " 🙃 "
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

    # special German encryption, ignore if you're not from Germany ;)

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
        # store punctuation marks in replacements to avoid also shifting them, will be appended in the end
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
    if grade > 4:
        outtext, hint_dummy = camelcase(outtext, language, 1)
    if grade > 7:
        # insert noise with reduced grade
        outtext, hint = insert_noise(outtext, language, grade -7 )

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
    # todo: make rotX with known plaintext attack for the higher grades to figure out X
    hint=""
    if grade < 5:
        hint="a=n, b=o, c=p, d=q, e=r, f=s, g=t, h=u, i=v, j=w, k=x, l=y, m=z, n=a, o=b, p=c, q=d, r=e, s=f, t=g, u=h, v=i, w=j, x=k, y=l, z=m."
    elif grade < 7:
        hint="a=n, b=o, c=p, d=q, e=r, ..."
    elif grade < 11:
        hint="a=n, b=o, c=p, ..."
    else:
        hint="Caesar, rot13, geocaching"

    if grade < 11:
        if language =='en':
            hint += " This encryption is called Caesar cipher or ROT13. Each letter in the plaintext is replaced by a letter 13 positions down the alphabet."
        elif language =='de':
            hint += " Diese Verschlüsselung nennt sich Caesar-Verschlüsselung oder ROT13. Jeder Buchstabe im Klartext wird ersetzt durch den Buchstaben 13 Stellen weiter im Alphabet."

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

def stego_acrostic(intext, language, grade):
    # hide message in first character of the words
    # top secret => Toll Oder Perfekt  Schön Ehrlich Computer Reichlich Ehrlich Toll
    # could be improved by trying to produce sentences which at least follow basic structures like: subject verb object (not yet the level of medival crypto https://en.wikipedia.org/wiki/Steganographia ;)
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

    return outtext.rstrip(' ')

def qr_code(intext, language, filename='qr.png'):

    # create qr code and save to png. not a puzzle until you print it out and cut it in pieces ;) or have a puzzle in the resulting content (ǝpᴉsdn uʍop works great on all devices I've tried so far)

    if not filename: filename='qr.png'

    # size of qr code
    # don't make it too small because some cheap kids smartphones with fix focus lenses aren't good at macro mode.
    # too big uses more ink
    scale = 3

    # set maximum error correction for better reading if parts of the QR code are crumbled or missing
    #qr = pyqrcode.create(intext, encoding='utf-8', mode='binary', error='L')
    qr = pyqrcode.create(intext, encoding='utf-8', mode='binary', error='H')

    # set color to grey to save ink at printing
    qr.png(filename, scale=scale, quiet_zone=4, module_color=(100, 100, 100))

    if 'ƃnqǝp' in globals() and ƃnqǝp:
        print("saved file: " + filename)

    return filename

def qr_inside_qr(innertext, outertext, language, grade, filename):

    # create big QR code with small QR in the middle and save to png. 
    # this puzzles gives no hint in text form, but it's put into the outer QR

    if not filename: 
        filename='qr_in_qr.png'

    # outer QR is always light grey to save ink at printing. default for inner is the same grey
    color_inner=[100, 100, 100]
    if grade <3:
        # inner qr black to have contrast
        color_inner=[20, 20, 20]
        if language == 'en':
            # instead of covering the outer QR, the players could also use scissors to cut it away. but that's risky if they cut wrong, so hint for covering it.
            outertext = 'Hmmm, this looks like there is another QR code in the middle of the big one. But your QR reader can not read it, because the bigger QR code all around confuses it. Covering the big outer QR code with some paper might do the trick.'
        elif language == 'de':
            outertext = 'Hmmm, sieht so aus wie wenn da ein weitere QR Code in der Mitte des großen ist. Aber Dein QR-Leser kann ihn nicht erkennen, weil der große QR Code außenrum ihn verwirrt. Den äußeren QR Code mit etwas Papier abdecken könnte funktionieren.'
    elif grade <6:
        # inner qr dark grey to have contrast
        color_inner=[40, 40, 40]
        if language == 'en':
            outertext = 'Hmmm, this looks like there is another QR code in the middle of the big one. But your QR reader can not read it, because the bigger QR code all around confuses it. Four sheets of paper might do the trick.'
        elif language == 'de':
            outertext = 'Hmmm, sieht so aus wie wenn da ein weitere QR Code in der Mitte des großen ist. Aber Dein QR-Leser kann ihn nicht erkennen, weil der große QR Code außenrum ihn verwirrt. Mit vier Papieren an den richtigen Stellen könnte es funktionieren.'
        outertext, hint = camelcase(outertext, language, 1)
    elif grade <11:
        # inner qr grey to have some contrast
        color_inner=[60, 60, 60]
        if language == 'en':
            outertext = 'Hmmm, this looks like there is a second QR code in the middle of the big one. Look for the three squares the outer QR has in the corners in the inside. But your QR reader can not read it, because the bigger QR code all around confuses it. Some paper might do the trick.'
        elif language == 'de':
            outertext = 'Hmmm, sieht so aus wie wenn da ein zweiter QR Code in der Mitte des großen ist. Suche die drei großen Quadrate, die der äußere QR Code in den Ecken hat, im Inneren. Aber Dein QR-Leser kann ihn nicht erkennen, weil der große QR Code außenrum ihn verwirrt. Mit etwas Papier könnte es funktionieren.'
        # make hint a bit harder to read
        outertext, hint = wrong_whitespace(outertext, language, 1)
    else:
        # inner qr grey to have some contrast (depends on the printer how good this is visible, maybe increase contrast?)
        color_inner=[90, 90, 90]
        if language == 'en':
            outertext = 'Hmmm, this looks like there is another QR code in the middle of the big one. Look for the three squares the outer QR has in the corners in the inside. But your QR reader can not read it, because the bigger QR code all around confuses it. Some paper might do the trick.'
        elif language == 'de':
            outertext = 'Hmmm, sieht so aus wie wenn da ein weitere QR Code in der Mitte des großen ist. Suche die drei großen Quadrate, die der äußere QR Code in den Ecken hat, im Inneren. Aber Dein QR-Leser kann ihn nicht erkennen, weil der große QR Code außenrum ihn verwirrt. Mit etwas Papier könnte es funktionieren.'

        # make hint a bit harder to read (upside_down worked on all QR readers I've tried so far)
        outertext, hint = upside_down(outertext, language, 1)

    # size of single qr code pixels
    # don't make it too small because some cheap kids smartphones with fix focus lenses aren't good at macro mode.
    # too big uses more ink
    scale = 3

    # todo: solve someday (mathematically? try&error?)
    # goal: make the outer qr as small as possible but still be readable
    # parameters: inner qr has minimum error correction, outer maximum
    # until then, this kind of works with linear scaling:
    min_size_factor = 4
    i_len = len(innertext)
    # 1-18 chars make no difference in size
    if i_len < 18: i_len = 18 
    o_len = len(outertext) 
    if i_len * min_size_factor > o_len:
        # somehow scaling linear works quite well, would have assumed something ** ???
        needed_len = i_len * min_size_factor
        outertext += '  ' + '🤔 🧐 ' * (int( (needed_len - o_len ) / 6 ) + 1)

        # old school filler ;)
        #outertext += '  ' + '°º¤ø,¸¸,ø¤º°`' * (int( (needed_len - o_len ) / 13 ) + 1)

    # set minimum error correction, otherwise at least the ios qr reader can read it in the middle of the bigger qr without any effort so the puzzle could be solved accidently by going to close
    inner_qr = pyqrcode.create(innertext, encoding='utf-8', mode='binary', error='L')
    # set maximum error correction because redundancy is needed to make up for the pixels hidden by the small qr in the middle
    outer_qr = pyqrcode.create(outertext, encoding='utf-8', mode='binary', error='H')


    # set color to grey to save ink at printing
    # no border for the inner qr to make it seamless
    inner_qr_file = '/tmp/qr_inner_tmp.png'
    outer_qr_file = '/tmp/qr_outer_tmp.png'

    if grade == 1:
        # make a border around the inner QR, very easy, the ios QR reader doesn't read the outer QR anymore
        inner_quiet_zone=1
    else:
        inner_quiet_zone=0

    inner_qr.png(inner_qr_file, scale=scale, quiet_zone=inner_quiet_zone, module_color=color_inner)
    outer_qr.png(outer_qr_file, scale=scale, quiet_zone=4, module_color=(100, 100, 100))

    # .convert('RGB') so that each image gets its own color palette, otherwise both qr will have the same color
    inner_img = Image.open(inner_qr_file).convert('RGBA')
    outer_img = Image.open(outer_qr_file).convert('RGBA')

    # ingnore width because qr codes are square :)
    height_outer = outer_img.size[0]
    height_inner = inner_img.size[0]

    offset = int((height_outer - height_inner ) / 2)

    outer_img.paste(inner_img,(offset,offset))

    outer_img.save(filename)


    if 'ƃnqǝp' in globals() and ƃnqǝp:
        outer_img.show()
        print("saved file: " + filename)

    return filename

def qr_really_inside_qr(intext, language, grade):

    # experimental! Needs some more tweaking!
    #
    # create unicode QR code from intext using quadrant symbols, e.g.:
    # ▗▄▄▄▗▖▗▗▄▄▄
    # ▐▗▄▐▗▚▐▐▗▄▐
    # ▐▐█▐▐▄▌▐▐█▐
    # ▐▄▄▟▗▗▗▐▄▄▟
    # ▗▄▖▗▗▜▘▖▗▄▗
    # ░▖▛▄▟▌▌▖▝░▟
    # ▗▟▙▚▛▄▞▗▚▌▀
    # ▗▄▄▄▝▝▌░▐░░
    # ▐▗▄▐░▜▌▘▗▟▞
    # ▐▐█▐▐░▄▛▘▀▘
    # ▐▄▄▟▐▀▟▛▖▗▝
    # The result is small enough to fit as text unicode input into another QR code, e.g. as PNG so you can use it in qr_inside_qr() with e.g.
    # ./crypto_puzzles.py -T RQ "top secret"
    # ... to have a unicode QR code inside a PNG QR code inside another PNGPNG QR code ;)
    # Scanning the PNG shows the unicode QR on the screen of the smartphone. How good this 2nd QR can be read depends mainly on the formatting on the 1st QR reader app
    # The displaying QR reader might introduce lines between the blocks. Varying the distance between both devices usually helps. 
    # If that doesn't work, a fallback is always to copy the unicode QR into some text editor and format it using a monospaced font like courier and then read it.

    # A working combination is "Lightning QR" on android  as 1st reader and default iphone reader to read from the android screen, a bit further away (to blur the lines between the blocks)

    # store quadrant chars:
    fp={}
    fp['1000'] = '▘'
    fp['1100'] = '▀'
    fp['1110'] = '▛'
    fp['0110'] = '▞'
    fp['1010'] = '▌'
    fp['0010'] = '▖'
    fp['0100'] = '▝'
    fp['0001'] = '▗'
    fp['1001'] = '▚'
    fp['1101'] = '▜'
    fp['1111'] = '█'
    fp['0111'] = '▟'
    fp['1011'] = '▙'
    fp['0011'] = '▄'
    fp['0101'] = '▐'
    # Most QR reader apps display the content in proportional fonts which is ok for all the 15 chars above because they have the same width even then.
    # But there's no proper empty "space" with the same width, at least I haven't found one yet.
    # I did some experiments with the different unicode whitespace characters but none of them had the same width in all font used by all QR reader apps as the quadrant characters. This light shade
    # square worked best for my devices & apps:
    fp['0000'] = '░'
    #fp['0000'] = ' '
    # using a single quadrant also works because of the error correction:
    #fp['0000'] = '▘'
    # spacing broken, as all with all unicode whitespace chars I tried:
    #fp['0000'] = ' '

    # generate QR code using minimum error correction to save space:
    number = pyqrcode.create(intext, error='L')

    # "render" QR code with with 0s and 1s:
    # 000000000000000000000000000
    # 011111110001001111011111110
    # 010000010111001111010000010
    # 010111010100000000010111010
    # 010111010010000111010111010
    # 010111010111010111010111010
    # 010000010101001011010000010
    # 011111110101010101011111110
    # 000000000101100011000000000
    # 011010011000101111011101100
    # 011111100110000101110000010
    # 011001110000011100000100110
    # 000000100011111000101010100
    # 000100110101111101110000000
    # 001100101110111000101000110
    # 010101011110101101001100010
    # 001001000110001110011000110
    # 011010110001010101111101010
    # 000000000111011001000101010
    # 011111110101001111010101110
    # 010000010011010111000101100
    # 010111010010011101111110000
    # 010111010111110011000111000
    # 010111010011001111011110010
    # 010000010101001010000010000
    # 011111110110111011101000110
    # 000000000000000000000000000

    # the small border with quiet_zone helps reading the ASCII QR on the smartphone screen a bit, maybe experiment a bit more ...
    # quietzone=0 gives messed up lines on ios
    quietzone=1
    qr = number.text(quiet_zone=quietzone).split('\n')
    # (max 32 characters with quiet_zone=1)
    if quietzone==0:
        del qr[-1]
        qr.append('0' * len(qr[0]))

    if 'ƃnqǝp' in globals() and ƃnqǝp:
        print('\n'.join(qr))

    # convert 01010101 to quadrant unicode chars
    # (this code sucks and could probably be done with some slicing and map() but it works :)
    line_num = 0
    outtext = ""
    lastline={}
    for line in qr:
        chunks = len(line)
        chunk_size  = 2

        # make num of chars in line even by appending a 0
        if chunks/2 != int(chunks/2): 
            line += '0'

        for i in range(0, chunks, chunk_size):
            # on even lines, just store chunks of 2 chars
            if line_num / 2 == int(line_num / 2):
                lastline[i] = line[i:i+chunk_size] 

            # on odd lines, combine stored chunks and 2 chars of this line to get the right quadrant unicode char (▜ ▌ ▐  ▘▛ ▛ ▀ ▜▙▞▌)
            else:
                if 'ƃnqǝp' in globals() and ƃnqǝp:
                    print(lastline[i] + line[i:i+chunk_size], end='' )

                # don't "draw" last column because it's empty anyway if there's a border because of quiet_zone (to save size)
                if i == chunks-1 and quietzone >= 1:
                    pass
                    #print(fp['empty'], end='')
                else:
                    bin = lastline[i] + line[i:i+chunk_size]
                    outtext += fp[bin]

        # append newline on every 2nd line
        if line_num / 2 == int(line_num / 2):
            outtext += '\n'

        line_num += 1

    if 'ƃnqǝp' in globals() and ƃnqǝp:
        print(outtext)
    

    return outtext



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

def deumlaut(text):
    # replace funny characters 
    # todo: other languages
    text = text.replace('ä','ae')
    text = text.replace('ö','oe')
    text = text.replace('ü','ue')
    text = text.replace('Ä','Ae')
    text = text.replace('Ö','Oe')
    text = text.replace('Ü','Ue')
    text = text.replace('ß','ss')
    return text

def emoji_alphabet(intext, language, grade):
#def ∈♏💍🕙ℹ️_ค🛴₱♓🆎∈✝️(intext, language, grade):)

    # top secret => 🔝  💰 € ☪️ ®️ 📧 ȶ
             
    outtext=intext.lower()

    # +' ' to have a space between emoji because kerning is wrong on some platforms
    spacing=' '
    if spacing:
        outtext = outtext.replace(' ', '  ')

    # multiple letters at once, e.g. "id" => 🆔
    # use .replace()
    for multi_letter in emoji_letter_multiple:
        outtext = outtext.replace(multi_letter, random.choice(emoji_letter_multiple[multi_letter].split(','))  )

    # single letters, 
    # iterate over text
    outtext_new=""
    for char in outtext:

        if char in emoji_letter:
            # choose random letter of multiple e.g. m=Ⓜ️ 〽️ ♏ 
            outtext_new += random.choice(emoji_letter[char].split(',')) + spacing
        else:
            outtext_new += char + spacing
            
    return outtext_new, ""

def emoji_alphabet_xmas(intext, language, grade):

    # top secret => 🔝  💰 € ☪️ ®️ 📧 ȶ   🎅🎅🎅🎅
             
    outtext=intext.lower()

    # +' ' to have a space between emoji because kerning is wrong on some platforms
    spacing=' '
    if spacing:
        outtext = outtext.replace(' ', '  ')

    # multiple letters at once, e.g. "id" => 🆔
    # use .replace()
    for multi_letter in emoji_letter_multiple:
        outtext = outtext.replace(multi_letter, random.choice(emoji_letter_multiple[multi_letter].split(','))  )

    # single letters, 
    # iterate over text
    outtext_new=""
    for char in outtext:

        if char in emoji_letter_xmas:
            # choose random letter of multiple e.g. m=Ⓜ️ 〽️ ♏ 
            outtext_new += random.choice(emoji_letter_xmas[char].split(',')) + spacing
        elif char in emoji_letter:
            # choose random letter of multiple e.g. m=Ⓜ️ 〽️ ♏ 
            outtext_new += random.choice(emoji_letter[char].split(',')) + spacing
        else:
            outtext_new += char + spacing
            
    outtext_new += " 🎅 🦌 🎁 "
    return outtext_new, ""

def emoji_alphabet_animals(intext, language, grade):

    # top secret => TODO
             
    outtext=intext.lower()

    # +' ' to have a space between emoji because kerning is wrong on some platforms
    spacing=' '
    if spacing:
        outtext = outtext.replace(' ', '  ')

    # single letters, 
    # iterate over text
    outtext_new=""
    for char in outtext:

        if char in emoji_animal:
            # choose animal letter of multiple e.g. s=🦂,🐌,🐍,🕷️,🦢  (works in english in german)
            outtext_new += random.choice(emoji_animal[char].split(',')) + spacing
        # fall back to the normal emoji alphabet
        elif char in emoji_letter:
            # choose random letter of multiple e.g. m=Ⓜ️ 〽️ ♏ 
            outtext_new += random.choice(emoji_letter[char].split(',')) + spacing
        else:
            outtext_new += char + spacing
            
            
            
    return outtext_new, ""
def figlet(intext, language, grade, font='ivrit'):

    outtext = ''

    # some fonts don't have e.g. ä so convert ä => ae
    intext = deumlaut(intext)

    if language == 'en':
        outtext = "Here's just a bunch of underscores, pipes, slahes, backslashes and brackets:   _ | / \ ( ) _ | / \ ( ) \n\nLet see, how we can write with them:\n\n\n"
    elif language == 'de':
        outtext = "Hier ist ein kleiner Haufen Unterstriche, senkrechter Striche, schräger Striche, Backslashes und Klammern:   | ||  __/ | | (_|  __/\__ \ | |_) | (_) | |_ \n\nLass mal schauen, wie wir damit schreiben können:\n\n\n"

    f = Figlet(font=font)
    outtext += f.renderText(intext)

    hint=''

    if grade < 3:
        if language == 'en':
            hint += 'Read backwards'
        elif language == 'de':
            hint += 'Rückwärts lesen'

    if language == 'de':
        hint += 'ae=ä, oe=ö, ue=ü, ss=ß'

    return outtext, hint


def stego_saurus(intext, language, grade):

    # todo! so far only 3 letters possible. Include more replacement letters? Or more dinosaurs?
    # Or put long messages into lots of noise and the coordinates for the beginning into the stegosaurus?

    outtext = ''

    if language == 'en':
        hint ='Steganography is the practice of concealing a message within e.g. an image. This stegosaurus (original by R.Millward) knows the secret! It looks a bit strange because it is painted with punctuation marks, mathematical symbols and the like ;)'
    elif language == 'de':
        hint ='Steganographie ist eine Methode um verborgene Botschaften in z.B. einem Bild zu verstecken. Dieser Stegosaurus (Original von R.Millward) kennt das Geheimnis! Er sieht etwas komisch aus, weil er aus Satzzeichen, mathematischen Symbolen und ähnlichem gemalt ist ;)'

    # r for raw string to avoid problem with backslashes at printing. the ①②③ will be replaced by the secret text
    # 🦕 ;)
    saurus =r"""
                         .       .
                        / `.   .' \
                .---.  <    > <    >  .---.
                |    \  \ - ~ ~ - /  /    |
                 ~-..-~             ~-..-~
             \~~~\.'                    `./~~~/
              \__/                        \__/
               /                  .-    .  \
        _._ _.-    .-~ ~-.       /       }   \/~~~/
    _.-'①  }~     /       }     {        ;    \__/
   {'__,  /      (       /      {       /      `. ,~~|   .     .
    `''''='~~-.__(      /_      |      /- _      `..-'   \\   //
                / \   =/  ~~--~~{    ./|    ~-.     `-..__\\_//_.-'
               {   \  +\         \  =\ (        ~ - . _ _ _..---~
               |  | {   }         \   \_\
              '---.②___,'       .③___,'       
"""


    saurus = saurus.replace('①', intext[0])    
    saurus = saurus.replace('②', intext[1])    
    saurus = saurus.replace('③', intext[2])    

    return saurus, hint


def generate_crackme_python(intext, language, grade, crackme_num=0):

    # generates easy crackmes in python3 for beginers. Can be made to print the secret by changing 1+ lines of code
    # for contributors: remember that understanding foreign code is a challenge in itself for beginers

    # todo: harder crackmes (e.g. eval(b64decode(...) ) (doesn't have to be this crazy: https://github.com/brandonasuncion/Python-Code-Obfuscator ;)
    # todo: other languages used by kids like js, scratch (is that possible?)
    outtext = ''

    # if no specific crackme is wanted, use grade:
    if not crackme_num:
        if grade <6:
            crackme_num = 1 
        if grade <7:
            crackme_num = 2 
        else:
            crackme_num = 3


    if crackme_num == 1:

        # define template for crackme, anything with TEMPL_ will be replaced with language specific stuff

        crackme_template = """#!/usr/bin/env python3

# TEMPL_COMMENT_1
# Python3!

import base64
import time

time.sleep(1)
ʇxǝʇ = 'TEMPL_PRINT_1'
print(ʇxǝʇ, end='', flush=True)

time.sleep(2)
print('TEMPL_PRINT_2', end='', flush=True)

time.sleep(4)
print('TEMPL_PRINT_3', end='', flush=True)

time.sleep(988989789)
print ('TEMPL_PRINT_4' + base64.b64decode('TEMPL_BASE64_SECRET').decode('utf8'))
"""

        if language == 'en':
            comment_1 = "This little script knows the secret you are looking for, but will only tell it in 890601 billion years, harhar :) If you don't have this much time, find a quicker way ..."
            print_1 = "The secret ... "
            print_2 = " is really very secret ... "
            print_3 = " so I wil tell it to you in 890601 billion years!"
            print_4 = "Thanks for waiting, here is your secret: "
        elif language == 'de':
            comment_1 = "# Dieses kleine Programm kennt das Geheimnis, das Du suchst, wird es Dir aber erst in 9582790 Billionen Jahren verraten, harhar :) Wenn Du nicht so viel Zeit hast, musst Du einen anderen Weg suchen ..."
            print_1 = "Das Geheimnis ... "
            print_2 = " ist wirklich sehr geheim ... "
            print_3 = " also werde ich es Dir erst in 9582790 Billionen Jahren verraten!"
            print_4 = "Danke für's Warten, hier ist Dein Geheimnis: "

        outtext = crackme_template

        # encode secret to base64 to not have it plaintext in the code (yeah, also cyberchefable)
        secret = str(base64.b64encode(intext.encode('utf-8')), 'utf-8')
        outtext = outtext.replace('TEMPL_BASE64_SECRET', secret)

        outtext = outtext.replace('TEMPL_COMMENT_1', comment_1)
        outtext = outtext.replace('TEMPL_PRINT_1', print_1)
        outtext = outtext.replace('TEMPL_PRINT_2', print_2)
        outtext = outtext.replace('TEMPL_PRINT_3', print_3)
        outtext = outtext.replace('TEMPL_PRINT_4', print_4)

    elif crackme_num == 2:

        # define template for crackme, anything with TEMPL_ will be replaced with beef
        crackme_template = """#!/usr/bin/env python3

# Python3!
# TEMPL_COMMENT_1

import base64
import hashlib
import time

password=input('TEMPL_PRINT_1')

hashitem=hashlib.new('sha256')
hashitem.update(password.encode('utf8'))
hexdigest_passwort=hashitem.hexdigest

if hexdigest_passwort == '9f86d081884c7d659a2feaa0c55ad015a3bf4fb12b0b822cd15d6c15b00f0a08' and password[:4:] == 'F' and hexdigest_passwort[1:2:] == 'XR' and False:
    print('TEMPL_PRINT_2')
    secret1 = 'TEMPL_BASE64_SECRET1'
    secret3 = 'TEMPL_BASE64_SECRET3'
    secret2 = 'TEMPL_BASE64_SECRET2'
    secret = secret1 + secret2 + secret3
    print (base64.b64decode(secret).decode('utf-8'))

else:
    print('TEMPL_PRINT_3')

"""

        secret = str(base64.b64encode(intext.encode('utf-8')), 'utf-8')

        # split secret into 2 strings to make copy&paste into cyberchef a bit harder
        # don't pick a slice dividable by 3 or it will work
        secret1 = secret[:4]
        secret2 = secret[4:8]
        secret3 = secret[8:]

        outtext = crackme_template
        outtext = outtext.replace('TEMPL_BASE64_SECRET1', secret1)
        outtext = outtext.replace('TEMPL_BASE64_SECRET2', secret2)
        outtext = outtext.replace('TEMPL_BASE64_SECRET3', secret3)

        if language == 'en':
            comment_1 = "This little script knows the secret you are looking for, but will never tell it to you, unless you force it to ;)"
            print_1 = "What it the password? "
            print_2 = "The secret is: "
            print_3 = "Wrong password!"
        elif language == 'de':
            comment_1 = "Dieses kleine Programm kennt das Geheimnis, das Du suchst, wird es Dir aber auf gar keinstem Fall überhaupt nicht verraten. Außer die zwingst es dazu ;)"
            print_1 = "Wie lautet das Passwort? "
            print_2 = "Das Geheimnis ist: "
            print_3 = "Falsches Passwort!"

        outtext = outtext.replace('TEMPL_COMMENT_1', comment_1)
        outtext = outtext.replace('TEMPL_PRINT_1', print_1)
        outtext = outtext.replace('TEMPL_PRINT_2', print_2)
        outtext = outtext.replace('TEMPL_PRINT_3', print_3)

    elif crackme_num == 3:

        # define template for crackme, anything with TEMPL_ will be replaced with language specific stuff

        crackme_template = """#!/usr/bin/env python3

# TEMPL_COMMENT_1
# Python3!

import base64
import time

exec('print("TEMPL_PRINT_1")')
time.sleep(1)
print()

command = 'print("TEMPL_PRINT_2")'
print('command: ' + command)
exec(command)
time.sleep(1)
print()

command1 = 'print("TEMPL_PRINT_3'
command2 = 'TEMPL_PRINT_4")'
print(command1 + ' --------------- ' + command2)
exec(command1 + command2)
time.sleep(1)
print()

secret_command ='''
TEMPL_BASE64_SECRET
'''

sec_cmd_dec = base64.b64decode(secret_command).decode('utf-8')
# ???
exec(sec_cmd_dec)

"""

        crackme_template_exec = """
print('TEMPL_PRINT_5', flush=True)
time.sleep(1)
print('TEMPL_PRINT_6', flush=True)
time.sleep(988989789)
print ('TEMPL_PRINT_7: ' + base64.b64decode('TEMPL_BASE64_SECRET_INNER').decode('utf8'))
"""

        if language == 'en':
            comment_1 = "This little script knows the secret you are looking for, but will only tell it in 890601 billion years, harhar :) If you don't have this much time, find a quicker way ..."
            print_1 = "exec is an interessting python command"
            print_2 = "exec is a really interessting python command"
            print_3 = 'This command is in two vari'
            print_4 = 'ables and soon it will be executed'
            print_5 = 'Huh, where does this code come from?'
            print_6 = 'I wil tell you the secret in 890601 billion years!'
            print_7 = 'Thanks for waiting, here is your secret: '
        elif language == 'de':
            comment_1 = "# Dieses kleine Programm kennt das Geheimnis, das Du suchst, wird es Dir aber erst in 9582790 Billionen Jahren verraten, harhar :) Wenn Du nicht so viel Zeit hast, musst Du einen anderen Weg suchen ..."
            print_1 = "exec ist ein interessanter Python Befehl"
            print_2 = "exec ist ein wirklich interessanter Python Befehl"
            print_3 = 'Dieser Befehl ist in zwei vari'
            print_4 = 'ablen und wird trotzdem ausgeführt'
            print_5 = 'Huh, woher kommt denn dieser Code?'
            print_6 = 'Ich werde Dir das Geheimnis in 80932 Jahren verraten!'
            print_7 = 'Danke für das Warten, hier ist Dein Geheimnis: '

        outtext = crackme_template
        outtext_exec = crackme_template_exec

        outtext_exec = outtext_exec.replace('TEMPL_PRINT_5', print_5)
        outtext_exec = outtext_exec.replace('TEMPL_PRINT_6', print_6)
        outtext_exec = outtext_exec.replace('TEMPL_PRINT_7', print_7)

        # encode secret to base64 to not have it plaintext in the code (yeah, also cyberchefable)
        secret = str(base64.b64encode(intext.encode('utf-8')), 'utf-8')
        outtext_exec = outtext_exec.replace('TEMPL_BASE64_SECRET_INNER', secret)
        outtext_exec_b64 = str(base64.encodebytes(outtext_exec.encode('utf-8')), 'utf-8')
        #outtext_exec_b64 = str(base64.b64encode(outtext_exec.encode('utf-8')), 'utf-8')
        outtext = outtext.replace('TEMPL_BASE64_SECRET', outtext_exec_b64)

        outtext = outtext.replace('TEMPL_COMMENT_1', comment_1)
        outtext = outtext.replace('TEMPL_PRINT_1', print_1)
        outtext = outtext.replace('TEMPL_PRINT_2', print_2)
        outtext = outtext.replace('TEMPL_PRINT_3', print_3)
        outtext = outtext.replace('TEMPL_PRINT_4', print_4)

    else:
        log("ERROR, unknown crackme_num: " + crackme_num)

    if language == 'en':
        hint="Run with Python"
    elif language == 'de':
        hint="Mit Python ausführen"

    return outtext, hint


def get_crypto_functions(type='all'):

    # encryption of flags has to be 100% reversible and not e.g. randomize the order of the numbers
    if type == 'reversible':
        crypto_functions_text="""insert_noise
upside_down
wrong_whitespace
mirror_words
shift_words
stego_acrostic
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
stego_acrostic
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
    parser.add_argument("--technique", "-T", help="Techniques used to \"encrypt\". Such argument is a string composed by any combination of NUMLlWmSC13AncjqQRuf characters where each letter stands for a different technique (details on github).", required=True)
    parser.add_argument("--noise_type", help="Type of noise. Can be numbers,numberwords, animals")
    parser.add_argument("--noise_chars", help="Character(s) for noise")
    parser.add_argument("--upside_down_rate", help="Turn every nth word", default=2)
    parser.add_argument("--grade", "-g", help="Adjust difficulty by school grade aka years of school experience.", default=1)
    parser.add_argument("--language", "-l", help="Language for hints", default='en')
    parser.add_argument("--crackme_num", help="Number of crackme", default=0)
    parser.add_argument("--num_parts", help="Number of parts for join_puzzle", default=2)
    parser.add_argument("--seed", help="Random seed (only set to static number to always get the same randomness for debugging!)")
    parser.add_argument("--show_function_name", action='store_true', help="Shows the python function name below the encrypted text (for internal use)")
    parser.add_argument("--ƃnqǝp", "-p", action='store_true', help="Debug")
    parser.add_argument("--outer_text", help="Outer text for QR inside QR")
    parser.add_argument("--filename", "-f", help="Output filename for e.g. QR codes", default='')
    args = parser.parse_args()
    noise_type = args.noise_type
    language = args.language
    noise_chars = args.noise_chars
    grade = int(args.grade)
    upside_down_rate = int(args.upside_down_rate)
    crackme_num = int(args.crackme_num)
    seed = args.seed
    show_function_name = args.show_function_name
    outer_text = args.outer_text
    filename = args.filename
    num_parts = int(args.num_parts)
    global ƃnqǝp
    ƃnqǝp = args.ƃnqǝp

    if ƃnqǝp:
        print("grade: " + str(grade))
        print("filename: " + filename)


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
            worktext, hint= stego_acrostic(worktext, language, grade)
            function_name = "stego_acrostic"
        # not really useful on command line yet:
        elif technique == "s":
            worktext, hint, count_letters = substitute_partly_solved_frequency_analysis(worktext, language, grade)
            function_name = "substitute_partly_solved_frequency_analysis"
        elif technique == "n":
            worktext = convert_num_to_number_words(worktext, language)
            function_name = "convert_num_to_number_words"
        elif technique == "c":
            worktext, hint = generate_crackme_python(worktext, language, grade, crackme_num)
            function_name = "generate_crackme_python"
        elif technique == "j":
            worktexts = join_puzzle(worktext, language, grade)
            function_name = "join_puzzle"
        elif technique == "q":
            qr_code(worktext, language, filename)
            function_name = "qr_code"
        elif technique == "Q":
            worktext = qr_inside_qr(worktext, outer_text, language, grade, filename)
            function_name = "qr_inside_qr"
        elif technique == "R":
            worktext = qr_really_inside_qr(worktext, language, grade)
            function_name = "qr_really_inside_qr"
        elif technique == "u":
            worktext, hint = stego_saurus(worktext, language, grade)
            function_name = "stego_saurus"
        elif technique == "f":
            worktext, hint = figlet(worktext, language, grade)
            function_name = "figlet"
        elif technique == "e":
            worktext, hint = emoji_alphabet(worktext, language, grade)
            function_name = "emoji_alphabet"
        elif technique == "x":
            worktext, hint = emoji_alphabet_xmas(worktext, language, grade)
            function_name = "emoji_alphabet_xmas"
        elif technique == "E":
            worktext, hint = emoji_alphabet_animals(worktext, language, grade)
            function_name = "emoji_alphabet_animals"
        else:
            print("Error: Technique unknown")
         
    if show_function_name:
        print(function_name)

    if worktexts:
        #print(worktexts)
        for worktext in worktexts:
            print(worktext, worktexts[worktext])
    elif worktext:
        print(worktext)

    if 'hint' in locals() and hint and not seed:
        if language == 'en':
            print('Hint: ' + hint)
        elif language == 'de':
            print('Hinweis: ' + hint)

if __name__ == "__main__":
    main()

