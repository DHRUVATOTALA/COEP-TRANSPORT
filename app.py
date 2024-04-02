from flask import Flask,render_template,request
import sqlite3

app=Flask(__name__)
#return the home page
@app.route('/')
def mainpg():
    return render_template('index.html')
@app.route('/home')
def mainpg1():
    return render_template('index.html')
#return about us page
@app.route('/aboutus')
def abtus():
    return render_template('aboutus.html')
#return about us page
@app.route('/contact')
def contactus():
    return render_template('contact.html')
#return main bus page
#connect database
#fetch areas
@app.route('/bus')
def bus():
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute("SELECT DISTINCT Area FROM area")
    items=c.fetchall()
    conn.close()
    return render_template('bus.html',items=items)
#return to next bus page
#fetch selected area from html form
#fetch stop from area
@app.route('/bus',methods=['POST'])
def getval():
    a=request.form['selected1']
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute("SELECT Stop FROM area WHERE Area=(?)",(a,))
    items2=c.fetchall()
    times=["08:00am-10:00am","10:00am-12:00pm","12:00pm-02:00pm","02:00pm-04:00pm","04:00pm-06:00pm"]
    conn.close()
    return render_template('bus1.html',items2=items2,times=times)
#result page
@app.route('/result',methods=['POST'])
def result():
    stop=request.form['selected2']
    t=request.form['selected3']
    tl=request.form['selected4']
    tmin=t[0:2]
    tmax=t[-7:-5]
    tlmin=tl[0:2]
    tlmax=tl[-7:-5]
    t1="07"
    print(tmin<t1)
    if(tmin<t1):
        m=int(tmin)
        m+=12
        tmin=str(m)
    if(tmax<t1):
        m=int(tmax)
        m+=12
        tmax=str(m)
    if(tlmin<t1):
        m=int(tlmin)
        m+=12
        tlmin=str(m)
    if(tlmax<t1):
        m=int(tlmax)
        m+=12
        tlmax=str(m)
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute("SELECT sid FROM area WHERE Stop=(?)",(stop,))
    id=c.fetchall()
    c.execute("SELECT Bid FROM time WHERE Sid=(?)",(id[0][0],))
    bidd=c.fetchall()
    c.execute("SELECT time FROM time WHERE Sid=(?)",(id[0][0],))
    temp=c.fetchall()
    bnam=[]
    for b in bidd:
        c.execute("SELECT bname FROM buses WHERE bid=(?)",(b[0],))
        bnam.append(c.fetchone())
    arr=[]
    arr2=[]
    bnam1=[]
    bidd1=[]
    for b in bnam:
        bnam1.append(b)
    for b in bidd:
        bidd1.append(b)
    f1=0
    f2=0
    c1=0
    c2=0
    for i in temp:
        col=[]
        col1=[]
        j=0
        while(8*j<len(i[0])):
            t=i[0][8*j:8*j+7]
            j+=1
            s=t[0:2]
            t1="07"
            if(s<t1):
                m=int(s)
                m+=12
                s=str(m)
            if (s<tmax and s>=tmin) or t==tmax+":00am" or t==tmax+":00pm":
                f1=1
                if t not in col:
                    col.append(t)
            if (s<tlmax and s>=tlmin) or t==tlmax+":00am" or t==tlmax+":00pm":
                f2=1
                if t not in col1:
                    col1.append(t)
        if col==[]:  
            print("HEREE")
            bidd.pop(c1)
            bnam.pop(c1)
        if col!=[]:
            c1+=1
            arr.append(col)
        if col1==[]:  
            print("HEREE")
            bidd1.pop(c2)
            bnam1.pop(c2)
        if col1!=[]:
            c2+=1
            arr2.append(col1)
            
    print(arr2,c2,bidd1,bnam1)
    t=arr
    data1=[]
    print(bnam1,bidd1)
    if(f1>0):
        for i in range(c1):
            col=[]
            col.append(bnam[i][0])
            col.append(bidd[i][0])
            col.append(t[i])
            data1.append(col)
    else:
        data1=[["NO BUSES"],["NO BUSES"],["NO BUSES"]]
    data2=[]
    if(f2>0):
        for i in range(c2):
            col=[]
            col.append(bnam1[i][0])
            col.append(bidd1[i][0])
            col.append(arr2[i])
            data2.append(col)
    else:
        data2=[["NO BUSES"],["NO BUSES"],["NO BUSES"]]

    return render_template('result.html',data1=data1,data2=data2,stop=stop)
@app.route('/cpool')
def cpool():
    time_ranges = [
        "08:00am-09:00am",
        "09:00am-10:00am",
        "10:00am-11:00am",
        "11:00am-12:00pm",
        "12:00pm-01:00pm",
        "01:00pm-02:00pm",
        "02:00pm-03:00pm",
        "03:00pm-04:00pm",
        "04:00pm-05:00pm",
        "05:00pm-06:00pm"
    ]
    return render_template('carpool.html',time=time_ranges)
@app.route('/cresult',methods=['POST'])
def cresult():
    area=request.form['area']
    arrival=request.form['arrive']
    depart=request.form['depart']
    area=area.upper()
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute("SELECT t1 from cpool WHERE area=(?) AND t1=(?)",(area,arrival,))
    t1=c.fetchall()
    c.execute("SELECT t2 from cpool WHERE area=(?) AND t2=(?)",(area,depart))
    t2=c.fetchall()
    f=0
    print(t1)
    print(t2)
    if t1==[] and t2==[]:
        return render_template('cresult.html',f=-1)
    data1=[]
    c.execute("SELECT name,contact FROM cpool WHERE area=(?) AND t1=(?)",(area,arrival,))
    data1=c.fetchall()
    print(data1)
    c.execute("SELECT name,contact FROM cpool WHERE area=(?) AND t2=(?)",(area,depart,))
    data2=c.fetchall()
    print(data2)
    conn.close()

    return render_template('cresult.html',data1=data1,data2=data2,area=area)
@app.route('/cresult1',methods=['POST'])
def adddata():
    info=[]
    name=request.form['name']
    area=request.form['area']
    arrival=request.form['t1']
    depart=request.form['t2']
    phno=request.form['phno']
    area=area.upper()
    name=name.upper()
    phno=int(phno)
    info.append(name)
    info.append(arrival)
    info.append(depart)
    info.append(area)
    info.append(phno)
    info=tuple(info)
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute("SELECT * FROM cpool")
    data=c.fetchall()
    if info not in data:
        c.execute("INSERT INTO cpool(name,area,t1,t2,contact) VALUES(?,?,?,?,?)",(name,area,arrival,depart,phno,))
        conn.commit()
    conn.close()
    return render_template('data.html',info=info)

@app.route('/train')
def metro():
    conn = sqlite3.connect('db1.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT station FROM metro")
    items = c.fetchall()
    conn.close()
    return render_template('train.html', items = items)

@app.route('/train', methods=['POST'])
def getval1():
    selected_station = request.form['st']
    conn = sqlite3.connect('db1.db')
    c = conn.cursor()
    c.execute("SELECT id FROM metro WHERE station = (?)", (selected_station[2:len(selected_station)-3],))
    station_id = c.fetchone()
    print(selected_station)
    print(station_id)
    c.execute("SELECT DISTINCT range FROM table2 WHERE metro_id = (?)", (station_id[0],))
    range= c.fetchall()
    c.execute("SELECT DISTINCT range1 FROM table3 WHERE metro_id1=?", (station_id[0],))
    range1 = c.fetchall()
    print(range)
    print(range1)
    conn.close()
    return render_template('train2.html', station=station_id, range=range, range1=range1)

@app.route('/resulttrain', methods=['POST'])
def result1():
    range = request.form['t']
    range1 = request.form['t2']

    conn = sqlite3.connect('db1.db')
    c = conn.cursor()
    print(range)
    c.execute("SELECT metro_id FROM table2 WHERE range=?", (range,))
    id = c.fetchall()
    print(id)
    c.execute("SELECT line FROM table2 WHERE metro_id=?", (id[0][0],))
    line = c.fetchall()
    c.execute("SELECT station FROM metro WHERE id=?", (id[0][0],))
    station = c.fetchall()
    c.execute("SELECT DISTINCT fare FROM table2 WHERE metro_id=?", (id[0][0],))
    fare = c.fetchone()

#edit
    c.execute("SELECT DISTINCT id FROM table2 WHERE range=?", (range,))
    idd=c.fetchall()
    print(idd)  
#edit end
    c.execute("SELECT DISTINCT timing FROM table2 WHERE id=?", (idd[0][0],))
    timing = c.fetchone()

#for departure
    c.execute("SELECT metro_id1 FROM table3 WHERE range1!=?", (range1,))
    id1=c.fetchall()
    print(id1)
    c.execute("SELECT DISTINCT station FROM metro WHERE id=?", (id1[0][0],))
    selected_station1=c.fetchall()
    print(selected_station1)    
    c.execute("SELECT DISTINCT line1 FROM table3 WHERE metro_id1=?", (id1[0][0],))
    line1 = c.fetchall()
    c.execute("SELECT DISTINCT fare1 FROM table3 WHERE metro_id1=?", (id1[0][0],))
    fare1 = c.fetchall()
    c.execute("SELECT DISTINCT id1 FROM table3 WHERE range1=?", (range1,))
    id2=c.fetchall()    
    c.execute("SELECT timing1 FROM table3 WHERE id1=?", (id2[0][0],))
    timing1=c.fetchall()

    return render_template('trainresult.html',  station= station[0][0], line = line, timing = timing[0], fare = fare[0], line1=line1[0][0],fare1=fare1[0][0], timing1=timing1[0][0])

if __name__=='__main__':
    app.run(debug=True)
