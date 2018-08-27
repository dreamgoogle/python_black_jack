import sys

import site
site.addsitedir(r'C:\users\deepika\anaconda3\lib\site-packages')

from colorama import Fore
from colorama import Style
print (f'This is {Fore.GREEN}color{Style.RESET_ALL}!')