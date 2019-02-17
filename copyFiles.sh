Ip=192.168.0.65
Password=aa

sshpass -p "$Password" scp app.py pi@$Ip:app.py
sshpass -p "$Password" scp config.py pi@$Ip:config.py
sshpass -p "$Password" scp power_generator_sensehat.py pi@$Ip:power_generator_sensehat.py
