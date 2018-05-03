FROM thrift:latest as builder
ADD ./examples/*.thrift /thrift/
WORKDIR /thrift
RUN find . -name "*.thrift" -exec thrift -r -gen py {} \;

FROM python:latest
ADD . /src/
WORKDIR /src
RUN pip install .
WORKDIR /src/examples/
COPY --from=builder /thrift/gen-py /src/examples/gen-py
ENTRYPOINT ["python"]
