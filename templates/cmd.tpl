mkdir {{vhost.vhost_root}} {{vhost.vhost_root}}/logs {{vhost.document_root}}
chown {{vhost.user}}:apache {{vhost.vhost_root}}
chown {{vhost.user}}:apache {{vhost.document_root}}
