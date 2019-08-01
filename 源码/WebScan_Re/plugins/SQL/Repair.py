#coding:utf-8
from WebScan import *



class repair:
    suggests=[
        " It is recommended to add filtering conditions, especially for single quotes. Other keywords >>; ,()* & ...... % #", # payload1 ["1","1 and 1=1", "1 and 1=2"]
        " It is recommended to add filtering conditions, especially for single quotes. Other keywords >>; ,()* & ...... % #", # payload2 ["1","1' and '1'='1", "1' and '1'='2"]
        "Increase the filtering format for comments: /*!/", #payload 3 ["1", "1' /*!and*/ '1'='1", "1' /*!and*/ '1'='2"]
        "Filter list to add case filtering",# payload4 ["1", "1' AND '1'='1", "1' AND '1'='2"]
        "Increase the filtering format for comments: /*//*/",# payload 4["1", "1' /*//*/and/*//*/ '1'='1", "1' /*//*/and/*//*/ '1'='2"]
        "Increase filtering on hexadecimal encoding",#payload5 ["1", "1' %61%6e%64 '1'='1", "1' %61%6e%64 '1'='2"]
        "Increase filtering of unicode encoding",#payload 6 "1", "1' \u0061\u006e\u0064 '1'='1", "1' \u0061\u006e\u0064 '1'='2"]
        "", # payload 7
        "", # payload 8
        "", # payload 9
        "", # payload 10

    ]
    questions=[
        "Injection Type=>Digital \n \tno filter sensitive symbols", #1
        "Injection Type=> Character Injection \n \tno filter sensitive symbols",
        "Injection Type=> Character Injection \n \tNo filter comment",
        "Injection Type=> Character Injection \n \tNo filter case",
        "Injection Type=> Character Injection \n \tNo filter comment",#5
        "Injection Type=> Character Injection \n \tNo filtering hexadecimal encoding",
        "Injection Type=> Character Injection \n \tNo filtering unicode encoding",
        "",
        "",
        "",#10
        ""
    ]
    def repair_suggest(self,i,islog):
        output.printf ("\t---------Repair advice--------- ","green")
        output.printf("\tSource of the problem:"+self.questions[i],'red')
        output.printf("\tfor this problem."+self.suggests[i],'purple')
        if islog:
            log.write("SQL","\tSource of the problem:"+self.questions[i])
            log.write("SQL","for this problem."+self.suggests[i])

class POC:
    POC=[
        "1 union select 1,schema_name from information_schema.schemata#",
        "1' union select 1,schema_name from information_schema.schemata#"

    ]