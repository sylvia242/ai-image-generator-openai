#!/bin/bash
# Cleanup script for AI Image Generation project
# Manages old sessions, temporary files, and archives

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

# Default values
DAYS_TO_KEEP=30
DRY_RUN=false
VERBOSE=false

# Help function
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Cleanup script for AI Image Generation project"
    echo ""
    echo "OPTIONS:"
    echo "  -d, --days N        Keep sessions for N days (default: 30)"
    echo "  -n, --dry-run       Show what would be deleted without actually deleting"
    echo "  -v, --verbose       Show detailed output"
    echo "  -h, --help          Show this help message"
    echo ""
    echo "EXAMPLES:"
    echo "  $0                    # Clean up sessions older than 30 days"
    echo "  $0 -d 7              # Clean up sessions older than 7 days"
    echo "  $0 -n                # Show what would be cleaned (dry run)"
    echo "  $0 -v                # Verbose output"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--days)
            DAYS_TO_KEEP="$2"
            shift 2
            ;;
        -n|--dry-run)
            DRY_RUN=true
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

# Check if directories exist
check_directories() {
    if [ ! -d "$OUTPUT_DIR" ]; then
        log_error "Output directory does not exist: $OUTPUT_DIR"
        exit 1
    fi
    
    if [ ! -d "$SESSIONS_DIR" ]; then
        log_warning "Sessions directory does not exist: $SESSIONS_DIR"
        return 1
    fi
}

# Clean up old sessions
cleanup_old_sessions() {
    log_info "Cleaning up sessions older than $DAYS_TO_KEEP days..."
    
    if [ ! -d "$SESSIONS_DIR" ]; then
        log_warning "No sessions directory found"
        return
    fi
    
    local cleaned_count=0
    local total_size=0
    
    # Find old session directories
    while IFS= read -r -d '' session_dir; do
        if [ -d "$session_dir" ] && [ "$(basename "$session_dir")" != "latest" ]; then
            local session_name=$(basename "$session_dir")
            local session_age=$(stat -f%m "$session_dir" 2>/dev/null || stat -c%Y "$session_dir" 2>/dev/null || echo 0)
            local current_time=$(date +%s)
            local age_in_days=$(( (current_time - session_age) / 86400 ))
            
            if [ $age_in_days -gt $DAYS_TO_KEEP ]; then
                local session_size=$(du -sk "$session_dir" | cut -f1)
                total_size=$((total_size + session_size * 1024))
                
                if [ "$DRY_RUN" = true ]; then
                    log_verbose "Would delete: $session_name (${age_in_days} days old, ${session_size}KB)"
                else
                    log_verbose "Deleting: $session_name (${age_in_days} days old, ${session_size}KB)"
                    rm -rf "$session_dir"
                fi
                cleaned_count=$((cleaned_count + 1))
            fi
        fi
    done < <(find "$SESSIONS_DIR" -maxdepth 1 -type d -print0)
    
            if [ $cleaned_count -gt 0 ]; then
            if [ "$DRY_RUN" = true ]; then
                log_warning "Would clean $cleaned_count sessions ($(($total_size / 1024))KB)"
            else
                log_success "Cleaned $cleaned_count sessions ($(($total_size / 1024))KB)"
            fi
        else
            log_info "No old sessions found to clean"
        fi
}

# Clean up temporary files
cleanup_temp_files() {
    log_info "Cleaning up temporary files..."
    
    if [ ! -d "$TEMP_DIR" ]; then
        log_warning "No temp directory found"
        return
    fi
    
    local temp_count=0
    local temp_size=0
    
    while IFS= read -r -d '' temp_file; do
        if [ "$(basename "$temp_file")" != ".gitkeep" ]; then
            local file_size=$(stat -f%z "$temp_file" 2>/dev/null || stat -c%s "$temp_file" 2>/dev/null || echo 0)
            temp_size=$((temp_size + file_size))
            
            if [ "$DRY_RUN" = true ]; then
                log_verbose "Would delete: $(basename "$temp_file") (${file_size}B)"
            else
                log_verbose "Deleting: $(basename "$temp_file") (${file_size}B)"
                rm -f "$temp_file"
            fi
            temp_count=$((temp_count + 1))
        fi
    done < <(find "$TEMP_DIR" -type f -print0)
    
            if [ $temp_count -gt 0 ]; then
            if [ "$DRY_RUN" = true ]; then
                log_warning "Would clean $temp_count temp files ($(($temp_size / 1024))KB)"
            else
                log_success "Cleaned $temp_count temp files ($(($temp_size / 1024))KB)"
            fi
        else
            log_info "No temporary files found to clean"
        fi
}

# Show disk usage
show_disk_usage() {
    log_info "Current disk usage:"
    
    if [ -d "$OUTPUT_DIR" ]; then
        echo "📊 Output directory usage:"
        du -sh "$OUTPUT_DIR"/* 2>/dev/null || echo "  No output directories found"
        
        if [ -d "$SESSIONS_DIR" ]; then
            echo ""
            echo "📁 Sessions:"
            find "$SESSIONS_DIR" -maxdepth 1 -type d -exec du -sh {} \; 2>/dev/null | grep -v "^0B" || echo "  No sessions found"
        fi
    fi
}

# Main execution
main() {
    log_info "Starting cleanup process..."
    log_verbose "Project root: $PROJECT_ROOT"
    log_verbose "Output directory: $OUTPUT_DIR"
    log_verbose "Days to keep: $DAYS_TO_KEEP"
    log_verbose "Dry run: $DRY_RUN"
    
    check_directories
    show_disk_usage
    echo ""
    
    cleanup_old_sessions
    cleanup_temp_files
    
    echo ""
    log_success "Cleanup process completed!"
    
    if [ "$DRY_RUN" = true ]; then
        log_warning "This was a dry run - no files were actually deleted"
    fi
}

# Run main function
main "$@" 