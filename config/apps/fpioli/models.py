from django.utils import timezone
from django.db import models

from django.conf import settings
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

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
