
<VirtualHost {{vhost.host_ip}}:80>
    DocumentRoot {{vhost.document_root}}
    ServerName {{vhost.vhost_name}}
    ServerAlias {{vhost.vhost_name}}
    <Directory "{{vhost.document_root}}">
    {{vhost.vhost_directory_options}}
    </Directory>
    ErrorLog {{vhost.vhost_root}}/logs/error_log
    CustomLog {{vhost.vhost_root}}/logs/access_log combined
{% if vhost.vhost_directives %}
    {{vhost.vhost_directives}}
{% endif %}
</VirtualHost>
