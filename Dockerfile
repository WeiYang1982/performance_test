FROM python:3.9.10-buster
MAINTAINER wei.yang
ADD . /opt/performance_test

ENV TZ "Asia/Shanghai"
ENV test_env test
ENV test_group performance

WORKDIR /opt/performance_test

RUN  chmod a+x /opt/*
RUN  pip install -r /opt/performance_test/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN  wget https://npmmirror.com/mirrors/node/v18.6.0/node-v18.6.0-linux-x64.tar.xz
RUN  tar -xf node-v18.6.0-linux-x64.tar.xz -C /opt/
RUN  ln -s /opt/node-v18.6.0-linux-x64/bin/node /usr/bin/node
RUN  apt-get update && apt-get install -y libgbm-dev libpangocairo-1.0-0 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libnss3 libcups2 libxss1 libxrandr2  libasound2 libatk1.0-0 libgtk-3-0

ENV PATH = $PATH:/opt/node-v18.6.0-linux-x64/bin
RUN npm install

CMD pytest --env="${test_env}"  -m "${test_group}" --headless=True
