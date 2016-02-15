#!/usr/bin/env groovy

import groovy.json.JsonOutput;
import groovy.json.JsonSlurper

def parser = new CliBuilder(usage: 'jsoncat.groovy [ JSON_FILE [ JSON_FILE [ ... ] ] ]')
parser.with {
	h longOpt: 'help', args: 1, 'Usage information.'
}

def options = parser.parse(args)
if (options.h) {
	parser.usage()
	return
}

def jsons = ( options.arguments().size() == 0 
		? { new JsonSlurper().parseText(System.in.text) }() 
		: options.arguments().collect { new JsonSlurper().parseText( new File(it).text) }
	).inject ([:]) { acc, e -> e.each { key, val -> acc[key] = val } ; acc }

println JsonOutput.prettyPrint(JsonOutput.toJson(jsons))