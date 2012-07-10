
[{{samba_share}}]
	force create mode = 600
	force user = {{user}}
	delete readonly = yes
	writeable = yes
	create mode = 644
	path = {{user_home}}
	force group = apache
