SPHINX_DIR       = docs/writer
SPHINX_BUILD_DIR = $(SPHINX_DIR)/_build/html
DESTINATION_DIR  = docs

.PHONY: all clean build copy

# Default target: clean, build, and copy
all: clean build copy

# Clean up generated files in docs/writer
clean:
	@echo "Cleaning Sphinx output in $(SPHINX_DIR)..."
	@cd $(SPHINX_DIR) && make clean

# Build the Sphinx HTML documentation
build:
	@echo "Building Sphinx HTML in $(SPHINX_DIR)..."
	@cd $(SPHINX_DIR) && make html

# Copy the built HTML files to the top-level docs/ directory
copy:
	@echo "Copying HTML from $(SPHINX_BUILD_DIR) to $(DESTINATION_DIR)..."
	@mkdir -p $(DESTINATION_DIR)
	@cp -r $(SPHINX_BUILD_DIR)/* $(DESTINATION_DIR)/
	@touch docs/.nojekyll
	@echo "Documentation copied to $(DESTINATION_DIR)"
