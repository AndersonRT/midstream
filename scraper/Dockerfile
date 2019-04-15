FROM python:3.7.3

WORKDIR /usr/src/app

COPY Robinhood ./Robinhood
CMD ["python", "./Robinhood/setup.py", "sdist"]
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY scraper.py .

CMD [ "python", "./scraper.py" ]
