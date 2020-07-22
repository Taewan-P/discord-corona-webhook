import time, ast
import json, requests

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse

WEBHOOK_ADDRESS="<YOUR DISCORD WEBHOOK ADDRESS>"

def parse_info():
  session = requests.Session()
  req = "http://ncov.mohw.go.kr/index_main.jsp"
  res = session.get(req)
  time.sleep(3)

  bs = BeautifulSoup(res.text, "html.parser")
  status = [i.text for i in bs.findAll("span", attrs={"class": "num"})[:4]]
  local_abroad_status = [i[4:] for i in bs.findAll("div", attrs={"class": "datalist"})[0].text.split()]
  try:
    print(status[0] + "//" + status[1] + "//" + status[2])
  except IndexError:
    req = Request("http://ncov.mohw.go.kr/index_main.jsp")
    bs = BeautifulSoup(res, "html.parser")
    status = [i.text for i in bs.findAll("span", attrs={"class": "num"})[:4]]
    local_abroad_status = [i[4:] for i in bs.findAll("div", attrs={"class": "datalist"})[0].text.split()]

  status[0] = status[0].split(")")[1]
  status.pop(2)
  status = [i + " 명" for i in status]

  return status, local_abroad_status

def send_result(stat, stat2):
  try:
    stat[0] += "\n┗*지역발생 {0} 명, 해외유입 {1} 명*".format(stat2[0], stat2[1])
    text = "확진환자수 : {0}\n\n확진환자 격리해제수 : {1}\n사망자수 : {2}".format(stat[0], stat[1], stat[2])
  except IndexError:
    return "ERROR"

  url = WEBHOOK_ADDRESS
  headers = {"Content-Type": 'application/json'}
  data = {"embeds": [{"title": " 😡　한국 코로나 바이러스 현황　😡", "description": text, "color": 14366005}]}
  r = requests.post(url, data=json.dumps(data), headers=headers)

def add_changes(last, recent):
  """
    Change num string(today and yesterday's stat) to num, then subtrack the difference between yesterday's stat and today's stat.
    After getting the difference, add them to the num string(today's stat) with parentheses.
    Example: 
      Yesterday's total COVID19 cases: "12,345" -> last[0]
      Today's total COVID19 cases: "12,550" -> recent[0]
      "12,550 (+205)" -> result[0]

    last: Yesterday's [COVID19 cases, cured cases, deaths]
    recent: Today's [COVID19 cases, cured cases, deaths]
  """
  prev1 = int(last[0].split(" ")[0].replace(",", ""))
  prev2 = int(last[1].split(" ")[0].replace(",", ""))
  prev3 = int(last[2].split(" ")[0].replace(",", ""))

  recent1 = int(recent[0].split(" ")[0].replace(",", ""))
  recent2 = int(recent[1].split(" ")[0].replace(",", ""))
  recent3 = int(recent[2].split(" ")[0].replace(",", ""))

  fin1 = " (+" + "{:,}".format(recent1 - prev1) + ")"
  fin2 = " (+" + "{:,}".format(recent2 - prev2) + ")"
  fin3 = " (+" + "{:,}".format(recent3 - prev3) + ")"

  result = []

  if (recent1 != prev1):
    result.append(recent[0] + fin1)
  else:
    result.append(recent[0])

  if (recent2 != prev2):
    result.append(recent[1] + fin2)
  else:
    result.append(recent[1])

  if (recent3 != prev3):
    result.append(recent[2] + fin3)
  else:
    result.append(recent[2])

  return result

def main():
  file = open("stats.txt", "r+")
  a, b = parse_info()
  laststat = file.readline()
  if laststat == "\n":
    laststat = []
  else:
    laststat = ast.literal_eval(laststat)
    laststat = [i.strip() for i in laststat]

  if (len(a) != 3):
    # Parse Error, Trying one more time.
    a, b = parse_info()

  if (laststat == []):
    # Initial
    send_result(a, b)
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
      r = add_changes(laststat, a)
      send_result(r, b)
      file.close()
      file = open("stats.txt", "w+")
      file.write(str(a))
      file.close()
      return "UPDATED"
  
  file.close()

print(main())