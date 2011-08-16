

__author__ = 'laithzahid'
__version__ = '0.1'


import sys
from Classes.ipCalcMainClass import ipCalcMainClass as ip


def main():
    """
    This is the main function:
    1. Check if the script has been run without arguments, and asks the user to give input and store it in "givenIP" as a string, then pass it to the main class.
    2. Check if multiple arguments are given, if so, it notifies the user.
    3. If the user ran the script with one argument, it calls the main class and pass it the given argument.
    """

    if len(sys.argv) == 1:
        givenIP = input('\nPlease give an IP address (IP/MASK), (to exit type "X"): ')
        try:
            ipAddress = ip(givenIP)

        except (IndexError, ValueError):
            if givenIP == 'x' or givenIP == 'X': sys.exit()
            else:
                print('\nPlease give a valid IPv4/MASK address in #.#.#.#/# format,' '\n'
                '\tfor example: 192.168.1.1/24, or 10.10.10.1/28')
                main()
    elif len(sys.argv) > 2:
        print("This version accepts only one IP address")
    else:
        givenIP = sys.argv[1]
        try:
            ipAddress = ip(givenIP)

        except (IndexError, ValueError):
            if givenIP == 'x' or givenIP == 'X': sys.exit()
            else:
                print('\nPlease give a valid IPv4/MASK address in #.#.#.#/# format,' '\n'
                '\tfor example: 192.168.1.1/24, or 10.10.10.1/28')
                


# Run the main application function, input format is: IP/MASK, IP is given in dotted decimal, MASK is given in prefix notation.

if __name__ == '__main__':
    main()
  