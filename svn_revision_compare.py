#! /bin/python
# -*- coding: UTF-8 -*-
from mail_utils import send_mail
from settings import SVN_SERVER_LIST, SVN_SETTINGS, SVN_REPOS_STR

svn_repos_str = SVN_REPOS_STR
svn_server_list = SVN_SERVER_LIST
svn_username = SVN_SETTINGS.get("username")
svn_password = SVN_SETTINGS.get("password")


def get_svn_repo_list():
    return svn_repos_str.splitlines()


def execute_cmd(command):
    import subprocess
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    return p.split("\n".encode())


def get_latest_revision_for_server(repo_path):
    svn_command = "svnlook youngest %s" % repo_path
    return execute_cmd(svn_command)[0].decode()


def get_latest_revision_for_client(repo_path):
    svn_command = "svn info --username %s --password %s %s|grep Revision: |cut -c11-" % (svn_username, svn_password, repo_path)
    return execute_cmd(svn_command)[0].decode()


def get_last_changed_date(repo_path):
    svn_command = "svn info --username %s --password %s %s|grep 'Last Changed Date:' |cut -c 20-29" % (svn_username, svn_password, repo_path)
    return execute_cmd(svn_command)[0].decode()


def generate_svn_info_matrix():
    svn_repo_list = get_svn_repo_list()
    svn_repo_info_matrix = []
    for svn_repo in svn_repo_list:
        print("svn_repo:" + svn_repo)
        svn_repo_info = [svn_repo]
        for svn_server in svn_server_list:
            repo_path = "http://%s/%s" % (svn_server, svn_repo)
            svn_latest_revision = get_latest_revision_for_client(repo_path)
            if svn_latest_revision is None or svn_latest_revision == "":
                svn_latest_revision = "0"
            print(repo_path + " " + str(svn_latest_revision))
            svn_repo_info.append(svn_latest_revision)
        first_repo_path = "http://%s/%s" % (svn_server_list[0], svn_repo)
        last_changed_date = get_last_changed_date(first_repo_path)
        print("last_changed_date: " + str(last_changed_date))
        svn_repo_info.append(last_changed_date)
        svn_repo_info_matrix.append(svn_repo_info)
    return svn_repo_info_matrix


def generate_svn_info_table(svn_repo_info_matrix):
    html_table = "<table border='1' cellspacing='0'>"
    html_table += "<tr>"
    html_table += "<td>number</td>"
    html_table += "<td>repo name</td>"
    for svn_server in svn_server_list:
        html_table += "<td>%s</td>" % svn_server
    html_table += "<td>last changed date</td>"
    html_table += "</tr>"
    number = 1
    for svn_repo_info in svn_repo_info_matrix:
        html_table += "<tr>"
        html_table += "<td>%s</td>" % number
        origin_revision_number = svn_repo_info[1]
        last_changed_date = svn_repo_info[-1]
        for tmp in svn_repo_info:
            if tmp.isdigit() and int(tmp) != int(origin_revision_number):
                difference = int(tmp) - int(origin_revision_number)
                warning_str = "<font color='red'>%s</font>" % difference
                html_table += "<td>%s(%s)</td>" % (tmp, warning_str)
            elif tmp == last_changed_date and date_compare_with_thirty_days_ago(last_changed_date):
                tips_str = "<font color='blue'>%s</font>" % tmp
                html_table += "<td>%s</td>" % tips_str
            else:
                html_table += "<td>%s</td>" % tmp
        html_table += "</tr>"
        number += 1
    html_table += "</table>"
    return html_table


def date_compare_with_thirty_days_ago(last_changed_date):
    if last_changed_date == "":
        return False
    from datetime import date, timedelta
    import time
    thirty_days_ago = (date.today() + timedelta(days=-30)).strftime("%Y-%m-%d")
    thirty_days_ago_seconds = time.mktime(time.strptime(thirty_days_ago, "%Y-%m-%d"))
    last_changed_date_seconds = time.mktime(time.strptime(last_changed_date, "%Y-%m-%d"))
    if last_changed_date_seconds > thirty_days_ago_seconds:
        return True
    else:
        return False


if __name__ == "__main__":
    # generate_svn_info_matrix
    svn_info_matrix = generate_svn_info_matrix()
    # generate_svn_info_matrix
    svn_info_table = generate_svn_info_table(svn_info_matrix)
    print(svn_info_table)
    # email notify
    send_mail("svn revision compare", svn_info_table)
