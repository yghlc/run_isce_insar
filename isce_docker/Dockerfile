FROM ubuntu:16.04
MAINTAINER Lingcao Huang

# nvidia docker for installing ISCE (InSAR software)

# gdal related:
#       libproj-dev libgdal-dev libgeos-dev libjson0-dev vim python-gdal \
#	    dans-gdal-scripts

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        pkg-config \
        m4 \
        g++ \
        zlib1g-dev \
        python \
        python3-dev \
        vim

#        zip \
#        unzip \
#        git \
#	    wget \
#	    gedit

# isce dependency
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgmp-dev libmpfr-dev libmpc-dev libc6-dev-i386 \
        gfortran \
        fftw-dev \
        libfftw3-dev \
        sqlite3 libsqlite3-dev \
        libmotif-dev \
        libxt-dev  \
        sudo \
        scons \
        libhdf5-dev \
        cython3 \
        libatlas-dev libatlas-base-dev

#cpython3 \
#libatlas-dev libatlas-base-dev \

# create a new user, hlc

# Install GDAL dependencies
## Update base container install
#RUN apt-get update
#RUN apt-get upgrade -y

# Add unstable repo to allow us to access latest GDAL builds
RUN echo deb http://ftp.uk.debian.org/debian unstable main contrib non-free >> /etc/apt/sources.list
RUN apt-get update

# Existing binutils causes a dependency conflict, correct version will be installed when GDAL gets intalled
#RUN apt-get remove -y binutils

# Install GDAL dependencies
RUN apt-get --allow-unauthenticated -t unstable install -y libgdal-dev

## Update C env vars so compiler can find gdal
#ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
#ENV C_INCLUDE_PATH=/usr/include/gdal

# This will install latest version of GDAL
#RUN pip3 install GDAL>=2.2.4

RUN apt-get update && apt-get --allow-unauthenticated -y install \
    libproj-dev gdal-bin libgdal-dev libgeos-dev

# libjson0-dev

RUN apt-get update && apt-get --allow-unauthenticated -y install \
    python3-pip

RUN pip3 install --upgrade pip

# after install isce
RUN pip3 install numpy
RUN pip3 install scipy

RUN pip3 install GDAL



# Clean-up
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# need to create a user: hlc

RUN useradd -m hlc && echo "hlc:hlc123" | chpasswd && adduser hlc sudo
USER hlc
CMD /bin/bash
WORKDIR /home/hlc


















