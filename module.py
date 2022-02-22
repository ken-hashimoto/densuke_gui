import PySimpleGUI as sg
import datetime as dt
import calendar

sg.theme('DarkAmber')

def isint(n):
  try:
    n = int(n)
    return True
  except ValueError:
    return False

def input_check(m_d):
  dt_now = dt.datetime.now()
  for s in m_d:
  #日時のフィールドに入力された文字列の各行が仕様通りか確認
    s = s.split()
    if len(s) != 2:
      return False
    m,d = s
    if not isint(m) or not isint(d):
      return False
    if int(m) < 1 or 12 < int(m) or int(d) < 1 or calendar.monthrange(dt_now.year, int(m))[1] < int(d):
      return False
  return True

def densuke_make(schedule,des,mail,title,option_id):
  from selenium import webdriver
  import pyperclip
  import chromedriver_binary
  import slackweb
  from selenium.webdriver.common.by import By
  from selenium.webdriver.support.ui import WebDriverWait
  from selenium.webdriver.support import expected_conditions as EC
  
  webdriver = webdriver.Chrome()
  webdriver.get("https://www.densuke.biz/event")
  #入力
  webdriver.find_element_by_xpath("//*[@id='edit']/form/div[2]/table/tbody/tr[1]/td/input").send_keys(title)
  webdriver.find_element_by_xpath("//*[@id='schedule']").send_keys(schedule)
  webdriver.find_element_by_xpath("//*[@id='edit']/form/div[2]/table/tbody/tr[3]/td/textarea").send_keys(des)
  webdriver.find_element_by_xpath("//*[@id='edit']/form/div[2]/table/tbody/tr[4]/td/input").send_keys(mail)
  webdriver.find_element_by_id(option_id).click()
  #次へ進むをクリック
  webdriver.find_element_by_xpath("//*[@id='edit']/form/table/tbody/tr/td/input").click()
  WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'mainbox'))) #待機
  make = webdriver.find_element_by_xpath("//*[@id='edit']/form/table/tbody/tr/td/input")
  #作成するをクリック
  webdriver.execute_script('arguments[0].click();', make)
  WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'copybtn')))
  #リンクをコピーする
  webdriver.find_element_by_xpath("//*[@id='newcomer']/form/div/table/tbody/tr/td/div/a[1]").click()
  link = pyperclip.paste()
  #slackのDMに送信
  if WEB_HOOK_URL != "":
    slack = slackweb.Slack(url=WEB_HOOK_URL)
    slack.notify(text = link)
#各個人でお好みに設定---------------------------------------------------------------------------------------------
WEB_HOOK_URL ="" #メッセージを投稿したいチャンネルのWebhook URLを入力
title = "" #伝助で作成するページのイベント名
mail_address = "" #作成したページのリンクを送るメールアドレス
default_text = "" #日付を入力するところにデフォルトで書いておきたいことがあれば(ないと思うけど....)
#選択肢が「◎○△×」「○△×」「○×」のときに表示させたいテキストを入力
description_four = "◎ いける\n○ 絶起可能性有\n△（途中からor途中まで参加可能、現時点で未確定など）\n× 無理"
description_three = "○ いける\n△（途中からor途中まで参加可能、現時点で未確定など）\n× 無理"
description_two = "○ いける\n× 無理"
#---------------------------------------------------------------------------------------------------------------
layout =  [ [sg.Text("タイトルを入力"),sg.InputText(title,size = (28,1),key = "title")],
            [sg.Text('日付を入力（ 例:1月2日なら「1 2」)  複数ある時は改行区切り')],
            [sg.Multiline(default_text,size = (50,8),key ="date")],
            [sg.Button(button_text="次の木曜と土曜",key = "b1"),sg.Button(button_text="月曜から土曜",key = "b2")],
            [sg.Text('時間を選択'),sg.Checkbox("10:30", default=True,key = "10"),sg.Checkbox("13:00", default=True,key = "13"),sg.Checkbox("15:00", default=True,key = "15")],
            [sg.Text("リンクを送信するメールを入力"),sg.InputText(mail_address,size = (28,1),key = 'mail')],
            [sg.Text("詳細を入力")],
            [sg.Radio("「○△×」から選択",group_id = "option",key = "three",default = True,enable_events= True),sg.Radio("「○×」から選択",group_id = "option",key = "two",enable_events= True),sg.Radio("「◎○△×」から選択",group_id = "option",key = "four",enable_events= True)],
            [sg.Multiline("○ いける\n△（途中からor途中まで参加可能、現時点で未確定など）\n× 無理",size =(60,8),key = "des")],
            [sg.Text("slackのDMにリンクを送信しますか？"),sg.Radio("はい",default=True,group_id = 'g1'),sg.Radio("いいえ",group_id = 'g1')],
            [sg.Button('作成', key='make')],
            ]
day_of_week = ["(月)","(火)","(水)","(木)","(金)","(土)","(日)"]
window = sg.Window('伝助作成ツール', layout,size=(530,600))
while True:
  event,values = window.read()
  if event is None:
    break
  if event == "b1":
    dt_now = dt.datetime.now()
    now_m = dt_now.month
    now_d = dt_now.day
    now_w = dt_now.weekday()
    #つぎの木曜日は何日後か
    s = (3 - int(now_w))%7
    thu = dt_now + dt.timedelta(days=s) #次の木曜日
    stu = dt_now + dt.timedelta(days=s+2) #次の土曜日
    li = [thu.month,thu.day,stu.month,stu.day]
    text = str(thu.month) + " " + str(thu.day) + "\n" + str(stu.month) + " " + str(stu.day)
    window["date"].update(text)
  if event == "b2": #次の月曜日から土曜日までを表示
    dt_now = dt.datetime.now()
    now_m = dt_now.month
    now_d = dt_now.day
    now_w = dt_now.weekday()
    #つぎの月曜日は何日後か
    s = (0 - int(now_w))%7
    li_week = []
    text = ""
    for i in range(6):
      wd = dt_now + dt.timedelta(days=s+i)
      text += str(wd.month) + " " + str(wd.day)
      if i != 5:
        text += "\n"
    window["date"].update(text)
  if event == "three":
    window["des"].update(description_three)
  if event == "four":
    window["des"].update(description_four)
  if event == "two":
    window["des"].update(description_two)
  if event == "make":
    #入力をもとに日時のフィールドに入れる文字列を作成
    schedule = []
    m_d = list(values["date"].split("\n")) #month_day
    new_m_d = []
    for i in range(len(m_d)):
      new_m_d.append(tuple(map(int,m_d[i].split())))
    for i in range(len(new_m_d)):
      m,d = new_m_d[i][0],new_m_d[i][1]
      dt_now = dt.datetime.now()
      y = dt_now.year
      tmp = dt.date(y, m, d)
      w = tmp.weekday()
      schedule.append((m,d,day_of_week[w]))
    str_schedule = ""
    time_table = []
    if values["10"] == True:
      time_table.append("10:30")
    if values["13"] == True:
      time_table.append("13:00")
    if values["15"] == True:
      time_table.append("15:00")
    for m,d,w in schedule:
      for t in time_table:
        str_schedule += "{0}/{1} {2} {3}-\n".format(m,d,w,t)
    if values["three"] == True:
      option_id = "eventchoice1"
    if values["two"] == True:
      option_id = "eventchoice2"
    if values["four"] == True:
      option_id = "eventchoice3"
    densuke_make(str_schedule,values["des"],values["mail"],values["title"],option_id)