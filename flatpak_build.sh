#!/bin/sh

clear
echo "##########################  building  package  ##########################"
flatpak-builder --force-clean --repo=repo build flatpak/io.github.unicornyrainbow.organizer.yml	
flatpak build-bundle repo organizer.flatpak io.github.unicornyrainbow.organizer
echo "#########################  deleting old pakage  #########################"
flatpak remove --force-remove --noninteractive -y organizer
echo "########################  installing new pakage  ########################"
flatpak-builder --user --install --force-clean build "flatpak/io.github.unicornyrainbow.organizer.yml"
