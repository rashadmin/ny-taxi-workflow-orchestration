FROM apache/airflow:2.10.1

ENV AIRFLOW_HOME=/opt/airflow

USER root

RUN apt-get -qq update && apt install -qqq vim

COPY requirements.txt .

USER ${AIRFLOW_UID}

RUN pip install --no-cache-dir -r requirements.txt

USER root

WORKDIR ${AIRFLOW_HOME}

USER ${AIRFLOW_UID}
