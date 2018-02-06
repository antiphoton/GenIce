BASE=../..
GENICE=$(BASE)/genice.x
UTIL=.
REFD=ref

all: test1.done test2.done test3.done test4.done test5.done
all: test6.done test7.done test8.done test9.done test10.done
all: test11.done test12.done test13.done test14.done test15.done
all: test16.done test17.done test18.done
#all: test19.done
all: test_tsl.done
all: test20.done 
all: test22.done test23.done 

clean:
	-rm *.done *~
	-rm -rf trash sort_tmp


test1.done:
	-mkdir trash
	$(GENICE) test1 --guest 12=g12 --rep 1 1 1 --debug > /dev/null
	touch test1.done
test2.done:
	-mkdir trash
	$(GENICE) test2 --guest 12=g12 --rep 1 1 1 --debug > /dev/null
	touch test2.done
test3.done:
	-mkdir trash
	$(GENICE) test3 --guest 12=g12 --rep 1 1 1 --debug > /dev/null
	touch test3.done
test4.done:
	-mkdir trash
	$(GENICE) test4 --guest 12=g12 --rep 1 1 1 --debug > /dev/null
	touch test4.done
test5.done:
	-mkdir trash
	$(GENICE) 2d --rep 2 2 3 > trash/2d.gro                                   ;diff $(REFD)/2d.gro trash/2d.gro
	touch test5.done
test6.done:
	-mkdir trash
	$(GENICE) 3  --rep 2 2 3 --format c > trash/3.ar3a                        ;diff $(REFD)/3.ar3a trash/3.ar3a
	touch test6.done
test7.done:
	-mkdir trash
	$(GENICE) 4  --rep 2 2 3 --format d > trash/4.ngph                        ;diff $(REFD)/4.ngph trash/4.ngph
	touch test7.done
test8.done:
	-mkdir trash
	$(GENICE) 5  --rep 2 2 3 --format e > trash/5.nx3a                        ;diff $(REFD)/5.nx3a trash/5.nx3a
	touch test8.done
test9.done:
	-mkdir trash
	$(GENICE) 6  --rep 2 2 4 --format g > trash/6.gro                         ;diff $(REFD)/6.gro  trash/6.gro
	touch test9.done
test10.done:
	-mkdir trash
	$(GENICE) 7  --rep 2 2 4 --format m > trash/7.mdv                         ;diff $(REFD)/7.mdv  trash/7.mdv
	touch test10.done
test11.done:
	-mkdir trash
	$(GENICE) 12 --rep 2 2 3 --format o > trash/12.scad                       ;diff $(REFD)/12.scad trash/12.scad
	touch test11.done
test12.done:
	-mkdir trash
	$(GENICE) 16 --rep 1 1 2 --format p > trash/16.py                         ;diff $(REFD)/16.py  trash/16.py
	touch test12.done
test13.done:
	-mkdir trash
	$(GENICE) 17 --rep 1 1 2 --format q > trash/17.nx4a                       ;diff $(REFD)/17.nx4a trash/17.nx4a
	touch test13.done
test14.done:
	-mkdir trash
	$(GENICE) 1c --rep 1 1 2 --format r > trash/1c.ar3r                       ;diff $(REFD)/1c.ar3r trash/1c.ar3r
	touch test14.done
test15.done:
	-mkdir trash
	$(GENICE) CS1 --guest 14=g14*0.5 -G 0=me --rep 1 1 2 --format cif > trash/CS1.cif     ;diff $(REFD)/CS1.cif trash/CS1.cif
	touch test15.done
test16.done:
	-mkdir trash
	$(GENICE) CS2 --nodep -c 0=Na -a 1=Cl --rep 1 1 2 --format cif2 > trash/CS2.cif    ;$(UTIL)/cifdiff.sh $(REFD)/CS2.cif trash/CS2.cif
	touch test16.done
test17.done:
	-mkdir trash
#test for spot semiclathrate (TBAB)
	$(GENICE) HS1 --nodep -c 3=N -a 1=Br -H 11=Bu-:3 -H 23=Bu-:3 -H 13=Bu-:3 -H 7=Bu-:3 --rep 1 1 2 --format xyz > trash/HS1.xyz; diff $(REFD)/HS1.xyz trash/HS1.xyz
	touch test17.done
test18.done:
	-mkdir trash
	$(GENICE) TS1 --guest 12=g12 --rep 1 1 2 --format yaplot > trash/TS1.yap  ;diff $(REFD)/TS1.yap trash/TS1.yap
	touch test18.done
test19.done:
	-mkdir trash
	$(GENICE) T --guest 12=g12 --rep 1 1 1 --format povray > trash/T.pov  ;diff $(REFD)/T.pov trash/T.pov
	touch test19.done
test20.done:
	-mkdir trash
	$(GENICE) 2d --rep 8 8 8 > trash/2dL.gro
	touch test20.done
test22.done:
	-mkdir trash
	$(GENICE) 1h --rep 1 1 1 --format reshape[1,1,-2,1,-1,0,1,1,1] > trash/1hreshape.py  ;diff $(REFD)/1hreshape.py trash/1hreshape.py
	touch test22.done
test_tsl.done:
	-mkdir trash
	$(GENICE) 2D3 --rep 5 5 1 --format _ring > trash/2D3.ringtest  ;diff $(REFD)/2D3.ringtest trash/2D3.ringtest
	touch test_tsl.done
test23.done:
	-mkdir trash
	$(GENICE) prism[7] --rep 1 1 1 --format _ring > trash/prism7.ringtest  ;diff $(REFD)/prism7.ringtest trash/prism7.ringtest
	touch test23.done