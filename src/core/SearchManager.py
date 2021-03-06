import re

class SearchManager():
    
    """
    Class to build the regex from the matchlist and use it to search the logfile for matches
    
    action =     Variable used to trigger an action
    regex =      Used to search the logfile 
    """
        
    action = False
    regex = ''
    
    def __init__(self, matchlist, rule, logfile):
        self.matchlist = matchlist
        self.rule = rule
        self.logfile = logfile
        
        self.build_regex()
        self.compare_count()
    
    """
    This function is used to build the regex from the matchlist
    """          
    def build_regex(self):
        temp = []
        
        if len(self.matchlist) == 1:
            self.regex = self.matchlist[0]
        else:
            for _x in range(len(self.matchlist)):
                match = re.match('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', self.matchlist[_x])
                if match:
                    for char in self.matchlist[_x]:
                        if char is '.':
                            #print 'char = ' + str(char)
                            char = char.replace('.','[.]')
                            temp.append(char)
                        else:
                            temp.append(char)
                    char = ''.join(temp)
                    self.matchlist [_x] = char
                    
                self.regex = self.regex +"(?=.*"+ str(self.matchlist[_x]) +')'
        
        print 'regex: ', self.regex    


    """
    This function is used to match the regex with the logfile and match the corresponding values
    """
    def match_with_log(self):
        regex_count = 0         
        for line in self.logfile:
            match = re.findall(self.regex, line)
            if match:
                regex_count+=1
        return regex_count
    
    
    """
    This function is used to get the COUNT operator in the rule.
    """
    def get_count_operator(self):
       
        for x in self.rule:
            match = re.findall('COUNT', x)
            if match:
                rule_count_value = self.rule.get(x)
                rule_count_value = rule_count_value.replace(" ", "")
                rule_count_value = int (rule_count_value)
                rule_count = x
        
        count_operator = rule_count[-2:]
        count_operator = count_operator.replace(" ", "")
        
        return rule_count_value, count_operator    
    
    """
    This function is used to compare the count operator of the rule with the count operator of the regex.
    """
    def compare_count(self):
        regex_count = self.match_with_log()        
        rule_count_value, count_operator = self.get_count_operator()
        
        print 'regex count: ', regex_count 

        if count_operator == '=':
            print regex_count, type(regex_count)
            print rule_count_value , type (rule_count_value)
            if regex_count == rule_count_value:
                self.action = True
        if count_operator == '<':
            if regex_count < rule_count_value:
                self.action = True
        if count_operator == '>':
            if regex_count > rule_count_value:
                self.action = True
        if count_operator == '<=':
            if regex_count <= rule_count_value:
                self.action = True
        if count_operator == '>=':
            if regex_count >= rule_count_value:
                self.action = True 
               