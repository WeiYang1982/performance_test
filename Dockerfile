FROM python:3.9.10-slim
MAINTAINER wei.yang
ADD . /opt/page_load_test

ENV TZ "Asia/Shanghai"
ENV test_env test
#ENV ALLURE_PATH /opt/libs/allure-2.13.9/bin/

RUN chmod a+x /opt/* && \
   pip install -r /opt/test_ui/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /opt/test_ui
CMD pytest --driver_type remote  --env ${test_env} --headless True
