import tkinter as tk
from tkinter import font  as tkfont
from tkinter import ttk
import time

accounts=[]

coins={
	10:0,
	20:0,
	50:0,
	100:0,
	200:0
}

idx=0
dataFile=open('id-pass-balance.txt','r')
for i in dataFile.readlines():
	accounts.append([])
	aux=i.split()
	accounts[idx].append(aux[0])
	accounts[idx].append(aux[1])
	accounts[idx].append(int(aux[2]))
	idx+=1

curr=open('currdata.txt','r').readlines()
idx=0
for i in coins.keys():
	coins[i]=int(curr[idx])
	idx+=1

accptr=None



def userfriendly():
	inATM=0
	for i in coins.keys():
		inATM+=coins[i]*i
	popup('\n\nNotice\n\nCash available: '+str(inATM)+'\n\n\n')


def resetdata():
	nb=[]
	nc=[]
	for i in accounts:
		nb.append(str(i[0])+' '+str(i[1])+' '+str(i[2])+'\n')
	for i in coins.keys():
		nc.append(str(coins[i])+'\n')
	dataFile=open('id-pass-balance.txt','w')
	dataFile.writelines(nb)
	dataFile.close()
	coinFile=open('currdata.txt','w')
	coinFile.writelines(nc)
	coinFile.close()

def popup(msg):
	popup=tk.Tk()
	popup.geometry('500x300')
	popup.configure(bg='#3d3d5c')
	popup.wm_title("Alert!")
	l=tk.Label(popup,text=msg,font=('orbitron',15),fg='white',bg='#3d3d5c')
	l.pack(fill='x',pady=10)
	B1=tk.Button(popup,text='Ok',width=20,command=popup.destroy)
	B1.pack()
	popup.mainloop()

def BalancePage():
	b=tk.Tk()
	b.configure(bg='#3d3d5c')
	b.geometry(str(b.winfo_screenwidth())+'x'+str(b.winfo_screenheight()))
	b.wm_title("Balance")
	headL4=tk.Label(b,text='ATM.CE201',font=('orbitron',45,'bold'),background='#3d3d5c',foreground='white').pack(pady=25)
	balanceIntroL=tk.Label(b,text='\n\nYour balance is',font=('orbitron',15),bg='#3d3d5c',fg='white').pack()
	balanceIntroL2=tk.Label(b,text=str(float(accounts[accptr][2]))+' EGP\n\n',font=('orbitron',25),bg='#3d3d5c',fg='white')
	balanceIntroL2.pack(pady=15)
	buttonFrame2=tk.Frame(b,bg='#33334d')
	buttonFrame2.pack(fill='both',expand=True)
	MenuButton=tk.Button(buttonFrame2,text='Exit page',command=b.destroy,relief='raised',
				borderwidth=3,width=40,height=5).pack(pady=8)

def draw(l):
	root = tk.Toplevel()      
	root.title('Drawn money')
	main_frame=tk.Frame(root)
	main_frame.pack(fill='both',expand=True)
	cvs=tk.Canvas(main_frame)
	cvs.pack(side='left',fill='both',expand=True)
	sb=ttk.Scrollbar(main_frame,orient='vertical',command=cvs.yview)
	sb.pack(side='right',fill='y')
	cvs.configure(yscrollcommand=sb.set)
	cvs.bind('<Configure>',lambda e:cvs.configure(scrollregion=cvs.bbox("all")))
	frame2=tk.Frame(cvs)
	cvs.create_window((192,342),window=frame2,anchor='center')
	m=[]
	for i in range(len(l)):
		auximg=tk.PhotoImage(file='imgAssets/EGP_'+str(l[i])+'.png')
		m.append(auximg)
		lab=tk.Label(frame2,image=m[i]).pack()
	root.mainloop()

class MainApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		self.frames = {}
		for F in (LoginPage, MenuPage, WithdrawPage, DepositePage):
		    page_name = F.__name__
		    frame = F(parent=container, controller=self)
		    self.frames[page_name] = frame
		    frame.grid(row=0, column=0, sticky="nsew")
		self.show_frame("LoginPage")
	def show_frame(self, page_name):
		frame = self.frames[page_name]
		frame.tkraise()

class LoginPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent,bg='#3d3d5c')
		self.controller = controller
		self.controller.geometry(str(self.controller.winfo_screenwidth())+'x'+str(self.controller.winfo_screenheight()))
		self.controller.title("ATM_Project_CE201")
		self.controller.iconphoto(False,tk.PhotoImage(file='imgAssets/atm-machine.png'))
		headL=tk.Label(self,
				text='ATM.CE201',
				font=('orbitron',45,'bold'),
				background='#3d3d5c',
				foreground='white').pack(pady=25)
		spL=tk.Label(self,height=4,background='#3d3d5c').pack()
		idL=tk.Label(self,text='Enter your ID',
			font=('orbitron',13),
			bg='#3d3d5c',fg='white').pack()
		theID=tk.StringVar()
		ID=tk.Entry(self,textvariable=theID,
			font=('orbitron',12),width=22).pack(pady=10)
		pwdL=tk.Label(self,text='Enter your Password',
			font=('orbitron',13),
			bg='#3d3d5c',fg='white').pack()
		thePWD=tk.StringVar()
		PWD=tk.Entry(self,show='*',textvariable=thePWD,
			font=('orbitron',12),width=22).pack(pady=10)

		def check():
			valid=False
			num=0
			global accptr
			for a in accounts:
				if(a[0]==theID.get() and a[1]==thePWD.get()):
					theID.set('')
					thePWD.set('')
					errorL['text']=''
					controller.show_frame('MenuPage')
					accptr=num
					valid=True
					userfriendly()
				num+=1
			if(not valid):
					errorL['text']='Incorrect Password'

		enter=tk.Button(self,text='Enter',command=check,
				relief='raised',
				borderwidth=2,width=33,
				height=3).pack(pady=10)
		errorL=tk.Label(self,font=('orbitron',13),text='',fg='white',bg='#33334d',anchor='n')
		errorL.pack(fill='both',expand=True)
		botFrame=tk.Frame(self,relief='raised',borderwidth=3).pack(fill='x',side='bottom')
		visacardPhoto=tk.PhotoImage(file='imgAssets/visa.png')
		visacardL=tk.Label(botFrame,image=visacardPhoto)
		visacardL.pack(side='left')
		visacardL.image=visacardPhoto
		mastercardPhoto=tk.PhotoImage(file='imgAssets/Mastercard.png')
		mastercardL=tk.Label(botFrame,image=mastercardPhoto)
		mastercardL.pack(side='left')
		mastercardL.image=mastercardPhoto
		def getTime():
			now=time.strftime("%I:%M %p")
			timeL.config(text=now)
			timeL.after(200,getTime)
		timeL=tk.Label(botFrame,font=('orbitron',12))
		timeL.pack(side='right')
		getTime()

class MenuPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent,bg='#3d3d5c')
		self.controller = controller
		headL2=tk.Label(self,
				text='ATM.CE201',
				font=('orbitron',45,'bold'),
				background='#3d3d5c',
				foreground='white').pack(pady=25)

		menuL=tk.Label(self,text='Home page\n\nPlease select an option',font=('orbitron',13),bg='#3d3d5c',fg='white').pack()
		buttonFrame=tk.Frame(self,bg='#33334d')
		buttonFrame.pack(fill='both',expand=True)

		withdrawButton=tk.Button(buttonFrame,text='Withdraw',command=lambda:controller.show_frame('WithdrawPage')
					,relief='raised',borderwidth=3,width=50,height=5).pack(pady=8)
		DepositButton=tk.Button(buttonFrame,text='Deposit',command=lambda:controller.show_frame('DepositePage'),relief='raised',
					borderwidth=3,width=50,height=5).pack(pady=8)
		BalanceButton=tk.Button(buttonFrame,text='Balance',command=BalancePage,relief='raised',
					borderwidth=3,width=50,height=5).pack(pady=8)
		ExitButton=tk.Button(buttonFrame,text='EXIT',command=lambda:controller.show_frame("LoginPage"),relief='raised',
					borderwidth=3,width=50,height=5).pack(pady=8)

class WithdrawPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent,bg='#3d3d5c')
		self.controller = controller
		headL3=tk.Label(self,
				text='ATM.CE201',
				font=('orbitron',45,'bold'),
				background='#3d3d5c',
				foreground='white').pack(pady=25)
		menuL2=tk.Label(self,text='Choose the amount you want to withdraw',font=('orbitron',13),bg='#3d3d5c',fg='white').pack()
		buttonFrame2=tk.Frame(self,bg='#33334d')
		buttonFrame2.pack(fill='both',expand=True)

		def withdraw(a):
			global accptr,accounts,coins
			if(a>accounts[accptr][2]):
				BalancePage()
			elif(str(a)[len(str(a))-1]!='0'):
				popup('\n\n\n\nInvalid entry\n\nplease enter a valid amount')
			else:
				clone=a
				done=False
				to=[]
				From=[]
				for i in coins.keys():
					for j in range(coins[i]):
						From.append(i)
				k=len(From)-1
				while(k>-1):
					if(done):
						break
					i=k
					while(i>-1):
						if(From[i]<=a):
							to.append(From[i])
							a-=From[i]
						i-=1
					if(sum(to)==clone and len(to)<=40):
						done=True
					else:
						a=clone
						to.clear()
					k-=1
				if(sum(to)==clone and len(to)<=40):
					accounts[accptr][2]-=clone
					for i in coins.keys():
						coins[i]-=to.count(i)
					draw(to)
				else:
					popup('\n\nSorry\n\nNo enough cash\n\n\n')
			resetdata()
			
		_50B=tk.Button(buttonFrame2,text='50',command=lambda:withdraw(50),
		relief='raised',borderwidth=3,width=50,height=5)
		_50B.grid(row=0,column=0,pady=5)
		sL1=tk.Label(buttonFrame2,height=0,width=62,bg='#33334d').grid(row=0,column=1)
		_600B=tk.Button(buttonFrame2,text='600',command=lambda:withdraw(600),
		relief='raised',borderwidth=3,width=50,height=5)
		_600B.grid(row=0,column=2,pady=5)
		
		_100B=tk.Button(buttonFrame2,text='100',command=lambda:withdraw(100),
		relief='raised',borderwidth=3,width=50,height=5)
		_100B.grid(row=1,column=0,pady=5)
		sL2=tk.Label(buttonFrame2,height=0,width=62,bg='#33334d').grid(row=1,column=1)
		_800B=tk.Button(buttonFrame2,text='800',command=lambda:withdraw(800),
		relief='raised',borderwidth=3,width=50,height=5)
		_800B.grid(row=1,column=2,pady=5)
		
		_200B=tk.Button(buttonFrame2,text='200',command=lambda:withdraw(200),
		relief='raised',borderwidth=3,width=50,height=5)
		_200B.grid(row=2,column=0,pady=5)
		sL3=tk.Label(buttonFrame2,height=0,width=62,bg='#33334d').grid(row=2,column=1)
		_1000B=tk.Button(buttonFrame2,text='1000',command=lambda:withdraw(1000),
		relief='raised',borderwidth=3,width=50,height=5)
		_1000B.grid(row=2,column=2,pady=5)

		_400B=tk.Button(buttonFrame2,text='400',command=lambda:withdraw(400),
		relief='raised',borderwidth=3,width=50,height=5)
		_400B.grid(row=3,column=0,pady=5)
		sL4=tk.Label(buttonFrame2,height=0,width=62,bg='#33334d').grid(row=3,column=1)
		cash=tk.StringVar()
		_Xamount=tk.Entry(buttonFrame2,textvariable=cash,width=21,font=('orbitron',18),justify='center')
		_Xamount.grid(row=3,column=2,pady=5,ipady=25)

		def other(_):
			if('.' in cash.get()):
				popup('\n\n\n\nInvalid entry\n\nplease enter a valid amount')
			else:
				try:
					withdraw(int(cash.get()))
				except:
					popup('\n\n\n\nInvalid entry\n\nplease enter a valid amount')

		_Xamount.bind('<Return>',other)
		xL=tk.Label(buttonFrame2,text='Other Amount',font=('orbitron',13),fg='white',bg='#33334d').grid(row=4,column=2)
		exitB=tk.Button(buttonFrame2,text='Exit page',command=lambda:controller.show_frame('MenuPage'),
		relief='raised',borderwidth=3,width=20,height=2)
		exitB.grid(row=5,column=0,padx=15)
		
class DepositePage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent,bg='#3d3d5c')
		self.controller = controller
		headL3=tk.Label(self,
				text='ATM.CE201',
				font=('orbitron',45,'bold'),
				background='#3d3d5c',
				foreground='white').pack(pady=25)
		def deposite():
			global accptr
			if(theDep.get() not in ['10','20','50','100','200']):
				errL['text']='Invalid entry'
			else:				
				errL['text']=''
				coins[int(theDep.get())]+=1
				accounts[accptr][2]+=int(theDep.get())
				controller.show_frame('MenuPage')
				popup('\n\n\n\n'+theDep.get()+' EGP are deposited succesfully\n')
				theDep.set('')
			resetdata()
			
		spL=tk.Label(self,height=4,background='#3d3d5c').pack()
		depositAmountL=tk.Label(self,text='Enter the amount you want to deposite',
			font=('orbitron',13),
			bg='#3d3d5c',fg='white').pack()
		theDep=tk.StringVar()
		DepositEntry=tk.Entry(self,textvariable=theDep,
			font=('orbitron',12),width=22,justify='center').pack(pady=10)
		enterDeposit=tk.Button(self,text='Enter',command=deposite,
				relief='raised',
				borderwidth=2,width=33,
				height=3).pack(pady=10)
		errL=tk.Label(self,font=('orbitron',13),text='',fg='white',bg='#3d3d5c',anchor='n')
		errL.pack()

app = MainApp()
app.mainloop()
