FROM python:3.11-alpine

# Set the time zone to Kyiv
RUN ln -sf /usr/share/zoneinfo/Europe/Kiev /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]