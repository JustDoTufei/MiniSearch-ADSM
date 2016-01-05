# -*- coding: utf-8 -*-

import pymssql
import re
import db_msg
from minisearch import settings
import datetime


def make_sql_arg(input_src, input_sport, input_dst, input_dport):

    prefix = " WHERE "
    where = ""
    args = []
    
    if None != input_src:
        where = where + prefix + "attack_src = %s"
        args.append(input_src)
        prefix = " AND "
    if None != input_sport:
        where = where + prefix + "attack_sport = %s"
        args.append(input_sport)
        prefix = " AND "
    if None != input_dst:
        where = where + prefix + "attack_dst = %s"
        args.append(input_dst)
        prefix = " AND "
    if None != input_dport:
        where = where + prefix + "attack_dport = %s"
        args.append(input_dport)
        prefix = " AND "

    return where, args


def make_sql_arg_and(input_src, input_sport, input_dst, input_dport):

    where = ""
    prefix = " AND "
    args = []

    if None != input_src:
        where = where + prefix + "attack_src = %s "
        args.append(input_src)
        prefix = " AND "
    if None != input_sport:
        where = where + prefix + "attack_sport = %s "
        args.append(input_sport)
        prefix = " AND "
    if None != input_dst:
        where = where + prefix + "attack_dst = %s "
        args.append(input_dst)
        prefix = " AND "
    if None != input_dport:
        where = where + prefix + "attack_dport = %s "
        args.append(input_dport)
        prefix = " AND "

    return where, args


def make_sql_arg_and_tech(where, args, tech_syn_flood, tech_ack_flood, tech_udp_flood, tech_icmp_flood,
                          tech_connection_flood, tech_stream_flood, tech_content_drop, tech_udp_dns_flood):

    prefix = " and ("
    if None != tech_syn_flood:
        where = where + prefix + " attack_type='SYN-Flood' "
        prefix = " or "
    if None != tech_ack_flood:
        where = where + prefix + " attack_type='ACK-Flood' "
        prefix = " or "
    if None != tech_udp_flood:
        where = where + prefix + " attack_type='UDP-Flood' "
        prefix = " or "
    if None != tech_icmp_flood:
        where = where + prefix + " attack_type='ICMP-Flood' "
        prefix = " or "
    if None != tech_connection_flood:
        where = where + prefix + " attack_type='Connection-Flood' "
        prefix = " or "
    if None != tech_stream_flood:
        where = where + prefix + " attack_type='Stream-Flood' "
        prefix = " or "
    if None != tech_content_drop:
        where = where + prefix + " attack_type='Content-Drop' "
        prefix = " or "
    if None != tech_udp_dns_flood:
        where = where + prefix + " attack_type='UDP-DNS-Flood' "
        prefix = " or "

    if tech_syn_flood is not None or tech_ack_flood is not None or tech_udp_flood is not None or\
        tech_icmp_flood is not None or tech_connection_flood is not None or tech_stream_flood is not None or\
        tech_content_drop is not None or tech_udp_dns_flood is not None:
        where = where + " ) "

    return where, args


def make_sql_arg_and_tech_count(where, args, tech_syn_flood, tech_ack_flood, tech_udp_flood, tech_icmp_flood,
                          tech_connection_flood, tech_stream_flood, tech_content_drop, tech_udp_dns_flood):

    if where != "":
        prefix = " and ("
    else:
        prefix = "where ( "

    if None != tech_syn_flood:
        where = where + prefix + " attack_type='SYN-Flood' "
        prefix = " or "
    if None != tech_ack_flood:
        where = where + prefix + " attack_type='ACK-Flood' "
        prefix = " or "
    if None != tech_udp_flood:
        where = where + prefix + " attack_type='UDP-Flood' "
        prefix = " or "
    if None != tech_icmp_flood:
        where = where + prefix + " attack_type='ICMP-Flood' "
        prefix = " or "
    if None != tech_connection_flood:
        where = where + prefix + " attack_type='Connection-Flood' "
        prefix = " or "
    if None != tech_stream_flood:
        where = where + prefix + " attack_type='Stream-Flood' "
        prefix = " or "
    if None != tech_content_drop:
        where = where + prefix + " attack_type='Content-Drop' "
        prefix = " or "
    if None != tech_udp_dns_flood:
        where = where + prefix + " attack_type='UDP-DNS-Flood' "
        prefix = " or "

    if tech_syn_flood is not None or tech_ack_flood is not None or tech_udp_flood is not None or\
        tech_icmp_flood is not None or tech_connection_flood is not None or tech_stream_flood is not None or\
        tech_content_drop is not None or tech_udp_dns_flood is not None:
        where = where + " ) "

    return where, args


def make_sql_arg_and_flag(where, args, flag_list):

    prefix = " and ("

    for flag_tmp in flag_list:
        if re.match('HTTP-KEYWORD', flag_tmp):
            where = where + prefix + " attack_flag like %s "
            args.append('HTTP-KEYWORD%')
            prefix = " or "
        elif re.match('DNS-KEYWORD', flag_tmp):
            where = where + prefix + " attack_flag like %s "
            args.append('DNS-KEYWORD%')
            prefix = " or "
        else:
            where = where + prefix + " attack_flag=%s "
            args.append(flag_tmp)
            prefix = " or "
    where = where + " ) "

    return where, args


def make_sql_arg_and_flag_count(where, args, flag_list):

    if where != "":
        prefix = " and ("
    else:
        prefix = "where ( "

    for flag_tmp in flag_list:
        if re.match('HTTP-KEYWORD', flag_tmp):
            where = where + prefix + " attack_flag like %s "
            args.append('HTTP-KEYWORD%')
            prefix = " or "
        elif re.match('DNS-KEYWORD', flag_tmp):
            where = where + prefix + " attack_flag like %s "
            args.append('DNS-KEYWORD%')
            prefix = " or "
        else:
            where = where + prefix + " attack_flag=%s "
            args.append(flag_tmp)
            prefix = " or "
    where = where + " ) "

    return where, args


def make_sql_arg_and_time_count(where, args, start_time, end_time):

    if where != "":
        prefix = " and ("
    else:
        prefix = "where ( "

    if start_time is None and end_time is None:
        return where, args
    if start_time is None and end_time is not None:
        where = where + prefix + " attack_datetime < %s )"
        args.append(end_time)
        return where, args
    if start_time is not None and end_time is None:
        where = where + prefix + " attack_datetime > %s )"
        args.append(start_time)
        return where, args
    if start_time is not None and end_time is not None:
        where = where + prefix + " attack_datetime between %s and %s )"
        args.append(start_time)
        args.append(end_time)
        return where, args


def make_sql_arg_and_time(where, args, start_time, end_time):

    prefix = "and ( "

    if start_time is None and end_time is None:
        return where, args
    if start_time is None and end_time is not None:
        where = where + prefix + " attack_datetime < %s )"
        args.append(end_time)
        return where, args
    if start_time is not None and end_time is None:
        where = where + prefix + " attack_datetime > %s )"
        args.append(start_time)
        return where, args
    if start_time is not None and end_time is not None:
        where = where + prefix + " attack_datetime between %s and %s )"
        args.append(start_time)
        args.append(end_time)
        return where, args


def query(input_src=None, input_sport=None, input_dst=None, input_dport=None, tech_syn_flood=None,
          tech_ack_flood=None, tech_udp_flood=None, tech_icmp_flood=None, tech_connection_flood=None,
          tech_stream_flood=None, tech_content_drop=None, tech_udp_dns_flood=None, flag_list=None,
          start_time=None, end_time=None,
          page=None, return_count=False):

    page = 0 if None == page or page < 0 else page
    pagesize = 20

    try:
        conn = pymssql.connect(host=db_msg.db_host, user=db_msg.db_user, password=db_msg.db_password, database=db_msg.db_database)
        cursor = conn.cursor()

        if return_count:
            where, args = make_sql_arg(input_src, input_sport, input_dst, input_dport)

            where, args = make_sql_arg_and_tech_count(where, args, tech_syn_flood, tech_ack_flood, tech_udp_flood,
                                                tech_icmp_flood, tech_connection_flood, tech_stream_flood,
                                                tech_content_drop, tech_udp_dns_flood)
            if flag_list is not None:
                flag_list = flag_list.split(',')
                where, args = make_sql_arg_and_flag_count(where, args, flag_list)

            where, args = make_sql_arg_and_time_count(where, args, start_time, end_time)

            sql_query = "SELECT COUNT(*) FROM AttackLog %s" % where
        else:
            where, args = make_sql_arg_and(input_src, input_sport, input_dst, input_dport)

            where, args = make_sql_arg_and_tech(where, args, tech_syn_flood, tech_ack_flood, tech_udp_flood,
                                    tech_icmp_flood, tech_connection_flood, tech_stream_flood,
                                    tech_content_drop, tech_udp_dns_flood)

            if flag_list is not None:
                flag_list = flag_list.split(',')
                where, args = make_sql_arg_and_flag(where, args, flag_list)

            where, args = make_sql_arg_and_time(where, args, start_time, end_time)

            sql_query = "select top %d * from AttackLog where ( msg_id not in (select top %d msg_id from AttackLog order by msg_id desc)) "
            sql_query = sql_query + where + "order by msg_id desc"
            args.insert(0, pagesize)
            args.insert(1, page*pagesize)

        #print sql_query
        cursor.execute(sql_query, tuple(args))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

    except Exception, e:
        pass
        #print "db-error:", e

    return rows


# the first part of report


def report_query1(report_type, report_start_date, report_end_date):
    attack_type_list = ['SYN-Flood', 'ACK-Flood', 'UDP-Flood', 'ICMP-Flood', 'Connection-flood',
                        'Stream-Flood', 'Content-Drop', 'UDP-DNS-Flood']
    color_list = ['#4572a7', '#aa4643', '#89a54e', '#80699b', '#3d96ae', '#a5c2d5', '#76a871', '#cbab4f']
    attack_type_count_list = []

    try:
        conn = pymssql.connect(host=db_msg.db_host, user=db_msg.db_user, password=db_msg.db_password, database=db_msg.db_database)
        cursor = conn.cursor()

        for attack_type_tmp in attack_type_list:
            args_tmp = []
            sql_query = "select count(*) from AttackLog where attack_type='%s' " % attack_type_tmp
            sql_query = sql_query + " and ( msg_date between %s and %s ) "
            args_tmp.append(report_start_date)
            args_tmp.append(report_end_date)

            cursor.execute(sql_query, tuple(args_tmp))
            rows = cursor.fetchall()

            tuple_tmp = map(None, rows[0])
            tmp = tuple_tmp[0]
            dict_tmp = {}
            dict_tmp['name'] = attack_type_tmp
            dict_tmp['value'] = tmp
            dict_tmp['color'] = color_list[attack_type_list.index(attack_type_tmp)]
            attack_type_count_list.append(dict_tmp)

        cursor.close()
        conn.close()
        return attack_type_count_list

    except Exception, e:
        pass
        #print "db-error", e


def report_query2(report_type, report_start_date, report_end_date):
    attack_type_list = ['SYN-Flood', 'ACK-Flood', 'UDP-Flood', 'ICMP-Flood', 'Connection-flood',
                    'Stream-Flood', 'Content-Drop', 'UDP-DNS-Flood']
    attack_type_count_unit_dict = {}
    attack_type_count_tmp_list = []

    try:
        conn = pymssql.connect(host=db_msg.db_host, user=db_msg.db_user, password=db_msg.db_password, database=db_msg.db_database)
        cursor = conn.cursor()

        if report_type == "day":
            # day report part 2
            for attack_type_tmp in attack_type_list:
                attack_type_count_tmp_list = []
                for hour in range(0, 24):
                    hour_start = report_start_date + " " + str(hour) + ":00:00"
                    hour_end = report_start_date + " " + str(hour) + ":59:59"
                    args_tmp = []

                    sql_query = "select count(*) from AttackLog where attack_type='%s' " % attack_type_tmp
                    sql_query = sql_query + " and (attack_datetime between %s and %s ) "
                    args_tmp.append(hour_start)
                    args_tmp.append(hour_end)

                    cursor.execute(sql_query, tuple(args_tmp))
                    rows = cursor.fetchall()

                    tuple_tmp = map(None, rows[0])
                    tmp = tuple_tmp[0]

                    attack_type_count_tmp_list.append(tmp)

                #print attack_type_count_tmp_list
                attack_type_count_unit_dict[attack_type_tmp] = attack_type_count_tmp_list

        else:
            # week or month report part 2
            date_args = get_time_period(report_start_date, report_end_date)

            for attack_type_tmp in attack_type_list:
                attack_type_count_tmp_list = []
                for day in date_args:
                    args_tmp = []
                    sql_query = " select count(*) from AttackLog where attack_type='%s' " % attack_type_tmp
                    sql_query = sql_query + " and msg_date=%s "
                    args_tmp.append(day)

                    cursor.execute(sql_query, tuple(args_tmp))
                    rows = cursor.fetchall()

                    tuple_tmp = map(None, rows[0])
                    tmp = tuple_tmp[0]

                    attack_type_count_tmp_list.append(tmp)

                attack_type_count_unit_dict[attack_type_tmp] = attack_type_count_tmp_list

        cursor.close()
        conn.close()

    except Exception, e:
        pass
        #print "db-error", e

    return attack_type_count_unit_dict


def report_query3(report_type, report_start_date, report_end_date):

    try:
        conn = pymssql.connect(host=db_msg.db_host, user=db_msg.db_user, password=db_msg.db_password, database=db_msg.db_database)
        cursor = conn.cursor()

        sql_query = " SELECT top 10 attack_dst, count(*)  from AttackLog where msg_date between %s and %s group by attack_dst order by COUNT(*) desc  "
        args = [report_start_date, report_end_date]

        cursor.execute(sql_query, tuple(args))
        rows = cursor.fetchall()

        color_list = ['#4572a7', '#aa4643', '#89a54e', '#80699b', '#3d96ae', '#a5c2d5', '#76a871', '#cbab4f', '#a5c2d5', '#cbab4f']
        color_list_id = 0
        top_n_list_result = []
        top_n_list_dict_tmp = {}

        for tmp in rows:
            top_n_list_dict_tmp = {}
            ip_tmp, count_tmp = tmp

            top_n_list_dict_tmp['name'] = ip_tmp
            top_n_list_dict_tmp['value'] = count_tmp
            top_n_list_dict_tmp['color'] = color_list[color_list_id]
            color_list_id = color_list_id + 1

            top_n_list_result.append(top_n_list_dict_tmp)

        cursor.close()
        conn.close()

    except Exception, e:
        pass
        #print "db-error", e

    return top_n_list_result


def get_time_period(start_time, end_time):

    start_date = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_time, '%Y-%m-%d')
    date_args = []
    date_args.append(start_time)
    i = datetime.timedelta(days=1)
    while i < (end_date - start_date):
        tmp = (start_date + i).strftime('%Y-%m-%d')
        date_args.append(tmp)
        i+=datetime.timedelta(days=1)

    date_args.append(end_time)

    return date_args

