FROM ubuntu:latest
RUN apt-get update && apt-get -y install cron
RUN touch /var/log/cron.log

RUN (crontab -l ; echo "* * * * * echo "Hello World" >> /var/log/cron.log") | crontab

CMD cron && tail -f /var/log/cron.log