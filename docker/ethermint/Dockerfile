FROM alpine:3.6

# This is the release of ethermint to pull in.
ENV EM_VERSION 0.5.3
# ENV EM_SHA256SUM c746b4485967af9f3bfd66238b1ca718a5d77baf2382cde027348313f502d34b

ENV DATA_ROOT /ethermint

# Set user right away for determinism
RUN addgroup emuser && \
    adduser -S -G emuser emuser

# Create directory for persistence and give our user ownership
RUN mkdir -p $DATA_ROOT && \
    chown -R emuser:emuser $DATA_ROOT

# It is nice to have bash so the users can execute bash commands.
RUN apk add --no-cache bash

RUN apk add --no-cache openssl && \
    wget https://github.com/tendermint/ethermint/releases/download/v${EM_VERSION}/ethermint_${EM_VERSION}_linux-amd64.zip  && \
    # echo "${EM_SHA256SUM}  ethermint_${EM_VERSION}_ethermint-linux-amd64.zip" | sha256sum -c && \
    unzip -d /bin ethermint_${EM_VERSION}_linux-amd64.zip && \
    rm -f ethermint_${EM_VERSION}_linux-amd64.zip

# Expose the data directory as a volume since there's mutable state in there
VOLUME $DATA_ROOT

EXPOSE 46658

RUN ethermint --datadir $DATA_ROOT init
