#!/usr/bin/env bash
# =============================================================================
# ULTIMATE TWEAKER COMPILER MACINTOSH TAHOE [C] SAMSOFT
# =============================================================================
# Every Hardware Platform Compiler Collection (1930-2025)
# Optimized for Apple M4 Pro Silicon
# Version: TAHOE-ULTIMATE-2025
# Copyright (C) SAMSOFT
# =============================================================================

set -euo pipefail

# ── ANSI Colors ───────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# ── Banner ───────────────────────────────────────────────────────────────────
print_banner() {
  echo -e "${CYAN}"
  cat << 'EOF'
╔════════════════════════════════════════════════════════════════════════════╗
║   _   _ _   _____ ___ __  __    _  _____ _____   _______        _______   ║
║  | | | | | |_   _|_ _|  \/  |  / \|_   _| ____| |_   _\ \      / / ____|  ║
║  | | | | |   | |  | || |\/| | / _ \ | | |  _|     | |  \ \ /\ / /|  _|    ║
║  | |_| | |___| |  | || |  | |/ ___ \| | | |___    | |   \ V  V / | |___   ║
║   \___/|_____|_| |___|_|  |_/_/   \_\_| |_____|   |_|    \_/\_/  |_____|  ║
║                                                                            ║
║        COMPILER MACINTOSH TAHOE [C] SAMSOFT                                ║
║        Every Hardware Platform Since 1930 – M4 Pro Optimized               ║
╚════════════════════════════════════════════════════════════════════════════╝
EOF
  echo -e "${NC}"
}

# ── Log helpers ──────────────────────────────────────────────────────────────
log()      { printf "${GREEN}[SAMSOFT]${NC} %s\n" "$*"; }
warn()     { printf "${YELLOW}[WARNING]${NC} %s\n" "$*" >&2; }
err()      { printf "${RED}[ERROR]${NC} %s\n" "$*" >&2; }
info()     { printf "${CYAN}[INFO]${NC} %s\n" "$*"; }
success()  { printf "${MAGENTA}[SUCCESS]${NC} %s\n" "$*"; }

# ── Environment checks ───────────────────────────────────────────────────────
require_homebrew() {
  if ! command -v brew >/dev/null 2>&1; then
    err "Homebrew not found. Install from https://brew.sh and re-run."
    exit 1
  fi
}

show_platform() {
  local arch="$(uname -m)"
  local os="$(uname -s)"
  info "Detected platform: ${os} ${arch}"
  if [[ "${os}" != "Darwin" ]]; then
    warn "This script is tuned for macOS; continuing anyway."
  fi
  if [[ "${arch}" != "arm64" ]]; then
    warn "Not on Apple Silicon; some toolchains may compile slowly or fail."
  fi
}

# ── Homebrew install wrapper (resilient) ─────────────────────────────────────
brew_install() {
  # Usage: brew_install pkg1 pkg2 ...
  for pkg in "$@"; do
    if brew list --versions "$pkg" >/dev/null 2>&1; then
      log "Already installed: ${pkg}"
      continue
    fi
    info "Installing: ${pkg}"
    if brew install "$pkg"; then
      success "Installed: ${pkg}"
    else
      # Don’t kill the entire run—just warn and continue
      warn "Install failed or formula not found: ${pkg}"
    fi
  done
}

# ── Mega toolchain installer ─────────────────────────────────────────────────
install_all_cpu_architectures() {
  log "═══ Every CPU Architecture Toolchain ═══"

  # Intel x86/x64
  info "Intel/AMD x86 family..."
  brew_install nasm yasm           # x86 assemblers
  brew_install mingw-w64           # Windows cross-compile

  # ARM Family
  info "ARM architectures (v6/v7/v8/v9)..."
  brew_install arm-none-eabi-gcc
  brew_install aarch64-elf-gcc

  # RISC-V
  info "RISC-V architecture..."
  brew_install riscv64-elf-gcc
  brew_install riscv32-elf-gcc

  # MIPS Family
  info "MIPS architectures..."
  brew_install mips-elf-gcc
  brew_install mips64-elf-gcc

  # PowerPC
  info "PowerPC/POWER architecture..."
  brew_install powerpc-elf-gcc
  brew_install powerpc64-elf-gcc

  # SPARC
  info "SPARC architecture..."
  brew_install sparc-elf-gcc
  brew_install sparc64-elf-gcc

  # 68000/ColdFire
  info "Motorola 68000 family..."
  brew_install m68k-elf-gcc

  # AVR (Arduino)
  info "AVR microcontrollers..."
  brew_install avr-gcc avrdude

  # MSP430
  info "TI MSP430..."
  brew_install msp430-gcc

  # 8051
  info "Intel 8051 family..."
  brew_install sdcc                 # Small Device C Compiler

  # Z80
  info "Zilog Z80..."
  brew_install z88dk

  # 6502/65816
  info "MOS 6502 family..."
  brew_install cc65
  brew_install wla-dx               # 65816 for SNES

  # PIC
  info "Microchip PIC..."
  brew_install gputils

  # Xtensa (ESP32)
  info "Xtensa/ESP32..."
  brew_install esp-idf

  # Alpha
  info "DEC Alpha..."
  brew_install alpha-elf-gcc

  # PA-RISC
  info "HP PA-RISC..."
  brew_install hppa-elf-gcc

  # SuperH
  info "Hitachi SuperH..."
  brew_install sh-elf-gcc

  # VAX
  info "DEC VAX..."
  brew_install vax-netbsdelf-gcc

  # Additional dedicated assemblers (universal & retro)
  info "Additional dedicated assembly compilers (universal & retro)..."
  brew_install acme          # 6502 cross-assembler
  brew_install asmx          # Multi-CPU (68xx, 808x, 8051, etc.)
  brew_install dasm          # 6502/6803/F8 macro assembler
  brew_install fasm          # Flat Assembler (x86/x64)
  brew_install keystone      # Modern multi-arch assembler engine
  brew_install pasmo         # Z80 cross-assembler
  brew_install sjasmplus     # Advanced Z80 assembler
  brew_install 64tass        # Ultimate 6502/65816 assembler
  brew_install vasm          # Versatile portable assembler (m68k, 6502, Z80, etc.)
  brew_install xa            # Fast 6502 cross-assembler
  brew_install z80asm        # Clean Z80 assembler

  success "All CPU architectures + EVERY dedicated assembler attempted."
  info "Note: some formulas may require extra taps; failures are logged and do not halt the run."
}

# ── Main ─────────────────────────────────────────────────────────────────────
main() {
  print_banner
  show_platform
  require_homebrew
  install_all_cpu_architectures
  success "TAHOE-ULTIMATE-2025 setup complete."
}

main "$@"
