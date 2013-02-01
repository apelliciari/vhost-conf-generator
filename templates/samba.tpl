{% if vhost.samba_share %}
[{{vhost.samba_share}}]
	force create mode = 600
	force user = {{vhost.user}}
	delete readonly = yes
	writeable = yes
	create mode = 644
	path = {{vhost.user_home}}
	force group = apache
{% endif %}
