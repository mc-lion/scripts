from argparse import ArgumentParser


def readLog(logfile_count: int) -> list:
    result = []
    log_dir = '/var/log/'

    i = 0
    while i < logfile_count:
        if i == 0:
            log = log_dir + 'openvpnas.log'
        else:
            log = log_dir + 'openvpnas.log.' + str(i)
        with open(log) as f:
            lines = f.readlines()
        f.close()

        count = 0
        count_failed = 0
        count_success = 0
        date = ''
        for line in lines:
            if date == '':
                date = line[:19]
            count += 1
            found = line.find("AUTH_FAILED")
            if found != -1:
                count_failed += 1
            found = line.find("AUTH SUCCESS")
            if found != -1:
                count_success += 1
        log_result = {'logfile': log, 'date': date, 'success': count_success, 'failed': count_failed}
        result.append(log_result)
        i += 1
    return result


def printData(data: list):
    for item in data:
        print(f'log_file: {item["logfile"]} {item["date"]}\tSUCCESS: {item["success"]}\tFAILED: {item["failed"]}')


def printZabbix(data: list, what: str):
    print(data[0][what])


def main():
    ap = ArgumentParser()
    ap.add_argument("-z", "--zabbix", help="print success or failed connections count for zabbix user parameters",
                    type=str, choices=["success", "failed"])
    ap.add_argument("-c", "--count", help="how many log files to read", type=int, default=10)
    options = ap.parse_args()

    data = readLog(options.count)
    if options.zabbix:
        printZabbix(data, options.zabbix)
    else:
        printData(data)


if __name__ == '__main__':
    main()
