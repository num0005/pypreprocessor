#!/usr/bin/env python
# pypreprocessor.py

import sys
import os
import traceback

class preprocessor:
    def __init__(self):
        # public variables
        self.defines = []
        self.input = os.path.join(sys.path[0],sys.argv[0])
        self.output = ''
        self.removeMeta = False
        # private variables
        self.__linenum = 0
        self.__excludeblock = False
        self.__ifblock = False
        self.__ifcondition = ''
        self.__ifconditions = []
        self.__evalsquelch = True

    # the #define directive
    def define(self, define):
        self.defines.append(define)

    def search_defines(self, define):
        if define in self.defines:
            return True
        else:
            return False

    # the #ifdef directive
    def compare_defines_and_conditions(self, defines, conditions):
        # if defines and conditions lists have no intersecting values (ie. else = true)
        if not [val for val in defines if val in conditions]:
            return True
        else:
            return False

    # the #undef directive
    def undefine(self, define):
        # re-map the defines list excluding the define specified in the args
        self.defines[:] = [x for x in self.defines if x != define]

    # evaluate
    def eval_pre(self, line):
    # return values are (squelch, metadata)
        if self.__ifblock is False and self.__excludeblock is False:
            # squelch the preprocessor parse on the first
            # pass to prevent preprocessor infinite loop
            if 'pypreprocessor.parse()' in line:
                return True, True
            if line[:1] != '#':
                return False, False
        # handle #define directives
        if line[:7] == '#define':
            if len(line.split()) != 2:
                self.exit_error('#define')
            else:
                self.define(line.split()[1])
                return False, True
        # handle #undef directives
        if line[:6] == '#undef':
            if len(line.split()) != 2:
                self.exit_error('#undef')
            else:
                self.undefine(line.split()[1])
                return False, True
        # handle #endif directives
        if line[:6] == '#endif':
            if len(line.split()) != 1:
                self.exit_error('#endif')
            else:
                self.__ifblock = False
                self.__ifcondition = ''
                self.__ifconditions = []
                return False, True
        # handle #endexclude directives
        if line[:11] == '#endexclude':
            if len(line.split()) != 1:
                self.exit_error('#endexclude')
            else:
                self.__excludeblock = False
                return False, True
        # handle #exclude directives
        if line[:8] == '#exclude':
            if len(line.split()) != 1:
                self.exit_error('#exclude')
            else:
                self.__excludeblock = True
        # process the excludeblock
        if self.__excludeblock is True:
            return True, False
        # handle #ifdef directives
        if line[:6] == '#ifdef':
            if len(line.split()) != 2:
                self.exit_error('#ifdef')
            else:
                self.__ifblock = True
                self.__ifcondition = line.split()[1]
                self.__ifconditions.append(line.split()[1])
        # handle #else directives
        if line[:5] == '#else':
            if len(line.split()) != 1:
                self.exit_error('#else')
        # process the ifblock
        if self.__ifblock is True:
            # evaluate and process an #ifdef
            if line[:6] == '#ifdef':
                if self.search_defines(self.__ifcondition):
                    self.__evalsquelch = False
                else:
                    self.__evalsquelch = True
                return False, True
            # evaluate and process the #else
            elif line[:5] == '#else':
                if self.compare_defines_and_conditions(self.defines, self.__ifconditions):
                    self.__evalsquelch = False
                else:
                    self.__evalsquelch = True
                return False, True
            else:
                return self.__evalsquelch, False
        else:
            return False, False

    # error handling
    def exit_error(self, directive):
        print('File: "' + self.input + '", line ' + str(self.__linenum))
        print('SyntaxError: Invalid ' + directive + ' directive')
        sys.exit(1)

    # parsing/processing
    def parse(self):
        # open the input file
        input_file = open(self.input,'r')
        outputBuffer = ''

        try:
            # process the input file
            for line in input_file:
                self.__linenum += 1
                # to squelch or not to squelch
                squelch, metaData = self.eval_pre(line)
                # process and output
                if self.removeMeta is True: 
                    if metaData is True or squelch is True:
                        continue
                if squelch is True:
                    outputBuffer += '#' + line
                    continue
                if squelch is False:
                    outputBuffer += line
                    continue
        finally:
            input_file.close()

        # open file for output (no auto-run)
        if self.output != '':
            self.run = False
            output_file = open(self.output, 'w')
        # open tmp file for output (auto-run)
        else:
            self.run = True
            self.output = self.input + '.tmp'
            output_file = open(self.output, 'w')

        # write post-processed code to file
        try:
            output_file.write(outputBuffer)
        finally:
            output_file.close()

        # run the post-processed code
        if self.run == True:
            try:
                exec(open(self.output,"rb").read())
            except:
                trace = traceback.format_exc().splitlines()
                index = 0
                for line in trace:
                    if index == (len(trace) - 2):
                        print(line.replace("<string>", self.input))
                    else:
                        print(line)
                    index += 1
            finally:
                os.remove(self.output)

        # break execution so python doesn't
        # run the rest of the pre-processed code
        sys.exit(0)

pypreprocessor = preprocessor()
