import re

def read_logfile():
    filename = 'log.txt'
    loglines = []
    read = open(filename, 'r')
    for _line in read:
        _line = _line.strip()
        loglines.append(_line)
    read.close()
    return loglines

def get_rules():
    from rules import Rules
    Rules = Rules()
    rule_files = Rules.get_rules()
    #ruledef = Rules.get_ruledef()
    
    return rule_files

def manager():
    #Get the rule and logfiles
    log = read_logfile()
    rules = get_rules()
    
    matchlist = []
    for x in rules:
        for keys in x:
            print keys
            if keys == 'SOURCEIP =' or keys == 'TARGETIP =' or keys == 'PROTOCOL =' or keys == 'MESSAGE =':
                matchlist.append(x[keys])
    
    matchlist = asterisk_check(matchlist, x)      
    matchlist, regex = build_regex(matchlist)
    regex_count = match_with_log(matchlist, regex, log)
    check_count(regex_count, x)

def asterisk_check(matchlijst, dictionary):


    count = 0
    for _x in matchlijst:
        y = _x.lstrip()
        matchlijst[count] = y
        count+=1
    
    for _x in matchlijst:
        if _x == '*':
            matchlijst.remove(_x)
            print _x

    return matchlijst   
   
def build_regex(matchlijst):

    regex = ''
    temp = []
    for _x in range(len(matchlijst)):
        match = re.findall('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', matchlijst[_x])
        if match:
            for char in matchlijst[_x]:
                if char is '.':
                    print 'char = ' + str(char)
                    char = char.replace('.','[.]')
                    temp.append(char)
                else:
                    temp.append(char)
            char = ''.join(temp)
            matchlijst [_x] = char
        
        regex = regex +"(?=.*"+ str(matchlijst[_x]) +')'
    
    return matchlijst, regex

def match_with_log(matchlijst, regex, log):
    
    regex_count = 0         
    for line in log:
        match = re.findall(regex, line)
        if match:
            #print 'regex = ' + str(regex) + "  line = " + str(line)
            regex_count+=1
    return regex_count

def check_count(regex_count, rule):
    
    print regex_count
    print rule
   
    for x in rule:
        match = re.findall('COUNT', x)
        if match:
            rule_count = x

    
    count_operator = rule_count[-1]
        
manager()


