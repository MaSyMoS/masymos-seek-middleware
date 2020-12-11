#!/bin/bash
docker run --rm \
       --detach \
       --name masemiwa \
       --user "$(id -u):$(id -g)" \
       --volume "/opt/masemiwa/config:/opt/config" \
       --volume "/opt/masemiwa/logs:/opt/logs" \
       --publish 4242:4242 \
       masemiwa
docker logs -f masemiwa
