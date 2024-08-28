#!/usr/bin/env ruby
#Encoding: UTF-8
require 'date'
require 'time'



 def load_properties()
	properties_filename=ENV['STATUS_PROPERTIES_FILE']
    properties = {}
    File.open(properties_filename, 'r') do |properties_file|
      properties_file.read.each_line do |line|
        line.strip!
        if (line[0] != ?# and line[0] != ?=)
          i = line.index('=')
          if (i)
            properties[line[0..i - 1].strip] = line[i + 1..-1].strip
          else
            properties[line] = ''
          end
        end
      end      
    end
    return properties
  end


