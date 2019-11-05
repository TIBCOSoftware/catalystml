SRCDIR=src
SPECVERSION=$(cat ../../current.txt)

cmlmaker.py: opsclasses.py $(SRCDIR)/base_cmlmaker.py ../../versions/$(SPECVERSION)/operations/*/*
	cat $(SRCDIR)/base_cmlmaker.py>cmlmaker.py;cat $(SRCDIR)/opsclasses.py>>cmlmaker.py

opsclasses.py: $(SRCDIR)/creating_operations_classes.py
	cd $(SRCDIR); python creating_operations_classes.py

clean:
	rm -f cmlmaker.py $(SRCDIR)/opsclasses.py 
