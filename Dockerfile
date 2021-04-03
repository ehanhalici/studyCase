FROM python
ADD . /todo
WORKDIR /todo
RUN pip install -r requirements.txt

EXPOSE 27017
