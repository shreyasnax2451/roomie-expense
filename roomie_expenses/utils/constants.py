import os
from datetime import datetime

from utils.enums import Month

months = [month.value for month in Month]
current_year = datetime.now().year
years = list(range(current_year, current_year + 50))
base_dir = os.path.abspath(os.path.dirname(__file__))
