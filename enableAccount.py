from datetime import datetime
from Account import Account

i = 0 
while 1:
    account = Account.query.filter(Account.isUsed != 0).first()
    if account == None:
        break
    account.reset()
    account.save()
    username, password, auth = account.getInfo()
    i += 1
    print "Reset Account: " + username +" " + password + " " + auth

print "Total Reset:" + str(i) + " accounts"


