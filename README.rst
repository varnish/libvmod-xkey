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

    # Example of purging using xkey:
    # The key to be purged is gotten from the xkey-purge header
    sub vcl_recv {
        if (req.http.xkey-purge) {
            if (xkey.purge(req.http.xkey-purge) != 0) {
                return (synth(200, "Purged"));
            } else {
                return (synth(404, "Key not found"));
            }
        }
    }

    # The backend is responsible for setting the header.
    # If you where to do it in VCL it will look something like this:
    sub vcl_backend_response {
        # Use the header vmod to add multiple headers for multiple keys
        set beresp.http.xkey = "purgeable_hash_key";
    }


DESCRIPTION
===========

This vmod adds one or more secondary hashes to objects, allowing fast purging
on all objects with this/these hash key/s.
Hash keys have to be separated by one or more "space" characters.
Space characters: {' ', '\n', '\t', '\v', '\f', '\r'}.

You can use this to indicate relationships, a bit like a "tag". Then
clear out all object that have this tag set. Two good use cases are
news sites, where one might add all the stories mentioned on a
particular page by article ID, letting each article referenced create
a xkey header.

Similarly with a ecommerce site, where various SKUs are often
referenced on a page.


Example use 1
-------------

On a ecommerce site with we have the backend application issue a
xkey header for every product that is referenced on that page. So
the header for a certain page might look like this:::

    HTTP/1.1 OK
    Server: Apache/2.2.15
    Via: varnish (v4)
    X-Varnish: 23984723 23231323
    xkey: 8155054
    xkey: 166412
    xkey: 234323

This requires a bit of VCL to be in place. The VCL can be found above.

Then, in order to keep the web in sync with the database, a trigger is
set up in the database. When an SKU is updated this will trigger a
HTTP request towards the Varnish server, clearing out every object
with the matching xkey header.::

    GET / HTTP/1.1
    Host: www.example.com
    xkey-purge: 166412

Note the xkey-purge header. It is probably a good idea to protect
this with an ACL so random people from the Internet can't purge your
cache.

Varnish will find the objects and clear them out. Responding to the response.::

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

	Purges all the objects that was hashed on the given
	key. Returns the number of objects that was purged.

INSTALLATION
============

The module can be installed using standard autotools::

    ./autogen.sh
    ./configure
    make
    make install

Header files must be installed.


COPYRIGHT
=========

This document is licensed under the same license as the
libvmod-xkey project. See LICENSE for details.

* Copyright (c) 2013-2015 Varnish Software
