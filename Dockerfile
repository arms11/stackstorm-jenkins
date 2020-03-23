ARG PACKS="file:///tmp/packs" 

FROM stackstorm/st2packs:builder AS builder
# considering you have your "local" pack under the `stackstorm-st2` dir relative to Dockerfile
# Here we copy local "stackstorm-st2" dir into Docker's "/tmp/stackstorm-st2"
COPY . /tmp/packs/
# Check it
RUN ls -la /tmp/packs

RUN /opt/stackstorm/st2/bin/st2-pack-install ${PACKS}
FROM stackstorm/st2packs:runtime