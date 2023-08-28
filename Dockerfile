FROM python:3

WORKDIR /crawler/

COPY requirements.txt /crawler/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /crawler/

CMD [ "python3", "/crawler/spiders/tplink_en.py" ]