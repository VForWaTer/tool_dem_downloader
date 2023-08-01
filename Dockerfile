# Pull any base image that includes python3
FROM python:3.10

# install the toolbox runner tools
RUN pip install json2args

# Install Dependencies
RUN pip install requests

# create the tool input structure
RUN mkdir /in
COPY ./in /in
RUN mkdir /out
RUN mkdir /src
COPY ./src /src

WORKDIR /src
CMD ["python", "run.py"]