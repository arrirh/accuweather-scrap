from bs4 import BeautifulSoup
import csv
from datetime import date
from datetime import datetime
import requests
import os
import os.path
import schedule
import time

print('result.csv is saving in', os.getcwd())

def send_results_via_mail(receiver):
    fromaddr = "some_email@gmail.com"
    toaddr = receiver

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Parser results"

    body = ""
    msg.attach(MIMEText(body, 'plain'))

    filename = "result.csv"
    attachment = open("result.csv", "rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % 'result.csv')

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()
    s.login(fromaddr, "some_email")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

def job():
    try:
        url = 'https://www.accuweather.com/ru/ru/nizhny-novgorod/294199/air-quality-index/294199'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0' 
        headers={'User-Agent':user_agent,} 
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.text, "html.parser")

        o3_block = soup.find('div', attrs={'class': 'air-quality-pollutant', 'data-qa': 'airQualityPollutantO3'})
        o3 = o3_block.text.strip()
        o3 = o3.split('\n')[-1]
        o3 = o3[:len(o3)-6]

        pm10_block = soup.find('div', attrs={'class': 'air-quality-pollutant', 'data-qa': 'airQualityPollutantPM10'})
        pm10 = pm10_block.text.strip()
        pm10 = pm10.split('\n')[-1]
        pm10 = pm10[:len(pm10)-6]

        pm25_block = soup.find('div', attrs={'class': 'air-quality-pollutant', 'data-qa': 'airQualityPollutantPM2_5'})
        pm25 = pm25_block.text.strip()
        pm25 = pm25.split('\n')[-1]
        pm25 = pm25[:len(pm25)-6]

        no2_block = soup.find('div', attrs={'class': 'air-quality-pollutant', 'data-qa': 'airQualityPollutantNO2'})
        no2 = no2_block.text.strip()
        no2 = no2.split('\n')[-1]
        no2 = no2[:len(no2)-6]

        so2_block = soup.find('div', attrs={'class': 'air-quality-pollutant', 'data-qa': 'airQualityPollutantSO2'})
        so2 = so2_block.text.strip()
        so2 = so2.split('\n')[-1]
        so2 = so2[:len(so2)-6]

        co_block = soup.find('div', attrs={'class': 'air-quality-pollutant', 'data-qa': 'airQualityPollutantCO'})
        co = co_block.text.strip()
        co = co.split('\n')[-1]
        co = co[:len(co)-6]
    except:
        o3 = pm10 = pm25 = no2 = so2 = co = ''

    try:
        url = 'https://www.accuweather.com/ru/ru/nizhny-novgorod/294199/current-weather/294199'
        url = 'https://www.accuweather.com/ru/ru/nizhny-novgorod/294199/current-weather/294199'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
        headers={'User-Agent':user_agent,} 
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.text, "html.parser")

        T_block = soup.find('div', attrs={'class': 'display-temp'})
        T = T_block.text.strip()
        T = T[:-2]

        try:
            H_block = soup.find('div', attrs={'class': 'current-weather-details'})
            H_block = H_block.text.strip()
            H = H_block.split('\n')[H_block.split('\n').index('Влажность')+1].split(' ')[0]
        except:
            H = ''

        try:
            H_block = soup.find('div', attrs={'class': 'current-weather-details'})
            H_block = H_block.text.strip()
            W = H_block.split('\n')[H_block.split('\n').index('Ветер')+1].split(' ')[1]
        except:
            W = ''

        precip_block = soup.find('div', attrs={'class': 'phrase'})
        precip = precip_block.text.strip()
    except:
        T = H = W = precip = ''

    metrics = [date.today().strftime("%d/%m/%Y"), datetime.now().strftime("%H:%M:%S"), o3, pm10, pm25, no2, so2, co, T, H, W, precip]

    try:
        if not os.path.exists('result.csv'):
            header = ['Date', 'Time', 'O3', 'PM_10', 'PM_25', 'NO2', 'SO2', 'CO', 'Temperature', 'Humidity', 'Precipitation']
            with open('result.csv', 'w') as fd:
                fd.write(','.join(header) + '\n')

        with open('result.csv','a') as fd:
                fd.write(','.join(metrics) + '\n')

        print('Saved in', datetime.now().strftime("%H:%M:%S"))
    except:
        print('Error while saving in', datetime.now().strftime("%H:%M:%S"))

    try:
        send_results_via_mail('receiver1@gmail.com')
        send_results_via_mail('receiver2@yandex.ru')
    except:
        True
    
    
job()


