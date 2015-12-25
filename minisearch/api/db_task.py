# coding = utf-8
import pymssql
import db_msg
import ads_msg
import datetime
import re

try:
    conn = pymssql.connect(host=db_msg.db_host, user=db_msg.db_user, password=db_msg.db_password, database=db_msg.db_database)
    cur = conn.cursor()
    query = "select * from Syslogd where MsgHostname=%s"
    cur.execute(query, ads_msg.ads_ip)
    #conn.commit()
    rows = cur.fetchall()
    insert_args = []
    delete_args = []
    insert_query = "insert into AttackLog (msg_date,msg_time,msg_priority,msg_hostname,msg_text, attack_type,attack_src,attack_dst,attack_sport,attack_dport,attack_flag,attack_datetime) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    delete_query = "delete from syslogd where MsgDate=%s and MsgTime=%s and MsgPriority=%s and MsgHostname=%s and MsgText=%s"


    for line in rows:
        msg_date, msg_time, msg_priority, msg_hostname, msg_text = line
        if re.match('.*src=(\S*)\s+dst=(\S*)\s+sport=(\S*)\s+dport=(\S*)\s+flag=(\S*)', msg_text):
            attack_msg = re.search('(\S*)\s+src=(\S*)\s+dst=(\S*)\s+sport=(\S*)\s+dport=(\S*)\s+flag=(\S*)', msg_text)
            attack_type, attack_src, attack_dst, attack_sport, attack_dport, attack_flag = attack_msg.groups()
            attack_datetime = msg_date + " " + msg_time
            insert_args.append((msg_date, msg_time, msg_priority, msg_hostname, msg_text, attack_type, attack_src, attack_dst, attack_sport, attack_dport, attack_flag, attack_datetime))
            delete_args.append((msg_date, msg_time, msg_priority, msg_hostname, msg_text))
        else:
            print "no"

    # Insert data into AttackLog
    try:
        cur.executemany(insert_query, insert_args)
        conn.commit()
    except Exception, e:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('dbtask_error.log', 'a') as error_file:
            error_file.write(now + "-----" + str(e) + "\n\n")

    # Delete data from Syslogd
    try:
        cur.executemany(delete_query, delete_args)
        conn.commit()
    except Exception, e:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('dbtask_error.log', 'a') as error_file:
            error_file.write(now + "-----" + str(e) + "\n\n")

    cur.close()
    conn.close()

except Exception, e:
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('dbtask_error.log', 'a') as error_file:
        error_file.write(now + "-----" + str(e) + "\n\n")



