FROM python

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir images

EXPOSE 80

CMD python -m uvicorn main:app --host 0.0.0.0 --port 80 
