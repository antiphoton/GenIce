BASE=../..
GENICE=$(BASE)/genice.x
UTIL=.
REFD=ref
.DELETE_ON_ERROR:

all: test1.done   test2.done   test3.done   test4.done   test_2d.gro
all: test_3.ar3a  test_4.ngph  test_5.nx3a  test_6.gro   test_7.mdv
all: test_12.scad test_16.py   test_17.nx4a test_1c.ar3r test_CS1.cif
all: test_CS2.cif test_HS1.xyz test_TS1.yap test_2dL.gro
#all: test19.done
all: test_1hreshape.py test_2D3.ringtest test_prism7.ringtest
all: test_3xFAU.yap
all: test_T.pov

clean:
	-rm test* *~
	-rm -rf sort_tmp


test1.done:
	$(GENICE) test1 --guest 12=g12 --rep 1 1 1 --debug > /dev/null
	touch test1.done
test2.done:
	$(GENICE) test2 --guest 12=g12 --rep 1 1 1 --debug > /dev/null
	touch test2.done
test3.done:
	$(GENICE) test3 --guest 12=g12 --rep 1 1 1 --debug > /dev/null
	touch test3.done
test4.done:
	$(GENICE) test4 --guest 12=g12 --rep 1 1 1 --debug > /dev/null
	touch test4.done
test_2d.gro:
	$(GENICE) 2d --rep 2 2 3 > $@                                   ;diff $(REFD)/$@ $@
test_3.ar3a:
	$(GENICE) 3  --rep 2 2 3 --format c > $@                        ;diff $(REFD)/$@ $@
test_4.ngph:
	$(GENICE) 4  --rep 2 2 3 --format d > $@                        ;diff $(REFD)/$@ $@
test_5.nx3a:
	$(GENICE) 5  --rep 2 2 3 --format e > $@                        ;diff $(REFD)/$@ $@
test_6.gro:
	$(GENICE) 6  --rep 2 2 4 --format g > $@                        ;diff $(REFD)/$@ $@
test_7.mdv:
	$(GENICE) 7  --rep 2 2 4 --format m > $@                        ;diff $(REFD)/$@ $@
test_12.scad:
	$(GENICE) 12 --rep 2 2 3 --format o > $@                        ;diff $(REFD)/$@ $@
test_16.py:
	$(GENICE) 16 --rep 1 1 2 --format p > $@                        ;diff $(REFD)/$@ $@
test_17.nx4a:
	$(GENICE) 17 --rep 1 1 2 --format q > $@                        ;diff $(REFD)/$@ $@
test_1c.ar3r:
	$(GENICE) 1c --rep 1 1 2 --format r > $@                        ;diff $(REFD)/$@ $@
test_CS1.cif:
	$(GENICE) CS1 --guest 14=g14*0.5 -G 0=me --rep 1 1 2 --format cif > $@ ;diff $(REFD)/$@ $@
test_CS2.cif:
	$(GENICE) CS2 --nodep -c 0=Na -a 1=Cl --rep 1 1 2 --format cif2 > $@  ;$(UTIL)/cifdiff.sh $(REFD)/$@ $@
test_HS1.xyz:
#test for spot semiclathrate (TBAB)
	$(GENICE) HS1 --nodep -c 3=N -a 1=Br -H 11=Bu-:3 -H 23=Bu-:3 -H 13=Bu-:3 -H 7=Bu-:3 --rep 1 1 2 --format xyz > $@; diff $(REFD)/$@ $@
test_TS1.yap:
	$(GENICE) TS1 --guest 12=g12 --rep 1 1 2 --format yaplot > $@ ;diff $(REFD)/$@ $@
test_T.pov:
	$(GENICE) T --guest 12=g12 --rep 1 1 1 --format povray > $@   ;diff $(REFD)/$@ $@
test_2dL.gro:
	$(GENICE) 2d --rep 8 8 8 > $@
test_1hreshape.py:
	$(GENICE) 1h --rep 1 1 1 --format reshape[1,1,-2,1,-1,0,1,1,1] > $@ ;diff $(REFD)/$@ $@
test_2D3.ringtest:
	$(GENICE) 2D3 --rep 5 5 1 --format _ring > $@                ;diff $(REFD)/$@ $@
test_prism7.ringtest:
	$(GENICE) prism[7] --rep 1 1 1 --format _ring > $@           ;diff $(REFD)/$@ $@
test_3xFAU.yap:
	$(GENICE) xFAU[3] --rep 1 1 1 --format yaplot > $@           ;diff $(REFD)/$@ $@
