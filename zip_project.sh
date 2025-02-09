#!/bin/bash

# Define variables for the parent directory and output zip file.
PARENT_DIR="spelling-corrector"
OUTPUT_ZIP="2mi0700130.zip"

# Remove any existing zip file.
if [ -f "$OUTPUT_ZIP" ]; then
  echo "Removing existing $OUTPUT_ZIP..."
  rm "$OUTPUT_ZIP"
fi

# Remove the parent directory if it already exists.
if [ -d "$PARENT_DIR" ]; then
  echo "Removing existing directory $PARENT_DIR..."
  rm -rf "$PARENT_DIR"
fi

# Create the parent directory.
mkdir "$PARENT_DIR"

# Function to copy directories with exclusions.
copy_dir() {
  local dir=$1
  local extra_exclude=$2  # Optional extra exclude pattern.
  if [ -d "$dir" ]; then
    echo "Copying directory: $dir"
    if [ -n "$extra_exclude" ]; then
      rsync -av --exclude='__pycache__' --exclude="$extra_exclude" "$dir" "$PARENT_DIR"/
    else
      rsync -av --exclude='__pycache__' "$dir" "$PARENT_DIR"/
    fi
  else
    echo "Directory $dir does not exist, skipping."
  fi
}

# Copy src, api, and web directories.
copy_dir "src"
copy_dir "api"
copy_dir "web"

# Copy tests directory while excluding the mocks folder.
copy_dir "tests" "mocks"

# Copy additional files from the project root.
for file in README requirements.txt .pytest.ini; do
  if [ -f "$file" ]; then
    echo "Copying file: $file"
    cp "$file" "$PARENT_DIR"/
  else
    echo "File $file not found, skipping."
  fi
done

# Create the zip archive of the parent directory.
echo "Creating zip archive $OUTPUT_ZIP from $PARENT_DIR..."
zip -r "$OUTPUT_ZIP" "$PARENT_DIR"

# Remove the parent directory.
echo "Removing directory $PARENT_DIR..."
rm -rf "$PARENT_DIR"

echo "Archive $OUTPUT_ZIP created successfully."