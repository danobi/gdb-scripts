FROM ubuntu

# To prevent tzdata from prompting input
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y \
  automake-1.15 \
  bash \
  bison \
  build-essential \
  libncurses-dev \
  libreadline-dev \
  texinfo \
  xsltproc \
  zlib1g-dev

WORKDIR /gdb

COPY scripts/configure.sh configure.sh
RUN chmod 755 configure.sh
