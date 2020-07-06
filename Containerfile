FROM ubuntu

# To prevent tzdata from prompting input
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y \
  automake \
  bash \
  bison \
  build-essential \
  libncurses-dev \
  libreadline-dev \
  texinfo \
  xsltproc \
  zlib1g-dev

RUN ln -s /bin/aclocal /bin/aclocal-1.15
RUN ln -s /bin/automake /bin/automake-1.15

WORKDIR /gdb

COPY scripts/configure.sh configure.sh
RUN chmod 755 configure.sh
