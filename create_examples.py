#!/usr/bin/env python3

# create markdown page if examples for kids_crypto
# intentionally call python not via function but shell to get the command lines examples right

import os
import argparse

techniques='NUMLlWSC1A'
# technique 's' doesn't work here, 'm' boring

max_grade=11
cp_path='./crypto_puzzles.py'

#plaintext = 'Top secret!'
plaintext = 'Top secret! The cookies are hidden in the red bowl!'


def escape_markdown(md):

    md=md.replace('|', '\|')
    return md

parser = argparse.ArgumentParser()
parser.add_argument("--create_function_list", "-c", action='store_true', help="Create list of all functions and distinct grades, which give different results")
args = parser.parse_args()
create_function_list = args.create_function_list

if not create_function_list:
    print('Crypto function | Minimum school grade | Encrypted output | Command line')
    print('--- | --- | --- | ---')

last_res=""
for technique in techniques:
    for grade in range(1,max_grade+1):
        cmd = cp_path + ' --seed 1 -T ' + technique + ' --grade ' + str(grade) + ' "' + plaintext + '"'
        cmd_real = cmd + ' --show_function_name'
        #print(cmd)
        res = os.popen(cmd_real).readlines()

        function_name, ciphertext = res

        ciphertext = escape_markdown(ciphertext.rstrip())

        if res != last_res:
            if not create_function_list:
                print('|'.join((function_name.rstrip(), str(grade), ciphertext,  cmd)) )
            else:
                print(function_name.rstrip(), str(grade))

        last_res=res

