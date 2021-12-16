import os.path
import sys

debug = False
logo = """
                         / _|                               | |   (_)          
   ___ _ __ ___  _ __   | |_ ___  _ __   _ __   _____      _| |__  _  ___  ___ 
  / __| '__/ _ \| '_ \  |  _/ _ \| '__| | '_ \ / _ \ \ /\ / / '_ \| |/ _ \/ __|
 | (__| | | (_) | | | | | || (_) | |    | | | |  __/\ V  V /| |_) | |  __/\__|
  \___|_|  \___/|_| |_| |_| \___/|_|    |_| |_|\___| \_/\_/ |_.__/|_|\___||___/
"""
info_string = """
Ive just crated it for my linux newbie... Feel free to write some of those options...
a) everyday at 13:00  do /home/user/script.sh
"""


def which_option(ans):
    if ans.split()[0] == "everyday" and ans.split()[1] == "at" and ans.split()[3] == "do" and len(ans.split()) == 5:
        return 1


# puts a parsed string into a crontab
# @arg parsed_str is parsed string
def put_to_crontab(parsed_str):
    try:
        if debug:
            print(f"Writing {parsed_str} to /etc/crontab...")
        f = open("/etc/crontab", 'w')
        f.write(parsed_str + "\n")
    except IOError:
        if debug:
            print("IOError while opening /etc/crontab")
        print("File not accessible")
    finally:
        if debug:
            print("Closing /etc/crontab.")
        f.close()
        return True


# gets a option number and string to parse
# return a parsed string just to place in crontab
# @option is kind of task @answer_str in string from user
def format_to_cron(option, answer_str):
    if debug:
        print(f"Option is {option} and answer string is {answer_str}")
    if option == 1:
        path = answer_str.split()[4]
        time = answer_str.split()[2]
        hour = time.split(":")[0]
        minute = time.split(":")[1]
        cron_str = f"{minute} {hour} * * * root {path}"
        if debug:
            print(f"Parsed string is {cron_str}")
            print("Passing it to crontab.")
        return cron_str


# this method checks if string from user is accurate, @return bool
def parse_str(option, ans_str):
    if option == 1:  # assume everyday task
        str_tab = ans_str.split()
        correct_var = False if str_tab[0] != "everyday" else True
        correct_var = False if str_tab[1] != "at" else True
        correct_var = False if str_tab[2] != "hour" else True
        correct_var = False if str_tab[3] != "do" else True
        correct_var = False if str_tab[4][0] != "/" else True
        correct_var = False if len(str_tab) == 4 else True
        if debug:
            print("String seems to be OK, passed it further...")
        return correct_var
    if option == 2:  # assume once a month task
        return False
    if option == 3:
        return False


def main():
    if len(sys.argv) > 1:
        if (sys.argv[1]) == "-v":
            global debug
            debug = True

    # logo and prompt
    print(logo)
    print(info_string)

    answer = input("")
    option = which_option(answer)  # recognize task
    if not parse_str(option, answer):
        print("Bad string. Check for mistakes and try again.")
        exit(1)
    else:
        res = put_to_crontab(format_to_cron(option, answer))
        print("Correctly added your cronjob to crontab.") if res is True else print("Can't add cronjob to file.")


if __name__ == '__main__':
    main()
