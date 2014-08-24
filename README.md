mmi-ifs
=======

**** HACK *** HACK *** HACK *** HACK ****

I hacked this together to unpack QNX flash images, in particular the ifs-root.ifs
image of Audi MMI systems. 

This code is probably buggy, missing features and simply does not work. Worked for me, though.

```
$ dumpifs ifs-root.ifs
dumpifs: Unable to find startup header in ifs-root.ifs
$ dumpifs ifs-root.ifs.imagefs.decomp
   Offset     Size  Name
        0       5c  Image-header mountpoint=/
       5c     6fdc  Image-directory
     ----     ----  Root-dirent
     7ef8    65000  proc/boot/procnto-instr
    6cef8     1680  proc/boot/.script
    6eef8       b5  proc/boot/serverstarterboot
    6fef8       89  proc/boot/server.cfg
    70ef8       b2  proc/boot/customer_update_boot
     ----        9  dev/console -> /dev/ser1
     ----        a  tmp -> /dev/shmem
[...]
```
