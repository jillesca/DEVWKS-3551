FROM cisco-nso-ldev:6.4.1

USER root

ENV HOME=/home/developer 

RUN echo 'alias ll="ls -al"' >> /etc/profile.d/alias.sh \
    && echo 'export PS1="\u@\h:\W > "' >> /etc/bash.bashrc 


