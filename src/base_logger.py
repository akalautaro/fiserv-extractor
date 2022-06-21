import logging as log
from pathlib import Path
import os

BASE_DIR = Path(os.path.abspath(os.path.dirname(__file__))).parent.absolute()

log.basicConfig(
    level=log.INFO,
    format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
    datefmt='%I:%M:%S %p',
    handlers=[log.FileHandler(f'{BASE_DIR}/fiserv_extractor.log'), log.StreamHandler()]
    )

