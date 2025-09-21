FROM ubuntu:latest
LABEL authors="SanCo"

ENTRYPOINT ["top", "-b"]