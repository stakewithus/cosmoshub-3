FROM golang:1.12.9-alpine3.10 as gaia-base

ARG cosmos_version

ENV cosmos_version=$cosmos_version

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh make g++ linux-headers

RUN mkdir -p /root/go/bin
RUN echo "export GOPATH=/root/go" >> ~/.bash_profile
RUN echo "export GOBIN=/root/go/bin" >> ~/.bash_profile
RUN echo "export PATH=$PATH:/root/go/bin" >> ~/.bash_profile

RUN mkdir -p $GOPATH/src/github.com/cosmos
WORKDIR $GOPATH/src/github.com/cosmos
RUN git clone https://github.com/cosmos/gaia
WORKDIR /$GOPATH/src/github.com/cosmos/gaia
RUN git checkout $cosmos_version

RUN GO111MODULE=on make install install-debug

FROM alpine:latest
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh make g++ linux-headers

COPY --from=gaia-base /go/bin/gaiad /usr/bin/gaiad
COPY --from=gaia-base /go/bin/gaiacli /usr/bin/gaiacli
COPY --from=gaia-base /go/bin/gaiadebug /usr/bin/gaiadebug

ENTRYPOINT ["gaiadebug"]
