from django.utils import timezone
from django.db import models

from urllib.request import urlopen
from django.conf import settings
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

from background_task import background
import math


class File(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='media/gelbeseiten')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Fetch(models.Model):
    name = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    website = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)

    @staticmethod
    def get_html_text(url, message):
        html = ''
        try:
            site = urlopen(url)
            message[0] += 'Open: {}<br>'.format(url)
            html = site.read()
            time.sleep(2)
            site.close()
        except Exception as e:
            message[0] += 'ERROR: {}<br>'.format(str(e))
        return html

    @staticmethod
    def generate_urls(category, location, message):
        urls = []
        first_url = 'https://www.gelbeseiten.de/Suche/{}/{}'.format(category, location)
        html = Entry.get_html_text(first_url, message)
        html = BeautifulSoup(html, 'lxml')
        amount_of_companies = Entry.find_amount_of_companies(html, message)
        pages = math.ceil(amount_of_companies / 50)
        for i in range(2, pages + 1):
            url = 'https://www.gelbeseiten.de/Suche/{}/{}/Seite-{}'.format(category, location, i)
            urls.append(url)
        return html, urls

    @staticmethod
    def find_amount_of_companies(soup, message):
        try:
            soup2 = soup.find('span', {'id': 'mod-TrefferlisteInfo'})
            soup3 = soup2.get_text()
            amount = [int(s) for s in soup3.split() if s.isdigit()]
            amount = amount[0]
        except:
            message[0] += "ERROR: Amount of companies could not be found.<br>"
            amount = 0
        return amount

    @staticmethod
    def find_all_data_clusters(soup):
        try:
            clusters = soup.find_all('article', {'class': 'mod-Treffer'})
        except:
            clusters = ''
        return clusters

    @staticmethod
    def find_name(soup):
        try:
            name = soup.find('h2')
            name = name.get_text()
        except:
            name = ''
        return name

    @staticmethod
    def fetch_soup(url, message):
        html = Entry.get_html_text(url, message)
        soup = BeautifulSoup(html, 'lxml')
        return soup

    @staticmethod
    def find_email(cluster):
        try:
            def find_email_sub(num):
                email = cluster.find_all('a', {'class': 'gs-btn'})
                email = email[num]
                email = email['href']
                email = email.replace('mailto:', '')
                email = email.split('?')
                email = email[0]
                return email

            email = find_email_sub(1)
            if not '@' in email:
                email = find_email_sub(0)
            if not '@' in email:
                email = ''
        except:
            email = ''
        return email

    @staticmethod
    def find_website(cluster):
        try:
            website = cluster.find_all('a', {'class': 'gs-btn'})
            website = website[0]
            website = website['href']
            if 'google' in website or '@' in website:
                website = ''
        except:
            website = ''
        return website

    @staticmethod
    def find_phone(cluster):
        try:
            phone = cluster.find('p', {'class': 'mod-AdresseKompakt__phoneNumber'})
            phone = phone.get_text()
        except:
            phone = ''
        return phone

    @staticmethod
    def find_address(cluster):
        try:
            address = cluster.find('p', {'data-wipe-name': 'Adresse'})
            address = address.find(text=True)
            address = address.replace('\t', '')
            address = address.replace('\n', ' ')
            address = address.replace('  ', ' ')
            address = address.replace(',', '')
        except:
            address = ''
        return address

    @staticmethod
    def find_zipcode(cluster):
        try:
            zipcode = cluster.find('span', {'class': 'nobr'})
            zipcode = zipcode.find(text=True)
            zipcode = [int(s) for s in zipcode.split() if s.isdigit()]
            zipcode = ''.join(map(str, zipcode))
        except:
            zipcode = ''
        return zipcode

    @staticmethod
    def find_city(cluster):
        try:
            city = cluster.find('span', {'class': 'nobr'})
            city = city.find(text=True)
            city = [str(s) for s in city.split() if s.isalpha()]
            city = ''.join(city)
        except:
            city = ''
        return city

    @staticmethod
    def fetch_data(soup, message, category='category', location='location'):
        data = []
        clusters = Entry.find_all_data_clusters(soup)
        for cluster in clusters:
            name = Entry.find_name(cluster)
            email = Entry.find_email(cluster)
            phone = Entry.find_phone(cluster)
            address = Entry.find_address(cluster)
            website = Entry.find_website(cluster)
            zipcode = Entry.find_zipcode(cluster)
            city = Entry.find_city(cluster)
            company_data = {'name': name, 'email': email, 'phone': phone, 'address': address, 'website': website,
                            'category': category, 'location': location, 'zipcode': zipcode, 'city': city}
            data.append(company_data)
        return data

    @staticmethod
    def save_companies(data, message):
        for company in data:
            companies = Entry.objects.filter(name=company['name'])
            if not companies.exists():
                gsc = Entry(**company)
                try:
                    gsc.save()
                    message[0] += 'Save: {name}<br>'.format(**company)
                except Exception as e:
                    message[0] += 'Exception (Save): {name}<br>'.format(**company)
                    message[0] += str(e)
            else:
                try:
                    companies.update(**company)
                    message[0] += 'Update: {name}<br>'.format(**company)
                except Exception as e:
                    message[0] += 'Exception (Update): {name}<br>'.format(**company)
                    message[0] += str(e)

    @staticmethod
    @background(queue='gelbeseiten_queue')
    def scrape(category, location):
        message = ['======= Start =======<br>']
        soup, urls = Entry.generate_urls(category, location, message)
        data = Entry.fetch_data(soup, message, category=category, location=location)
        Entry.save_companies(data, message)
        for url in urls:
            soup = Entry.fetch_soup(url, message)
            data = Entry.fetch_data(soup, message, category=category, location=location)
            Entry.save_companies(data, message)
        message[0] += '======== End ========'
        name = '{} - {} - {}'.format(location, category, timezone.localtime().strftime('%d.%m.%Y %H:%M'))
        message = message[0]
        run = Fetch(name=name, message=message)
        run.save()

    @staticmethod
    def to_csv(category, location):
        clubs = Entry.objects.filter(category=category, location=location)
        df = pd.DataFrame(list(clubs.values(
            'name', 'email', 'phone', 'website', 'address', 'zipcode', 'city', 'category', 'location'))
        )
        file_name_short = 'gelbeseiten/{}-{}-{}.csv'.format(
            timezone.localtime().strftime('%Y%m%d%H%M'),
            category,
            location)
        file_name = os.path.join(settings.MEDIA_ROOT, file_name_short)
        df.to_csv(file_name, index=False)
        name = "{}-{}-{}.csv".format(
            category,
            location,
            timezone.localtime().strftime('%Y%m%d%H%M')
        )
        file = File(name=name, file=file_name_short)
        file.save()

    @staticmethod
    def to_xlsx(category, location):
        clubs = Entry.objects.filter(category=category, location=location)
        df = pd.DataFrame(list(clubs.values(
            'name', 'email', 'phone', 'website', 'address', 'zipcode', 'city', 'category', 'location'))
        )
        file_name_short = 'gelbeseiten/{}-{}-{}.xlsx'.format(
            category,
            location,
            timezone.localtime().strftime('%Y%m%d%H%M')
        )
        file_name = os.path.join(settings.MEDIA_ROOT, file_name_short)
        df.to_excel(file_name, index=False)
        name = "{}-{}-{}.xlsx".format(
            category,
            location,
            timezone.localtime().strftime('%Y%m%d%H%M')
        )
        file = File(name=name, file=file_name_short)
        file.save()
