from datetime import datetime
import argparse
import os
import re
import subprocess
import sys
import urllib2


_VALID_HOST_PATTERN = r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}([:]\d+)?$'


def _validate_host(host):
    if re.match(_VALID_HOST_PATTERN, host):
        return host
    else:
        raise argparse.ArgumentTypeError('{} is not a valid host!'.format(host))


def rp(current_file, relative_path):
    """
    Returns absolute path to the specified path relative to current file.
    
    :param str module_file:
        The ``__file__`` attribute of the module where
        this function is being called.
        
    :param str relative_path:
        The relative path.
    
    :returns:
        Absolute path.
    """
    
    return os.path.join(os.path.dirname(current_file), relative_path)


def split_host(host):
    """
    Splits host into host and port.
    
    :param str host:
        Host including port.
    
    :returns:
        A ``(str(host), int(port))`` tuple.
    """
    
    host, port = (host.split(':') + [None])[:2]
    return host, int(port)


def parse_args():
    """
    Parses command line arguments.
    
    Looks for --testliveserver [host]
    
    :returns:
        A ``(str(host), int(port))`` or ``(None, None)`` tuple.
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--testliveserver',
                        help='Run as test live server.',
                        type=_validate_host,
                        nargs='?',
                        const='170.0.0.1:5000')
    args = parser.parse_args()
        
    if args.testliveserver:
        print 'Running as test live server at {}'.format(args.testliveserver)
        return split_host(args.testliveserver)
    else:
        return (None, None)


def check(url, timeout=10.0):
    """
    Checks whether a server is running.
    
    :param str url:
        URL of the server.
        
    :param float timeout:
        Timeout in seconds.
    """
    
    response = None
    sleeped = 0.0
    
    t = datetime.now()
    
    while not response:
        try:
            response = urllib2.urlopen(url)
        except urllib2.URLError:
            if sleeped > timeout:
                raise Exception('Live server didn\'t start in specified timeout {} seconds!'\
                                .format(timeout))
            sleeped = (datetime.now() - t).total_seconds()
    
    return (datetime.now() - t).total_seconds()


def start(path, host, timeout=10.0):
    """
    Starts a live server in a separate process and checks whether it is running.
    
    :param str path:
        Absolute path to a python module.
        
    :param str host:
        A host at which the live server should listen.
        
    :param float timeout:
        Timeout in seconds for the check.
    
    :returns:
        A :class:`subprocess.Popen` instance.
    """
    
    host = str(host)
    if re.match(_VALID_HOST_PATTERN, host):
        process = subprocess.Popen(['python', path, '--testliveserver', str(host)])
        duration = check('http://{}'.format(host))
        print('Live server started in {} seconds.'.format(duration))
        return process
    else:
        raise Exception('{} is not a valid host!'.format(host))









