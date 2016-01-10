# coding=utf-8
import pymssql
import db_msg
import ads_msg
import datetime
import re
import os
import time
import sys

# Syslogd定时任务函数
# 对于符合条件的日志进行入库处理，对于不符合条件的日志进行备份处理，对于Syslogd库中已经读取并处理的日志进行删除


def syslogd_db_task():

    try:
        # 连接数据库
        conn = pymssql.connect(host=db_msg.db_host, user=db_msg.db_user, password=db_msg.db_password, database=db_msg.db_database)
        cur = conn.cursor()

        # 查询Syslogd表中的所有数据
        query = "select * from Syslogd where MsgHostname=%s"
        cur.execute(query, ads_msg.ads_ip)
        rows = cur.fetchall()

        # insert_args，delete_args,bak_args用于后续进行数据库操作的时候使用
        insert_args = []
        delete_args = []
        bak_args = []

        # insert_query, delete_query, bak_query，用户进行后续处理
        insert_query = "insert into AttackLog (msg_date,msg_time,msg_priority,msg_hostname,msg_text, attack_type,attack_src,attack_dst,attack_sport,attack_dport,attack_flag,attack_datetime) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        delete_query = "delete from syslogd where MsgDate=%s and MsgTime=%s and MsgPriority=%s and MsgHostname=%s and MsgText=%s"
        bak_query = "insert into BakLog (MsgDate,MsgTime,MsgPriority,MsgHostname,MsgText) values (%s,%s,%s,%s,%s)"

        # 将从Syslogd中读取出来的数据进行处理
        for line in rows:
            msg_date, msg_time, msg_priority, msg_hostname, msg_text = line

            # 符合ADS安全事件的日志的处理
            if re.match('.*src=(\S*)\s+dst=(\S*)\s+sport=(\S*)\s+dport=(\S*)\s+flag=(\S*)', msg_text):
                # 匹配ADS安全事件日志字段特征
                attack_msg = re.search('(\S*)\s+src=(\S*)\s+dst=(\S*)\s+sport=(\S*)\s+dport=(\S*)\s+flag=(\S*)', msg_text)
                attack_type, attack_src, attack_dst, attack_sport, attack_dport, attack_flag = attack_msg.groups()
                attack_datetime = msg_date + " " + msg_time

                # 生成insert_args和delete_args
                insert_args.append((msg_date, msg_time, msg_priority, msg_hostname, msg_text, attack_type, attack_src, attack_dst, attack_sport, attack_dport, attack_flag, attack_datetime))
                delete_args.append((msg_date, msg_time, msg_priority, msg_hostname, msg_text))

            else:
                # 生成bak_args和delete_args
                bak_args.append((msg_date, msg_time, msg_priority, msg_hostname, msg_text))
                delete_args.append((msg_date, msg_time, msg_priority, msg_hostname, msg_text))

        # 将不符合入库条件的日志插入到备份库中
        try:
            cur.executemany(bak_query, bak_args)
            conn.commit()
        except Exception, e:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_log_file = sys.path[0] + "dbtask_error.log"
            with open(error_log_file, 'a') as error_file:
                error_file.write(now + "-----" + str(e) + "\n\n")

        # 将符合安全事件条件的日志插入到Attack中
        try:
            cur.executemany(insert_query, insert_args)
            conn.commit()
        except Exception, e:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_log_file = sys.path[0] + "dbtask_error.log"
            with open(error_log_file, 'a') as error_file:
                error_file.write(now + "-----" + str(e) + "\n\n")

        # 删除Syslogd中已经读取并处理的日志
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


# 设置循环条件运行数据处理功能


while(1):

    # 生成任务日志文件路径及文件名（ 目录db_task.py目录下的 db_task目录，文件名为当天时间 ）
    task_log_file = sys.path[0] + '\\db_task\\' + datetime.datetime.now().strftime("%Y-%m-%d")

    # 任务开始，记录开始时间
    task_log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  db task start\n"
    with open(task_log_file, 'a') as task_file:
        task_file.write(task_log)
        
    # 执行数据处理任务
    syslogd_db_task()

    # 任务结束，记录结束时间
    task_log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  db task finish\n"   
    with open(task_log_file, 'a') as task_file:
        task_file.write(task_log)
     
    # 任务时间间隔
    time.sleep(20)


