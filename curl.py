import subprocess
import os

__version__="1"

class cURLException(Exception):pass


def test_call(*args, **kwargs):
    try:
        subprocess.check_output(*args, **kwargs)
        return True
        
    except Exception:
        return False


# Checking for CURL tool
t = test_call(["curl", "--version"])

if not t:
    
    if test_call("apt-get"):
        os.system("apt-get install curl")
        
    elif test_call("apt"):
        os.system("apt install curl")
        
    elif test_call("yum"):
        os.system("yum install curl")
        
    elif test_call("zypper"):
        os.system("zypper install curl")
        
    elif test_call("pacman"):
        os.system("pacman -Sy curl")
        
    else:
        import webbrowser
        webbrowser.open("https://curl.haxx.se/download.html")
        
    t = test_call(["curl", "--version"])
    
    if not t:
        raise CURLException("CURL Not Working. install it from https://curl.haxx.se/download.html or your package manager")
    
    else:
        curl="curl"
else:
    curl="curl"


__doc__ = os.popen(curl+" --manual").read()

__doc__=__doc__.replace(      """                                  _   _ ____  _
  Project                     ___| | | |  _ \| |
                             / __| | | | |_) | |
                            | (__| |_| |  _ <| |___
                             \___|\___/|_| \_\_____|""","")

__doc__=__doc__.replace("-", "")

__doc__+="""
This is licensed under MIT license
created by Kavindu Santhusa ( https://github.com/Ksengine/cURL-light )"""


__version_string__ = os.popen(curl+" --version").read()

__version__ = __version_string__.split(" ")[1]+"."+__version__


def _message(args, writeable, caller=None):
    env = os.environ.copy()
    env["WINDOWID"] = ""
    
    if writeable:
        p = subprocess.Popen([curl] + args,stdin=subprocess.PIPE,stderr=subprocess.PIPE,stdout=subprocess.PIPE,env=env)
        
        return p
        
    else:
        p = subprocess.Popen([curl] + args,stdin=subprocess.PIPE,stderr=subprocess.PIPE,stdout=subprocess.PIPE,env=env)
        
        try:
            lines_iterator = iter(p.stdout.readline, b"")
            data=""
            
            while p.poll() is None:
                
                for line in lines_iterator:
                    nline = line.rstrip()
                    nline=nline.decode("utf-8", "ignore")
                    
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
        
    for arg in args:
        arg=str(arg)
        url=False
        
        for protocol in ("DICT", "FILE", "FTP", "FTPS", "GOPHER", "HTTP", "HTTPS",  "IMAP",
       "IMAPS",  "LDAP",  "LDAPS",  "POP3",  "POP3S",  "RTMP", "RTSP", "SCP", "SFTP", "SMB", "SMBS",
       "SMTP", "SMTPS", "TELNET", "TFTP"):
           
            if arg.lstrip().upper().startswith(protocol+"://"):
                url=True
                
        for char in r"""!"#$%&"()*+,-./:;<=>?@[\]^_`{|}~""":
            
            if char in arg:
                url=True
                
        if url:
            flags_list.append("\""+arg+"\"")
            
        else:
            flags_list.append("--"+arg.replace("_","-"))
            
    return _message(flags_list,w,y)

def cli():
    import sys
    os.system(curl+" "+" ".join(sys.argv[1:]))

  
if __name__=="__main__":
    cli()
