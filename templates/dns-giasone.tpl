dnscmd /ZoneAdd {{vhost.dns_zone}} /Primary /file {{vhost.dns_zone}}.dns
dnscmd /RecordAdd {{vhost.dns_zone}} {{vhost.dns_record}} A {{vhost.ip}}
dnscmd /RecordAdd {{vhost.dns_zone}} @ NS castore.netidea.local
