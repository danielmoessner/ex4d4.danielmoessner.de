from django.utils import timezone
from django.db import models

from django.conf import settings
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import re

import math
from background_task import background


class BtvClub(models.Model):
    name = models.CharField(max_length=200)
    number = models.PositiveIntegerField()
    address = models.CharField(max_length=1000, null=True, blank=True)
    email = models.EmailField()
    members = models.SmallIntegerField(null=True, blank=True)
    adult_members = models.SmallIntegerField(null=True, blank=True)
    youth_members = models.SmallIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    outside_courts = models.SmallIntegerField(null=True, blank=True)
    indoor_courts = models.SmallIntegerField(null=True, blank=True)
    competition_courts = models.SmallIntegerField(null=True, blank=True)
    url = models.CharField(max_length=300)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return '{} - {}'.format(self.number, self.name)

    @staticmethod
    def get_html_text(url, message):
        site = urlopen(url)
        message[0] += 'Open: {}<br>'.format(url)
        html = site.read()
        time.sleep(2)
        site.close()
        return html

    @staticmethod
    def get_search_urls(start, end, message):
        url = 'https://www.btv.de/de/mein-verein/vereinssuche.html?search={}'
        urls = []
        for i in range(start, end + 1):
            number = str(i).zfill(5)
            urls.append(url.format(number))
        return urls

    @staticmethod
    def get_club_urls(url, message):
        html = BtvClub.get_html_text(url, message)
        soup = BeautifulSoup(html, 'lxml')
        links = soup.find_all("a", {'class': 'article__header-link'})
        urls = []
        for link in links:
            url = 'https://www.btv.de{}'
            url = url.format(link['href'])
            urls.append(url)
        if len(links) == 0:
            message[0] += 'Found nothing: {}<br>'.format(url)
        return urls

    @staticmethod
    def find_number(soup):
        try:
            number = soup.find('div', {'class': 'c-rte--icon-tile'})
            number = number.find_all('p')[-1].get_text()
            number = number[-5:]
            number = int(number)
        except Exception as e:
            number = 00000
        return number

    @staticmethod
    def find_name(soup):
        try:
            name = soup.find('h2', {'class': 'text__headline'}).get_text()
        except Exception as e:
            name = 'None'
        return name

    @staticmethod
    def find_address(soup):
        try:
            soup2 = soup.find_all('div', {'class': 'c-rte--icon-tile'})
            soup3 = soup2[1].find_all('p')
            address = '{} {}'.format(soup3[0].get_text(), soup3[1].get_text())
        except Exception as e:
            address = 'None'
        return address

    @staticmethod
    def find_email(soup):
        try:
            soup2 = soup.find_all('div', {'class': 'c-rte--icon-tile'})
            soup3 = soup2[1].find_all('p')
            email = soup3[-1].get_text()
            email = email.replace('E-Mail: ', '')
        except Exception as e:
            email = 'None'
        return email

    @staticmethod
    def find_members(soup):
        try:
            soup2 = soup.find_all('div', {'class': 'c-rte--icon-tile'})
            soup3 = soup2[3].find_all('p')
            members = soup3[0].get_text()
            members = members.replace('Insgesamt: ', '')
            members = members.replace('.', '')
            members = members.replace(',', '')
            members = int(float(members))
        except Exception as e:
            members = -1
        return members

    @staticmethod
    def find_adult_members(soup):
        try:
            soup2 = soup.find_all('div', {'class': 'c-rte--icon-tile'})
            soup3 = soup2[3].find_all('p')
            members = soup3[2].get_text()
            members = members.replace('Erwachsene: ', '')
            members = members.replace('.', '')
            members = members.replace(',', '')
            members = int(float(members))
        except Exception as e:
            members = -1
        return members

    @staticmethod
    def find_youth_members(soup):
        try:
            soup2 = soup.find_all('div', {'class': 'c-rte--icon-tile'})
            soup3 = soup2[3].find_all('p')
            members = soup3[1].get_text()
            members = members.replace('Jugendliche: ', '')
            members = members.replace('.', '')
            members = members.replace(',', '')
            members = int(float(members))
        except Exception as e:
            members = -1
        return members

    @staticmethod
    def find_outside_courts(soup):
        try:
            soup2 = soup.find_all('div', {'class': 'c-rte--icon-tile'})
            soup3 = soup2[2].find_all('p')
            courts = soup3[0].get_text()
            courts = courts.replace('Freiplätze: ', '')
            courts = courts.replace('.', '')
            courts = courts.replace(',', '')
            courts = int(float(courts))
        except Exception as e:
            courts = -1
        return courts

    @staticmethod
    def find_indoor_courts(soup):
        try:
            soup2 = soup.find_all('div', {'class': 'c-rte--icon-tile'})
            soup3 = soup2[2].find_all('p')
            courts = soup3[1].get_text()
            courts = courts.replace('Hallenplätze: ', '')
            courts = courts.replace('.', '')
            courts = courts.replace(',', '')
            courts = int(float(courts))
        except Exception as e:
            courts = -1
        return courts

    @staticmethod
    def find_competition_courts(soup):
        try:
            soup2 = soup.find_all('div', {'class': 'c-rte--icon-tile'})
            soup3 = soup2[2].find_all('p')
            courts = soup3[2].get_text()
            courts = courts.replace('Wettspielplätze: ', '')
            courts = courts.replace('.', '')
            courts = courts.replace(',', '')
            courts = int(float(courts))
        except Exception as e:
            courts = -1
        return courts

    @staticmethod
    def find_phone(soup):
        return ''

    @staticmethod
    def get_club_data(url, message):
        html = BtvClub.get_html_text(url, message)
        soup = BeautifulSoup(html, 'lxml')
        name = BtvClub.find_name(soup)
        number = BtvClub.find_number(soup)
        email = BtvClub.find_email(soup)
        address = BtvClub.find_address(soup)
        members = BtvClub.find_members(soup)
        adult_members = BtvClub.find_adult_members(soup)
        youth_members = BtvClub.find_youth_members(soup)
        outside_courts = BtvClub.find_outside_courts(soup)
        indoor_courts = BtvClub.find_indoor_courts(soup)
        competition_courts = BtvClub.find_competition_courts(soup)
        phone = BtvClub.find_phone(soup)

        return {
            'name': name,
            'number': number,
            'address': address,
            'email': email,
            'members': members,
            'adult_members': adult_members,
            'youth_members': youth_members,
            'outside_courts': outside_courts,
            'indoor_courts': indoor_courts,
            'competition_courts': competition_courts,
            'phone': phone,
            'url': url
        }

    @staticmethod
    def save_club(data, message):
        clubs = BtvClub.objects.filter(number=data['number'])
        if not clubs.exists():
            club = BtvClub(**data)
            try:
                club.save()
                message[0] += 'Save: {number} - {name}<br>'.format(**data)
            except Exception as e:
                message[0] += 'Exception (Save): {number} - {name}<br>'.format(**data)
                message[0] += str(e)
        else:
            try:
                clubs.update(**data)
                message[0] += 'Update: {number} - {name}<br>'.format(**data)
            except Exception as e:
                message[0] += 'Exception (Update): {number} - {name}<br>'.format(**data)
                message[0] += str(e)

    @staticmethod
    @background(queue='scrape_queue')
    def scrape(start, end):
        message = ['======= Start =======<br>']
        search_urls = BtvClub.get_search_urls(start, end, message)
        club_urls = []
        for url in search_urls:
            club_urls += BtvClub.get_club_urls(url, message)
        for url in club_urls:
            data = BtvClub.get_club_data(url, message)
            BtvClub.save_club(data, message)
        message[0] += '======== End ========'
        name = '{} - {} - {}'.format(start, end, timezone.localtime().strftime('%d.%m.%Y %H:%M'))
        message = message[0]
        run = ScrapeRun(name=name, message=message)
        run.save()

    @staticmethod
    def to_csv(start, end):
        numbers = []
        for i in range(start, end + 2):
            number = str(i).zfill(5)
            numbers.append(number)
        clubs = BtvClub.objects.filter(number__in=numbers)
        df = pd.DataFrame(list(clubs.values('number', 'name', 'email', 'address', 'members', 'adult_members',
                                            'youth_members', 'outside_courts', 'indoor_courts', 'competition_courts',
                                            'url')))
        df.loc[:, "number"] = df.loc[:, "number"].astype(str)
        df.loc[:, "number"] = df.loc[:, "number"].apply(lambda s: s.zfill(5))
        file_name_short = 'fpioli/{}-{}-{}.csv'.format(
            timezone.localtime().strftime('%Y%m%d%H%M'),
            str(start).zfill(5),
            str(end).zfill(5))
        file_name = os.path.join(settings.MEDIA_ROOT, file_name_short)
        df.to_csv(file_name, index=False)
        name = "{}-{}.csv".format(str(start).zfill(5), str(end).zfill(5))
        btv_file = ScrapeFile(name=name, file=file_name_short, tool='BTV')
        btv_file.save()

    @staticmethod
    def to_xlsx(start, end):
        numbers = []
        for i in range(start, end + 2):
            number = str(i).zfill(5)
            numbers.append(number)
        clubs = BtvClub.objects.filter(number__in=numbers)
        df = pd.DataFrame(list(clubs.values('number', 'name', 'email', 'address', 'members', 'adult_members',
                                            'youth_members', 'outside_courts', 'indoor_courts', 'competition_courts',
                                            'url')))
        df.loc[:, "number"] = df.loc[:, "number"].astype(str)
        df.loc[:, "number"] = df.loc[:, "number"].apply(lambda s: s.zfill(5))
        file_name_short = 'fpioli/{}-{}-{}.xlsx'.format(
            timezone.localtime().strftime('%Y%m%d%H%M'),
            str(start).zfill(5),
            str(end).zfill(5))
        file_name = os.path.join(settings.MEDIA_ROOT, file_name_short)
        df.to_excel(file_name, index=False)
        name = "{}-{}.xlsx".format(str(start).zfill(5), str(end).zfill(5))
        btv_file = ScrapeFile(name=name, file=file_name_short, tool='BTV')
        btv_file.save()


class ScrapeFile(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='media/fpioli')
    created_at = models.DateTimeField(auto_now_add=True)
    tool_choices = [('BTV', 'BTV Tool'), ('GS', 'Gelbe Seiten Tool')]
    tool = models.CharField(choices=tool_choices, max_length=20)

    def __str__(self):
        return self.name


class ScrapeRun(models.Model):
    name = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tool_choices = [('BTV', 'BTV Tool'), ('GS', 'Gelbe Seiten Tool')]
    tool = models.CharField(choices=tool_choices, max_length=20)

    def __str__(self):
        return self.name


class GelbeSeitenCompany(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    website = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    address = models.CharField(max_length=200)

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
        html = GelbeSeitenCompany.get_html_text(first_url, message)
        html = BeautifulSoup(html, 'lxml')
        amount_of_companies = GelbeSeitenCompany.find_amount_of_companies(html, message)
        pages = math.ceil(amount_of_companies / 50)
        for i in range(2, pages+1):
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
        html = GelbeSeitenCompany.get_html_text(url, message)
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
        except:
            address = ''
        return address

    @staticmethod
    def fetch_data(soup, message, category='category', location='location'):
        data = []
        clusters = GelbeSeitenCompany.find_all_data_clusters(soup)
        for cluster in clusters:
            name = GelbeSeitenCompany.find_name(cluster)
            email = GelbeSeitenCompany.find_email(cluster)
            phone = GelbeSeitenCompany.find_phone(cluster)
            address = GelbeSeitenCompany.find_address(cluster)
            website = GelbeSeitenCompany.find_website(cluster)
            company_data = {'name': name, 'email': email, 'phone': phone, 'address': address, 'website': website,
                            'category': category, 'location': location}
            data.append(company_data)
        return data

    @staticmethod
    def save_companies(data, message):
        for company in data:
            companies = GelbeSeitenCompany.objects.filter(name=company['name'])
            if not companies.exists():
                gsc = GelbeSeitenCompany(**company)
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
        soup, urls = GelbeSeitenCompany.generate_urls(category, location, message)
        data = GelbeSeitenCompany.fetch_data(soup, message, category=category, location=location)
        GelbeSeitenCompany.save_companies(data, message)
        for url in urls:
            soup = GelbeSeitenCompany.fetch_soup(url, message)
            data = GelbeSeitenCompany.fetch_data(soup, message, category=category, location=location)
            GelbeSeitenCompany.save_companies(data, message)
        message[0] += '======== End ========'
        name = '{} - {} - {}'.format(location, category, timezone.localtime().strftime('%d.%m.%Y %H:%M'))
        message = message[0]
        run = ScrapeRun(name=name, message=message, tool='GS')
        run.save()

    @staticmethod
    def to_csv(category, location):
        clubs = GelbeSeitenCompany.objects.filter(category=category, location=location)
        df = pd.DataFrame(list(clubs.values('name', 'email', 'phone', 'website', 'address', 'category', 'location')))
        file_name_short = 'fpioli/{}-{}-{}.csv'.format(
            timezone.localtime().strftime('%Y%m%d%H%M'),
            category,
            location)
        file_name = os.path.join(settings.MEDIA_ROOT, file_name_short)
        df.to_csv(file_name, index=False)
        name = "{}-{}.csv".format(category, location)
        file = ScrapeFile(name=name, file=file_name_short, tool='GS')
        file.save()

    @staticmethod
    def to_xlsx(category, location):
        clubs = GelbeSeitenCompany.objects.filter(category=category, location=location)
        df = pd.DataFrame(list(clubs.values('name', 'email', 'phone', 'website', 'address', 'category', 'location')))
        file_name_short = 'fpioli/{}-{}-{}.xlsx'.format(
            timezone.localtime().strftime('%Y%m%d%H%M'),
            category,
            location)
        file_name = os.path.join(settings.MEDIA_ROOT, file_name_short)
        df.to_excel(file_name, index=False)
        name = "{}-{}.xlsx".format(category, location)
        file = ScrapeFile(name=name, file=file_name_short, tool='GS')
        file.save()
