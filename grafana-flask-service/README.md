

# grafana-flask-service

The Flask data retrieval service was developed to retrieve data from the ScienceLogic MySQL database back to Grafana.

The Flask service is currently installed and ran as a service using Apache `httpd` module for Python. The location of the service is configured in `poly_grafana_monitoring.wsgi`

```bash
[root@grafana-monitoring-dev conf.d]# pwd
/etc/httpd/conf.d
```

look for `poly-grafana-monitoring-flask-service.conf`
```
[root@grafana-monitoring-dev conf.d]# ls -al
total 44
drwxr-xr-x. 2 root root  201 Oct  5 08:46 .
drwxr-xr-x. 5 root root   92 Sep  3 07:50 ..
...
-rw-r--r--  1 root root  661 Oct  5 08:45 poly-grafana-monitoring-flask-service.conf
-rw-r--r--  1 root root 9444 Sep 21 07:35 ssl.conf
...
```

```apache
<VirtualHost *:8443>
    SSLEngine on
    SSLCertificateFile /etc/pki/tls/certs/monitor_rmmdev_poly_com.crt
    SSLCertificateKeyFile /etc/pki/tls/certs/monitor_rmmdev_poly_com.key
    ServerName monitor.rmmdev.poly.com
    WSGIScriptAlias /u /var/www/grafana-flask-service/poly_grafana_monitoring.wsgi
    <Directory /var/www/grafana-flask-service/>
        Order allow,deny
        Allow from all
        Header set Access-Control-Allow-Origin "https://monitor.rmmdev.poly.com"
        Header set Access-Control-Allow-Credentials true
    </Directory>
    LogLevel info
</VirtualHost>
```