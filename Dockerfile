FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements-demo.txt

ENV HOST=0.0.0.0
ENV PORT=7860

EXPOSE 7860

CMD ["sh", "-c", "cd backend && python -m app.webserver"]
