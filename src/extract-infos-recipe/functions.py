import datetime
import re

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def log_function(color: bcolors, message):
  now = datetime.datetime.now()
  string = f"[ {bcolors.OKGREEN}{now.hour}:{now.minute}:{now.second}{bcolors.ENDC} ]--> "
  string += message
  print(string)


def process_text(text) -> str:
  text = re.sub("/"," ",text)
  text = re.sub("['-=\[\]+;/.,<>]"," ",text)
  text = re.sub(" +","-",text)
  return text
