import sqlite3
conn=sqlite3.connect('database.db')
c=conn.cursor()
name="ishita"
area="vimannagar"
arrival="9"
depart="10"
phno=1234567
c.execute("INSERT INTO cpool (name,t1,t2,area,contact) VALUES(?,?,?,?,?)",(name,arrival,depart,area,phno))
conn.commit()
# c.execute("CREATE TABLE cpool(name TEXT,Vehicle TEXT,t1 TEXT,t2 TEXT,area TEXT)")
# c.execute("CREATE TABLE buses(bname TEXT,bid INTEGER,PRIMARY KEY(bid))")
# c.execute("CREATE TABLE time(Sid INTEGER REFERENCES area('sid'),Bid INTEGER REFERENCES buses('bid'),time TEXT)")
# stop='Baner-Phata'
# c.execute("SELECT sid FROM area WHERE Stop=(?)",(stop,))
# id=c.fetchall()
# c.execute("SELECT Bid FROM time WHERE Sid=(?) AND time=(?)",(id[0][0],'9:00'))
# bidd=c.fetchall()
# print(bidd)
# for i in bidd:
#     print(i)