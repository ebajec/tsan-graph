import re

pattern_thread_num = r"Thread T(\d+) \(tid=\d+, (?finished|running)"
pattern_thread_id = r"Thread T(\d+) \(tid=\d+, (?finished|running)"
pattern_thead_status = r"Thread T\d+ \(tid=\d+, (finished|running)"
pattern_thead_parent= r"Thread T\d+ \(tid=\d+, (?finished|running) created by (.*) thread"

pattern_race_type = r".*.*(read|write).* of size"#"(\d+) at (0x\d+) by thread T(\d+)"
pattern_race_opsize = r".* of size (\d+)"
pattern_race_address = r".* of size \d+ at (0x\d+)"
pattern_race_thread = r"by thread T(\d+)"


def parse_line(line):
    
    return

def main():
    file = open("./.user/out.txt","r")

    for line in file.readlines():
        print(line)

    return

if __name__ == "__main__":
    main()