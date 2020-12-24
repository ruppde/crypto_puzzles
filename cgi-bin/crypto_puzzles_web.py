#!/usr/bin/python3 -u
 
import cgi, cgitb
cgitb.enable()

import html
import sys
sys.path.insert(1, '..')
import crypto_puzzles

# TODO: somehow get the order of handling multiple functions right, e.g. first rot13, then qr_code bec won't work the other way around
function_list=[
"emoji_alphabet_xmas",
"emoji_alphabet",
"emoji_alphabet_animals",
"insert_noise",
"upside_down",
"randomize_middle_of_words",
"lässn_tursch_chraipen",
"leet",
"wrong_whitespace",
"mirror_words",
"shift_words",
"camelcase",
"char_to_num",
"rot13",
"stego_acrostic",
#"substitute_partly_solved_frequency_analysis",
#"convert_num_to_number_words",
"generate_crackme_python",
#"join_puzzle",
"stego_saurus",
"figlet",
# pyqrcode missing on my webserver and would need some code to show the pics for downloading
#"qr_code",
#"qr_inside_qr",
#"qr_really_inside_qr",
]

# set defaults
grade =1
language='en'
noise_type=''
noise_chars=''

print(
'''Content-Type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<HTML>
<HEAD>
    <title>Crypto Puzzles Web</title>
    <meta charset="UTF-8">
    <style>
      span {
        background-color: lightblue;
      }
      pre {
        background-color: lightblue;
      }
    </style>
</HEAD>
<BODY>




<a href="https://github.com/2d4d/crypto_puzzles"><img loading="lazy" width="149" height="149" src="https://github.blog/wp-content/uploads/2008/12/forkme_left_red_aa0000.png?resize=149%2C149" class="attachment-full size-full" alt="Fork me on GitHub" data-recalc-dims="1"></a>

<font size=+2>Crypto Puzzles Web</font><p>

<p>
''')

form = cgi.FieldStorage()

if form.getvalue('message'):
    message=form.getvalue('message')
    worktext=message

    collect_html =''

    if form.getvalue('grade'):
        # basic sanity and security check, call int()
        grade = int(form.getvalue('grade')) or 1

    if form.getvalue('language'):
        # basic sanity and security check, max len 2
        if len(form.getvalue('language')) == 2:
            language = form.getvalue('language')

    collect_html += ('Language: <span>' + language + '</span> Grade: <span>' + str(grade) + '</span><p>')

    # handle passed functions
    functions=form.getlist('functions')
    collect_html += ('Selected functions: <ul>')
    for function in functions:

        # basic sanity and security check, call only functions from predefined list:
        if function in function_list:
            collect_html += ('<li><span>' + function  + '</span></li>')
            # call function out of variable
            func = getattr(crypto_puzzles, function)
            worktext, hint = func(worktext, language, grade )

    collect_html += ('</ul>')

    worktext_escaped = html.escape(worktext) 
    if function == "emoji_alphabet" or function == "emoji_alphabet_xmas":
        worktext_escaped = worktext_escaped.replace(' ', '&nbsp;')

    # multiline text gets different format:
    if worktext.count('\n') > 1:
        print('Cipher text: <span><pre>' + worktext_escaped + '</pre></span><p>')
    else:
        print('Cipher text: <span>' + worktext_escaped + '</span><p>')

    if hint:
        print('Hint: <span>' + html.escape(hint) + '</span><p>')

    #ciphertext, hint = crypto_puzzles.insert_noise(message, language, grade, noise_type, noise_chars) 
    print('Plain text: <span>' + html.escape(message) + '</span><p>')

    print(collect_html)

else:
    print('''

<form action=crypto_puzzles_web.py  method = "post">

Secret message:
<textarea name = "message" cols = "40" rows = "4">
Top secret! The sweets are hidden under your chair!
</textarea>

<h3>Please select crypto functions:</h3>

<!--See <a href="https://htmlpreview.github.io/?https://github.com/2d4d/crypto_puzzles/blob/master/examples/Examples.html">example list</a> for what the functions do.-->
See example list below for what the functions do.<br>

<select name = "functions" size=16 multiple>
''', flush=True)

    selected = " selected "
    for function in function_list:
        print(' <option value = "' + function + '"' + selected + '>' + function + '</option>')
        selected = ""
    print('''</select><br>
<font size=-2>(You can select multiple functions by holding the Ctrl key while clicking but start with single ones.)</font><br>
<p>

Select school grade (rough measure of difficulty):
<select name = "grade">
    <option value = "1">1</option>
    <option value = "2">2</option>
    <option value = "3">3</option>
    <option value = "4">4</option>
    <option value = "5">5</option>
    <option value = "6">6</option>
    <option value = "7">7</option>
    <option value = "8">8</option>
    <option value = "9">9</option>
    <option value = "10">10</option>
    <option value = "11">11</option>
    <option value = "12">12</option>
</select><p>

Select language:
<select name = "language">
    <option value = "en">English</option>
    <option value = "de">Deutsch</option>
</select><p>


<input type = "submit" value = "Submit"/>
</form> 
<hr>
''')

    with open('Examples.html') as f:
        print(f.read())




print('''
</BODY>
</HTML>
''')
