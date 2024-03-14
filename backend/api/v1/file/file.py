import time
import os 



time_str = time.strftime('%Y-%m%d - %H%M%S')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")