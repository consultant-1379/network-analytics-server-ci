#!/usr/bin/env rubyl
#Encoding: UTF-8
require 'rubygems'
require "selenium-webdriver"
require 'json'
require 'nokogiri'
require 'open-uri'
require 'date'
require 'time'
require 'net/http'
require 'uri'
require 'csv'

def loadProperties()
  properties = YAML.load(File.open("config.yml", "r"))
  return properties
end

def loadEmailProperties()
  properties = YAML.load(File.open("email.yml", "r"))
  return properties
end

def saveEmailProperties(data)
  File.open('email.yml','w+') do |h|
     h.write data.to_yaml
  end
end

def defaultConfigFile()
  newConfig=Hash.new()

  File.open('config.yml','w+') do |h|
     h.write newConfig.to_yaml
  end
end

def defaultEmailFile()
  newConfig=Hash.new()
  newConfig['teams']=Hash.new()
  File.open('email.yml','w') do |h|
     h.write(newConfig.to_yaml)
  end
  return YAML.load(File.open("email.yml", "r"))
end

def saveProperties(data)
  File.open("config.yml", "w") do |f|
    f.write(data.to_yaml)
  end
end
