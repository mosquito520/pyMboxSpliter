import sys
import mailbox
import os

size = 1000*1000*1000*4 #4G # size, maybe optional later

if len(sys.argv) == 1:
    print("usage:")
    print("     %s <size> filename" % sys.argv[0])
    print("")
    print("example:")
    print("     %s huge.mbox" % sys.argv[0])
    print("     %s *.mbox" % sys.argv[0])

for mbox_file in sys.argv[1:]:
    print(mbox_file)
    if os.path.getsize(mbox_file) < size:
        print("... small than split size, skipped!")
        continue

    mbox = mailbox.mbox(mbox_file)

    mbox_split_count = 1
    mbox_split_size = 0
    mbox_split_filename = "%s.%03d" % (mbox_file, mbox_split_count)
    print("===> %s" % mbox_split_filename)
    if os.path.isfile(mbox_split_filename):
        os.unlink(mbox_split_filename)
    mbox_split = mailbox.mbox(mbox_split_filename)

    for idx, mboxMessage in enumerate(mbox):
        if (mbox_split_size + sys.getsizeof(mbox.get_bytes(idx))) > size:
            #next split file
            mbox_split.flush()
            mbox_split.close()
            mbox_split_count += 1
            mbox_split_size = 0
            mbox_split_filename = "%s.%03d" % (mbox_file, mbox_split_count)
            print("===> %s" % mbox_split_filename)
            if os.path.isfile(mbox_split_filename):
                os.unlink(mbox_split_filename)
            mbox_split = mailbox.mbox(mbox_split_filename)

        mbox_split_size +=  sys.getsizeof(mbox.get_bytes(idx))
        mbox_split.add(mbox[idx])

    mbox_split.flush()
    mbox_split.close()
    mbox.close()
