from typing import List, Dict, Tuple, Optional
from enum import Enum
import re

#pattern_thread_num = r"Thread T(\d+) \(tid=\d+, (?finished|running)"
#pattern_thread_id = r"Thread T\d+ \(tid=(\d+), (?finished|running)"
#pattern_thead_status = r"Thread T\d+ \(tid=\d+, (finished|running)"
#pattern_thead_parent= r"Thread T\d+ \(tid=\d+, (?finished|running) created by (.*) at"
#pattern_race_type = r".*.*(read|write).* of size"#"(\d+) at (0x\d+) by thread T(\d+)"
#pattern_race_opsize = r".* of size (\d+)"
#pattern_race_address = r".* of size \d+ at (0x[0-9A-Fa-f])"
#pattern_race_thread = r"by thread T(\d+)"

pattern_thead = r"Thread T(\d+) \(tid=(\d+), (finished|running)\) created by (.*) at"
pattern_race = r"(.*)(Read|Write|read|write|atomic read|atomic write).* of size (\d+) at (0x\d+) by thread T(\d+)"
pattern_location = r"Location is (.*) '(.*)' of size (\d+) at (0x[0-9A-Fa-f])"
pattern_call = r".*#\d+ (\S+) (\S+)"

class NodeType(Enum):
    CALL = 0
    RACE = 1

class ThreadNode:
    def __init__(self):
        self.type = None

class RaceType(Enum):
    READ = 0
    WRITE = 1

class RaceNode(ThreadNode):
    def __init__(self,line: str,op: RaceType,addr: str, size: int):
        self.type = NodeType.RACE
        self.line = line
        self.op = op
        self.size = size
        self.addr = addr

class CallNode(ThreadNode):
    def __init__(self,func: str):
        self.type = NodeType.CALL
        self.func = func
        self.children = {}

    # Insert a new entry into this call node. If the entry already exists, return it
    def insertCall(self,line:str,call: "CallNode"):
        node:CallNode = self.children.get(line)

        if node == None:
            new_node = call
            self.children[line] = new_node
            node = new_node

        return node
    
    # Insert a new entry into this call node. If the entry already exists, return it
    def insertRace(self,line: str, race: RaceNode):
        node:ThreadNode = self.children.get(line)

        if node == None:
            new_node = race
            self.children[line] = new_node
            node = new_node

        return node

    def compare(self, func):
        return self.func == func
    
    def __eq__(self,other):
        return self.func == other.func
        
class TSanThread:

    def __init__(self,id):
        self.calls: ThreadNode = None # CallNode, tree of calls made by thread
        self.id = id
threads = {}

def get_callstack(lines):
    
    calls = []
    
    while True:
        line = lines.pop(0)
        rmatch = re.match(pattern_call,line)

        if rmatch is None: break

        func = rmatch.group(1)
        path = rmatch.group(2)
        calls.append((func,path))

    return calls


# Parses output section after data race warning
def parse_warning_race(lines: list):

    prev_op: CallNode
    curr_op: CallNode

    while len(lines) != 0:
        line: str = lines.pop(0)

        match_race = re.match(pattern_race,line)
        match_thread = re.match(pattern_thead,line)
        match_location = re.match(pattern_location,line)

        # Check for read/write info
        if match_race:
            order  = match_race.group(1) # non empty if previous operation
            op     = match_race.group(2).lower() # read/write
            size   = match_race.group(3) # size of read/write
            addr   = match_race.group(4) # 
            thread = match_race.group(5) # thread number tracked by tsan

            if threads.get(thread) is None:
                threads[thread] = TSanThread()

            threadObj: TSanThread = threads[thread]

            calls = get_callstack(lines)
            calls.reverse()

            # DEBUG
            print(f"Thread T{thread}:")

            func: str 
            line: str
            (func,line) = calls.pop(0)

            if (threadObj.calls is None):   
                threadObj.calls = CallNode(func)

            node: CallNode = threadObj.calls

            print(f"    # {func} {line}")

            # otherwise, add calls up the stack
            while len(calls) > 0:
                (func,line) = calls.pop(0)
                print(f"    # {func} {line}")
                new_node = CallNode(func)
                node = node.insertCall(line,new_node)

            # once bottom of call stack is reached, add the data race
            race = RaceNode(line,RaceType.READ if op == "read" else RaceType.WRITE,addr,int(size))
            node.insertRace(line,race)
        
        # Check for thread creation info
        elif match_thread:
            thread = match_thread.group(1) # thread number tracked by tsan
            tid    = match_thread.group(2) # thread id in program
            status = match_thread.group(3) # running/finished
            parent = match_thread.group(4) # parent thread

        # Check for memory location info
        elif match_location:
            type = match_location.group(1) # global/local?
            name = match_location.group(2) 
            size = match_location.group(3)
            addr = match_location.group(4)

    return

def parse_warning_deadlock(lines):
    return

def parse_output(lines):

    while len(lines) != 0:
        line = lines.pop(0)

        if (line.startswith("WARNING: ThreadSanitizer: data race")):
            parse_warning_race(lines)
            continue
        if (line.startswith("WARNING: ThreadSanitizer: lock-order-inversion")):
            parse_warning_deadlock(lines)
            continue

    return

def main():
    file = open("./out.txt","r")

    parse_output(file.readlines())

    return

if __name__ == "__main__":
    main()