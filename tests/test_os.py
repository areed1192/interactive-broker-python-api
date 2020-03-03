import os

# os.kill(29264, 0)

# import os

# # for item in os.popen('tasklist').read().splitlines():
# #     print(item.split())

for process in os.popen('tasklist').read().splitlines()[4:]:
    process_details = process.split()
    # print(process_details)
    if process_details[1] =='29264' or process_details[2] == '29264':
        print(True)
    else:
        # print(process_details)
        print(False)
    # ['cmd.exe', '54184', 'Console', '1', '4,148', 'K']
# print([item.split() for item in os.popen('tasklist').read().splitlines()[4:]])

# getpid('cmd.exe')