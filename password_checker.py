import requests
from getpass import getpass
import hashlib

def request_api_data(query_char):
	print('checking query character', query_char )
	api_url = 'https://api.pwnedpasswords.com/range/'+query_char
	response = requests.get(api_url)
	if response.status_code != 200:
		raise RuntimeError('Error fetching: {}, check the api and try again'.format(response.status_code))
	return response	

def get_password_leaks_count(hashes,hash_to_check):
	hashes=(line.split(':') for line in hashes.split('\n'))
	for h,count in hashes:
		if h == hash_to_check:
			return float(count)
	return 0

def pwned_api_check(password):
	sha1password=hashlib.sha1(password.encode('utf8')).hexdigest().upper()
	first5_char,tail=sha1password[:5],sha1password[5:]
	response=request_api_data(first5_char)
	count=get_password_leaks_count(response.text,tail)
	if count:
		print('your password was leaked ',count,' times')
	else:
		print('Congrats! your password was not part of any data breaches')

if __name__=='__main__':
	password=getpass('Check whether your password is secure\nEnter your password : ')
	pwned_api_check(password)


