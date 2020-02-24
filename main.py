import threading, time
import json, requests

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse

WAIT_TIME = 600
WEBHOOK_ADDRESS="<YOUR DISCORD WEBHOOK ADDRESS>"

def parse_info():
  req = Request("http://ncov.mohw.go.kr/bdBoardList.do")
  res = urlopen(req)

  bs = BeautifulSoup(res, "html.parser")
  status = [i.text for i in bs.findAll("ul", attrs={"class": "s_listin_dot"})[:1]]
  print(status[0])
  return status[0]


def main():
  ticker = threading.Event()
  temp = ""
  while not ticker.wait(WAIT_TIME):
    a = parse_info()
    time.sleep(10)
    # Initialize
    if (temp == ""):
      temp = a
      # Send request to discord then pass
      url = WEBHOOK_ADDRESS
      headers = {"Content-Type": 'application/json'}
      data = {"embeds": [{"title": "## 한국 코로나 바이러스 현황 ##", "description": temp, "color": 14366005}]}
      r = requests.post(url, data=json.dumps(data), headers=headers)
      pass


    if (a == temp):
      print("Same Status")
      pass
    else:
      temp = a
      data = {"embeds": [{"title": "## 한국 코로나 바이러스 현황 ##", "description": temp, "color": 14366005}]}
      # Send request to discord
      r = requests.post(url, data=json.dumps(data), headers=headers)


main()