GloboFS Planning
================

Assume Nothing Style
--------------------

We 'require' a few things.. but assume nothing.

Things we require:

- Python

- Access to hard links on the local filesystem (for now)

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

Hashing use
-----------

SHA256 will be used for hashing data blocks.  Blocks will be set to an arbitrary 
size based on configuration information.

Directory Structure
-------------------
