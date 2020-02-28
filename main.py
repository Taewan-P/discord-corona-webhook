import time, ast
import json, requests

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse

WEBHOOK_ADDRESS="<YOUR DISCORD WEBHOOK ADDRESS>"

def parse_info():
  req = Request("http://ncov.mohw.go.kr/index_main.jsp")
  res = urlopen(req)
  time.sleep(3)

  bs = BeautifulSoup(res, "html.parser")
  status = [i.text for i in bs.findAll("a", attrs={"class": "num"})]
  try:
    print(status)
  except IndexError as e:
    req = Request("http://ncov.mohw.go.kr/index_main.jsp")
    bs = BeautifulSoup(res, "html.parser")
    status = [i.text for i in bs.findAll("a", attrs={"class": "num"})]

  return status

def send_result(stat):
  try:
    text = "확진환자수 : " + stat[0] + "\n" + "확진환자 격리해제수 : " + stat[1] + "\n" + "사망자수 : " + stat[2]
  except IndexError as e:
    return "ERROR"

  url = WEBHOOK_ADDRESS
  headers = {"Content-Type": 'application/json'}
  data = {"embeds": [{"title": "## 한국 코로나 바이러스 현황 ##", "description": text, "color": 14366005}]}
  r = requests.post(url, data=json.dumps(data), headers=headers)


def main():
  file = open("stats.txt", "r+")
  a = parse_info()
  laststat = file.readline()
  if laststat == "\n":
    laststat = []
  else:
    laststat = ast.literal_eval(laststat)
    laststat = [i.strip() for i in laststat]

  if (len(a) != 3):
    # Parse Error, Trying one more time.
    a = parse_info()

  if (laststat == []):
    # Initial
    send_result(a)
    file.close()
    file = open("stats.txt", "w+")
    file.write(str(a))
    file.close()
    return "INITIAL"

  else:
    # Regular
    if (a == laststat):
      # Same Status
      file.close()
      return "PASS"
    else:
      # Update Status
      send_result(a)
      file.close()
      file = open("stats.txt", "w+")
      file.write(str(a))
      file.close()
      return "UPDATED"
  
  file.close()

print(main())