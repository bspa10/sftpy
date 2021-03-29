FROM docker-registry.funpresp.com.br/lib/python:3.8

RUN apk --no-cache add                      \
        openssh==8.4_p1-r3                  \
        openssh-sftp-server==8.4_p1-r3      \
        rsyslog==8.2012.0-r0                \
        supervisor==4.2.1-r0                \
     && rm -rf /var/cache/apk/*             \
     && rm -f /etc/ssh/ssh_host_*key*       \

RUN mkdir /var/run/sshd

VOLUME /data
EXPOSE 22

COPY rootfs /
COPY src/users.py /opt/sftpy/py.d/00-users.py
COPY src/folders.py /opt/sftpy/py.d/01-folders.py

RUN chmod +x /opt/sftpy/bin/entrypoint
ENTRYPOINT ["bash", "-c", "/opt/sftpy/bin/entrypoint"]