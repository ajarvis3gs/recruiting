# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'fileutils'
require 'socket'

Vagrant.require_version(">= 1.7.0")

Vagrant.configure("2") do |config|

  # Set our operating system
  config.vm.box = "ubuntu/trusty64"

  #change the name carefully. it has dependencies in ops/provisioner/standalone.sh
  config.vm.hostname = Socket.gethostname

  config.ssh.insert_key = false

  # Forward port 80 so we can see our work
  config.vm.network "forwarded_port", guest: 22, host: 9122
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # Ip Addresses
  config.vm.network "private_network", ip: "192.168.33.20"

  # Explicitly declare our /vagrant sync including file permissions
  # config.vm.synced_folder ".", "/vagrant", mount_options: ["dmode=777,fmode=777"]
  config.vm.synced_folder ".", "/opt/recruiting", type: "nfs", mount_options: ["actimeo=2"]

  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    vb.gui = false

    # Customize the amount of memory on the VM:
    vb.memory = "2048"

    # Enable internet access
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]

    # allow more frequent resyncs of time with host machine when guest additions is available
    vb.customize ["guestproperty", "set", :id, "/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold", 10000]
  end

  # Pre-recipe provisions
  #config.vm.provision "shell", :path => "ops/provisioner/standalone-pre-recipes.sh"

  # Configure our provisioner script
  #config.vm.provision :opsworks, type: 'shell' do |shell|
  #  shell.inline = '/bin/bash /tmp/provisioner/opsworks "$@"'
  #  shell.args = 'ops/dna/php-app.json'
  #end

  # Post-recipe provisions
  #config.vm.provision "shell", :path => "ops/provisioner/standalone-post-recipes.sh"

  # update apt-get
  # sudo apt-get update && sudo apt-get -y upgrade

  # install dependencies
  # sudo apt-get install python-pip python-dev python-pillow python-reportlab
  # sudo apt-get install libxml2-dev libxslt1-dev libffi-dev python-lxml
  # sudo pip install -r requirements.txt
  #
  # setup a new database
  # python manage.py makemigrations
  # python manage.py migrate
  # python manage.py createsuperuser
  #
  # then run the server
  # python manage.py runserver 0.0.0.0:80
end
