LATEX=pdflatex
LATEXMK=latexmk
LATEXOPT=-file-line-error


MAIN=main
SOURCES=$(MAIN).tex Makefile refs.bib *.tex 
FIGURES := #$(shell ls fig/*.pdf)

all:    $(MAIN).pdf

.refresh:
	touch .refresh

$(MAIN).pdf: $(MAIN).tex .refresh $(FIGURES) $(SOURCES) interpolation_results
	$(LATEXMK) -pvc -pdf $(MAIN).tex

interpolation_results: plot_interpolation_results.py
	python3 plot_interpolation_results.py

force:
	touch .refresh
	$(MAKE) $(MAIN).pdf

.PHONY: clean force all

clean:
	$(LATEXMK) -C $(MAIN).tex
	rm -f $(MAIN).pdfsync
	rm -rf *~ *.tmp

