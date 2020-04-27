# telegraf

USB mount
----------
sudo mount -t ext4 -o defaults /dev/sda1 /media/usb/

UUID=36A1-D852 /media/usb vfat auto,nofail,noatime,users,rw,uid=pi,gid=pi 0 0


Create a docker network
docker network create influxdb

Setup influx 
---------------
https://hub.docker.com/_/influxdb
docker pull influx:latest
Cd /media/usb/influx

docker run -d -p 8086:8086 \
-v $PWD/influxdb.conf:/etc/influxdb/influxdb.conf:ro \
-v $PWD:/var/lib/influxdb \
--name influxdb \
--net=influxdb \
influxdb -config /etc/influxdb/influxdb.conf

Setup chronograf
-----------------
docker pull chronograf:latest
https://hub.docker.com/_/chronograf
Cd /media/usb/chronograf

docker run -d -p 8888:8888 \
-v $PWD:/var/lib/chronograf \
--net=influxdb \
--name chronograf \
chronograf --influxdb-url=http://influxdb:8086


Setup telegraf
-----------------
https://hub.docker.com/_/telegraf
Cd /media/usb/telegraf
docker pull telegraf:latest
docker run --rm telegraf telegraf config > telegraf.conf
[[outputs.influxdb]]
    urls = ["http://influxdb:8086"]

docker run -d --name=telegraf \
--net=influxdb \
--hostname=localhost \
-e HOST_PROC=/host/proc \
-v /proc:/host/proc:ro \
-e HOST_SYS=/host/sys \
-v /sys:/host/sys:ro \
-e HOST_ETC=/host/etc \
-v /etc:/host/etc:ro \
-v /var/run/docker.sock:/var/run/docker.sock:ro \
-v $PWD/telegraf.conf:/etc/telegraf/telegraf.conf:ro \
--name telegraf \
telegraf

Setup a host telegraph
----------------------

https://docs.influxdata.com/telegraf/v1.14/introduction/installation/
# Before adding Influx repository, run this so that apt will be able to read the repository.

sudo apt-get update && sudo apt-get install apt-transport-https

# Add the InfluxData key

wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/os-release
test $VERSION_ID = "7" && echo "deb https://repos.influxdata.com/debian wheezy stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
test $VERSION_ID = "8" && echo "deb https://repos.influxdata.com/debian jessie stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
test $VERSION_ID = "9" && echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
test $VERSION_ID = "10" && echo "deb https://repos.influxdata.com/debian buster stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt-get update && sudo apt-get install telegraf
sudo systemctl start telegraf

Setup kapacitor
-----------------
https://hub.docker.com/_/kapacitor
Cd /media/usb/kapacitor
docker pull kapacitor:latest

docker run --rm kapacitor kapacitord config > kapacitor.conf


docker run -d -p 9092:9092 \
-v $PWD/kapacitor.conf:/etc/kapacitor/kapacitor.conf:ro \
--name=kapacitor \
-h kapacitor \
--net=influxdb \
-e KAPACITOR_INFLUXDB_0_URLS_0=http://influxdb:8086 \
kapacitor




Docker commands 
---------------
docker rm influxdb / chronograf
Docker stop influxdb / chronograf
Docker ps -a
docker logs -f telegraf
docker exec -it telegraf bash
docker exec -it influxdb influx
In a crash
docker start influxdb chronograf kapacitor

