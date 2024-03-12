import time
import logging
import os
import socket
import sys
from logging.handlers import TimedRotatingFileHandler

 
hostname = socket.gethostname()
# date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
project_name = (root_path.split(os.path.sep))[-1]
 
 
def get_current_time():
    # current_time = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))  # 返回当前时间
    current_time = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))  # 返回当前时间
    return current_time
 
 
class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射
    count = 0
    formatter = "[%(levelname)s] %(asctime)s [%(filename)s:%(lineno)d, %(funcName)s] %(message)s"
    def __init__(self, fmt='%(message)s'):
        log_dir = str(current_directory) + '/logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)    
        self.current_time = get_current_time()
        filename = str(current_directory) + '/logs/' + get_current_time() + '.log'
        self.logger = logging.getLogger(filename)
        self.format_str = logging.Formatter(self.formatter)  # 设置日志格式
        self.create_handler()
        Logger.count += 1
 
    def create_handler(self):
        self.current_time = get_current_time()
        filename = str(current_directory) + '/logs/' + get_current_time() + '.log'
        self.logger = logging.getLogger(filename)
        # self.logger.setLevel(logging.INFO)  # 设置日志级别
        # sh = logging.StreamHandler()  # 往屏幕上输出
        # sh.setFormatter(self.format_str)  # 设置屏幕上显示的格式
        th = logging.FileHandler(filename=filename, encoding='utf-8')
        th.setFormatter(self.format_str)  # 设置文件里写入的格式
        # self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)

        # time_hdls = self.logger.handlers.TimedRotatingFileHandler(filename, when='D', interval=1, backupCount=7)
        # self.logger.getLogger().addHandler(time_hdls)

        self.logger.setLevel(logging.INFO)
        info_file_name = 'info-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'

       

        # 控制台日志
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.format_str)


        # info日志处理器
        # filename：日志文件名
        # when：日志文件按什么维度切分。'S'-秒；'M'-分钟；'H'-小时；'D'-天；'W'-周
        #       这里需要注意，如果选择 D-天，那么这个不是严格意义上的'天'，而是从你
        #       项目启动开始，过了24小时，才会从新创建一个新的日志文件，
        #       如果项目重启，这个时间就会重置。所以这里选择'MIDNIGHT'-是指过了午夜
        #       12点，就会创建新的日志。
        # interval：是指等待多少个单位 when 的时间后，Logger会自动重建文件。
        # backupCount：是保留日志个数。默认的0是不会自动删除掉日志。
        info_handler = TimedRotatingFileHandler(filename=current_directory + info_file_name,
                                                when='MIDNIGHT',
                                                interval=1,
                                                backupCount=7,
                                                encoding='utf-8')
        info_handler.setFormatter(self.format_str)
        info_handler.setLevel(logging.INFO)
        # error日志文件名
        error_file_name = 'error-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
        # 错误日志处理器
        err_handler = TimedRotatingFileHandler(filename=current_directory +  error_file_name,
                                            when='MIDNIGHT',
                                            interval=1,
                                            backupCount=7,
                                            encoding='utf-8')
        err_handler.setFormatter(self.format_str)
        err_handler.setLevel(logging.ERROR)
        # 添加日志处理器
        self.logger.addHandler(info_handler)
        self.logger.addHandler(err_handler)
        self.logger.addHandler(console_handler)


 
    def info(self, msg):
        current_time = get_current_time()
        if self.current_time != current_time:
            self.create_handler()
 
        self.logger.info(msg)
        # self.logger.removeHandler(self.logger.handlers)
        # cls.log.info(msg)
        #print("有{}个日志打印类对象".format(Logger.count))
        return
 
    def warning(self, msg):
        current_time = get_current_time()
        if self.current_time != current_time:
            self.create_handler()
        self.logger.warning(msg)
        return
 
    def error(self, msg):
        current_time = get_current_time()
        if self.current_time != current_time:
            self.create_handler()
        self.logger.error(msg)
        return
 

# 定义一个log全局变量
log = Logger()




# 查看系统类型
# platform_ = platform.system()
# if platform_ == "Windows":
#     log_file_path = str(root_path) + '/logs/' + project_name + "-" + date + '.log'
# else:
#     log_file_path = '/home/logs/' + hostname + '.log'
 
 
# if __name__ == '__main__':
#     log = Logger()
#     log.logger.debug('debug')
#     log.logger.info('info')
#     log.logger.warning('警告')
#     log.logger.error('报错')
#     log.logger.critical('严重')
#     Logger().logger.error('error')