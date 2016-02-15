#!/usr/bin/env groovy

import groovy.json.JsonOutput;
import groovy.json.JsonSlurper

def parser = new CliBuilder(usage: 'jsongrep.groovy [ -f FILE ] EXPRESSION [ EXPRESSION [...] ]')
parser.with {
	f longOpt: 'file', args: 1, 'Path of JSON file.'
	h longOpt: 'help', args: 1, 'Usage information.'
}

def options = parser.parse(args)
if (options.h) {
	parser.usage()
	return
}

def path = options.f ? options.f : null

def arguments = options.arguments()
def cfg = new JsonSlurper().parseText(path == null ? System.in.text : new File(path).text)

Binding binding = new Binding()
binding.setVariable("cfg", cfg)
GroovyShell shell = new GroovyShell(binding)

arguments.each { println (shell.evaluate ("cfg.$it")) }
