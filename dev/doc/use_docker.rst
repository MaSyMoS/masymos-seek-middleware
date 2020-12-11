.. _use_docker:

******
Docker
******

.. include:: rst_directives.rst

.. contents:: 
    :local:

Build MaSeMiWa-Docker-Image yourself
####################################

#. open a terminal in the root folder of `the repository <https://github.com/MaSyMoS/masymos-seek-middleware>`__ (the ``Dockerfile`` is located here)
#. create docker image ``masemiwa``, i.e. with :c_bash:`docker build -t masemiwa .`

Run MaSeMiWa-Docker-Image
#########################
- run the docker image with something like the code from the file ``docker/start_docker.sh`` in the root of the repository

    .. code-block:: bash

        docker run --rm \
               --detach \
               --name masemiwa \
               --user "$(id -u):$(id -g)" \
               --volume "/my/local/folder/with/masemiwa/config:/opt/config" \
               --volume "/my/local/folder/with/masemiwa/logs:/opt/logs" \
               --publish 8080:4242 \
               masemiwa

    - ``--rm`` to remove the container after running from cache
    - ``--detach`` to ru in background mode
    - ``--name`` naming of the container
    - ``--user`` to use the current users id and group id for writing files in the mounted volumes
    - ``--volume`` to bind a local directory or any docker-volume to save the logs and read the configuration, please replace ``/my/local/folder/with/masemiwa/`` accordingly
        - ⚠ make sure, the local directories exist and belong to the same user and group as the process in the docker container. With the ``--user`` option, you need to use the same IDs.
    - ``--publish`` to map the internal listener to a port on your machine
- the server in the container will listen on port ``4242`` for SEEK requests

Hints
=====
- stop the container with :c_bash:`docker stop masemiwa`
- see console output with :c_bash:`docker logs --follow masemiwa`
- get a root bash inside the running container with :c_bash:`docker exec -u 0 -it masemiwa bash`
