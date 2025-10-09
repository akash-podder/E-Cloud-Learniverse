#!/bin/bash

# kind Installation Script
# This script installs kind (Kubernetes in Docker) for Linux, macOS, and Windows (Git Bash/WSL)
# Version: 0.30.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

KIND_VERSION="v0.30.0"
INSTALL_DIR="/usr/local/bin"

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if kind is already installed
check_existing_installation() {
    if command -v kind &> /dev/null; then
        CURRENT_VERSION=$(kind version 2>/dev/null | grep -oP 'kind v\K[0-9.]+' || echo "unknown")
        print_warning "kind is already installed (version: ${CURRENT_VERSION})"
        read -p "Do you want to reinstall/update? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled."
            exit 0
        fi
    fi
}

# Detect OS and Architecture
detect_platform() {
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    ARCH=$(uname -m)

    case "$OS" in
        linux*)
            OS_TYPE="linux"
            ;;
        darwin*)
            OS_TYPE="darwin"
            INSTALL_DIR="/usr/local/bin"
            ;;
        mingw*|msys*|cygwin*)
            OS_TYPE="windows"
            INSTALL_DIR="$HOME/bin"
            ;;
        *)
            print_error "Unsupported operating system: $OS"
            exit 1
            ;;
    esac

    case "$ARCH" in
        x86_64|amd64)
            ARCH_TYPE="amd64"
            ;;
        aarch64|arm64)
            ARCH_TYPE="arm64"
            ;;
        *)
            print_error "Unsupported architecture: $ARCH"
            exit 1
            ;;
    esac

    print_info "Detected OS: $OS_TYPE"
    print_info "Detected Architecture: $ARCH_TYPE"
}

# Download kind binary
download_kind() {
    print_info "Downloading kind ${KIND_VERSION} for ${OS_TYPE}-${ARCH_TYPE}..."

    if [ "$OS_TYPE" = "windows" ]; then
        BINARY_NAME="kind-windows-${ARCH_TYPE}.exe"
        DOWNLOAD_URL="https://kind.sigs.k8s.io/dl/${KIND_VERSION}/kind-windows-${ARCH_TYPE}"
    else
        BINARY_NAME="kind"
        DOWNLOAD_URL="https://kind.sigs.k8s.io/dl/${KIND_VERSION}/kind-${OS_TYPE}-${ARCH_TYPE}"
    fi

    # Download the binary
    if command -v curl &> /dev/null; then
        curl -Lo "./${BINARY_NAME}" "${DOWNLOAD_URL}"
    elif command -v wget &> /dev/null; then
        wget -O "./${BINARY_NAME}" "${DOWNLOAD_URL}"
    else
        print_error "Neither curl nor wget is available. Please install one of them."
        exit 1
    fi

    if [ $? -ne 0 ]; then
        print_error "Failed to download kind binary"
        exit 1
    fi

    print_info "Download completed successfully"
}

# Install kind binary
install_kind() {
    print_info "Installing kind to ${INSTALL_DIR}..."

    # Make binary executable
    chmod +x "./${BINARY_NAME}"

    # Create install directory if it doesn't exist
    if [ ! -d "$INSTALL_DIR" ]; then
        mkdir -p "$INSTALL_DIR"
    fi

    # Move binary to install directory
    if [ "$OS_TYPE" = "windows" ]; then
        mv "./${BINARY_NAME}" "${INSTALL_DIR}/kind.exe"
        print_info "kind installed to ${INSTALL_DIR}/kind.exe"
    else
        # Check if we need sudo
        if [ -w "$INSTALL_DIR" ]; then
            mv "./${BINARY_NAME}" "${INSTALL_DIR}/kind"
        else
            print_warning "Requires sudo permission to install to ${INSTALL_DIR}"
            sudo mv "./${BINARY_NAME}" "${INSTALL_DIR}/kind"
        fi
        print_info "kind installed to ${INSTALL_DIR}/kind"
    fi
}

# Verify installation
verify_installation() {
    print_info "Verifying installation..."

    # Add install dir to PATH for this session if needed
    if [[ ":$PATH:" != *":${INSTALL_DIR}:"* ]]; then
        export PATH="${INSTALL_DIR}:${PATH}"
    fi

    if command -v kind &> /dev/null; then
        VERSION=$(kind version)
        print_info "Installation successful!"
        print_info "kind version: ${VERSION}"
    else
        print_error "Installation failed. kind command not found."
        print_warning "You may need to add ${INSTALL_DIR} to your PATH"
        print_warning "Add this line to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
        echo "    export PATH=\"${INSTALL_DIR}:\$PATH\""
        exit 1
    fi
}

# Main installation flow
main() {
    print_info "Starting kind installation..."

    check_existing_installation
    detect_platform
    download_kind
    install_kind
    verify_installation

    echo ""
    print_info "===================================="
    print_info "kind has been installed successfully!"
    print_info "===================================="
    echo ""
    print_info "Quick start commands:"
    echo "  kind create cluster        # Create a new cluster"
    echo "  kind get clusters          # List all clusters"
    echo "  kind delete cluster        # Delete default cluster"
    echo ""
    print_info "For more information, visit: https://kind.sigs.k8s.io/"
}

# Run main function
main
