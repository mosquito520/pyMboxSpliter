import sys
import mailbox
import os

def extractattachements(message):
    if message.get_content_maintype() == 'multipart':
        for part in message.walk():
            if part.get_content_maintype() == 'multipart': continue
            if part.get('Content-Disposition') is None: continue
            filename = part.get_filename()
            print(filename)
            fb = open(filename,'wb')
            fb.write(part.get_payload(decode=True))
            fb.close()

if len(sys.argv) == 1:
    print("usage:")
    print("     %s <size> filename" % sys.argv[0])
    print("")
    print("example:")
    print("     %s huge.mbox" % sys.argv[0])
    print("     %s *.mbox" % sys.argv[0])

for mbox_file in sys.argv[1:]:
    print(mbox_file)

    mbox = mailbox.mbox(mbox_file)

    for idx, mboxMessage in enumerate(mbox):
        #print("==> " % idx)
        extractattachements(mbox[idx])

    mbox.close()
