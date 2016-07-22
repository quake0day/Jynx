from Pokemon import Pokemon
from datetime import datetime
from Location import Location
from Account import Account
#no1 = Pokemon(pid=1,lat=10.001,lng=10.101, encounter_id="123123" ,report_time =  datetime.now() )
#no1.save()

no1 = Account(username = 'zzzlog', password = '@Lara4cs', auth='ptc')
no1.save()
no3 = Account(username = 'zzzlog1', password = '@Lara4cs', auth='ptc')
no3.save()
no4 = Account(username = 'zzzlog2', password = '@Lara4cs', auth='ptc')
no4.save()
no5 = Account(username = 'quakezeroday@gmail.com', password = '@Lara4cs', auth='google')
no5.save()
no2 = Location(lat = 43.00046, lng = -78.78305)
no2.save()
no5 = Location(lat = 42.99981, lng = -78.78648)
no5.save()

no6 = Location(lat = 43.00027 , lng = -78.78966)
no6.save()

no7 = Location(lat = 43.00758 , lng = -78.78527)
no7.save()
    
res = Location.query.all()
print res[0].getLocation()
print res[0].getOn()
res = Account.query.all()
print res[0].getInfo()
print res[0].getUsed()
#res = Pokemon.query.all()
#print res[0].get_name()
#print res[0].get_loc()