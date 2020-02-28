import time, ast
import json, requests

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse

WAIT_TIME = 600
WEBHOOK_ADDRESS="<YOUR DISCORD WEBHOOK ADDRESS>"

def parse_info():
  req = Request("http://ncov.mohw.go.kr/index_main.jsp")
  res = urlopen(req)

  bs = BeautifulSoup(res, "html.parser")
  status = [i.text for i in bs.findAll("a", attrs={"class": "num"})]
  try:
    print(status)
  except IndexError as e:
    req = Request("http://ncov.mohw.go.kr/index_main.jsp")
    bs = BeautifulSoup(res, "html.parser")
    status = [i.text for i in bs.findAll("a", attrs={"class": "num"})]

  return status


def main():
  ticker = threading.Event()
  temp = ""
  while not ticker.wait(WAIT_TIME):
    a = parse_info()
    time.sleep(60)

    if (len(a) != 3):
      a = temp

    # Initialize
    if (temp == ""):
      temp = a
      # Send request to discord then pass
      text = "확진환자수 : " + temp[0] + "\n" + "확진환자 격리해제수 : " + temp[1] + "\n" + "사망자수 : " + temp[2]
      url = WEBHOOK_ADDRESS
      headers = {"Content-Type": 'application/json'}
      data = {"embeds": [{"title": "## 한국 코로나 바이러스 현황 ##", "description": text, "color": 14366005}]}
      r = requests.post(url, data=json.dumps(data), headers=headers)
      pass


    if (a == temp):
      print("Same Status")
      pass
    else:
      temp = a
      url = WEBHOOK_ADDRESS
      text = "확진환자수 : " + temp[0] + "\n" + "확진환자 격리해제수 : " + temp[1] + "\n" + "사망자수 : " + temp[2]
      data = {"embeds": [{"title": "## 한국 코로나 바이러스 현황 ##", "description": text, "color": 14366005}]}
      # Send request to discord
      r = requests.post(url, data=json.dumps(data), headers=headers)


main()