# SFTPY

SFTP server automated with python scripts.

## How it works


Firstly the container will create the users based on `/opt/sftpy/conf/users.conf`. All the user's content will be 
stored in it's home folder.

Secondly the container will create any desired shared folder found in `/opt/sftpy/conf/folders.conf`.
This kind of shared folder is ideal to share content among user. The folder is created with it own GUID
and the designated users with participate of that GUID. The shared bolder will be 
`mount --bind /home/{user}/{shared} /data/{shared}` into the user's home.

It is necessary to run the container with SYS_ADMIN capability so the `mount --bind` works properly.

## Usage

+ Define the `/opt/sftpy/conf/users.conf` with the desired users;
+ [optional] Define the `/opt/sftpy/conf/folders.conf` with some shared folders;

## Examples

### Example 01

This example creates tree users `user01`, `user02` and `user03`. Notice that for `user02` the UID is defined. 
In the shared folder file is defined the `/foo` and `/bar` folders wich are create at `/data`.

```
user01:pass01
user02:pass02:3128
```

```
5000:/foo
5000:user01,user02

5001:/bar
5001:user02
```
