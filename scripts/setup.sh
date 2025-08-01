#!/bin/bash
# Setup script for AI Image Generation project
# Initializes directory structure and environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="$PROJECT_ROOT/output"
SESSIONS_DIR="$OUTPUT_DIR/sessions"
TEMP_DIR="$OUTPUT_DIR/temp"
ARCHIVE_DIR="$OUTPUT_DIR/archive"
DOCS_DIR="$PROJECT_ROOT/docs"

# Default values
VERBOSE=false
FORCE=false

# Help function
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Setup script for AI Image Generation project"
    echo ""
    echo "OPTIONS:"
    echo "  -f, --force         Force recreation of existing directories"
    echo "  -v, --verbose       Show detailed output"
    echo "  -h, --help          Show this help message"
    echo ""
    echo "EXAMPLES:"
    echo "  $0                    # Setup project structure"
    echo "  $0 -f                # Force recreation of directories"
    echo "  $0 -v                # Verbose output"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--force)
            FORCE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}🔍 $1${NC}"
    fi
}

# Create directory structure
create_directories() {
    log_info "Creating directory structure..."
    
    # Main output directories
    local dirs=(
        "$OUTPUT_DIR"
        "$SESSIONS_DIR"
        "$TEMP_DIR"
        "$ARCHIVE_DIR"
        "$DOCS_DIR/guides"
        "$DOCS_DIR/api"
    )
    
    for dir in "${dirs[@]}"; do
        if [ -d "$dir" ] && [ "$FORCE" = true ]; then
            log_verbose "Removing existing directory: $dir"
            rm -rf "$dir"
        fi
        
        if [ ! -d "$dir" ]; then
            log_verbose "Creating directory: $dir"
            mkdir -p "$dir"
            log_success "Created: $dir"
        else
            log_verbose "Directory already exists: $dir"
        fi
    done
}

# Create .gitkeep files
create_gitkeep_files() {
    log_info "Creating .gitkeep files..."
    
    local gitkeep_dirs=(
        "$TEMP_DIR"
        "$ARCHIVE_DIR"
        "$DOCS_DIR/guides"
        "$DOCS_DIR/api"
    )
    
    for dir in "${gitkeep_dirs[@]}"; do
        local gitkeep_file="$dir/.gitkeep"
        if [ ! -f "$gitkeep_file" ]; then
            log_verbose "Creating .gitkeep: $gitkeep_file"
            touch "$gitkeep_file"
        fi
    done
}

# Create README files
create_readme_files() {
    log_info "Creating README files..."
    
    # Output directory README
    local output_readme="$OUTPUT_DIR/README.md"
    if [ ! -f "$output_readme" ]; then
        cat > "$output_readme" << 'EOF'
# Output Directory

This directory contains all generated outputs from the AI Image Generation project.

## Structure

- `sessions/` - Session-based outputs organized by timestamp
- `temp/` - Temporary files (auto-cleanup)
- `archive/` - Archived important results

## Sessions

Each session contains:
- `products/` - Downloaded product images
- `composites/` - Composite layouts
- `final_designs/` - Generated final designs
- `analysis/` - Analysis results
- `shopping_lists/` - Generated shopping lists
- `debug/` - Debug outputs

## Cleanup

Use `scripts/cleanup.sh` to manage old sessions and temporary files.
EOF
        log_success "Created: $output_readme"
    fi
    
    # Archive directory README
    local archive_readme="$ARCHIVE_DIR/README.md"
    if [ ! -f "$archive_readme" ]; then
        cat > "$archive_readme" << 'EOF'
# Archive Directory

This directory contains archived important results and designs.

## Usage

- Copy important sessions here for long-term storage
- Use descriptive names for archived sessions
- This directory is not automatically cleaned up

## Example

```bash
# Archive a session
cp -r output/sessions/2025-07-31_14-30-00 output/archive/bohemian_living_room_design
```
EOF
        log_success "Created: $archive_readme"
    fi
}

# Update .gitignore
update_gitignore() {
    log_info "Updating .gitignore..."
    
    local gitignore_file="$PROJECT_ROOT/.gitignore"
    local gitignore_content="
# Output directories
output/sessions/*/
output/temp/*
!output/sessions/.gitkeep
!output/temp/.gitkeep

# Keep only important archives
output/archive/*
!output/archive/README.md

# Session-specific files
**/serpapi_product_*.jpg
**/composite_layout_*.png
**/real_products_overlay_design_*.png
**/design_results.json
**/analysis_results.json

# Debug outputs
debug_output_*/
**/debug_*.png
**/debug_*.jpg
**/debug_*.json

# Temporary files
*.tmp
*.temp
*_temp.*
"
    
    # Check if gitignore already has output patterns
    if ! grep -q "output/sessions" "$gitignore_file" 2>/dev/null; then
        log_verbose "Adding output patterns to .gitignore"
        echo "$gitignore_content" >> "$gitignore_file"
        log_success "Updated: $gitignore_file"
    else
        log_verbose ".gitignore already contains output patterns"
    fi
}

# Test session manager
test_session_manager() {
    log_info "Testing session manager..."
    
    local test_script="$PROJECT_ROOT/src/utils/session_manager.py"
    if [ -f "$test_script" ]; then
        log_verbose "Running session manager test..."
        cd "$PROJECT_ROOT"
        python3 "$test_script" 2>/dev/null && log_success "Session manager test passed" || log_warning "Session manager test failed (this is normal if dependencies aren't installed)"
    else
        log_warning "Session manager script not found: $test_script"
    fi
}

# Show setup summary
show_summary() {
    log_info "Setup Summary:"
    echo ""
    echo "📁 Directory Structure:"
    echo "  $OUTPUT_DIR/"
    echo "  ├── sessions/     # Session-based outputs"
    echo "  ├── temp/         # Temporary files"
    echo "  └── archive/      # Archived results"
    echo ""
    echo "📚 Documentation:"
    echo "  $DOCS_DIR/"
    echo "  ├── guides/       # How-to guides"
    echo "  └── api/          # API documentation"
    echo ""
    echo "🔧 Scripts:"
    echo "  scripts/cleanup.sh    # Cleanup utility"
    echo "  scripts/setup.sh      # This setup script"
    echo ""
    echo "📋 Next Steps:"
    echo "  1. Update your code to use SessionManager"
    echo "  2. Run cleanup script: ./scripts/cleanup.sh"
    echo "  3. Test with a sample session"
}

# Main execution
main() {
    log_info "Setting up AI Image Generation project structure..."
    log_verbose "Project root: $PROJECT_ROOT"
    log_verbose "Force mode: $FORCE"
    
    create_directories
    create_gitkeep_files
    create_readme_files
    update_gitignore
    test_session_manager
    
    echo ""
    show_summary
    echo ""
    log_success "Setup completed successfully!"
}

# Run main function
main "$@" 