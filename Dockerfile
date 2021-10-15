FROM python:3.8
EXPOSE 8501
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
RUN python -m textblob.download_corpora
COPY . .
CMD streamlit run main.py