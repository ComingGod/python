import logging
import logging.config
import os
import time

# def log_init():
current_time = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
file_path = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')
main_path = os.path.abspath(os.path.join(file_path, '..')).replace('\\','/')


log_file = main_path + '/result/' + current_time + '_run.txt'
log_conf = main_path + '/config/logging.conf'


if not os.path.exists(os.path.dirname(log_file)):
    os.makedirs(os.path.dirname(log_file))
else:
    pass

# a = dict(log_file=log_file)
# print a 

logging.config.fileConfig(log_conf, defaults=dict(log_file=log_file))

    
    
#     logging.config.fileConfig('log_configure.txt', defaults=dict('log.txt'))
#     logging.info(imput)


# if __name__ == "__main__":
#     log_init()
