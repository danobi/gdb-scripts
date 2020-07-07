FROM ubuntu

# To prevent tzdata from prompting input
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y \
  automake-1.15 \
  bash \
  bison \
  build-essential \
  curl \
  dejagnu \
  flex \
  g++ \
  libncurses-dev \
  libreadline-dev \
  texinfo \
  xsltproc \
  zlib1g-dev

WORKDIR /gdb

COPY scripts/configure.sh configure.sh
RUN chmod 755 configure.sh

COPY scripts/gdbinit /root/.gdbinit

# Install latest rust compiler
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain nightly

# Update path to include rust binaries
ENV PATH="~/.cargo/bin:${PATH}"
# Also symlink rustc into /bin b/c for some reason the test framework needs it
RUN ln -s ~/.cargo/bin/rustc /bin/rustc
