{% if vhost.user.samba %}
[{{vhost.user.samba}}]
	force create mode = 600
	force user = {{vhost.user.name}}
	delete readonly = yes
	writeable = yes
	create mode = 644
	path = {{vhost.user.home}}
	force group = apache
{% endif %}
