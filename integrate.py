from math import *
import numpy as np
from multiprocessing import Pool


def convert_function(code, varname):
	code = f'from math import *\n' +\
		   f'def f({varname}):\n' +\
		   f'	return {code}'

	_locals = locals()
	exec(code, _locals)

	return _locals['f']


__f = None

def worker_init(f):
	global __f
	__f = f

def worker(x):
	return __f(x)


def _integrate(f, a, b, n):
	step = (b - a) / n

	sum = f(a) + f(b)
	pool = Pool(None, initializer=worker_init, initargs=(f, ))

	P = np.arange(a+step, b-step, step)
	fx = pool.map(worker, P)
	sum += 2*np.sum(fx)
	# for x in np.arange(a+step, b-step, step):
	# 	sum += 2*f(x)

	return sum * step / 2


def integrate(f, a, b, psi=None, n=None):
	if psi is None:
		return _integrate(f, a, b, n)
	if n is None:
		n = abs(b-a) * 100  # random
	if n is None and psi is None:
		raise ValueError('Either psi or n should be defined')

	sum = _integrate(f, a, b, n)
	sum2 = _integrate(f, a, b, 2*n)

	err = abs(sum - sum2) / 3  # Runge rule
	if err < psi:
		return sum
	else:
		return integrate(f, a, b, psi, 2*n)


def inf_integrate(f, a, psi, n=None, l=None):
	if "state" not in inf_integrate.__dict__:
		inf_integrate.state = False

	if psi is None:
		raise ValueError("psi should be defined")
	if l is None:
		l = 100 # random
	if n is None:
		n = abs(l-a) * 100  # random

	sum = _integrate(f, a, l, n)
	sum2 = _integrate(f, a, l, 2*n)

	err = abs(sum - sum2)
	if err < psi:
		return sum, l
	else:
		if inf_integrate.state:
			n = n*2
		else:
			l = l*2
		inf_integrate.state = not inf_integrate.state
		return inf_integrate(f, a, psi, n, l)

