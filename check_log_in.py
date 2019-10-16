from flask import session, redirect, url_for
from functools import wraps


def check_logged_in(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'logged_in' in session:
			return func(*args, **kwargs)
		return redirect(url_for('login_page'))
	return wrapper

def forbid_transition_if_logged_in(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'logged_in' in session:
			return redirect(url_for('profile_page'))
		return func(*args, **kwargs)
	return wrapper

def block_wrap(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if 'logged_in' in session:
			return redirect(url_for('profile_page'))
		return func(*args, **kwargs)
	return wrapper

