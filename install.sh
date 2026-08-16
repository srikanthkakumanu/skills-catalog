#!/usr/bin/env bash
# ==============================================================================
# skills-catalog: Agent Skills Installer
# Compatible with Antigravity 2.x, Claude Code, and OpenAI Codex
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${SCRIPT_DIR}/skills"
TARGET="all"
MODE="symlink"
SPECIFIC_SKILL="all"
FORCE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Runtime destination paths
ANTIGRAVITY_SKILLS_DIR="${HOME}/.antigravity/skills"
CLAUDE_SKILLS_DIR="${HOME}/.claude/skills"
CODEX_SKILLS_DIR="${HOME}/.codex/skills"

print_banner() {
    echo -e "${BLUE}${BOLD}"
    echo "================================================================"
    echo "          Agent Skills Catalog Installer v1.0.0                 "
    echo "================================================================"
    echo -e "${NC}"
}

usage() {
    print_banner
    echo -e "${BOLD}Usage:${NC} $0 [OPTIONS]"
    echo ""
    echo -e "${BOLD}Options:${NC}"
    echo "  -t, --target <TARGET>     Target runtime environment:"
    echo "                            antigravity   -> ~/.antigravity/skills"
    echo "                            claude        -> ~/.claude/skills"
    echo "                            codex         -> ~/.codex/skills"
    echo "                            all           -> All supported runtimes (default)"
    echo "  -m, --mode <MODE>         Installation mode:"
    echo "                            symlink       -> Create symbolic links (default)"
    echo "                            copy          -> Copy directory contents"
    echo "  -s, --skill <SKILL_NAME>  Install a specific skill (e.g. brd) or 'all' (default)"
    echo "  -f, --force               Force overwrite existing skill destinations"
    echo "  -h, --help                Display this help message and exit"
    echo ""
    echo -e "${BOLD}Examples:${NC}"
    echo "  $0                                # Install all skills to all runtimes via symlink"
    echo "  $0 --target antigravity           # Install all skills for Antigravity 2.x only"
    echo "  $0 --target claude --mode copy    # Copy all skills to Claude Code"
    echo "  $0 --skill brd --target codex     # Install only the 'brd' skill to Codex"
    echo ""
    exit 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -t|--target)
            TARGET="$2"
            shift 2
            ;;
        -m|--mode)
            MODE="$2"
            shift 2
            ;;
        -s|--skill)
            SPECIFIC_SKILL="$2"
            shift 2
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}Error: Unknown argument '$1'${NC}" >&2
            echo "Run '$0 --help' for usage details." >&2
            exit 1
            ;;
    esac
done

# Validate target argument
case "${TARGET}" in
    antigravity|claude|codex|all|all-platforms)
        ;;
    *)
        echo -e "${RED}Error: Invalid target '${TARGET}'. Must be one of: antigravity, claude, codex, all${NC}" >&2
        exit 1
        ;;
esac

# Validate mode argument
case "${MODE}" in
    symlink|copy)
        ;;
    *)
        echo -e "${RED}Error: Invalid mode '${MODE}'. Must be 'symlink' or 'copy'${NC}" >&2
        exit 1
        ;;
esac

# Check Python 3 availability for skill validators
check_prerequisites() {
    if ! command -v python3 &>/dev/null; then
        echo -e "${YELLOW}Warning: python3 is not detected in PATH. Skill validators may not run automatically.${NC}"
    fi
}

install_skill_to_dir() {
    local skill_src="$1"
    local skill_name="$2"
    local dest_parent_dir="$3"
    local runtime_name="$4"
    local dest_skill_dir="${dest_parent_dir}/${skill_name}"

    mkdir -p "${dest_parent_dir}"

    if [[ -e "${dest_skill_dir}" || -L "${dest_skill_dir}" ]]; then
        if [[ "${FORCE}" == true ]]; then
            rm -rf "${dest_skill_dir}"
        else
            echo -e "  ${YELLOW}[SKIP]${NC} ${skill_name} already exists in ${runtime_name} (${dest_skill_dir}). Use --force to overwrite."
            return 0
        fi
    fi

    if [[ "${MODE}" == "symlink" ]]; then
        ln -sf "${skill_src}" "${dest_skill_dir}"
        echo -e "  ${GREEN}[LINK]${NC} ${BOLD}${skill_name}${NC} -> ${dest_skill_dir}"
    else
        cp -R "${skill_src}" "${dest_skill_dir}"
        echo -e "  ${GREEN}[COPY]${NC} ${BOLD}${skill_name}${NC} -> ${dest_skill_dir}"
    fi
}

deploy_to_runtime() {
    local runtime_name="$1"
    local runtime_dir="$2"

    echo -e "\n${BLUE}Deploying to ${BOLD}${runtime_name}${NC} (${runtime_dir}):"

    local skills_to_install=()
    if [[ "${SPECIFIC_SKILL}" == "all" ]]; then
        for item in "${SKILLS_DIR}"/*; do
            if [[ -d "${item}" && -f "${item}/SKILL.md" ]]; then
                skills_to_install+=("$(basename "${item}")")
            fi
        done
    else
        if [[ -d "${SKILLS_DIR}/${SPECIFIC_SKILL}" && -f "${SKILLS_DIR}/${SPECIFIC_SKILL}/SKILL.md" ]]; then
            skills_to_install+=("${SPECIFIC_SKILL}")
        else
            echo -e "${RED}Error: Skill '${SPECIFIC_SKILL}' not found at ${SKILLS_DIR}/${SPECIFIC_SKILL}${NC}" >&2
            exit 1
        fi
    fi

    if [[ ${#skills_to_install[@]} -eq 0 ]]; then
        echo -e "${YELLOW}No valid skills found in ${SKILLS_DIR}.${NC}"
        return 0
    fi

    for skill in "${skills_to_install[@]}"; do
        local src_path="${SKILLS_DIR}/${skill}"
        install_skill_to_dir "${src_path}" "${skill}" "${runtime_dir}" "${runtime_name}"
    done
}

main() {
    print_banner
    check_prerequisites

    echo "Mode:   ${MODE}"
    echo "Target: ${TARGET}"
    echo "Skill:  ${SPECIFIC_SKILL}"
    echo "Force:  ${FORCE}"

    if [[ "${TARGET}" == "antigravity" || "${TARGET}" == "all" || "${TARGET}" == "all-platforms" ]]; then
        deploy_to_runtime "Antigravity 2.x" "${ANTIGRAVITY_SKILLS_DIR}"
    fi

    if [[ "${TARGET}" == "claude" || "${TARGET}" == "all" || "${TARGET}" == "all-platforms" ]]; then
        deploy_to_runtime "Claude Code" "${CLAUDE_SKILLS_DIR}"
    fi

    if [[ "${TARGET}" == "codex" || "${TARGET}" == "all" || "${TARGET}" == "all-platforms" ]]; then
        deploy_to_runtime "OpenAI Codex" "${CODEX_SKILLS_DIR}"
    fi

    echo -e "\n${GREEN}${BOLD}✓ Installation finished successfully!${NC}"
    echo -e "Skills are now available in your configured runtime environments."
}

main "$@"
