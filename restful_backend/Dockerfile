FROM python:3.8-buster
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# RUN wget \
#     https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
#     && mkdir /root/.conda \
#     && bash Miniconda3-latest-Linux-x86_64.sh -b \
#     && rm -f Miniconda3-latest-Linux-x86_64.sh 
# RUN conda --version
RUN echo \
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free \
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free \
    deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free \
    > /etc/apt/sources.list && \
    apt update && \
    apt-get install python3-dev default-libmysqlclient-dev -y && \
    # apt install -y python3-dev libmariadb-dev-compat libmariadb-dev&& \
    wget -O /wait.sh https://cdn.jsdelivr.net/gh/vishnubob/wait-for-it@master/wait-for-it.sh && \
    chmod +x /wait.sh
# RUN conda --version
RUN mkdir /app
COPY requirements.txt /app
# COPY environment.yml /app
WORKDIR /app
# RUN conda env create -f environment.yml
# RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt 
RUN pip3 install -r requirements.txt --no-cache-dir

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . .
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]