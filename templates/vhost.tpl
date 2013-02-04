
<VirtualHost {{vhost.ip}}:80>
    DocumentRoot {{vhost.document_root}}
    ServerName {{vhost.name}}
    ServerAlias {{vhost.name}}
    <Directory "{{vhost.document_root}}">
    {{vhost.directory_options}}
    </Directory>
    ErrorLog {{vhost.root}}/logs/error_log
    CustomLog {{vhost.root}}/logs/access_log combined
{% if vhost.directives %}
    {{vhost.directives}}
{% endif %}
</VirtualHost>
