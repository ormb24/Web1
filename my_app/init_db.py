from my_app import db
from my_app.models import User, Riddle, Clue, Category

db.drop_all()
db.create_all()
db.session.commit()

user1 = User(email='olivier.biard@student.unamur.be',username='obiard',password='ihdcb336',firstname='Olivier',lastname='Biard')
user1.admin=True
user1.set_password('ihdcb336')
user2 = User(email='john.smith@student.unamur.be',username='jsmith',password='12345678',firstname='John',lastname='Smith')
user2.set_password('12345678')

riddle1 = Riddle(riddle="MyRiddle01",answer="MyAnswer01",level=2,user=user1)
riddle2 = Riddle(riddle="MyRiddle02",answer="MyAnswer02",level=3,user=user1)
riddle3 = Riddle(riddle="MyRiddle03",answer="MyAnswer03",level=5,user=user1)
riddle4 = Riddle(riddle="MyRiddle04",answer="MyAnswer04",level=1,user=user1)
riddle5 = Riddle(riddle="MyRiddle05",answer="MyAnswer05",level=7,user=user1)
riddle6 = Riddle(riddle="MyRiddle06",answer="MyAnswer06",level=9,user=user1)
riddle7 = Riddle(riddle="MyRiddle07",answer="MyAnswer07",level=1,user=user1)
riddle8 = Riddle(riddle="MyRiddle08",answer="MyAnswer08",level=3,user=user1)
riddle9 = Riddle(riddle="MyRiddle09",answer="MyAnswer09",level=3,user=user1)
riddle10 = Riddle(riddle="JSRiddle10",answer="JSAnswer10",level=4,user=user2)
riddle11 = Riddle(riddle="JSRiddle11",answer="JSAnswer11",level=1,user=user2)
riddle12 = Riddle(riddle="JSRiddle12",answer="JSAnswer12",level=5,user=user2)
riddle13 = Riddle(riddle="JSRiddle13",answer="JSAnswer13",level=8,user=user2)
riddle14 = Riddle(riddle="JSRiddle14",answer="JSAnswer14",level=2,user=user2)

#clue1=Clue(clue="MyClue01",riddle_id=riddle1.id)

clue1=Clue(clue="MyClue01",riddle=riddle1)
clue1a=Clue(clue="MyClue01a",riddle=riddle1)
clue1b=Clue(clue="MyClue01b",riddle=riddle1)
clue1c=Clue(clue="MyClue01c",riddle=riddle1)
clue2=Clue(clue="MyClue02",riddle=riddle2)
clue3=Clue(clue="MyClue03",riddle=riddle3)
clue4=Clue(clue="MyClue04",riddle=riddle4)
clue5=Clue(clue="MyClue05",riddle=riddle5)

category1=Category(name="Devinette")
category2=Category(name="Mathématiques")
category3=Category(name="Logique")
category4=Category(name="Connaissances")
category5=Category(name="Animaux")

db.session.add_all([user1,user2])
db.session.add_all([riddle1, riddle2, riddle3, riddle4, riddle5, riddle6, riddle7, riddle8, riddle9, riddle10, riddle11, riddle12, riddle13, riddle14])
db.session.add_all([clue1, clue2, clue3, clue4, clue5, clue1a, clue1b, clue1c])
db.session.add_all([category1,category2,category3,category4,category5])

db.session.commit()