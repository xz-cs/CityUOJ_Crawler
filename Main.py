# CityUOJ Crawler (Python 3)
# Designed and programmed by Xun Zhang
# 27 Nov. 2020

import requests
from bs4 import BeautifulSoup as bs
from getpass import getpass

def submit(id, path):
    url = 'http://acm.cs.cityu.edu.hk/oj2/index.php/submit/' + id
    fl = open(path, 'rb')
    files = {'submission[source_code_file]': (id + '.cpp', fl, 'application/octet-stream', {'Expires': '0'})}

    r = s.get(url, headers = headersR)
    soup = bs(r.content, features="html.parser")
    once = soup.find('input', {'name' : 'submission[_csrf_token]'})['value']   # get token

    data = {
        "submission[_csrf_token]" : once,
        "submission[problem_id]:" : id,
        "submission[compiler]:" : 'c++11'
    }
    res = s.post(url, data, files = files, headers = headersR, allow_redirects = True)
    # for i in res.history:
    #     print(i.url)
    #     print(i.headers)
    #     print()
    # print(res.url)
    # print(res.headers)
    if (len(res.history) <= 0):
        print("\nSomething went wrong.\n")
    else:
        print("\nSuccessfully submitted!\n")
    

def lookup(id):
    url = 'http://acm.cs.cityu.edu.hk/oj2/index.php/p/' + id
    r = s.get(url, headers = headersR)
    soup = bs(r.content, features="html.parser")
    title = str(soup.find('h2')).split('</span>')
    print( "\n ======  " + id + " : " + title[2].split("</h2>")[0].strip() + "  ======")
    if 'To be solved' in title[0]:
        print("You haven't solved this problem yet.\n")
    else:
        print("You have already solved this problem.\n")

    tags = str(soup.find('ul', {'class' : 'horizontal-list problem-tag-list'})).split('<li>')
    if tags[0] != 'None':
        print("  **Tags**  ")
        for xi in tags:
            if "href" in xi:
                print("* " + xi.split(">")[1].split("<")[0])

    user = str(soup.find('a', {'class' : 'icon-user'}))
    if user != 'None':
        best = user.split('>')[1].split("</a")[0].strip()
        print("\nBest submission is by " + best + " .\n")
    else:
        print("\nNo one solved this problem.\n")
    

def download(id):
    url = "http://acm.cs.cityu.edu.hk/oj2/index.php/pget/" + id
    r = requests.get(url, headers = headersR)
    fd = open(id + '.pdf', 'wb')
    fd.write(r.content)
    fd.close()
    print("\nSuccessfully downloaded!\n")

def isSolved(id):
    url = 'http://acm.cs.cityu.edu.hk/oj2/index.php/p/' + id
    r = s.get(url, headers = headersR)
    soup = bs(r.content, features="html.parser")
    title = str(soup.find('h2')).split('</span>')
    return not('To be solved' in title[0])

def check(course):
    lists = {
        "3334" : ['78', '142', '372', '737', '738', '739', '740', '741', '742', '743', '744', '745',
                '746', '747', '748', '749', '750', '751', '752', '753', '754', '755', '756', '757', '758' ]
    }
    if (not(course in lists)):
        print("\nUnknown course.\n")
    else:
        print()
        count = 0
        for id in lists[course]:
            if (isSolved(id)):
                print("✅ "+ id)
            else:
                print("⭕ "+ id)
                count += 1
        print("\nYou have " + str(count) + " unsolved question(s) for CS" + course + " assignment.\n")

def getLast():
    url = "http://acm.cs.cityu.edu.hk/oj2/index.php/profile/getSubmissionHistory"
    r = requests.get(url, headers = headersR)
    html = r.content
    soup = bs(html, features="html.parser")
    tds = soup.find("tbody").find("tr").find_all("td")
    print("\n    ==== Your Last Submission ====    ")
    print("{:<18}".format("ID:"), end="")
    print(str(tds[0]).split("</a>")[0].split(">")[2])
    print("{:<18}".format("Problem:"), end="")
    print(str(tds[1]).split("</a>")[0].split(">")[2], end=" ")
    print(str(tds[2]).split("</a>")[0].split(">")[2])
    print("{:<18}".format("Verdict:"), end="")
    print(str(tds[3]).split("</td>")[0].split(">")[1])
    print("{:<18}".format("Run Time:"), end="")
    print(str(tds[4]).split("</td>")[0].split(">")[1], end=" sec.\n")
    print("{:<18}".format("Memory:"), end="")
    print(str(tds[5]).split("</td>")[0].split(">")[1], end=" KB\n")
    print("{:<18}".format("Submission Time:"), end="")
    print(str(tds[6]).split("</td>")[0].split(">")[1])
    print()
    



print("\n   === Welcome to CityUOJ Crawler ===   ")
url = 'http://acm.cs.cityu.edu.hk/oj2/index.php/account/login'

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'


headers = {
        "User-Agent" : user_agent,
        "Referer": "http://acm.cs.cityu.edu.hk/oj2/index.php/account/login",
        'Origin': 'http://acm.cs.cityu.edu.hk',
        'Host': 'acm.cs.cityu.edu.hk'
}

s = requests.Session()

r = s.get(url, headers = headers)
soup = bs(r.content, features="html.parser")
once = soup.find('input', {'name' : 'logon[_csrf_token]'})['value']   # get token
#print(once)

data = {'logon[contact]': input("\nEID/Username/Email: "),
        'logon[password]': getpass(),
        'logon[return_url]': 'http://acm.cs.cityu.edu.hk/oj2/index.php/profile',
        'logon[_csrf_token]': once
        }

#requests.post(url,data).headers)
r = s.post(url,data, headers = headers, allow_redirects = False)   # get cookie
cookie_jar = r.cookies

#print(r.headers)

cookie = requests.utils.dict_from_cookiejar(cookie_jar)
cookie_str = cookie['cs_oj_session']
#print(cookie_str)


newurl = 'http://acm.cs.cityu.edu.hk/oj2/index.php/profile/getSubmissionHistory'

headersR = {
    'User-Agent': user_agent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    "Referer": "http://acm.cs.cityu.edu.hk/oj2/index.php/account/login",
    'Origin': 'http://acm.cs.cityu.edu.hk',
    'Host': 'acm.cs.cityu.edu.hk',
    'Cookie': 'cs_oj_session=' + cookie_str
}

print("\nLogin Success!\n")

r = s.get(newurl, headers = headersR)
soup = bs(r.content, features="html.parser")
res = str(soup.find('a', {'href' : "/oj2/index.php/profile"})).split("</a>")[0].split("\">")[1]
print("Welcome, " + res + " !\n")

string = ''
while (True):
    string = input(">>> ").split()
    if (string[0] == 'help'):
        print("\n   === Help for CityUOJ Crawler ===   \n")
        print("1. >>> submit [Problem ID] [Path to Source Code]\n   (Submit your code to the server for judging.)\n")
        print("2. >>> getLast\n   (View the details of your last submission.)\n")
        print("3. >>> lookup [Problem ID]\n   (View the details of a problem.)\n")
        print("4. >>> download [Problem ID]\n   (Download the statement of a problem.)\n")
        print("5. >>> check [Course Number]\n   (View your completion of the assignment of a course.)\n")
        print("6. >>> bye  OR  >>> exit\n   (Exit the program.)\n")
        print("\n   === © 2020 Xun Zhang. All rights reserved. ===   \n")
    elif (string[0] == 'bye' or string[0] == 'exit'):
        print("\nBye bye! Hope to see you again!\n")
        break
    elif (string[0] == 'submit'):
        try:
            submit(string[1], string[2])
        except:
            print("\nSomething went wrong.\n")
    elif (string[0] == 'lookup'):
        try:
            lookup(string[1])
        except:
            print("\nSomething went wrong.\n")
    elif (string[0] == 'download'):
        try:
            download(string[1])
        except:
            print("\nSomething went wrong.\n")
    elif (string[0] == 'check'):
        try:
            check(string[1])
        except:
            print("\nSomething went wrong.\n")
    elif (string[0] == 'getLast'):
        try:
            getLast()
        except:
            print("\nSomething went wrong.\n")
    else:
        print("\nUnknown command. Enter 'help' to view all commands.\n")
