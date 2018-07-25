import sys
import struct


def read_sectors(fd, sector, count=1):
    fd.seek(sector * 512)
    return fd.read(count * 512)


def print_partition_entry(partition_entry):
    partition = 0
    while True:
        if struct.unpack_from("<I", partition_entry[partition: partition + 128], 0)[0] != 0:
            test = struct.unpack_from("<I", partition_entry[partition + 40: partition + 48], 0)[0] - struct.unpack_from("<I", partition_entry[partition + 32: partition + 40], 0)[0]
            print("=======================================")
            print("LBA Address of Start : ", struct.unpack_from("<I", partition_entry[partition + 32: partition + 40], 0)[0])
            print("Size : ", test)
            partition += 128
        else:
            break


def print_partition_entries_starting(table):
    print("=======================================")
    print("Partition Entry of Start: ", struct.unpack_from("<I", table, 0)[0])


if len(sys.argv) is 1:
    print(sys.stderr, '읽을 파일명을 입력해 주십시오.')
    exit(1)

filename = sys.argv[1]

try:
    f = open(filename, 'rb')

except IOError:
    print(sys.stderr, '파일이 없거나, 파일 열기 에러입니다.')
    exit(1)

data = read_sectors(f, 1)

partition_data = data[0:0 + 92]
table = partition_data[72:80]
print_partition_entries_starting(table)

partition_entry = read_sectors(f, struct.unpack_from("<I", table, 0)[0], 10)
print_partition_entry(partition_entry)
