ARG ALPINE_VERSION=3.7

FROM alpine:${ALPINE_VERSION}

RUN apk add --update \
  bash \
  bison \
  build-base \
  expat-dev \
  flex-dev \
  gettext-dev \
  git \
  libintl \
  libxslt \
  linux-headers \
  ncurses-dev \
  perl \
  python3-dev \
  readline-dev \
  texinfo \
  zlib-dev

WORKDIR /gdb

COPY scripts/configure.sh configure.sh
RUN chmod 755 configure.sh
