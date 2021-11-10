FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# CMD [ "python", "./your-daemon-or-script.py" ]
CMD flask run --host=0.0.0.0