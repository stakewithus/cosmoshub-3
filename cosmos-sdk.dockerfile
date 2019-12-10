FROM golang:1.13-alpine AS build-env

ENV PACKAGES curl make git libc-dev bash gcc linux-headers eudev-dev git

RUN apk add --no-cache $PACKAGES

WORKDIR /root

RUN git clone https://github.com/cosmos/cosmos-sdk

WORKDIR /root/cosmos-sdk

RUN git checkout v0.34.10

RUN GO111MODULE=on go mod tidy

RUN GO111MODULE=on make install

FROM alpine:edge

# Install ca-certificates
RUN apk add --update ca-certificates

# Copy over binaries from the build-env
COPY --from=build-env /go/bin/gaiad /usr/bin/gaiad
COPY --from=build-env /go/bin/gaiacli /usr/bin/gaiacli

ENTRYPOINT ["gaiad"]
