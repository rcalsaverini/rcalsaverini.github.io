Q = /usr/local/bin/quarto
SOURCES := $(shell find . -name '*.qmd')
OBJECTS := $(patsubst %.qmd, %.md, $(SOURCES))
DIRECTORIES := $(patsubst %.qmd, %_files, $(SOURCES))
FINAL_OBJECTS = $(patsubst ./%, ../blog/%, $(OBJECTS))
FINAL_DIRECTORIES = $(patsubst ./%, ../blog/%, $(DIRECTORIES))


all: $(FINAL_OBJECTS) $(FINAL_DIRECTORIES)

clean:
	rm -rf $(DIRECTORIES)
	rm $(OBJECTS)
	rm -rf $(FINAL_DIRECTORIES)
	rm $(FINAL_OBJECTS)

%.md: %.qmd
	$Q render $<

%_files: %.qmd
	$Q render $<

../blog/%.md: %.md
	mv $< $@

../blog/%_files: %_files
	mv $< $@
