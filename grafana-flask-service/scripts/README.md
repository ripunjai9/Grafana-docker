

# grafana-flask-excel-cleanup

The script(1cleanreports) is used to cleanup the last 60 min saved xls/report files.

```bash
[root@grafana-monitoring-dev grafana]# cd /etc/cron.hourly/
[root@grafana-monitoring-dev cron.hourly]# ll
total 12
-rwxr-xr-x. 1 root root 392 Aug  9  2019 0anacron
-rw-r--r--  1 root root 377 Oct 13 06:41 1cleanreports
-rwxr-xr-x. 1 root root 191 Aug  9  2019 mcelog.cron
```

After adding new file restart the cron service 

```bash
[root@grafana-monitoring-dev cron.hourly]# service crond restart
Redirecting to /bin/systemctl restart crond.service
```

**NOTE**: change clean_xls_reports.sh to clean_xls_reports