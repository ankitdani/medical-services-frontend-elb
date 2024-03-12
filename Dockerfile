FROM ubuntu:latest

WORKDIR /usr/app/src

ARG LANG='en_us.UTF-8'

# Download and Install Dependencies
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	apt-utils \
	# build-essentials \
	locales \
	python3-pip \
	python3-yaml \
	rsyslog systemd systemd-cron sudo \
	&& apt-get clean

RUN pip3 install --upgrade pip

RUN pip3 install streamlit

RUN pip3 install folium

RUN pip3 install streamlit_folium

RUN pip3 install requests

COPY / ./

EXPOSE 8501

#Tell the image what to do when it starts as a container
CMD ["streamlit", "run", "test.py"]
