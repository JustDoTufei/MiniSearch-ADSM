# coding = utf-8
import pymssql
import db_msg
import ads_msg
import datetime
import re
import os
import time
import sys

def syslogd_db_task():

    try:
        conn = pymssql.connect(host=db_msg.db_host, user=db_msg.db_user, password=db_msg.db_password, database=db_msg.db_database)
        cur = conn.cursor()
        query = "select * from Syslogd where MsgHostname=%s"
        cur.execute(query, ads_msg.ads_ip)
        #conn.commit()
        rows = cur.fetchall()
        insert_args = []
        delete_args = []
        bak_args = []
        insert_query = "insert into AttackLog (msg_date,msg_time,msg_priority,msg_hostname,msg_text, attack_type,attack_src,attack_dst,attack_sport,attack_dport,attack_flag,attack_datetime) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        delete_query = "delete from syslogd where MsgDate=%s and MsgTime=%s and MsgPriority=%s and MsgHostname=%s and MsgText=%s"
        bak_query = "insert into BakLog (MsgDate,MsgTime,MsgPriority,MsgHostname,MsgText) values (%s,%s,%s,%s,%s)"

        for line in rows:
            msg_date, msg_time, msg_priority, msg_hostname, msg_text = line
            
            if re.match('.*src=(\S*)\s+dst=(\S*)\s+sport=(\S*)\s+dport=(\S*)\s+flag=(\S*)', msg_text):
                attack_msg = re.search('(\S*)\s+src=(\S*)\s+dst=(\S*)\s+sport=(\S*)\s+dport=(\S*)\s+flag=(\S*)', msg_text)
                attack_type, attack_src, attack_dst, attack_sport, attack_dport, attack_flag = attack_msg.groups()
                attack_datetime = msg_date + " " + msg_time
                insert_args.append((msg_date, msg_time, msg_priority, msg_hostname, msg_text, attack_type, attack_src, attack_dst, attack_sport, attack_dport, attack_flag, attack_datetime))
                delete_args.append((msg_date, msg_time, msg_priority, msg_hostname, msg_text))

            else:
                bak_args.append((msg_date, msg_time, msg_priority, msg_hostname, msg_text))
                delete_args.append((msg_date, msg_time, msg_priority, msg_hostname, msg_text))

        # Insert data into BakLog
        try:
            cur.executemany(bak_query, bak_args)
            conn.commit()
        except Exception, e:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_log_file = sys.path[0] + "dbtask_error.log"
            with open(error_log_file, 'a') as error_file:
                error_file.write(now + "-----" + str(e) + "\n\n")

        # Insert data into AttackLog
        try:
            cur.executemany(insert_query, insert_args)
            conn.commit()
        except Exception, e:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_log_file = sys.path[0] + "dbtask_error.log"
            with open(error_log_file, 'a') as error_file:
                error_file.write(now + "-----" + str(e) + "\n\n")

        # Delete data from Syslogd
        try:
            cur.executemany(delete_query, delete_args)
            conn.commit()
        except Exception, e:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_log_file = sys.path[0] + "dbtask_error.log"
            with open(error_log_file, 'a') as error_file:
                error_file.write(now + "-----" + str(e) + "\n\n")

        cur.close()
        conn.close()      

    except Exception, e:
        
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_log_file = sys.path[0] + "dbtask_error.log"
        with open(error_log_file, 'a') as error_file:
            error_file.write(now + "-----" + str(e) + "\n\n")

while(1):

    task_log_file = sys.path[0] + '\\db_task\\' + datetime.datetime.now().strftime("%Y-%m-%d")
    task_log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  db task start\n"
    with open(task_log_file, 'a') as task_file:
        task_file.write(task_log)
        
    syslogd_db_task()

    task_log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  db task finish\n"   
    with open(task_log_file, 'a') as task_file:
        task_file.write(task_log)
     
    time.sleep(20)


