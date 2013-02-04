mkdir {{vhost.root}} {{vhost.root}}/logs {{vhost.document_root}}
chown {{vhost.user.name}}:apache {{vhost.root}}
chown {{vhost.user.name}}:apache {{vhost.document_root}}
