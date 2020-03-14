import tkinter
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import subprocess
import csv
import pymysql
import datetime


def dbimport(a1,a2,a3,a4,a5,a6,a7,a8,a9):
	sql1 = """CREATE TABLE IF NOT EXISTS log4 ( 
	Date_Stamp DATE NOT NULL, 
	IP CHAR(20) NOT NULL, 
	Country CHAR(20),
	Sub_Division TEXT(120),
	City CHAR(20),
	HTTP_Status CHAR(4) NOT NULL, 
	Request_Paramenter TEXT(200),  
	Referrer TEXT(300), 
	User_agent TEXT(500))"""
	cursorInstance = connectionInstance.cursor()
	cursorInstance.execute(sql1)
	sql2 = """INSERT INTO log4 VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % \
	(a1,a2,a3,a4,a5,a6,a7,a8,a9)
	cursorInstance.execute(sql2)
	

def ipfn(a):
	from urllib.request import urlopen
	import json
	s_ip = a
	sb_ip = s_ip
	country1 =''
	sub_div1 =''
	city1 =''
	ctr = 3
	i=0
	for j in s_ip:
		if ctr == 0:
			s_ip = s_ip[:i-1]
		if j ==".":
			ctr = ctr -1
		i = i +1
	
	geoid = ''
	with open('cbs.csv') as f:
		rd = csv.reader(f)
		for row in rd:
			if s_ip == row[0]:
				geoid = row[1] 
				
	y = 0
	for x in geoid:
		if x =='.':
			geoid = geoid[:y]
		y = y+1

	with open('CityLocs.csv', newline = '\n', encoding='utf-8') as f1:
		rd1 = csv.reader(f1)
		for row1 in rd1:
			if geoid == row1[0]:
				country1 = row1[1]
				sub_div1 = row1[2]
				city1 = row1[3]
				

	if country1 =='':
		x = "https://tools.keycdn.com/geo.json?host="+sb_ip
		response = urlopen(x)
		geo = json.load(response)
		x1 = geo['data']
		x2 = x1['geo']
		country1 = (x2["country_name"])
		sub_div1 = (x2["region_name"])
		city1 = (x2["city"])
			
		if str(sub_div1) == 'None':
			sub_div =''
		if str(city1) == 'None':	
			city1 =''

	return country1, sub_div1, city1 #add prev ip check 

#PyMySQL initiation
databaseServerIP = "127.0.0.1"
databaseUsername = "root"
databaseUserPassword = ""
NewDatabaseName = "part2"
connectionInstance = pymysql.connect(host = databaseServerIP, user = databaseUsername, password = databaseUserPassword, db="part2")

filename = ''

def fileimp():
	global filename
	filename = askopenfilename()
	
	with open(filename,"r")as log:
		for line in log:
			s = line
			slice(s)

	msg = messagebox.showinfo("Complete!","Rows Imported to DB!")


def slice(s):
	ip =[]
	hstatus = []
	ref = str()
	UA = str()
	date = str()
	RP = ' '
	country = ''
	sub_div = ''
	city =''
	y = 0
	for x in s:
		if x == ' ':
			ip = s[:y]
			break
		y = y+1
	y = y+5

	for x in s[y:]:
		if x=='[':
			date = s[y+1:y+12]
			break
		y = y+1
	y = y+30
	
	for x in s[y:]:
		if x == '-':
			RP = '-'
			y = y+1
			break
		elif x ==' ':
			for z in s[y+1:]:
				if z !=' ':
					RP = RP+z
				else:
					break
			y = y+1
			break	
			
		elif x == ' ' and s[y-1] =="\"":
				break
		y= y+1

	for x in s[y:]:
		
		if x == '-':
			if s[y-1]==' ':
				hstatus = s[y+2:y+5]
				break
		y = y+1
	y = y+6
	
	for x in s[y:]:
		if x !=' ':
			y = y+1
		else:
			break

	for x in s[y:]:
		if x =="\"":
			y = y+1
			break
		y = y+1

	for x in s[y:]:
		if x!="\"":
			ref = ref+x
		else:
			break
		y =y+1
	y = y+2

	for x in s[y:]:
		if x =="\"":
			y = y+1
			break
		y = y+1
	for x in s[y:]:
		if x!="\"":
			UA = UA+x
		else:
			break
		y =y+1

	
	country,sub_div,city = ipfn(ip)

	ds = datetime.datetime.strptime(date,'%d/%b/%Y')
	dss = ds.strftime('%Y-%m-%d')
	
	#print(dss,ip,country,sub_div,city,hstatus,RP,ref,UA)
	dbimport(dss,ip,country,sub_div,city,hstatus,RP,ref,UA)

def view():
	subprocess.Popen(['C:/WINDOWS/system32/notepad.exe', filename])

def dbnow():
	try : 
		cursorInstance = connectionInstance.cursor()
				
		cursorInstance.execute("SELECT * FROM log4")
		with open("out.csv", "w", newline='\n') as csv_file:
			csv_writer = csv.writer(csv_file)
			csv_writer.writerow([i[0] for i in cursorInstance.description])
			csv_writer.writerows(cursorInstance)
			#subprocess.Popen(['C:/WINDOWS/system32/notepad.exe', "out.csv"])
		
		root = tkinter.Tk(screenName=None, baseName=None, className='_DataBase',)
		root.geometry("2000x500")

		# open file
		tree = ttk.Treeview(root)
		tree = ttk.Treeview(root, columns = ('Date','IP','Country','Sub-Division','City','HTTP Code','Request','Referrer','User Agent'))
		tree.heading('#0', text='Date')
		tree.heading('#1', text='IP')
		tree.heading('#2', text='Country')
		tree.heading('#3', text='Sub-Division')
		tree.heading('#4', text='City')
		tree.heading('#5', text='HTTP Code')
		tree.heading('#6', text='Request')
		tree.heading('#7', text='Referrer')
		tree.heading('#8', text='User Agent')
		treeview = tree
		with open("out.csv", newline = "") as file:
		   reader = csv.reader(file)   
		   c = True
		   for col in reader:
		         if c == True:
		            c = False
		            continue
		         treeview.insert('','end',text = str(col[0]),values =(col[1],col[2],col[3],col[4],col[5],col[6],col[7],col[8]))   
		treeview.place(x =0, y =0)
		root.mainloop()

	except Exception as e:
		print ("Exception occured:{}".format(e))


def generate():
	p = l[0][0]+l[0][1]+l[0][2]+l[0][3]+l[0][4]+l[0][5]+l[0][6]+l[0][7]+l[0][8]
	sql = """SELECT %s FROM log4 where %s='%s'""" % \
	(p,so,sf)
	cursorInstance = connectionInstance.cursor()
	cursorInstance.execute(sql)
	with open("report.csv", "w", newline='\n') as csv_file:
			csv_writer = csv.writer(csv_file)
			csv_writer.writerow([i[0] for i in cursorInstance.description])
			csv_writer.writerows(cursorInstance)
			#subprocess.Popen(['C:/WINDOWS/system32/notepad.exe', "report.csv"])
	
	report_columns  = 0
	report_col_names = ''
	with open("report.csv","r",newline='\n') as csv_count:
		reader = csv.reader(csv_count,delimiter=',')	
		for row in reader:
			report_col_names = row
			break
		report_columns=len(next(reader))
	
	global c
	c =0	
		
	#print('col no. : ',report_columns, '\ncols  :',report_col_names)

	root = tkinter.Tk(screenName=None, baseName=None, className='_Report',)
	root.geometry("1000x500")

	# treeview -- gui table
	tree = ttk.Treeview(root)
	tree = ttk.Treeview(root, columns = report_col_names)
	for i in range(report_columns):
		head = "#"+str(i)
		chead = report_col_names[i]
		tree.heading(head,text=chead)
	
	treeview = tree
	#open file
	with open("report.csv", newline = "") as file:
	   reader = csv.reader(file)   
	   cond = True
	   for col in reader:
	        if cond == True:
	           cond = False
	           continue

	        treeview.insert('','end',text = str(col[0]),values =(col[1:])  ) 
	treeview.place(x =0, y =0)
	root.mainloop() 

l = ['Date_Stamp',',IP',',Country',',Sub_Division',',City',',HTTP_Status',',Request_Paramenter',',Referrer',',User_agent'],[0,0,0,0,0,0,0,0,0]
c = 0
def checklist(x):
	global c
	if x.get() == 0:
		l[0][c] = ''
	c = c+1

#search variables
so =''
sf =''

#Graph variables
sf1 =''
g1 = ''

#date variables
now = datetime.datetime.now()
start_date = ''
end_date = ''


def s_date():
	import sys
	from ttkcalendar import Calendar, get_calendar
	import calendar
	root = tkinter.Tk(screenName=None, baseName=None, className='Select Date',)
	root.geometry("300x300")
   
	ttkcal = Calendar(root,firstweekday=calendar.SUNDAY)
	ttkcal.pack(expand=1, fill='both')
    
	if 'win' not in sys.platform:
		style = ttk.Style()
		style.theme_use('clam')

	def give():
		x = ttkcal.selection 
		g = x.strftime("%d/%b/%Y")
		global start_date
		start_date = g
		
	b1 = ttk.Button(root, text="Return", command= lambda :[give(),root.destroy()]).pack()
	root.mainloop()
  
def e_date():
    import sys
    from ttkcalendar import Calendar, get_calendar
    import calendar
    root = tkinter.Tk(screenName=None, baseName=None, className='Select Date',)
    root.geometry("300x300")
   
    ttkcal = Calendar(root,firstweekday=calendar.SUNDAY)
    ttkcal.pack(expand=1, fill='both')
    
    if 'win' not in sys.platform:
        style = ttk.Style()
        style.theme_use('clam')

    def give2():
	    x = ttkcal.selection 
	    g = x.strftime("%d/%b/%Y")
	    global end_date
	    end_date = g
	    global now
	    now = x
	    #print(start_date)
    
    b1 = ttk.Button(root, text="Return", command=lambda :[give2(),root.destroy()]).pack()
    root.mainloop()

    x = ttkcal.selection 
    g = x.strftime("%d/%b/%Y")
    
def plot():
	import matplotlib.pyplot as plt

	global start_date, end_date, now

	ds = datetime.datetime.strptime(start_date,'%d/%b/%Y')
	dss = ds.strftime('%Y-%m-%d')

	de = datetime.datetime.strptime(end_date,'%d/%b/%Y')
	des = de.strftime('%Y-%m-%d')

	sql1 = """ SELECT COUNT(*) FROM log4
	WHERE Date_Stamp BETWEEN '%s' AND '%s'
	AND %s ='%s'""" % \
	(dss,des,g1,sf1)
	#print(sql1)
	cursorInstance = connectionInstance.cursor()
	cursorInstance.execute(sql1)

	result = cursorInstance.fetchone()
	r1 = result[0]
	#print(r1)

	h = "Hits for "+sf1
	#plt.title(h)
	
	fig,plx = plt.subplots()
	p1 = plx.bar([g1],[r1])

	weeks =[]
	week_val =[]
	ctr = 2
	
	wb = de
	wbs = wb.strftime('%Y-%m-%d')
	
	wb2 = de - datetime.timedelta(days=7)
	wbs2 = wb2.strftime('%Y-%m-%d')
	
	weeks.append("Week 1")
	
	sqlwv = """ SELECT COUNT(*) FROM log4
	WHERE Date_Stamp BETWEEN '%s' AND '%s'
	AND %s ='%s'""" % \
	(wbs2,wb,g1,sf1)
	#print(sqlwv)
	cursorInstance = connectionInstance.cursor()
	cursorInstance.execute(sqlwv)
	resultwv = cursorInstance.fetchone()
	rwv = resultwv[0]
	week_val.append(rwv)#sql query
	#print("1.",wbs,wbs2)
	
	while(wb2>ds):
		
		weeks.append("Week "+str(ctr))
		ctr = ctr+1
		wb = wb - datetime.timedelta(days=7)
		wbs = wb.strftime('%Y-%m-%d')
		wb2 = wb2 - datetime.timedelta(days=7)
		if (wb2<ds):
			wb2 = ds
		
		wbs2 = wb2.strftime('%Y-%m-%d')
		#print(wbs,wbs2)
		sqlwv1 = """ SELECT COUNT(*) FROM log4
		WHERE Date_Stamp BETWEEN '%s' AND '%s'
		AND %s ='%s'""" % \
		(wbs2,wb,g1,sf1)
		#print(sqlwv)
		cursorInstance = connectionInstance.cursor()
		cursorInstance.execute(sqlwv1)
		resultwv1 = cursorInstance.fetchone()
		rwv1 = resultwv1[0]
		week_val.append(rwv1)

	#print(weeks,week_val)

	p2 = plx.bar(weeks,week_val)
	plt.savefig('graph.pdf')
	plt.show()

def pdf():
	from PyPDF2 import PdfFileMerger
	import pdfer
	import os
	
	pdfer.pdfer()

	pdfs = ['report.pdf','graph.pdf']

	merger = PdfFileMerger()
	for pdf in pdfs :
		merger.append(open(pdf,'rb'))

	with open ('result.pdf','wb') as fout:
		merger.write(fout)

	env = os.environ
	fp = "C:/Users/Dell/Desktop/Package/result.pdf"
	subprocess.Popen(fp, shell=True)

def gui():
#GUI	
#Tkinter Initiation
	top = tkinter.Tk(screenName=None, baseName=None, className="_WEB SERVER LOG FILE ANALYSIS", )
	top.geometry("500x550")
	
#top left	
	l1 = Label(top, text = 'LOG FILE ANALYSIS', bg = 'lime')
	l1.place(x =0, y=0)

	b1 = Button(top, text = 'Import File', command = fileimp)
	b1.place(x = 25, y= 50)

	b2 = Button(top, text = 'View imported file', command = view)
	b2.place(x = 25, y = 85)
	
	b3 =Button(top, text = 'Show Database', command = dbnow )
	b3.place(x =25, y=120)

#list-fetch function
	def search_option(x):
		idxs = str(lb.curselection())
		idx = idxs[1]
		global so
		if idx == '0':
			 so = 'IP'
		if idx == '1':
			 so = 'HTTP_Status'
		if idx== '2':
			 so = 'Country'
		if idx=='3':
			 so = 'Referrer'

#listbox
	l8 = Label(top, text = 'Search & Display', bg = 'lightblue')
	l8.place(x= 230, y = 5 )

	l2 = Label(top, text = 'Select search option :')
	l2.place(x=250,y=30)
	lb = Listbox(top,height =4)
	lb.insert(1, 'IP')
	lb.insert(2, 'HTTP Status')
	lb.itemconfigure(1, background='#f0f0ff')
	lb.insert(3, 'Country')
	lb.insert(4, 'Referrer')
	lb.itemconfigure(3, background='#f0f0ff')
	lb.pack()
	lb.place(x = 270, y = 50)
	lb.bind('<<ListboxSelect>>', search_option )
	
#search field
	s = StringVar()
	te = Entry(top, textvariable = s)
	te.place(x =270, y = 150 )
	l4 = Label(top, text = "Search field :")
	l4.place(x=250, y=125)
	
	def fetch():
		global sf
		sf = te.get()
	

#checklist
	l3 = Label(top, text = 'Select Columns to include :')
	l3.place(x=250, y = 175 )

	datec = IntVar(value = 1)
	c1 = Checkbutton(top, text = 'Date Stamp', variable = datec, onvalue = 1, offvalue = 1)
	c1.place(x=250, y=200)
	
	ipc = IntVar(value = 1)
	c2 = Checkbutton(top, text = 'IP Address', variable = ipc, onvalue = 1, offvalue = 0)
	c2.place(x=250, y=220)
	

	countryc = IntVar(value = 1)
	c3 = Checkbutton(top, text = 'Country', variable = countryc, onvalue = 1, offvalue = 0)
	c3.place(x=250, y=240)
	
	subdc = IntVar(value = 1)
	c4 = Checkbutton(top, text = 'Sub Division', variable = subdc, onvalue = 1, offvalue = 0)
	c4.place(x=250, y=260)
		
	cityc = IntVar(value = 1)
	c5 = Checkbutton(top, text = 'City', variable = cityc, onvalue = 1, offvalue = 0)
	c5.place(x=250, y=280)
	
	hsc = IntVar(value = 1)
	c6 = Checkbutton(top, text = 'HTTP Status', variable = hsc, onvalue = 1, offvalue = 0)
	c6.place(x=250, y=300)
	
	rp1c = IntVar(value = 1)
	c7 = Checkbutton(top, text = 'Request parameter', variable = rp1c, onvalue = 1, offvalue = 0)
	c7.place(x=250, y=320)
	
	refc = IntVar(value = 1)
	c8 = Checkbutton(top, text = 'Referrer', variable = refc, onvalue = 1, offvalue = 0)
	c8.place(x=250, y=340)
	
	uac = IntVar(value = 1)
	c9 = Checkbutton(top, text = 'User Agent', variable = uac, onvalue = 1, offvalue = 0)
	c9.place(x=250, y=360)
	
#bottom buttons
	b4 =Button(top, text = 'Generate DB', command =lambda:[checklist(datec),
		checklist(ipc),checklist(countryc),checklist(subdc),checklist(cityc),
		checklist(hsc),checklist(rp1c),checklist(refc),
		checklist(uac),fetch(), generate() ])
	b4.place(x= 300, y= 450)
	b5 = Button(top, text ='Export as PDF',command=pdf)#command - fetch generate and pdf export
	b5.place(x = 180, y = 495)
	
	txt = StringVar()
	def txtb():
		global s_date
		txt = s_date
		l111 = Label(top,text='sfeasb') #show current selected date
		l111.place(x =275,y=410)


	#date selector Report - can't display selected date GAWD HALp
	l11 = Label(top,text='Start Date:')
	l11.place(x =250, y= 390)
	b11 = Button(top, text = "⇘", height =0, width =2, command = lambda :[s_date(),txtb()])
	b11.place(x= 250, y =410 )
	 
	#l111 = Label(top,text=txt) #show current selected date
	#l111.place(x =275,y=410)

	l12 = Label(top,text='End Date:')
	l12.place(x =350, y= 390)
	b12 = Button(top, text = "⇘", height =0, width =2, command = e_date)
	b12.place(x = 350, y =410)
	'''global end_date
	svar2 = end_date
	l121 = Label(top,text=svar2) #show current selected date
	l121.place(x =375,y=410)'''


#optionmenu func
	def func(value):
		global g1
		if value == 'HTTP Code':
			g1 = 'HTTP_Status'
		else:
			g1 = value
#Graphical x-y axis selector

	l7 = Label(top, text = 'Graph', bg = 'lightblue')
	l7.place(x= 15, y = 220)

	l5 = Label(top, text = 'Select Graph Option :')
	l5.place(x= 25, y = 250)
	ovar1 = StringVar()
	o1 = OptionMenu(top, ovar1, 'IP','Country','HTTP Code' , command = func)
	o1.place(x =30, y = 270)
	
	l6 = Label(top, text = 'Input Value for Graph option :')
	l6.place(x = 25, y = 310)
	s1 = StringVar()
	te1 = Entry(top, textvariable = s1)
	te1.place(x=30, y=330)
	
	def fetchg():
		global sf1
		sf1 = te1.get()

	#date selector graph
	l13 = Label(top,text='Start Date:')
	l13.place(x =25, y= 360)
	b13 = Button(top, text = "⇘", height =0, width =2, command = s_date)
	b13.place(x= 25, y =380 )
	'''svar3 = start_date
	l131 = Label(top,text=svar3) #show current selected date
	l131.place(x =50,y=380)'''

	l14 = Label(top,text='End Date:')
	l14.place(x =125, y= 360)
	b14 = Button(top, text = "⇘", height =0, width =2, command = e_date)
	b14.place(x = 125, y =380)
	'''svar4 = end_date
	l141 = Label(top,text=svar4) #show current selected date
	l141.place(x =150,y=380)'''


	b6 = Button(top, text = 'Generate Graph', command = lambda:[fetchg(), plot()])
	b6.place(x=50, y = 420)
#GUI end
	top.mainloop()
gui()
connectionInstance.close()