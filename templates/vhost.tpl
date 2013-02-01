
<VirtualHost {{host_ip}}:80>
    DocumentRoot {{document_root}}
    ServerName {{vhost_name}}
    ServerAlias {{vhost_name}}
    <Directory "{{document_root}}">
    {{vhost_directory_options}}
    </Directory>
    ErrorLog {{vhost_root}}/logs/error_log
    CustomLog {{vhost_root}}/logs/access_log combined
    {{vhost_directives}}
</VirtualHost>
