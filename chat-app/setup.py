import sys
import socket

EXIT_PROMPT = "Press Enter to exit"

version = sys.version[:5]
if version[0] != "3" or int(version[2]) < 7:
    print("Version  of python unsufficient: < 3.7.1. Update to a newer version.")
    input(EXIT_PROMPT)
    exit()
try:
    import websockets
except ImportError:
    print("Websockets not installed: Install by running pip3 install --user websockets")
    input(EXIT_PROMPT)
    exit()

localhost = input("Do you want to serve on localhost (testing only. accessible only from your computer?) (y/N) ")
if localhost.lower().startswith("y"):
    print("Configuring for localhost usage")
    INNER = ""
    OUTER = "localhost"
else:
    print("Configuring for real-life usage")
    INNER = socket.gethostbyname(socket.gethostname())
    web = input("Will you be using this over web or only on the Wi-Fi? (web/wifi) ")
    if web == "web":
        OUTER = input("Enter the public IP: ")
    elif web == "wifi":
        OUTER = INNER
    else:
        print("Not one of the options")
        input(EXIT_PROMPT)
        exit()
print("Saving to config file...", end="")
with open("./config.py", "x") as fp:
    fp.write("INNER_IP=\"%s\"\nOUTER_IP=\"%s\"" % (INNER, OUTER))

input(EXIT_PROMPT)
