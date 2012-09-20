GloboFS Planning
================

Push/Pull
---------

Changes on remote sites are pushed inward into upstream logs style files using 
append mode.

Access to hashes that don't exist locally are pulled inward as needed.

You should be able to `cat **/* > /dev/null` to create a mirror of the entire 
volume.  Helper tools will be provided via the globofs script.

No RPC
------

No RPC servers

No HTTP servers

No dedicated metadata servers

No masters

No slaves

Just love

Use remote filesystems as data stores and rely on append mode writes as much as 
possible.  It's not super atomic.. but it is reliable.

Assume Nothing Style
--------------------

We 'require' a few things.. but assume nothing.

Things we require:

- Python
- Access to hard and soft links on the local filesystem (for now)
- Access to other POSIX filesystems via
  - local access
  - nfs
  - sshfs
  - posixish file servers

The two things we assume:

- User will make good decisions based on practical filesystem experience
- Filesystem will have directories

Things we don't assume will work:

- Remote tailing of files
- Local notification of file changes
- File metadata

Things we don't assume will happen:

- Only one 'client' per node.

Hashing use
-----------

SHA256 will be used for hashing data blocks.  Blocks will be set to an arbitrary 
size based on configuration information.

Directory Structure
-------------------

There should be a "self" directory defining a nodes direct data store linked to 
a directory named after the unique id of the node. In the same directory are 
directories defining other servers elsewhere.

A GloboFS Volume is simply a directory.. somewhere.. locally.

```68d25a11-a34a-4bbb-a29e-c9bd06ff8c53``` is a unique id i've chosen for my 
local test node and ```ea8192ee-593f-437f-af60-90d213995480``` was chosen for a 
remote test node.

Example for local directory ```/srv/globofs/```:

```
self -> 68d25a11-a34a-4bbb-a29e-c9bd06ff8c53
68d25a11-a34a-4bbb-a29e-c9bd06ff8c53/...
ea8192ee-593f-437f-af60-90d213995480 -> /mnt/somewhereelse/globofs/ea8192ee-593f-437f-af60-90d213995480/...
```

Config file: In the works.. so far mostly made up of remote file access gleened 
information.

Example filesystem we want to store in GloboFS:

```
./Photos
./Photos/Trips
./Photos/Trips/Moon
./Photos/Trips/Moon/Photo1.jpg
./Photos/Trips/Moon/Photo2.jpg
./Photos/Trips/Moon/Photo3.jpg
./Photos/Cats
./Photos/Cats/Meowser
./Photos/Cats/Meowser/Photo1.jpg
./Photos/Cats/Meowser/Photo2.jpg
./Videos
./Videos/HowTo
./Videos/HowTo/Fly
./Videos/HowTo/Fly/UsingHotAir.avi
```

The metadata and hashes for Photos/Trips/Moon/Photo1 will be exploded like this:

```
Inode  File
------ ---------------------------------------------------------------------------------------------------------------
767445 ./spool/inbound/ea8192ee-593f-437f-af60-90d213995480/Photos/Trip/Moon/Photo1.jpg/versions/log
768546 ./spool/inbound/ea8192ee-593f-437f-af60-90d213995480/Photos/Trip/Moon/Photo1.jpg/versions/1348096782.553456124
767546 ./spool/outbound/ea8192ee-593f-437f-af60-90d213995480/Photos/Trip/Moon/Photo1.jpg/versions/log
768621 ./spool/outbound/ea8192ee-593f-437f-af60-90d213995480/Photos/Trip/Moon/Photo1.jpg/versions/1348096028.125255438
...
768490 ./root/Photos/Trip/Moon/Photo1.jpg/versions/log
768546 ./root/Photos/Trip/Moon/Photo1.jpg/versions/1348096782.553456124
768621 ./root/Photos/Trip/Moon/Photo1.jpg/versions/1348096028.125255438
...
768570 ./root/Photos/Trip/Moon/Photo1.jpg/hashes/98/ea/6e/4f/216f2fb4b69fff9b3a44842c38686ca685f3f55dc48c5d3fb1107be4
768573 ./root/Photos/Trip/Moon/Photo1.jpg/hashes/50/c3/93/f1/58c3de2db92fa9661bfb00eda5b67c3a777c88524ed3417509631625
768575 ./root/Photos/Trip/Moon/Photo1.jpg/hashes/17/2b/36/ca/b7a022ede944a25629da5a98ea1a45049d92b7b62f734138364ccebc
...
768570 ./hashes/98/ea/6e/4f/216f2fb4b69fff9b3a44842c38686ca685f3f55dc48c5d3fb1107be4
768573 ./hashes/50/c3/93/f1/58c3de2db92fa9661bfb00eda5b67c3a777c88524ed3417509631625
768575 ./hashes/17/2b/36/ca/b7a022ede944a25629da5a98ea1a45049d92b7b62f734138364ccebc
```

The contents of the log files is as follows:
```
cat ./spool/inbound/ea8192ee-593f-437f-af60-90d213995480/Photos/Trip/Moon/Photo1.jpg/versions/log:

1348096782.553456124

cat ./spool/outbound/ea8192ee-593f-437f-af60-90d213995480/Photos/Trip/Moon/Photo1.jpg/versions/log

1348096028.125255438

cat ./root/Photos/Trip/Moon/Photo1.jpg/versions/log

1348096028.125255438
1348096782.553456124
```
The last line of the log file represents the most recent file that lists off 
the hashes in order.. for example:

```
cat 1348096782.553456124

98ea6e4f216f2fb4b69fff9b3a44842c38686ca685f3f55dc48c5d3fb1107be4
50c393f158c3de2db92fa9661bfb00eda5b67c3a777c88524ed3417509631625
172b36cab7a022ede944a25629da5a98ea1a45049d92b7b62f734138364ccebc
```

There are a few places for a collision so to speak.. which can be avoided by 
using a major per node.  For instance the nanoseconds behind the timestamp
1348096782.553456124 can be 1348096782.553456124100 for a major of 100 without 
freaking out the nanosecond timer at all.  This is to be considered for the uber 
paranoid.. however if you have two servers select the same second + nanosecond 
to the 9th decimal place.. you're awesome.

For brevity sake.. the full path for ```Photos/Trip/Moon/Photo1.jpg``` and the 
recent hashes would be ```/srv/globofs/68d25a11-a34a-4bbb-a29e-c9bd06ff8c53/root/Photos/Trip/Moon/Photo1.jpg/versions/log```.

Hard links (vs sym links) are used to allow us to do reference counting on 
demand.  The hashes in the Photo direcory are hard linked to a primary hash 
directory that will be shared by all files.  These can also be compressed.

Versioning is not yet a requirement.. however it is useful when we may plan to 
send deltas of hash data.

There may be the potential of storing a log file per hash in order to reduce 
hard link requirements on filesystems that don't support many hard links per 
directory... however the chances of having 200+ hashes 8 chars in to it is 
substantially low.  It's still a race condition.

Double referencing seems like a good option using log files to help with that 
and it won't increase storage size that much since lots of data will fit into a 
single filesystem block.
