from main import Pokemon
from datetime import datetime
no1 = Pokemon(pid=1,lat=10.001,lng=10.101, report_time =  datetime.now() )
no1.save()


res = Pokemon.query.all()
print res[0].get_name()
print res[0].get_loc()