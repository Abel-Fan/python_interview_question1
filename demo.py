from multiprocessing import Process 
import pymysql,time,threading
db = pymysql.connect(host="localhost",user="root",password="",db="demo")

t_id = ""

def fn1():
    """
    进程启动时，会往teacher表里插入一条记录，记下这条记录的id值，保存为t_id
    """
    global t_id
    id = 1
    t_id = id  #保存t_id
    name = "小白"
    check_time = time.mktime(time.localtime())
    
    sql = "insert into teacher (id,name,check_time) values(%s,'%s',%s)"%(id,name,check_time)

    cur = db.cursor()
    cur.execute(sql)
    db.commit()

    timer = threading.Timer(2,fn2) #开启线程
    timer.start()  #开启线程

    timer1 = threading.Timer(2,fn3) #开启线程
    timer1.start()  #开启线程

def fn2():
    """
    进程定期更新t_id对应记录的check_time字段
    """
    print("hello timer")
    global timer 
    check_time = time.mktime(time.localtime())

    timer = threading.Timer(3,fn2)
    timer.start()
    print("t_id:",t_id)
    sql = "UPDATE teacher SET check_time=%s WHERE id=%s"%(check_time,t_id)
    cur = db.cursor()
    cur.execute(sql)
    db.commit()

def fn3():
    """
    定期扫描student表，如果有teacher_id为0的记录，将该字段更新为其t_id
    """

    timer = threading.Timer(3,fn3)
    timer.start()

    sql = "UPDATE student SET teacher_id=%s WHERE teacher_id=0"%t_id
    cur = db.cursor()
    cur.execute(sql)
    db.commit()


if __name__ == "__main__":
    p1 = Process(target=fn1)
    p1.start()
    p1.join()
