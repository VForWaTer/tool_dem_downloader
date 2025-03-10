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

# copy the citation file - looks funny to make COPY not fail if the file is not there
COPY ./CITATION.cf[f] /src/CITATION.cff

WORKDIR /src
CMD ["python", "run.py"]