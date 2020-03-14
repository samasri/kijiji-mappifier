FROM ubuntu

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY webApp/package*.json ./

# Bundle app source
COPY . .

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install git build-essential bash-completion python3-dev vim curl wget tar python3-pip 
RUN pip3 install --upgrade pip
RUN pip3 install beautifulsoup4 requests
RUN touch apartmentInfo