AM_CPPFLAGS = @VMOD_INCLUDES@ -Wall -Werror

vmoddir = @VMOD_DIR@
vmod_LTLIBRARIES = libvmod_xkey.la

libvmod_xkey_la_LDFLAGS = -module -export-dynamic -avoid-version -shared

libvmod_xkey_la_SOURCES = \
	vcc_if.c \
	vcc_if.h \
	vmod_xkey.c \
	vtree.h

VTC_LOG_COMPILER = $(VARNISHTEST) -v -i \
	-Dvarnishd=$(VARNISHD) -Dvmod_topbuild=$(abs_top_builddir)
TEST_EXTENSIONS = .vtc
TESTS = @VMOD_TESTS@

BUILT_SOURCES = vcc_if.c vcc_if.h

vcc_if.c vcc_if.h: @VMODTOOL@ $(top_srcdir)/src/vmod_xkey.vcc
	@VMODTOOL@ $(top_srcdir)/src/vmod_xkey.vcc

EXTRA_DIST = \
	vmod_xkey.vcc \
	$(TESTS)

CLEANFILES = $(builddir)/vcc_if.c \
	$(builddir)/vcc_if.h \
	$(builddir)/vmod_xkey.man.rst \
	$(builddir)/vmod_xkey.rst
