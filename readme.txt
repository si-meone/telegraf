cd /home/pi/scripts
sudo cp temperature.service /lib/systemd/system/
sudo cp temperature.timer /lib/systemd/system/
sudo cp telegraf_pi_temp_logparser.conf /etc/telegraf/telegraf.d/
sudo systemctl enable temperature.timer temperature.service
sudo systemctl start temperature.timer temperature.service
sudo systemctl restart telegraf
sudo systemctl status temperature
sudo systemctl status telegraf
sudo journalctl -flu telegraf
cat temperature.log
