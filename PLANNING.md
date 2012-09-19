GloboFS Planning
================

Push/Pull
---------
Changes on remote sites are pushed inward into upstream logs style files using 
append 
mode.

Access to hashes that don't exist locally are pulled inward as needed.

You should be able to `cat **/* > /dev/null` to create a mirror of the entire 
volume.  Helper tools will be provided via the globofs script.

Assume Nothing Style
--------------------

We 'require' a few things.. but assume nothing.

Things we require:

- Python

- Access to symlinks on the local filesystem (for now)

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

There should be a "local" directory always containing locally cached hashes as 
well as a copy of the local metadata.  In the same directory are directories 
defining other servers elsewhere. "local" should be user defined.

A GloboFS Volume is simply a directory.. somewhere.. locally.

Example:

- GloboFS Volume Directory
  - local
  - server01.alaska.example.com
  - server01.idaho.example.com
  - server03.hawaii.example.com

Each directory will have a small config file named "config" that has a very 
simple syntax.

Example:

- local

  - config

```python
uuid=68d25a11-a34a-4bbb-a29e-c9bd06ff8c53
path=/srv/globofs_volume/ #So that we can just specify a config
cacheonly=no
cachetime=30m
```
- server01.alaska.example.com

  - config

```python
uuid=ea8192ee-593f-437f-af60-90d213995480
path=/network/remote/server01.alaska/srv/globofs_volume/
```
The following requires a bit of an example tree structure

- File System
  - Photos
    - Trips
      - Moon
        - Photo1
        - Photo2
        - Photo3
    - Cats
      - Photo1
      - Photo2
      - Photo3
  - Spreadsheets
    - Spreadsheet1

The metadata and hashes for Photos/Trips/Moon/Photo1 will be exploded like this:

- GloboFS Volume
  - local
    - root
      - Photos
        - Trips
          - Moon
            - Photo1
              - versions
                - latest (not a symlink)
                - 1348096774.177556349
                - 1348095423.553456124
              - hashes
                  - 98
                    - ea
                      - 6e4f216f2fb4b69fff9b3a44842c38686ca685f3f55dc48c5d3fb1107be4.gz    
                  - 50
                    - c3
                      - 93f158c3de2db92fa9661bfb00eda5b67c3a777c88524ed3417509631625.gz
                  - 17
                    - 2b
                      - 36cab7a022ede944a25629da5a98ea1a45049d92b7b62f734138364ccebc.gz
                  - ...
    - hashes
      - 98
        - ea
          - 6e4f216f2fb4b69fff9b3a44842c38686ca685f3f55dc48c5d3fb1107be4.gz    
      - 50
        - c3
          - 93f158c3de2db92fa9661bfb00eda5b67c3a777c88524ed3417509631625.gz
      - 17
        - 2b
          - 36cab7a022ede944a25629da5a98ea1a45049d92b7b62f734138364ccebc.gz
      - ...
    - upstream
      - ea8192ee-593f-437f-af60-90d213995480
        - updates
            - latest
            - 1348096028.125255438
        
