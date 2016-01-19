=========
vmod_xkey
=========

------------------------------------
Varnish surrogate keys Module (xkey)
------------------------------------

:Author: Martin Blix Grydeland, Per Buer
:Date: 2015-09-30
:Version: 1.0
:Manual section: 3

SYNOPSIS
========

::

    import xkey;

    # Example of purging using xkey.
    #
    # The key to be purged is specified in the xkey-purge header.
    sub vcl_recv {
        if (req.http.xkey-purge) {
            if (xkey.purge(req.http.xkey-purge) != 0) {
                return (synth(200, "Purged"));
            } else {
                return (synth(404, "Key not found"));
            }
        }
    }

    # Normally the backend is responsible for setting the header.
    # If you were to do it in VCL it will look something like this:
    sub vcl_backend_response {
        set beresp.http.xkey = "purgeable_hash_key1 purgeable_hash_key2";
    }


DESCRIPTION
===========

This vmod adds secondary hashes to objects, allowing fast purging on
all objects with this hash key.

You can use this to indicate relationships, a bit like a "tag". Then
clear out all object that have this tag set. Two good use cases are
news sites, where one might add all the stories mentioned on a
particular page by article ID, letting each article referenced create
an xkey header.

Similarly with an e-commerce site, where various SKUs are often
referenced on a page.

Hash keys are specified in the ``xkey`` response header. Multiple keys
can be specified per header line with a space
separator. Alternatively, they can be specified in multiple ``xkey``
response headers.

Preferably the secondary hash keys are set from the backend
application, but can also be set from VCL in ``vcl_backend_response``
as in the above example.

Example
-------

On an e-commerce site we have the backend application issue an xkey
header for every product that is referenced on that page. So the
header for a certain page might look like this::

    HTTP/1.1 OK
    Server: Apache/2.2.15
    xkey: 8155054
    xkey: 166412
    xkey: 234323

This requires a bit of VCL to be in place. The VCL can be found above.

Then, in order to keep the web in sync with the database, a trigger is
set up in the database. When an SKU is updated this will trigger an
HTTP request towards the Varnish server, clearing out every object
with the matching xkey header::

    GET / HTTP/1.1
    Host: www.example.com
    xkey-purge: 166412

Note the xkey-purge header. It is probably a good idea to protect
this with an ACL so random people from the Internet cannot purge your
cache.

Varnish will find the objects and clear them out, responding with::

    HTTP/1.1 200 Purged
    Date: Thu, 24 Apr 2014 17:08:28 GMT
    X-Varnish: 1990228115
    Via: 1.1 Varnish

The objects are now cleared.


FUNCTIONS
=========

purge
-----

Prototype
	::

	   purge(STRING S)

Return value
	INT

Description

	Purges all objects hashed on the given key. Returns the number
	of objects that were purged.

softpurge
---------

Prototype
	::

	   softpurge(STRING S)

Return value
	INT

Description

	Performs a "soft purge" for all objects hashed on the given
	key. Returns the number of objects that were purged.

	A softpurge differs from a regular purge in that it resets an
	object's TTL but keeps it available for grace mode and conditional
	requests for the remainder of its configured grace and keep time.

INSTALLATION
============

The module can be installed on latest Varnish Cache using standard autotools::

    ./configure
    make
    make install

Header files must be installed.

This module is made to work on the latest released Varnish Cache version.
Support for older versions is explicitly not a priority.


COPYRIGHT
=========

This document is licensed under the same license as the
libvmod-xkey project. See LICENSE for details.

* Copyright (c) 2015 Varnish Software Group
