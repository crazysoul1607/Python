import requests
import hashlib
import sys

def request_api_data(query_char):
    url="https://api.pwnedpasswords.com/range/"+query_char
    res=requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res

def get_password_leak_count(hashes, hash_to_check):
    hashes=(line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0
        
def pwned_api_check(password):
    sha1password=hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5,tail=sha1password[:5],sha1password[5:]
    res= request_api_data(first5)
    return get_password_leak_count(res,tail)

def main(args):
    for password in args:
        count=pwned_api_check(password)
        if count:
            print(f'the password {password} was found {count} no. of times, you should change the password...')
        else:
            print(f'the password {password} was found {count} no. of times, Good Choice')
    return "Password checking Completed."

if __name__=="__main__":
    sys.exit(main(sys.argv[1:]))