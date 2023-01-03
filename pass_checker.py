import hashlib
import requests
import sys


def requestAPI(sha_char):
    url = 'https://api.pwnedpasswords.com/range/' + sha_char
    response = requests.get(url)

    if response.status_code != 200:
        print(f'error code : {response.status_code}')
        return 0

    return response


def get_leaked_passwords(response, tail):
    hashes_tail = (line.split(':') for line in response.text.splitlines())

    for hashtail, count in hashes_tail:
        if hashtail == tail:
            return count

    return 0


def check_password(password):
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5char = sha1pass[:5]
    tail = sha1pass[5:]
    response = requestAPI(first5char)
    return get_leaked_passwords(response, tail)


def main(args):
    for password in args:
        resp = check_password(password)

        if resp:
            print(f'{password} found {resp} times.')
        else:
            print(f'{password} not found. All good!!')
    return '---------------finished-------------------'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
