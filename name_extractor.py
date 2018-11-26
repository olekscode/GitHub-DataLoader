# DRAFT

import re


class NameExtractor:
    def __extract_class_names(self, string):
        """Matches only class name in the defition of a class.

        Such as: 'public static class Human extends Mammal'
        Match: ['Human']"""

        pattern = '(?<=class )[A-Za-z]*'
        p = re.compile(pattern)
        return p.findall(string)


    def __diff_to_lines(self, diff):
        lines = diff.split('\n')
        lines = [line for line in lines if len(line) > 0]
        return lines


    def __split_diff_blocks(self, diff):
        pattern = '@@ -\d+,\d+ \+\d+,\d+ @@'
        return re.split(pattern, diff)[1:]


    def __is_addition(self, line):
        return line[0] == '+'


    def __is_deletion(self, line):
        return line[0] == '-'


    def __mark_line(self, line):
        # Marks additions with 1, deletions with -1, and all other lines with 0
        if self.__is_addition(line):
            return 1
        elif self.__is_deletion(line):
            return -1
        else:
            return 0


    def __mark_lines(self, chunk):
        return [self.__mark_line(line) for line in chunk]


    def __extract_replacements(self, chunk):
        marks = self.__mark_lines(chunk)
        
        start_del = -1
        start_add = -1
        
        prev = 0
        replacements = []
        
        for i in range(len(marks)):
            curr = marks[i]
            
            if curr == -1 and prev != -1:
                start_del = i
            elif curr == 1 and prev == -1:
                start_add = i
            elif curr == 0 and prev == 1 and start_del > -1:
                deletion = chunk[start_del:start_add]
                addition = chunk[start_add:i]
                replacements.append([deletion, addition])
            elif curr == 0 and prev == -1:
                start_del = -1
                start_add = -1
                
            prev = curr
                
        return replacements