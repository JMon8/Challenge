FROM python:3

RUN apt update -y && \
    apt install -y curl wget odbc-postgresql unixodbc-dev

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install additional pip packags as needed
COPY solution/requirements.txt $VIRTUAL_ENV/requirements.txt
RUN pip install --upgrade pip && \
    pip install uwsgi && \
    pip install -r $VIRTUAL_ENV/requirements.txt

    
# Primary TCP listen ports
EXPOSE 8008

RUN mkdir /solution
WORKDIR /solution
# add backend code to working directory
COPY solution ./

RUN echo "Starting server"
ENV PYTHONPATH "${PYTHONPATH}:/solution"
CMD ["python","pybe/app.py"]
