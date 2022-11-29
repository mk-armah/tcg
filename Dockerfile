FROM python:3.10-alpine

COPY requirements.txt tcg-scraper/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r tcg-scraper/requirements.txt

WORKDIR tcg-scraper

COPY . .

CMD ["python", "-m", "main"]