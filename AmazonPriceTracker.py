import requests
from bs4 import BeautifulSoup
from time import sleep
import smtplib
import pandas as pd
import sys
import os

''' todo: add an argv option for the url '''

class Tracker:
    def __init__(self, target_price, url):
        '''
        Constructor for the price tracker

        :param price: integer that will represent the price we're checking for
        :param url: the url for the product that we will compare
        '''
        self.url = url
        self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
        self.page = requests.get(self.url, headers = self.headers)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.target_price = target_price
        self.price = self.soup.find('span', id = 'priceblock_ourprice').get_text()
        self.title = self.soup.find('span', id = 'productTitle').get_text().strip()
        self.converted = float(self.price.strip('$').replace(',', ''))

    def check_price(self, send_email, rec_email, app_key):
        '''
        Checks if the current item price is less than the target price. If so, sends an email.

        :param send_email: An email from which the email will be sent. This is the one associated with the apps key
        :param rec_email: An email to which the email will be set. 

        '''
        if self.converted <= self.target_price:
            self.__send_mail(send_email, rec_email, app_key)
        else:
            return None

    def __send_mail(self, send_email, rec_email, app_key):
        '''
        Sends an email to the one specified in the constructor via gmail. Will need an active google apps key
        password for this to work.

        Params are taken from check_price()

        :param send_email: An email from which the email will be sent. This is the one associated with the apps key
        :param rec_email: An email to which the email will be set. 
        '''
        
        try:
            # connect to email server
            smtp_server = '64.233.184.108'
            port = 587
            server = smtplib.SMTP(smtp_server, port)
            server.connect(smtp_server, port)
            # server.ehlo is called by starttls if required
            server.starttls()

            server.login(send_email, app_key)

            # create message body
            subject = f'Price dropped for {self.title}'
            body = f'''
            Good news,

            The price dropped on one of your items. You can view the page  at: {self.url}
            '''
            msg = f'Subject: {subject}\n\n {body}'

            server.sendmail(
                send_email,
                rec_email,
                msg
            )

            print('Email sent')
        except Exception as e:
            print('Error: ',e)
            print('Go to link: https://www.google.com/settings/security/lesssecureapps')
        finally:
            server.quit()

def main():
    # allow user to choose option and copy/paste url
    # todo: add more options
    print('''
    Welcome to the Amazon price checker. Enter the url of the product
    in question to get updated emails on the price

    
    1. Check price of a given amazon url. Will run until stopped
    2. Exit
    ''')
    user_int = input('Enter :')
    if user_int == '1':
        while True:
            track = Tracker(
                target_price = 700.00,
                url = 'https://www.amazon.com/Google-Pixel-XL-Unlocked-Renewed/dp/B0824BR684/ref=sr_1_4?dchild=1&keywords=google+pixel&qid=1603376831&sr=8-4'
            )
            track.check_price(
                send_email = 'mhoban16@gmail.com',
                rec_email = 'mhoban16@gmail.com',
                app_key = 'bfwqgnpwulyyuiuy'
            )
            # run every 10 mins
            sleep(60 * 10)
    elif user_int == '2':
        sys.exit()
        return None
    else:
        print('That is not a valid choice.')

if __name__ == '__main__':
    main()
    








