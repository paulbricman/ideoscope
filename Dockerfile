FROM ubuntu
RUN echo hi
RUN apt update
RUN apt install -y git python3 python3-pip
RUN cd ~ && git clone https://github.com/paulbricman/ideoscope
RUN cd ~/ideoscope && python3 -m pip install -r requirements.txt
CMD cd ~/ideoscope; streamlit run main.py
EXPOSE 8501