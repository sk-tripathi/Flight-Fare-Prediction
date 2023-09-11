import os
import logging
from datetime import datetime
#log file name
logfile_name=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

#log directory
logs_path=os.path.join(os.getcwd(),'logs')
#create folder if not available
os.makedirs(logs_path,exist_ok=True)
#log file path
log_file_path = os.path.join(logs_path,logfile_name)

logging.basicConfig(
    filename=log_file_path,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


if __name__ =="__main__":
    logging.info('logging has started')
