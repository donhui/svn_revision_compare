FROM centos:7.3.1611

ENV TZ=Asia/Shanghai
ENV LC_ALL en_US.UTF-8

RUN yum install -y svn

COPY .subversion/* /root/.subversion/

RUN mkdir -p /opt/svn_revision_compare/
WORKDIR /opt/svn_revision_compare/

COPY . /opt/svn_revision_compare/

ENTRYPOINT python /opt/svn_revision_compare/svn_revision_compare.py
