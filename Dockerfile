FROM docker-registry.funpresp.com.br/lib/python:3.8

RUN apk --no-cache add                      \
        openssh==8.4_p1-r3                  \
        openssh-sftp-server==8.4_p1-r3      \
        rsyslog==8.2012.0-r0                \
     && rm -rf /var/cache/apk/*             \
     && rm -f /etc/ssh/ssh_host_*key*       \
     && mkdir /var/dev                      \
     && mkdir /var/run/sshd                 \
     && mkdir /etc/rsyslog.d

VOLUME /data
COPY config/sshd_config /etc/ssh/sshd_config

COPY src/users.py /opt/sftpy/py.d/00-users.py
COPY src/folders.py /opt/sftpy/py.d/01-folders.py
COPY src/entrypoint /opt/sftpy/bin/entrypoint

RUN chmod +x /opt/sftpy/bin/entrypoint
ENTRYPOINT ["bash", "-c", "/opt/sftpy/bin/entrypoint"]