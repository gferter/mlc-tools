import fileutils
from arguments_parser import get_arg
from Parser import Parser
from WriterCpp import WriterCpp
from WriterCppSerializatorJson import WriterCppSerializatorJson
from WriterCppSerializatorXml import WriterCppSerializatorXml
from WriterJava import WriterJava
from WriterPython import WriterPython
from WriterPySerializationJson import WriterPySerializationJson
from WriterPySerializationXml import WriterPySerializationXml

print "MLC step1: parce arguments"
configs_directory = get_arg( "-i", "config" )
if configs_directory[-1] != "/":
	configs_directory += "/"
	
out_directory = get_arg( "-o", "out" )
if out_directory[-1] != "/":
	out_directory += "/"

tests = get_arg( "-t", "False" )
tests = tests == "True" or tests == "true" or tests == "yes" or tests == "y"

language = get_arg( "-l", "cpp" )
format = get_arg( "-f", "xml" )
side = get_arg( "-side", "both" )

print "MLC step2: find config files"
str = ""
files = fileutils.getFilesList( configs_directory )
parser = Parser(side)
print "MLC step3: parsing"
for file in files:
	if file.find( ".mlc" ) == len(file)-4:
		str = open(configs_directory + file,"r").read()
		parser.parse(str)

print "MLC step4: link "
parser.link()

print "MLC step5: create classes"
if language == 'py':
	if format == 'xml':
		writer = WriterPySerializationXml(out_directory, parser, tests, configs_directory)
	else:
		writer = WriterPySerializationJson(out_directory, parser, tests, configs_directory)
if language == 'cpp':
	if format == 'xml':
		writer = WriterCppSerializatorXml(out_directory, parser, tests)
	else:
		writer = WriterCppSerializatorJson(out_directory, parser, tests)
print "MLC step6: remove old files"
writer.removeOld()
print "MLC finished successful"

#parser = Parser()
#parser.parse(str)
#writer = WriterJava("out", parser)
#removeOldFiles(parser)