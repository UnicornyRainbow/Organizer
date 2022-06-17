#!/bin/sh


echo "building package...................."
flatpak-builder build io.github.unicornyrainbow.organizer.yml --force-clean
echo "making .flatpak file..............."
rm -rf repo
flatpak-builder --force-clean --repo=repo build io.github.unicornyrainbow.organizer.yml	
flatpak build-bundle repo organizer.flatpak io.github.unicornyrainbow.organizer
echo "installing........................"
flatpak remove --force-remove --delete-data --noninteractive -y organizer
flatpak-builder --user --install --force-clean build "io.github.unicornyrainbow.organizer.yml"