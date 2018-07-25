import sys
import struct


activeCheck = {'80': 'active', '0': 'inactive'}
fileSystem = {'0': 'EMPTY', '1': 'FAT12', '4': 'FAT16', '5': 'MS_Extended', '6': 'FAT16', '7': 'NTFS', 'b': 'FAT32', 'c': 'FAT32', 'e': 'FAT16', 'f': 'MS_Extended', '83': 'Linux', '85': 'Linux_Extended', 'a5': 'FreeBSD', 'a8': 'MACOSX', 'ab': 'MAC_OSX_BOOT', 'ee': 'EFI_GTP_DISK'}


def read_sectors(fd, sector, count=1):
    fd.seek(sector * 512)
    return fd.read(count * 512)


def print_table_entry(table):
    global checkSum
    global firstEBR_sector
    global EBR_sector
    if str(table[4]) != '0':
        if str(table[4]) != '5' and str(table[4]) != 'a5':
            print("=======================================")
            print("Active: 0x%02X" % table[0], "(", activeCheck[str(table[0])], ")")
            print("FileSystem : 0x%02X" % table[4], "(", fileSystem[str(table[4])], ")")
            print("LBA Address of Start : ", EBR_sector + struct.unpack_from("<I", table, 8)[0])
            print("Partition Size : ", struct.unpack_from("<I", table, 12)[0])

        else:
            checkSum += 1
            if checkSum == 1:
                firstEBR_sector = struct.unpack_from("<I", table, 8)[0]
                EBR_sector = struct.unpack_from("<I", table, 8)[0]
                ext_data = read_sectors(f, firstEBR_sector)

            else:
                EBR_sector = firstEBR_sector + struct.unpack_from("<I", table, 8)[0]
                ext_data = read_sectors(f, firstEBR_sector + struct.unpack_from("<I", table, 8)[0])

            ext_partition_data = ext_data[446:446 + 64]

            extend_table1 = ext_partition_data[0:16]
            extend_table2 = ext_partition_data[16:32]

            print_table_entry(extend_table1)
            print_table_entry(extend_table2)


if len(sys.argv) is 1:
    print(sys.stderr, '읽을 파일명을 입력해 주십시오.')
    exit(1)

filename = sys.argv[1]

try:
    f = open(filename, 'rb')

except IOError:
    print(sys.stderr, '파일이 없거나, 파일 열기 에러입니다.')
    exit(1)

data = read_sectors(f, 0)

if data[-2] == 85 and data[-1] == 170:
    EBR_sector = 0
    firstEBR_sector = 0
    checkSum = 0

    print("=======================================")
    print("Boot Record")

    partition_data = data[446:446 + 64]

    table1 = partition_data[0:16]
    table2 = partition_data[16:32]
    table3 = partition_data[32:48]
    table4 = partition_data[48:64]

    print_table_entry(table1)
    print_table_entry(table2)
    print_table_entry(table3)
    print_table_entry(table4)

else:
    print("Not Boot Record")
