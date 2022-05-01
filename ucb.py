import code
import functools
import inspect
import re
import signal
import sys


def main(fn):
	if inspect.stack()[1][0].f_locals['__name__'] == '__main__':
		args = sys.argv[1:]
		fn(*args)

	return fn


_PREFIX = ''

def trace(fn):
	@functools.wraps(fn)

	def wrapped(*args, **kwds):
		global _PREFIX
		reprs = [repr(e) for e in args]
		reprs += [repr(k) + '=' + repr(v) for k, v in kwds.items()]
		log('{0}({1})'.format(fn.__name__, ','.join(reprs)) + ':')
		_PREFIX += '     '

		try:
			result = fn(*args, **kwds)
			_PREFIX = _PREFIX[:-4]

		except Exception as e:
			log(fn.__name__ + 'exited via Exception')
			_PREFIX = _PREFIX[:-4]
			raise

		log('{0}({1}->{2}'.format(fn.__name__, ','.join(reprs),result))
		return result

	return wrapped



def log(message):
	print(_PREFIX + re.sub('\n', '\n' + _PREFIX, str(message)))



def log_current_line():
	frame = inspect.stack()[1]
	log('current line: File "{f[1]}", line {f[2]}, in {f[3]}').format(f = frame)


def interact(msg = None):
	frame = inspect.currentframe().f_back
	namespace = frame.f_global.copy()
	namespace.update(frame.f_locals)


	def handler(signum, frame):
		print()
		exit(0)

	signal.signal(signal.SIGINT, handler)

	if not msg:
		_, filename, line, _, _, _ = inspect.stack()[1]
		msg = 'interacting at file"{0}", line{1} \n'.format(filename, line)
		msg += '   unix:   <control> -D continues the program; \n'
		msg += '   windows: <control> - Z <enter> continues the program \n'
		msg += '   exit() or <control> - C exits the program'

	code.interact(msg, None, namespace)























