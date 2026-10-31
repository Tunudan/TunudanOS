# Tunudan OS — construction des éditions
#   make iso EDITION=debutant        (minimal | debutant | avance | expert)
#   make iso EDITION=avance CYBER=1  (Avancé + pack cybersécurité)
#   make all                         (les quatre ISO)
#   make test EDITION=debutant       (démarre l'ISO dans QEMU)
#   make themes-archive              (pack de thèmes pour 12 interfaces)
#   Débutant = Linux Mint 22.x · Minimal et Avancé = Debian 13 · Expert = Arch Linux

EDITION ?= debutant
CYBER   ?= 0
DOCKER  ?= docker
VERSION := $(shell cat VERSION)
DEB_IMG := tunudan-builder-debian
ARCH_IMG:= tunudan-builder-arch
MINT_IMG:= tunudan-builder-mint
RUN     := $(DOCKER) run --rm --privileged -v $(CURDIR):/src -w /src

.PHONY: help builders builder-debian builder-arch builder-mint debs iso all test lint branding themes themes-archive clean distclean

help:
	@sed -n "2,8p" Makefile

builders: builder-debian builder-arch builder-mint

builder-debian:
	$(DOCKER) build -t $(DEB_IMG) -f docker/Dockerfile.debian docker
builder-arch:
	$(DOCKER) build -t $(ARCH_IMG) -f docker/Dockerfile.arch docker
builder-mint:
	$(DOCKER) build -t $(MINT_IMG) -f docker/Dockerfile.mint docker

# Seules les images utiles à l'édition demandée sont construites
ifeq ($(EDITION),expert)
ISO_BUILDERS := builder-arch
else ifeq ($(EDITION),debutant)
ISO_BUILDERS := builder-debian builder-mint
else
ISO_BUILDERS := builder-debian
endif

branding:
	FORCE=1 ./scripts/prepare-branding.sh

# Thèmes pour 10 interfaces (themes/README.md)
themes:
	python3 themes/build.py

themes-archive:
	mkdir -p out
	tar --exclude='themes/vendor' --exclude='themes/build*.py' --exclude='themes/*/build_*.py' --exclude='__pycache__' \
	    -czf out/tunudan-themes-$(VERSION).tar.gz --transform 's#^themes#tunudan-themes#' themes
	@echo "Archive : out/tunudan-themes-$(VERSION).tar.gz"

debs: builder-debian
	$(RUN) $(DEB_IMG) scripts/build-debs.sh

iso: $(ISO_BUILDERS)
ifeq ($(EDITION),expert)
	$(RUN) $(ARCH_IMG) arch/build-expert.sh
else ifeq ($(EDITION),debutant)
	@ls out/debs/tunudan-theme_*.deb >/dev/null 2>&1 || $(RUN) $(DEB_IMG) scripts/build-debs.sh
	$(RUN) -v tunudan-cache:/tmp/tunudan-build $(MINT_IMG) mint/build-debutant.sh
else
	$(RUN) -v tunudan-cache:/tmp/tunudan-build $(DEB_IMG) \
		debian-live/build-edition.sh $(EDITION) $(if $(filter 1,$(CYBER)),--cyber,)
endif

all:
	$(MAKE) iso EDITION=minimal
	$(MAKE) iso EDITION=debutant
	$(MAKE) iso EDITION=avance
	$(MAKE) iso EDITION=expert

test:
	./tests/boot-qemu.sh $(EDITION)

lint:
	./tests/lint.sh

clean:
	rm -rf out/debs packages/*/debian/.debhelper packages/*/debian/debhelper-build-stamp

distclean: clean
	rm -rf out branding/out
	-$(DOCKER) volume rm tunudan-cache
