# Environnement de build de l'édition Débutant (remaster de l'ISO Linux Mint 22.x)
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        xorriso squashfs-tools curl ca-certificates rsync \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
