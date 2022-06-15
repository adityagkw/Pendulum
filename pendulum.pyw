import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
#import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk

class Oscilator:
    def __init__(self,x,v,g,m,l,z,f,w):
        self.x=x
        self.v=v
        self.g=g
        self.m=m
        self.z=z
        self.l=l
        self.f=f
        self.w=w
    def damped(self,t):
        k = self.m*self.g/self.l
        wn = (k/self.m)**0.5
        wd = wn * (1-self.z**2)**0.5
        c = (self.v+self.z*wn*self.x)/wd
        u = (c**2+self.x**2)**0.5
        p = np.arctan2(self.x,c)
        return np.e**-(self.z*wn*t) * u*np.sin(wd*t+p)
    def damped_velocity(self,t):
        k = self.m*self.g/self.l
        wn = (k/self.m)**0.5
        wd = wn * (1-self.z**2)**0.5
        c = (self.v+self.z*wn*self.x)/wd
        u = (c**2+self.x**2)**0.5
        p = np.arctan2(self.x,c)
        return -self.z*wn*np.e**-(self.z*wn*t) * u*np.sin(wd*t+p) + np.e**-(self.z*wn*t) * wd*u*np.cos(wd*t+p)
    def forced(self,t):
        k = self.m*self.g/self.l
        wn = (k/self.m)**0.5
        r = self.w/wn
        u = (self.f/k)
        u2 = ((1-r**2)**2 + (2*self.z*r)**2)**0.5
        if u2!=0:
            u/=u2
        else:
            u/=0.0000001
        p = np.arctan2(1-r**2,-2*self.z*r)
        return u*np.sin(self.w*t+p)
    def forced_velocity(self,t):
        k = self.m*self.g/self.l
        wn = (k/self.m)**0.5
        r = self.w/wn
        u = (self.f/k)
        u2 = ((1-r**2)**2 + (2*self.z*r)**2)**0.5
        if u2!=0:
            u/=u2
        else:
            u/=0.0000001
        p = np.arctan2(-2*self.z*r,1-r**2)
        return self.w*u*np.cos(self.w*t+p)
    def run(self,t):
        return self.damped(t)+self.forced(t)
    def run_velocity(self,t):
        return self.damped_velocity(t)+self.forced_velocity(t)
        

root = tk.Tk()
root.title("Pendulum")
root.geometry("400x400")
fig = Figure(figsize=(10,10),dpi=96)
plt = fig.add_subplot(111)
fig2 = Figure(figsize=(10,10),dpi=96)
plt2 = fig2.add_subplot(111)
o = Oscilator(x=0.1,v=0,g=9.8,m=1,l=10,z=0.01,f=0,w=0)
tf = tk.Frame(root)
xl = tk.Label(tf,text="\u03b80:")
xl.grid(row=1,column=1)
xe = tk.Entry(tf)
xe.insert("end","0.1")
xe.grid(row=1,column=2)
vl = tk.Label(tf,text="\u03c90:")
vl.grid(row=1,column=3)
ve = tk.Entry(tf)
ve.insert("end","0")
ve.grid(row=1,column=4)
gl = tk.Label(tf,text="g:")
gl.grid(row=2,column=1)
ge = tk.Entry(tf)
ge.insert("end","9.8")
ge.grid(row=2,column=2)
zl = tk.Label(tf,text="\u03b6:")
zl.grid(row=1,column=5)
ze = tk.Entry(tf)
ze.insert("end","0.01")
ze.grid(row=1,column=6)
ll = tk.Label(tf,text="L:")
ll.grid(row=2,column=3)
le = tk.Entry(tf)
le.insert("end","10")
le.grid(row=2,column=4)
ml = tk.Label(tf,text="m:")
ml.grid(row=2,column=5)
me = tk.Entry(tf)
me.insert("end","1")
me.grid(row=2,column=6)
fl = tk.Label(tf,text="F:")
fl.grid(row=3,column=1)
fe = tk.Entry(tf)
fe.insert("end","0")
fe.grid(row=3,column=2)
wl = tk.Label(tf,text="\u03c9:")
wl.grid(row=3,column=3)
we = tk.Entry(tf)
we.insert("end","0")
we.grid(row=3,column=4)
t1l = tk.Label(tf,text="t1:")
t1l.grid(row=4,column=1)
t1e = tk.Entry(tf)
t1e.insert("end","0")
t1e.grid(row=4,column=2)
t2l = tk.Label(tf,text="t2:")
t2l.grid(row=4,column=3)
t2e = tk.Entry(tf)
t2e.insert("end","100")
t2e.grid(row=4,column=4)
tf.pack(side='top')
def update():
    o.x = float(xe.get())
    o.v = float(ve.get())
    o.g = float(ge.get())
    o.z = float(ze.get())
    o.l = float(le.get())
    o.m = float(me.get())
    o.f = float(fe.get())
    o.w = float(we.get())
def plot():
    update()
    t1 = float(t1e.get())
    t2 = float(t2e.get())
    t = np.linspace(t1,t2,1000)
    a = o.run(t)
    s = gds.get()
    if s=="Angle":
        plt.plot(t,a)
        plt.set_ylabel("\u03b8 (rad)")
    elif s=="Angular Velocity":
        v = o.run_velocity(t)
        plt.plot(t,v)
        plt.set_ylabel("\u03c9 (rad/s)")
    elif s=="Envelope":
        wn = (o.g/o.l)**0.5
        wd = wn*(1-o.z**2)**0.5
        u0 = (((o.v+o.z*wn*o.x)/wd)**2 + (o.x)**2)**0.5
        e = u0 * np.e**(-o.z*(o.g/o.l)**0.5*t)
        plt.plot(t,e)
        plt.plot(t,-e)
        plt.set_ylabel("\u03c9 (rad/s)")
    elif s=="X":
        plt.plot(t,o.l*np.sin(a))
        plt.set_ylabel("X (m)")
    else:
        plt.plot(t,-o.l*np.cos(a))
        plt.set_ylabel("Y (m)")
    plt.set_xlabel("time(s)")
    plt.set_xlim(t[0]-0.01*(t[-1]-t[0]),t[-1]+0.01*(t[-1]-t[0]))
    canvas.draw()

def fullplot():
    plt.cla()
    plt.clear()
    plot()
time = 0
playing=False
tupdate = True
def animate(para):
    global time
    global tupdate
    if not playing and not tupdate:
        return
    try:
        update()
        t1 = float(t1e.get())
        t2 = float(t2e.get())
        t0 = t1+(time*((t2-t1)))
        a = o.run(t0)
        v = o.run_velocity(t0)
        plt2.cla()
        plt2.clear()
        x = o.l*np.sin(a)
        y = -o.l*np.cos(a)
        plt2.plot([0,x],[0,y])
        plt2.scatter(0,0)
        plt2.scatter(x,y)
        plt2.annotate(f"t: {t0} s\n\u03b8: {a} rad\n\u03c9: {v} rad/s\nx: {x} m\ny: {y} m",(-o.l,o.l),va='top')
        plt2.set_xlim(-o.l-o.l/10,o.l+o.l/10)
        plt2.set_ylim(-o.l-o.l/10,o.l+o.l/10)
        plt2.set_xlabel("X (m)")
        plt2.set_ylabel("Y (m)")
        canvas2.draw()
    except:
        pass
    if not tupdate:
        tslider.set(time)
    time+=0.01
    if time>1:
        time = 0
    tupdate = False

tab = ttk.Notebook(root)
gf = tk.Frame(tab)
bf = tk.Frame(gf)
pb = tk.Button(bf,text="Plot")
pb.grid(row=1,column=1)
pb["command"]=fullplot
p2b = tk.Button(bf,text="Plot more")
p2b.grid(row=1,column=2)
p2b["command"]=plot
gds = tk.StringVar()
gd = ttk.OptionMenu(bf,gds,"Angle","Angle","Angular Velocity","Envelope","X","Y")
#gds.set("Angle")
gd.grid(row=2,column=1)
bf.pack()
canvas = FigureCanvasTkAgg(fig,master=gf)
canvas.get_tk_widget().pack()
gf.pack()
tab.add(gf,text='Graph')
af = tk.Frame(tab)
playb = tk.Button(af,text="Play/Pause")
playing=False
def play():
    global playing
    playing = not playing
playb['command']=play
playb.pack()
tslider = ttk.Scale(af,from_=0.0,to=1.0,orient='horizontal')
tslider.set(0)
def time_set(t):
    global time, tupdate
    tupdate=True
    time = int(float(t)*100)/100
    animate(0)
tslider["command"]=time_set
tslider.pack()
canvas2 = FigureCanvasTkAgg(fig2,master=af)
canvas2.get_tk_widget().pack()
af.pack()
ani = anim.FuncAnimation(fig2,animate,interval=10)
tab.add(af,text='Animation')
df = tk.Frame(tab)
dt = tk.Text(df)
dt['state']='disabled'
dt.pack()
df.pack()
tab.add(df,text='Details')
tab.pack()
def tab_selected(e):
    ct = e.widget.tab('current')['text']
    if ct=='Details':
        dt['state']='normal'
        dt.delete("1.0",'end')
        try:
            update()
            k = o.m*o.g/o.l
            w = o.m*o.g
            wn = (k/o.m)**0.5
            fn = wn/(2*np.pi)
            tn = 1/fn
            wd = wn * (1-o.z**2)**0.5
            fd = wd/(2*np.pi)
            td = 1/fd
            du = (((o.v+o.z*wn*o.x)/wd)**2 + (o.x)**2)**0.5
            dp = np.arctan2(o.x,(o.v+o.z*wn*o.x)/wd)
            fu = (o.f/k) * ((1-(o.w/wn)**2)**2 + (2*o.z*o.w/wn)**2)**-0.5
            fp = np.arctan2(-2*o.z*o.w/wn,1-(o.w/wn)**2)
            rd = ((1-(o.w/wn)**2)**2 + (2*o.z*o.w/wn)**2)**-0.5
            cc = 2*o.m*wn
            c = cc*o.z
            d = 2*np.pi*o.z*(1-o.z**2)**-0.5
            dts =f"\u03c9n: {wn} rad/s\n"
            dts+=f"fn: {fn} Hz\n"
            dts+=f"Tn: {tn} s\n"
            dts+=f"\u03c9d: {wd} rad/s\n"
            dts+=f"fd: {fd} Hz\n"
            dts+=f"Td: {td} s\n"
            dts+=f"damped u0: {du} rad\n"
            dts+=f"damped \u03a60: {dp} rad\n"
            dts+=f"forced u0: {fu} rad\n"
            dts+=f"forced \u03a60: {fp} rad\n"
            dts+=f"Rd: {rd}\n"
            dts+=f"W: {w} N\n"
            dts+=f"k: {k} N/m\n"
            dts+=f"c: {c} Ns/m\n"
            dts+=f"cc: {cc} Ns/m\n"
            dts+=f"\u03b4: {d}"
            dt.insert('end',dts)
        except Exception as e:
            dt.insert('end',"Error: "+str(e))
        dt['state']='disabled'
tab.bind('<<NotebookTabChanged>>',tab_selected)
root.mainloop()
