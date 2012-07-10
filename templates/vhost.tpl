
<VirtualHost {{host_ip}}:80>
    DocumentRoot {{document_root}}
    ServerName {{user}}
    <Directory "{{document_root}}">
    Options -Indexes FollowSymLinks
    AllowOverride All
    </Directory>
    ErrorLog {{user_home}}/logs/error_log
    CustomLog {{user_home}}/logs/access_log combined
</VirtualHost>
