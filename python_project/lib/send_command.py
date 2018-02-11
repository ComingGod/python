import subprocess
import logging
import sys
import log

buffer = ''

def send_command(cmd):
    global buffer
    p = subprocess.Popen(cmd, 0, None, subprocess.PIPE, subprocess.PIPE, None, shell=True)
    logging.info('send command :%s', cmd)
    (sout, serr) = p.communicate()
    buffer = buffer + sout
#     print '=============================='
#     print buffer
    logging.info('output: \n%s', sout)
    
def find_string(string):
    global buffer    
    #find will return the location of string, location for value 0 , if not found the string will return -1
    if (-1 == buffer.find(string)) :
        logging.info('can not find %s',string)
        sys.exit(1)
    else: 
        buffer = buffer.split(string,1)[1]
        logging.info('find %s successfully.',string)
#         print '************************'
#         print 'find string successfully' + string
#         print buffer

def get_string(string, count):
    global buffer
    location = buffer.find(string)
    if (-1 == location) :
        logging.info('can not find %s',string)
        sys.exit(1)
    else: 
        count = len(string)
        pos   = location + count
        get_string = buffer[pos:count+pos]
        buffer = buffer.split(string,1)[1]
        logging.info('find %s successfully.',string)
        return get_string
        print get_string
    
if __name__ == '__main__':
    send_command('dir')
    send_command('dir')
    get_string('log.py',10)
#     find_string('Directory of E:\python_project\lib')
#     find_string('send_command.py')
#     find_string('log.py')
#     find_string('hah')
    
    
    
