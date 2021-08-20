import os
import string
import time
import zipfile

from selenium import webdriver
import random
from selenium.webdriver.common.proxy import Proxy, ProxyType

msg = "WoW That is excellent!"
account = "moin"


def random_string(string_length=13):
    # Generate a random string of letters and digits
    letters_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_digits) for i in range(string_length))

p1 = "ip:port@username:password"
use_proxy = False        #change to "False" to turn off proxy
proxy = p1      #choose proxy from above (Ex: "proxy = p30")

if use_proxy:
    ip = proxy.split(':')[0]
    port = int(proxy.split(':')[1])
    login = proxy.split(':')[2]
    password = proxy.split(':')[3]

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (ip, port, login, password)

def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath("C:\\chromedriver.exe"))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
        chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(
        os.path.join(path, 'chromedriver'),
        chrome_options=chrome_options)
    return driver


driver = get_chromedriver(use_proxy)
url = "https://www.instagram.com/"
driver.get(url)

email = random_string(7)
email += "@protonmail.com"
name = random_string(13)
username = random_string(8)
password = random_string(9)

time.sleep(1)

email_xpath = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input")
email_xpath.send_keys(email)

name_xpath = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/div/label/input")
name_xpath.send_keys(name)

username_xpath = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[5]/div/label/input")
username_xpath.send_keys(username)

password_xpath = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[6]/div/label/input")
password_xpath.send_keys(password)

# login - - click search - type user - click user - click most recent post -
driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[7]/div/button").click()
# time.sleep(1)
# driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div/div[2]/div").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div").click()
driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input").send_keys(account)
time.sleep(2)
driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]").click()

# click first post via x and y coordinates refrenced from middle div
action = webdriver.common.action_chains.ActionChains(driver)
el = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[2]")
action.move_to_element_with_offset(el, 170, 300)
action.click()
action.perform()
time.sleep(1)

# click comment button
driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[2]/button").click()
driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea").send_keys(msg)
driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/button").click()
