import subprocess
import os

class cURLException(Exception):pass

def test_call(*args, **kwargs):
    """ Test whether a subprocess call succeeds.
    """
    try:
        subprocess.check_output(*args, **kwargs)
        return True
    except Exception:
        return False

def _message(args, writeable, caller=None):
    env = os.environ.copy()
    env['WINDOWID'] = ''
    if writeable:
        p = subprocess.Popen(['curl'] + args,stdin=subprocess.PIPE,stderr=subprocess.PIPE,stdout=subprocess.PIPE,env=env)
        return p
    else:
        p = subprocess.Popen(['curl'] + args,stdin=subprocess.PIPE,stderr=subprocess.PIPE,stdout=subprocess.PIPE,env=env)
        try:
            lines_iterator = iter(p.stdout.readline, b"")
            data=""
            while p.poll() is None:
                for line in lines_iterator:
                    nline = line.rstrip()
                    nline=nline.decode('utf-8', 'ignore')
                    if caller:
                        caller( nline)
                    else:
                        data+=nline+"\n"
            if caller:
                caller (not p.poll())
            else:
                return not p.poll(),data
        finally:
            if p.poll() is None:  # pragma: no cover
                p.kill()

# Checking for CURL tool
t = test_call(['curl', '--version'])
if not t:
    try:
        os.system("sudo apt-get install curl")
    except Exception as e:
        raise CURLException("CURL Not Working : "+str(e))
    t = test_call(['curl', '--version'])
    if not t:
        raise CURLException("cURL Not Working")

__doc__ = os.popen('curl --manual').read().replace('--', '').replace('-', '_')
__version_string__ = os.popen('curl --version').read()
__version__ = __version_string__.split(' ')[1]

def get(*args,**kwargs):
    w=False
    y=None
    flags_list=[]
    if "proc" in kwargs:
        w=True
        del kwargs["writeable"]
    if "caller" in kwargs:
        y=kwargs["caller"]
        del kwargs["caller"]
    for kwarg in kwargs:
        flags_list.append("--"+kwarg+"=\""+str(kwargs[kwarg])+"\"")
    flags_list.append(args[0])
    args=args[1:]
    for arg in args:
        flags_list.append('--'+arg.replace('_','-'))
    print(flags_list)
    return _message(flags_list,w,y)

def cli():
    import sys
    os.system('curl'+' '.join(sys.argv[1:]))

  
if __name__=='__main__':
    cli()
