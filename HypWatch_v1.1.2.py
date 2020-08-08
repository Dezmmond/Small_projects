import requests
import time
import sched
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import threading

# Отдельная функция-заготовка для вынесения 
# последующих функций в отдельный поток
def thread(my_func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
        #my_thread.join()
    return wrapper

url_list = ['https://www.hypbrain.com', 'https://www.drive.hypbrain.com', 'https://www.millesime.store', 'http://www.elitwine.ru', 'https://www.gee.store']
url_copy = ['https://www.hypbrain.com', 'https://www.drive.hypbrain.com', 'https://www.millesime.store', 'http://www.elitwine.ru', 'https://www.gee.store']

errors = {'500' : 'Internal Server Error («внутренняя ошибка сервера»)',
         '501' : 'Not Implemented («не реализовано»)',
         '502' : 'Bad Gateway («плохой, ошибочный шлюз»)',
         '503' : 'Service Unavailable («сервис недоступен»)',
         '504' : 'Gateway Timeout («шлюз не отвечает»)',
         '505' : 'HTTP Version Not Supported («версия HTTP не поддерживается»)',
         '506' : 'Variant Also Negotiates («вариант тоже проводит согласование»)',
         '507' : 'Insufficient Storage («переполнение хранилища»)',
         '508' : 'Loop Detected («обнаружено бесконечное перенаправление»)',
         '509' : 'Bandwidth Limit Exceeded («исчерпана пропускная ширина канала»)',
         '510' : 'Not Extended («не расширено»)',
         '511' : 'Network Authentication Required («требуется сетевая аутентификация»)',
         '520' : 'Unknown Error («неизвестная ошибка»)',
         '521' : 'Web Server Is Down («веб-сервер не работает»)',
         '522' : 'Connection Timed Out («соединение не отвечает»)',
         '523' : 'Origin Is Unreachable («источник недоступен»)',
         '524' : 'A Timeout Occurred («время ожидания истекло»)',
         '525' : 'SSL Handshake Failed («квитирование SSL не удалось»)',
         '526' : 'Invalid SSL Certificate («недействительный сертификат SSL»)',
         }

# -- Настройка ящика --
mail_sender = 'noreply@hypbrain.com'  
usr = 'noreply@hypbrain.com'
pwd = 'XXXXXXXXXX'
tolist = ['p.employee@hypbrain.com', 'e.employee@hypbrain.com', 'a.employee@hypbrain.com', 'm.employee@hypbrain.com']

# -- Функция отправки электронных сообщений --
@thread
def send_emes(emsg):
    server = smtplib.SMTP('smtp.masterhost.ru:228') 
    server.starttls()
    server.login(usr, pwd)
    server.sendmail(mail_sender, tolist, emsg.as_string())
    server.quit()

# -- Функция отправки смс сообщений --
@thread
def send_sms(sms):
    #time.sleep(20) #180
    requests.get(f'https://sms.ru/sms/send?api_id=2CB2F964-2037-9304-A126-A1DBFDE00189&to=<input_over_here_phone_numbers_of_employeers>&from=Hypbrain&msg={sms}&json=1')
    for i in range(6):
        time.sleep(15) #60
        requests.get(f'https://sms.ru/sms/send?api_id=2CB2F964-2037-9304-A126-A1DBFDE00189&to=input_over_here_phone_numbers_of_employeers&from=Hypbrain&msg={sms}&json=1')


# -- Функция проверки и запуска функций отправки сообщений --
@thread
def prover(response, url):
    # -- Тело сообщения --
    system_name = u'Система оповещений Hypbrain'
    subject = u'!Милорд!!!Один из наших сайтов в опасности!'
    body = errors[response] + ". Вот этому сайту плохо: " + url
    sms = url + ' ' + response
    emsg = MIMEText(body, 'plain', 'utf-8')
    emsg['From'] = Header(system_name, 'utf-8')
    emsg['Subject'] = Header(subject, 'utf-8')
    #--------------------------
    send_emes(emsg)
    send_sms(sms)


emes_send_thread = threading.Thread(target = send_emes)
sms_send_thread = threading.Thread(target = send_sms)
# -- Цикл опроса --
@thread
def main():
    while True:
        for url in url_copy:
            response = requests.get(url).status_code
            response = str(response)
            print(response)
            print(url)
            if response in errors and response != '200':
                print(url + errors[response])
                url_copy.remove(url)
                prover(response, url)
            elif response not in errors and response != '200':
                print(url + "Нет в списке")
                sms = "Скрипт обнаружил ошибку, которая не была внесена в список! Срочно проверить!"
                send_sms(sms)
                system_name = u'Система оповещений Hypbrain'
                subject = u'!Милорд!!!Один из наших сайтов в опасности!'
                body = "Скрипт обнаружил ошибку, которая не была внесена в список! Срочно проверить!"
                emsg = MIMEText(body, 'plain', 'utf-8')
                emsg['From'] = Header(system_name, 'utf-8')
                emsg['Subject'] = Header(subject, 'utf-8')
                send_emes(emsg)
                url_copy.remove(url)
            else: 
                pass
        print(url_copy)
        print(emes_send_thread.is_alive())
        print(sms_send_thread.is_alive())
        time.sleep(60) #60

if __name__ == "__main__":
    main()
