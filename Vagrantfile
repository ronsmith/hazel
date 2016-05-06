# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "fletcherh/trusty64"

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provider "hyperv" do |vb|
    vb.memory = "1024"
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  #config.vm.network "private_network", ip: "192.168.22.64"
  config.vm.network "public_network"
  config.vm.synced_folder "./", "/vagrant", owner: 'vagrant', group: 'vagrant', mount_options: ["dmode=775,fmode=775"]
  config.vm.provision "shell", path: "scripts/provision_vagrant.sh"
end
