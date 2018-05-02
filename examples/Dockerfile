FROM thrift:latest as builder
ADD ./*.thrift /thrift/
WORKDIR /thrift
RUN find . -name "*.thrift" -exec thrift -r -gen py {} \;

ADD requirements.txt /src/requirements.txt
RUN pip install --compile --no-cache-dir -r requirements.txt
ADD . /src/
COPY --from=builder /thrift/gen-py /src/gen-py
ENTRYPOINT ["python"]